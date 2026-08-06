---
name: sqlite-patterns
description: "Apply SQLite patterns for connection PRAGMAs, WAL, transactions, migrations, FTS5, indexing, and parameterized queries. Use when embedding SQLite in an application, choosing journal or synchronous settings, writing SQL that takes user input, planning a schema change, building full-text search, backing up or copying a database file, or diagnosing `database is locked`, a slow query, a corrupt FTS index, or a database file that will not shrink."
---

# SQLite Patterns

SQLite is a library linked into your process, not a server you connect to. Almost every rule below
follows from that: configuration is per-connection and has to be reapplied every time you open one,
there is exactly one writer at a time, and the database is a file whose permissions and backups are
your problem rather than a DBA's.

This skill is engine-level and language-neutral — the rules are SQL and PRAGMA. Worked examples use
Python's standard-library `sqlite3` because it is the thinnest binding; the same calls exist in
every other binding.

## How to Use

Read the reference for the task at hand — not all of them.

| Read | When |
|---|---|
| [references/advanced-patterns.md](references/advanced-patterns.md) | Writing a migration or rebuilding a table, setting up or repairing FTS5, using recursive CTEs, window functions, or the JSON functions, reusing connections across threads, or scheduling `ANALYZE`/`VACUUM`/backups |
| [references/security-examples.md](references/security-examples.md) | Any SQL that carries user input, `LIKE` patterns, dynamic column or sort order, file permissions on the database and its sidecar files, error messages that reach a user, an audit log, or injection test cases |
| [references/rust-bindings.md](references/rust-bindings.md) | Working in Rust, where `rusqlite`, `sea-query`, and `r2d2` supply the same patterns |

## Connection Setup

Only `journal_mode` and a handful of others persist in the file. The rest are per-connection
defaults that reset on every open, so set them in one place that every connection goes through.

```python
def connect(path):
    conn = sqlite3.connect(path, isolation_level=None)  # explicit BEGIN, no implicit commits
    conn.executescript("""
        PRAGMA journal_mode = WAL;      -- persists in the file; set once, harmless to repeat
        PRAGMA foreign_keys = ON;       -- OFF by default, per connection, every time
        PRAGMA busy_timeout = 5000;     -- wait for the writer instead of failing instantly
        PRAGMA synchronous = NORMAL;    -- safe under WAL; see below
        PRAGMA cache_size = -64000;     -- negative means KiB, so 64 MB
        PRAGMA temp_store = MEMORY;
    """)
    return conn
```

- **`foreign_keys` is off by default and is per-connection.** A connection that forgets it silently
  accepts orphan rows. It also cannot be changed inside a transaction.
- **`synchronous = NORMAL` is safe with WAL and not otherwise.** Under WAL it cannot corrupt the
  database; a power loss can lose transactions committed since the last checkpoint. Under the
  rollback journal, `NORMAL` risks corruption — keep `FULL` there.
- **`busy_timeout` is the fix for most `database is locked` reports.** Without it a second writer
  fails immediately rather than waiting.
- **Do not set `mmap_size` as a default.** Memory-mapped reads save a copy, but an I/O error inside
  a mapping arrives as a fatal signal (`SIGBUS`) instead of an error code your program can handle,
  and the mapping consumes process address space. Treat it as a tuning knob: measure first, then
  set it to the size of the working set you actually read, on a build and platform you have tested.
  The frequently copied `PRAGMA mmap_size = 30000000000` is a 30 GB address-space reservation
  pasted as if it were a default, and it is not one.
- **Do not set `page_size` after the fact.** It only takes effect before the first table is created
  or immediately after a `VACUUM`, and 4096 has been the default since 3.12 — the usual
  `PRAGMA page_size = 4096` line does nothing.

**WAL costs you the single-file property.** The database becomes `app.db`, `app.db-wal`, and
`app.db-shm`. Copying only `app.db` from a running system loses every committed transaction still
in the WAL. WAL also requires shared memory, so it does not work on most network filesystems.

## Queries and User Input

- **Bind parameters; never format SQL.** `?` positional or `:name` named. This is the whole of
  injection defence for values.
- **Values bind, identifiers do not.** A column or sort direction chosen at runtime must come from
  a whitelist you wrote, compared exactly, before it goes into the string.
- **`LIKE` needs its own escaping.** `%` and `_` in user input are wildcards. Escape them and add
  `ESCAPE '\'` to the query — escaping without the clause does nothing.
- **Error messages should not carry SQL.** Log the driver error; return a category to the caller.

See [references/security-examples.md](references/security-examples.md) for each of these worked out,
including the test cases that prove them.

## Transactions and Concurrency

- **One writer at a time, database-wide.** WAL lets readers run during a write; it does not give
  you two writers. Under contention, `busy_timeout` plus short transactions is the answer, not a
  larger connection pool.
- **Name the transaction type.** `BEGIN IMMEDIATE` takes the write lock up front. A plain `BEGIN`
  is deferred, so a read-then-write transaction can fail with `SQLITE_BUSY` on the upgrade after it
  has already done work — and that failure cannot be resolved by waiting.
