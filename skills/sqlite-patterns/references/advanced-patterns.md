# SQLite Advanced Patterns

Migrations, full-text search, query features, connection reuse, and maintenance. Examples are SQL
where the rule is SQL, and Python's standard-library `sqlite3` where a host language is needed.
The Rust equivalents are in [rust-bindings.md](rust-bindings.md).

## Migrations

### Tracking the schema version

`PRAGMA user_version` is a 32-bit integer stored in the database header. It costs nothing and is
enough when migrations are a numbered list in code.

```python
version = conn.execute("PRAGMA user_version").fetchone()[0]
conn.execute(f"PRAGMA user_version = {version + 1}")  # PRAGMA values cannot be bound
```

A table buys you names, timestamps, and a record of what ran when.

```sql
CREATE TABLE IF NOT EXISTS schema_migrations (
    version    INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    applied_at TEXT NOT NULL DEFAULT (datetime('now'))
);
```

### A migration runner

Each migration applies and records itself in one transaction. A migration that applied but was not
recorded runs a second time on the next start.

```python
MIGRATIONS = [
    (1, "create_users", """
        CREATE TABLE users (
            id         INTEGER PRIMARY KEY,
            name       TEXT NOT NULL,
            email      TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );
    """),
    (2, "create_documents", """
        CREATE TABLE documents (
            id      INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            title   TEXT NOT NULL,
            content TEXT
        );
        CREATE INDEX idx_documents_user ON documents(user_id);
    """),
    (3, "add_user_status", "ALTER TABLE users ADD COLUMN status TEXT NOT NULL DEFAULT 'active';"),
]


def migrate(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version    INTEGER PRIMARY KEY,
            name       TEXT NOT NULL,
            applied_at TEXT NOT NULL DEFAULT (datetime('now'))
        );
    """)
    applied = {row[0] for row in conn.execute("SELECT version FROM schema_migrations")}

    for version, name, sql in MIGRATIONS:
        if version in applied:
            continue
        conn.execute("BEGIN IMMEDIATE")
        try:
            conn.executescript(sql)
            conn.execute(
                "INSERT INTO schema_migrations (version, name) VALUES (?, ?)", (version, name)
            )
            conn.execute("COMMIT")
        except Exception:
            conn.execute("ROLLBACK")
            raise
```

Index the foreign key column yourself, as migration 2 does. SQLite indexes the parent's primary key,
never the child's column, and `ON DELETE CASCADE` scans the child table without it.

### Rollback

Down migrations are worth writing only where they are honest. `DROP TABLE` reverses a `CREATE TABLE`
exactly; nothing reverses a `DROP COLUMN`, because the data is gone. Where a migration is not
reversible, say so and rely on the backup instead of pretending.

```python
def rollback_to(conn, target_version):
    rows = conn.execute(
        "SELECT version FROM schema_migrations WHERE version > ? ORDER BY version DESC",
        (target_version,),
    ).fetchall()
    for (version,) in rows:
        down = DOWN_SQL[version]  # KeyError here is the correct outcome for an irreversible step
        conn.execute("BEGIN IMMEDIATE")
        conn.executescript(down)
        conn.execute("DELETE FROM schema_migrations WHERE version = ?", (version,))
        conn.execute("COMMIT")
```

### What `ALTER TABLE` can do

| Change | Supported | Since |
|---|---|---|
| `ADD COLUMN` (with a constant default) | yes | always |
| `RENAME TO` | yes | always |
| `RENAME COLUMN` | yes | 3.25 |
| `DROP COLUMN` | yes, with restrictions | 3.35 |
| Add or drop a constraint, change a type, reorder columns | no | rebuild the table |

`ADD COLUMN` cannot add a `PRIMARY KEY` or `UNIQUE` column, and its default must be a constant —
`datetime('now')` is not one.

### Rebuilding a table

This is the procedure from the SQLite documentation, and the order matters.

```python
def rebuild_users(conn):
    conn.execute("PRAGMA foreign_keys = OFF")   # outside the transaction; it is a no-op inside one
    conn.execute("BEGIN IMMEDIATE")
    try:
        conn.executescript("""
            CREATE TABLE users_new (
                id         INTEGER PRIMARY KEY,
                full_name  TEXT NOT NULL,          -- renamed from name
                email      TEXT NOT NULL UNIQUE,
                status     TEXT NOT NULL DEFAULT 'active',
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            );

            INSERT INTO users_new (id, full_name, email, status, created_at)
            SELECT id, name, email, COALESCE(status, 'active'), created_at FROM users;

            DROP TABLE users;
            ALTER TABLE users_new RENAME TO users;

            -- indexes, triggers, and views that referenced the old table must be recreated here
            CREATE INDEX idx_users_email ON users(email);
        """)
        violations = conn.execute("PRAGMA foreign_key_check").fetchall()
        if violations:
            raise RuntimeError(f"rebuild left dangling references: {violations}")
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise
    finally:
        conn.execute("PRAGMA foreign_keys = ON")
```

