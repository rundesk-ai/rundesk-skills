# SQLite Security Examples

Injection defence, input validation, error handling, file permissions, backups, audit logging, and
the tests that prove them. Examples use Python's standard-library `sqlite3`; the Rust equivalents
are in [rust-bindings.md](rust-bindings.md).

SQLite has no users, roles, or grants. Whoever can read the file can read every row, so the
protections here are the parameter binder, the constraints in the schema, and the filesystem.

## Parameterized Queries

Every value that came from outside your program is bound, never formatted.

```python
# Correct: positional parameters.
def get_user(conn, user_id):
    return conn.execute(
        "SELECT id, name, email FROM users WHERE id = ?", (user_id,)
    ).fetchone()


# Correct: named parameters, which survive reordering and repetition.
def search_users(conn, name, status):
    return conn.execute(
        """
        SELECT id, name, email FROM users
        WHERE name LIKE :pattern ESCAPE '\\' AND status = :status
        """,
        {"pattern": f"%{escape_like(name)}%", "status": status},
    ).fetchall()


# Correct: many rows, one statement, one transaction.
def insert_documents(conn, rows):
    conn.execute("BEGIN IMMEDIATE")
    conn.executemany(
        "INSERT INTO documents (user_id, title, content) VALUES (?, ?, ?)", rows
    )
    conn.execute("COMMIT")


# Wrong: string formatting. `user_id` of "1 OR 1=1" returns every row; worse payloads run
# statements you did not write.
def get_user_unsafe(conn, user_id):
    return conn.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
```

A single-element tuple needs its trailing comma: `(user_id,)`, not `(user_id)`. Without it Python
passes a bare value and `sqlite3` raises rather than binding — a small trap that pushes people back
towards formatting.

## Escaping `LIKE` Patterns

`%` and `_` are wildcards inside a `LIKE` pattern. A user searching for `50%` gets every row unless
you escape, and escaping without an `ESCAPE` clause in the SQL does nothing at all — the backslashes
are then just literal characters to match.

```python
def escape_like(value):
    """Make a user string safe to embed in a LIKE pattern, paired with ESCAPE '\\'."""
    return (
        value.replace("\\", "\\\\")
        .replace("%", "\\%")
        .replace("_", "\\_")
    )


def search_by_name(conn, term):
    return conn.execute(
        "SELECT id, name, email FROM users WHERE name LIKE ? ESCAPE '\\'",
        (f"%{escape_like(term)}%",),
    ).fetchall()
```

Escape the escape character first, or you double-escape the ones you add afterwards.

This is a correctness fix, not an injection fix — the value was always bound. The injection risk is
in the *pattern*, which the user should not control.

## Identifiers Cannot Be Bound

Parameters bind values. A column name, a table name, or a sort direction chosen at runtime has to be
compared against a list you wrote, and only then interpolated.

```python
SORTABLE = frozenset({"id", "name", "email", "created_at"})
DIRECTIONS = {"asc": "ASC", "desc": "DESC"}


def list_users_sorted(conn, sort_column, direction):
    if sort_column not in SORTABLE:
        raise ValueError(f"unsortable column: {sort_column!r}")
    order = DIRECTIONS.get(direction.lower(), "ASC")

    # Safe: both fragments came from constants above, not from the caller.
    return conn.execute(
        f"SELECT id, name, email FROM users ORDER BY {sort_column} {order}"
    ).fetchall()


SELECTABLE = frozenset({"id", "name", "email", "status", "created_at"})


def get_user_fields(conn, user_id, fields):
    chosen = [f for f in fields if f in SELECTABLE]
    if not chosen:
        raise ValueError("no selectable fields requested")

    columns = ", ".join(chosen)
    row = conn.execute(
        f"SELECT {columns} FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    return dict(zip(chosen, row)) if row else None
```

Membership in a set, not a substring test and not a regular expression. `"name; DROP TABLE users"`
does not appear in `SORTABLE`, and that is the whole check.

Quoting an identifier is not a substitute. `"` quoting in SQLite silently falls back to treating an
unmatched identifier as a string literal, so a typo becomes a constant rather than an error.