- **Batch writes into one transaction.** Committing per row is roughly two orders of magnitude
  slower, because each commit is a durability barrier.
- **Do no network or user I/O inside a transaction.** You are holding the only write lock.

```python
conn.execute("BEGIN IMMEDIATE")
conn.executemany("INSERT INTO items (name) VALUES (?)", records)
conn.execute("COMMIT")
```

## Schema and Migrations

- **Version the schema in the file.** `PRAGMA user_version` is a free integer counter for simple
  cases; a `schema_migrations` table buys you names and timestamps.
- **Run each migration in a transaction, and record it in the same transaction.** A migration that
  applied but was not recorded runs twice.
- **`ALTER TABLE` is narrow.** Add a column, rename a column or table, drop a column (3.35+). Any
  other change — adding a constraint, changing a type, reordering — means rebuilding the table.
- **Rebuild tables by the documented procedure.** `PRAGMA foreign_keys = OFF` *outside* the
  transaction, create the new table, copy, drop, rename, `PRAGMA foreign_key_check`, commit, then
  turn foreign keys back on. Rebuilding with foreign keys enabled lets `ON DELETE CASCADE` delete
  rows out of other tables when you drop the old table.

The full rebuild sequence and a migration runner are in
[references/advanced-patterns.md](references/advanced-patterns.md).

## Full-Text Search

- **Use FTS5, not `LIKE '%term%'`.** A leading wildcard cannot use an index; FTS5 is an inverted
  index built for this.
- **External-content tables need all three triggers.** `INSERT`, `UPDATE`, and `DELETE`, with the
  `'delete'` command issued using the *old* values. Ship only the insert trigger and the index
  drifts out of sync with the table and returns rows that no longer exist.
- **`ORDER BY rank`, ascending.** FTS5's `rank` is the `bm25()` score, which is more negative for a
  better match, so ascending order puts the best matches first.
- **Do not pass raw user input to `MATCH`.** It is a query language, not a string: a stray `"` or
  `*` is a syntax error, not a no-result search. Quote user terms as a phrase, doubling any `"`.

## Indexing and Query Plans

- **`EXPLAIN QUERY PLAN` is the evidence.** `SCAN <table>` on a table you expected to seek means
  the index is missing or unusable.
- **Composite index order is equality columns first, then the range or sort column.**
- **SQLite does not index foreign key columns for you.** The parent side is indexed by its primary
  key; the child side is not, and `ON DELETE CASCADE` scans without it.
- **`ANALYZE` once the table has representative data**, then `PRAGMA optimize` on close. Without
  statistics the planner guesses.

## Maintenance and Operations

- **`VACUUM` rewrites the whole database and needs free space for a second copy.** Run it when the
  free-page count justifies it, not on a schedule and not during peak load. `VACUUM INTO 'path'`
  writes a compacted copy without touching the live file.
- **Back up with the backup API or `VACUUM INTO`, not `cp`.** Copying a live database file races
  with the writer and with the WAL.
- **The file permissions are the access control.** SQLite has no users or grants: whoever can read
  the file can read every row. Mode `0600` on the database and on `-wal`/`-shm`.
- **Track the engine version.** Fixes ship in point releases and the features here have floors:
  FTS5 and window functions 3.25+, `ALTER TABLE ... DROP COLUMN` 3.35+, `VACUUM INTO` 3.27+. Pin a
  minimum you have tested and keep moving it forward.

## Common Mistakes

| Mistake | Wrong | Right |
|---|---|---|
| Building SQL by formatting | `f"... WHERE name = '{name}'"` | `"... WHERE name = ?"` with a bound value |
| Foreign keys assumed on | Default connection | `PRAGMA foreign_keys = ON` on every connection |
| Commit per row | `execute` + `commit` in a loop | One transaction around `executemany` |
| `LIKE` for search | `LIKE '%term%'` | FTS5 `MATCH` |
| Escaping `LIKE` without the clause | `name LIKE ?` with `\%` in the value | `name LIKE ? ESCAPE '\'` |
| Copying a live database | `cp app.db backup.db` | `VACUUM INTO` or the backup API |
| `mmap_size` pasted as a default | `PRAGMA mmap_size = 30000000000` | Leave unset until measured |
| Deferred read-then-write | `BEGIN` | `BEGIN IMMEDIATE` |

## Guardrails

- Measure before and after. A change that does not show up in `EXPLAIN QUERY PLAN` or in the timing
  did not do anything.
- State the version floor when the advice depends on one.
- Get explicit human approval before destructive operations — `DROP`, `VACUUM` on a live database,
  unbounded `DELETE`, or any table rebuild against real data without a verified backup.
- Other engines are other skills. For PostgreSQL see `postgres-patterns`; for MySQL/InnoDB see
  `mysql-patterns`. For modelling questions that precede the engine choice, see `database-design`.

## References

- https://www.sqlite.org/docs.html
- https://www.sqlite.org/wal.html
- https://www.sqlite.org/fts5.html
- https://www.sqlite.org/lang_altertable.html#otheralter