Two things go wrong when this is done casually:

- **Foreign keys left on.** `DROP TABLE users` fires `ON DELETE CASCADE` on every child table and
  deletes rows you were not migrating.
- **`PRAGMA foreign_key_check` skipped.** With foreign keys off, nothing validated the copy. Check
  before you commit, while a rollback is still available.

Indexes, triggers, and views attached to the dropped table go with it. Recreate them in the same
transaction.

## Full-Text Search (FTS5)

### External-content table and its triggers

An external-content table stores only the index and reads the columns from the source table, so it
does not duplicate the text. The cost is that you own the synchronisation, and all three triggers
are required.

```sql
CREATE VIRTUAL TABLE docs_fts USING fts5(
    title,
    content,
    tags,
    content=documents,
    content_rowid=id,
    tokenize='porter unicode61 remove_diacritics 2',
    prefix='2,3'
);

CREATE TRIGGER docs_ai AFTER INSERT ON documents BEGIN
    INSERT INTO docs_fts(rowid, title, content, tags)
    VALUES (new.id, new.title, new.content, new.tags);
END;

CREATE TRIGGER docs_ad AFTER DELETE ON documents BEGIN
    INSERT INTO docs_fts(docs_fts, rowid, title, content, tags)
    VALUES ('delete', old.id, old.title, old.content, old.tags);
END;

CREATE TRIGGER docs_au AFTER UPDATE ON documents BEGIN
    INSERT INTO docs_fts(docs_fts, rowid, title, content, tags)
    VALUES ('delete', old.id, old.title, old.content, old.tags);
    INSERT INTO docs_fts(rowid, title, content, tags)
    VALUES (new.id, new.title, new.content, new.tags);
END;
```

The `'delete'` command must be given the **old** values. FTS5 uses them to find the index entries to
remove; passing the new ones leaves the old terms in the index. Skip the delete and update triggers
entirely and the index accumulates entries for rows that no longer exist, so searches return
`rowid`s that join to nothing.

`prefix='2,3'` builds extra indexes so that `term*` is fast for two- and three-character prefixes.
It costs space; leave it out if you do not do prefix search.

### Querying

```sql
-- Best matches first: rank is the bm25 score, and a better match is more negative.
SELECT d.id, d.title, docs_fts.rank
FROM documents d JOIN docs_fts ON d.id = docs_fts.rowid
WHERE docs_fts MATCH ?
ORDER BY docs_fts.rank
LIMIT 20;

-- Snippet and highlight: column index, open tag, close tag, ellipsis, token budget.
SELECT d.id,
       highlight(docs_fts, 0, '<mark>', '</mark>')             AS title_marked,
       snippet(docs_fts, 1, '<b>', '</b>', '…', 32)            AS excerpt
FROM documents d JOIN docs_fts ON d.id = docs_fts.rowid
WHERE docs_fts MATCH ?
ORDER BY docs_fts.rank;

-- Weighted ranking: title matches count more than body matches.
SELECT d.id, bm25(docs_fts, 10.0, 1.0, 1.0) AS score
FROM documents d JOIN docs_fts ON d.id = docs_fts.rowid
WHERE docs_fts MATCH ?
ORDER BY score;
```

The `MATCH` argument is a query language: `AND`, `OR`, `NOT`, `NEAR(a b, 5)`, `"exact phrase"`,
`col : term`, and `term*`. That is exactly why raw user input does not belong in it — an unbalanced
quote raises `SQLITE_ERROR`, and `NOT` typed as a word means something the user did not intend.

```python
def as_phrase(user_input):
    """Treat whatever the user typed as one literal phrase."""
    return '"' + user_input.replace('"', '""') + '"'
```

Expose the operators deliberately if you want them, by parsing your own search syntax and building
the FTS5 expression from it — not by forwarding the raw string.

### Maintenance

```sql
INSERT INTO docs_fts(docs_fts) VALUES('optimize');         -- merge b-tree segments; do this after bulk loads
INSERT INTO docs_fts(docs_fts) VALUES('rebuild');          -- discard and rebuild from the content table
INSERT INTO docs_fts(docs_fts) VALUES('integrity-check');  -- raises SQLITE_CORRUPT if the index is inconsistent
```

`integrity-check` returns no rows. It reports by raising an error, so check it by catching one:

```python
def fts_is_consistent(conn):
    try:
        conn.execute("INSERT INTO docs_fts(docs_fts) VALUES('integrity-check')")
        return True
    except sqlite3.DatabaseError:
        return False
```

`rebuild` is the repair for an index that drifted — it is also the only way back after a period with
missing triggers.

## Query Features

### Recursive CTEs for hierarchies

```sql
WITH RECURSIVE subtree AS (
    SELECT id, parent_id, name, 0 AS depth, name AS path
    FROM categories WHERE id = :root

    UNION ALL

    SELECT c.id, c.parent_id, c.name, s.depth + 1, s.path || '/' || c.name
    FROM categories c JOIN subtree s ON c.parent_id = s.id
)
SELECT * FROM subtree ORDER BY path;
```

Add `WHERE depth < 32` to the recursive arm if the data can contain a cycle. Nothing in an adjacency
list prevents one, and the recursion will not terminate on its own.

### Window functions (3.25+)

```sql
SELECT id,
       name,
       score,
       RANK()       OVER (ORDER BY score DESC) AS rank,
       DENSE_RANK() OVER (ORDER BY score DESC) AS dense_rank,
       score - LAG(score) OVER (ORDER BY score DESC) AS gap_to_previous,
       SUM(score)   OVER (ORDER BY score DESC ROWS UNBOUNDED PRECEDING) AS running_total
FROM users
ORDER BY score DESC;
```

`RANK` leaves gaps after ties, `DENSE_RANK` does not, and `ROW_NUMBER` breaks ties arbitrarily unless
the `ORDER BY` is total. Pick the one whose tie behaviour you want.

### JSON

```sql
-- Validate on the way in.
CREATE TABLE records (
    id   INTEGER PRIMARY KEY,
    data TEXT NOT NULL CHECK (json_valid(data))
);

-- Query a path.
SELECT id FROM records WHERE json_extract(data, '$.status') = 'active';

-- An expression index makes that query seekable; the expression must match the query exactly.
CREATE INDEX idx_records_status ON records(json_extract(data, '$.status'));

-- Expand an array into rows.
SELECT DISTINCT je.value
FROM documents, json_each(documents.tags) AS je
ORDER BY je.value;
```

JSON columns are for genuinely variable shapes. A field every row has, that you filter on, is a
column — with a type, a `NOT NULL`, and an ordinary index.

## Connection Reuse

Opening a connection is cheap compared to a network database but not free, and every open has to
reapply the per-connection PRAGMAs. Keep connections and hand them out.

```python
import queue
import sqlite3
from contextlib import contextmanager


class ConnectionPool:
    def __init__(self, path, size=5):
        self._pool = queue.Queue(size)
        for _ in range(size):
            self._pool.put(self._open(path))

    @staticmethod
    def _open(path):
        conn = sqlite3.connect(path, isolation_level=None, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.executescript("""
            PRAGMA journal_mode = WAL;
            PRAGMA foreign_keys = ON;
            PRAGMA busy_timeout = 5000;
            PRAGMA synchronous = NORMAL;
            PRAGMA cache_size = -64000;
        """)
        return conn

    @contextmanager
    def acquire(self):
        conn = self._pool.get()
        try:
            yield conn
        finally:
            self._pool.put(conn)
```

`check_same_thread=False` is only safe because the pool guarantees one thread holds a connection at a
time. Two threads on one connection is a data race whatever the flag says.

A larger pool does not buy write throughput: SQLite has one writer for the whole database, so extra
connections queue on the same lock. Size the pool for readers.

## Maintenance and Backup

```python
def maintain(conn):
    conn.execute("ANALYZE")                    # refresh planner statistics
    conn.execute("PRAGMA optimize")            # cheap; SQLite decides what is worth doing

    free = conn.execute("PRAGMA freelist_count").fetchone()[0]
    total = conn.execute("PRAGMA page_count").fetchone()[0]
    if total and free / total > 0.25:
        conn.execute("VACUUM")                 # rewrites the file; needs room for a second copy
```

`VACUUM` takes a write lock for its whole duration and needs free disk space of roughly the database
size. Run it when the free-page ratio justifies it, not nightly by reflex. `PRAGMA optimize` on
connection close is the low-cost habit that keeps statistics fresh.

Back up with the online backup API — it copes with a concurrently written database, which `cp` does
not:

```python
def backup(conn, destination_path):
    with sqlite3.connect(destination_path) as dest:
        conn.backup(dest, pages=64, sleep=0.25)
```

`VACUUM INTO 'path'` (3.27+) is the one-line alternative and produces a compacted copy. Either way,
what you get is a real database file — unlike a copy of `app.db` taken while `app.db-wal` holds
committed transactions.