## Layered Validation

The database constraint is the last line, not the first. Neither layer replaces the other: the
application gives a good error message, the schema makes the bad state impossible.

```sql
CREATE TABLE users (
    id            INTEGER PRIMARY KEY,
    email         TEXT NOT NULL UNIQUE CHECK (email LIKE '%_@_%._%'),
    name          TEXT NOT NULL CHECK (length(name) BETWEEN 2 AND 50),
    password_hash TEXT NOT NULL,
    status        TEXT NOT NULL DEFAULT 'pending'
                  CHECK (status IN ('pending', 'active', 'suspended')),
    created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);
```

```python
def create_user(conn, name, email, password):
    # Layer 1: shape and format, with an error the caller can show a person.
    if not 2 <= len(name) <= 50:
        raise ValidationError("name must be 2–50 characters")
    if "@" not in email:
        raise ValidationError("email is not an address")
    if len(password) < 12:
        raise ValidationError("password must be at least 12 characters")

    # Layer 2: hash before storage. Argon2id or bcrypt — never a bare SHA.
    password_hash = hash_password(password)

    # Layer 3: let the UNIQUE constraint decide the race, rather than checking first.
    try:
        cursor = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, password_hash),
        )
    except sqlite3.IntegrityError as exc:
        raise DuplicateEmail(email) from exc
    return cursor.lastrowid
```

A `SELECT` to check whether the email exists, followed by an `INSERT`, is a race. The `UNIQUE`
constraint is not.

Parse values into their real types at the boundary. `int(user_id)` raising `ValueError` on
`"1; DROP TABLE users"` is a better outcome than passing the string onward, whatever the query does
with it.

## Error Messages

Driver errors name tables, columns, and constraints. That belongs in your log, not in a response.

```python
class NotFound(Exception): pass
class ValidationError(Exception): pass
class DuplicateEmail(Exception): pass


def load_user(conn, user_id):
    try:
        row = conn.execute(
            "SELECT id, name, email FROM users WHERE id = ?", (user_id,)
        ).fetchone()
    except sqlite3.DatabaseError:
        logger.exception("user lookup failed", extra={"user_id": user_id})
        raise RuntimeError("an internal error occurred") from None
    if row is None:
        raise NotFound(f"no user {user_id}")
    return row
```

`from None` suppresses the chained driver exception so it cannot reach a traceback that is rendered
to a user. The full error is already in the log.

## File Permissions

```python
import os
import stat


def secure_database_files(db_path):
    """Owner read/write only, on the database and both sidecar files."""
    for path in (db_path, f"{db_path}-wal", f"{db_path}-shm"):
        if os.path.exists(path):
            os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)  # 0600


def secure_database_directory(directory):
    """SQLite creates -wal, -shm, and journal files itself; the directory mode governs them."""
    os.makedirs(directory, mode=0o700, exist_ok=True)
    os.chmod(directory, 0o700)
```

Securing the directory matters more than securing the file. SQLite creates and recreates the
sidecar files as it runs, and they inherit the process umask, not the mode you set on the database
an hour ago.

On Windows the mode bits are ignored — use an ACL, and be explicit that the guarantee differs.

Put the database in an application data directory, not next to the executable and not anywhere
world-readable. Rows a user should not read are protected by nothing else.

## Backups

```python
def backup(conn, destination_path):
    """The online backup API is consistent against a database being written."""
    with sqlite3.connect(destination_path) as dest:
        conn.backup(dest, pages=64, sleep=0.25)
    os.chmod(destination_path, 0o600)
```

`cp app.db backup.db` on a running system produces a file that may be torn, and that in WAL mode is
missing every transaction still in `app.db-wal`. Use the backup API or `VACUUM INTO`.

**Encryption is not built in.** A plain SQLite file is readable with any copy of the `sqlite3` CLI,
and so is a plain backup. Three options, in order of how much they change:

- **Filesystem or volume encryption** — no code, protects the file at rest, protects nothing from a
  process that can read the mount.
- **Encrypt the backup artefact** before it leaves the machine — the right layer for anything that
  goes to object storage. Use a vetted library (`cryptography`'s Fernet, `age`, or the platform
  keystore); do not assemble AES-GCM from parts, and do not invent nonce handling.
- **An encrypting build of SQLite** (SQLCipher, or the commercial SEE) when the live database itself
  must be encrypted. This is a different library with a different file format, decided before you
  ship, not bolted on afterwards.

Whichever you choose, the key does not live in the repository or beside the backup.

## Audit Logging

```sql
CREATE TABLE audit_log (
    id         INTEGER PRIMARY KEY,
    actor_id   INTEGER,
    action     TEXT NOT NULL,
    resource   TEXT NOT NULL,
    row_id     INTEGER,
    occurred_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_audit_resource ON audit_log(resource, row_id);
CREATE INDEX idx_audit_actor ON audit_log(actor_id, occurred_at DESC);
```

```python
def execute_audited(conn, sql, params, *, actor_id, action, resource, row_id=None):
    """Write and audit atomically: an unaudited write is worse than no audit table."""
    conn.execute("BEGIN IMMEDIATE")
    try:
        cursor = conn.execute(sql, params)
        conn.execute(
            """
            INSERT INTO audit_log (actor_id, action, resource, row_id)
            VALUES (?, ?, ?, ?)
            """,
            (actor_id, action, resource, row_id if row_id is not None else cursor.lastrowid),
        )
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise
    return cursor.rowcount
```

Two rules the shape above encodes:

- **The audit row commits with the change.** Logging after the commit means a crash in between
  leaves a change nobody recorded.
- **Log the identifiers, not the payload.** An audit table that stores the values written becomes a
  second copy of your sensitive data with none of its access controls — and one that quietly
  survives a `DELETE` from the table it shadows.

For before/after values on specific columns, see the audit trail patterns in the `database-design`
skill, which owns that modelling question.

## Testing

Injection tests assert on the data, not on the absence of an exception. A query that fails safely
and a query that silently matched every row both "did not raise".

```python
import sqlite3
import unittest


class InjectionTests(unittest.TestCase):
    PAYLOADS = [
        "'; DROP TABLE users; --",
        "admin' OR '1'='1",
        "' UNION SELECT id, password_hash, email FROM users --",
        "1; DELETE FROM users WHERE 1=1; --",
        "' OR 1=1--",
        "admin'--",
    ]

    def setUp(self):
        self.conn = sqlite3.connect(":memory:", isolation_level=None)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.executescript("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                status TEXT NOT NULL DEFAULT 'active'
            );
            INSERT INTO users (name, email) VALUES ('Real User', 'real@example.test');
        """)
        self.addCleanup(self.conn.close)

    def test_payloads_match_nothing_and_change_nothing(self):
        for payload in self.PAYLOADS:
            with self.subTest(payload=payload):
                rows = search_users(self.conn, payload, "active")
                self.assertEqual([], rows, "payload matched rows it should not")

                count = self.conn.execute("SELECT count(*) FROM users").fetchone()[0]
                self.assertEqual(1, count, "payload modified the table")

    def test_payload_stored_as_a_literal_round_trips(self):
        user_id = self.conn.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            ("'; DROP TABLE users; --", "payload@example.test"),
        ).lastrowid
        row = self.conn.execute(
            "SELECT name FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        self.assertEqual("'; DROP TABLE users; --", row[0])

    def test_like_wildcards_do_not_leak_rows(self):
        self.conn.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)", ("50% off", "sale@example.test")
        )
        rows = search_by_name(self.conn, "%")
        self.assertEqual(1, len(rows), "bare wildcard matched every row")
        self.assertEqual("50% off", rows[0][1])

    def test_unsortable_column_is_rejected(self):
        with self.assertRaises(ValueError):
            list_users_sorted(self.conn, "name; DROP TABLE users", "asc")
```

The second test is the one that matters most: a bound payload should come back out byte-for-byte.
That proves the value was data rather than SQL, which "no exception" never does.
