# SQLite from Rust

The rules in `SKILL.md` are engine-level and hold whatever the host language is. This file is the
Rust binding: `rusqlite` for the connection, `r2d2` for reuse, `sea-query` when a query has to be
assembled at runtime. Read it only if you are writing Rust — the SQL and PRAGMA guidance lives in
[advanced-patterns.md](advanced-patterns.md) and [security-examples.md](security-examples.md).

## Versions and Dependencies

| Crate | Floor | Notes |
|---|---|---|
| SQLite | 3.35 | `ALTER TABLE ... DROP COLUMN`; 3.25 is the floor for FTS5 and window functions |
| `rusqlite` | 0.29 | `bundled` compiles a known SQLite version in rather than using the system one |
| `sea-query` | 0.28 | Only needed for runtime-assembled queries |
| `r2d2` | 0.8 | Connection pool |

```toml
[dependencies]
rusqlite = { version = "0.31", features = ["bundled", "backup", "functions"] }
sea-query = "0.30"
sea-query-rusqlite = "0.5"
r2d2 = "0.8"
r2d2_sqlite = "0.24"
```

The `bundled` feature is the reason to prefer it: the SQLite version is then a property of your
build rather than of whatever the machine happens to ship, so the version floors above are
something you control. Check the crate's own release notes for the exact SQLite version each
release bundles.

## Opening a Connection

```rust
use rusqlite::{Connection, Result};
use std::path::Path;

pub fn open(path: &Path) -> Result<Connection> {
    let conn = Connection::open(path)?;
    conn.execute_batch(
        "PRAGMA journal_mode = WAL;
         PRAGMA foreign_keys = ON;
         PRAGMA busy_timeout = 5000;
         PRAGMA synchronous = NORMAL;
         PRAGMA cache_size = -64000;
         PRAGMA temp_store = MEMORY;",
    )?;
    Ok(conn)
}
```

Every one of those except `journal_mode` is per-connection and resets on the next open, so this
function is the only place a connection should be created. Note what is absent: no `mmap_size`, no
`page_size`. See `SKILL.md` for why neither belongs in a default.

## Parameterized Queries

```rust
use rusqlite::{params, Connection, OptionalExtension, Result};

// Correct: positional parameters.
pub fn get_user(conn: &Connection, id: i64) -> Result<Option<User>> {
    conn.query_row(
        "SELECT id, name, email FROM users WHERE id = ?1",
        [id],
        |row| Ok(User { id: row.get(0)?, name: row.get(1)?, email: row.get(2)? }),
    )
    .optional()
}

// Correct: named parameters, with the ESCAPE clause the escaping depends on.
pub fn search_users(conn: &Connection, name: &str, status: &str) -> Result<Vec<User>> {
    let mut stmt = conn.prepare(
        "SELECT id, name, email FROM users
         WHERE name LIKE :pattern ESCAPE '\\' AND status = :status",
    )?;
    let pattern = format!("%{}%", escape_like(name));
    stmt.query_map(
        &[(":pattern", &pattern as &dyn rusqlite::ToSql), (":status", &status)],
        |row| Ok(User { id: row.get(0)?, name: row.get(1)?, email: row.get(2)? }),
    )?
    .collect()
}

// Correct: params! for a mix of types.
pub fn insert_document(conn: &Connection, user_id: i64, title: &str, body: &str) -> Result<i64> {
    conn.execute(
        "INSERT INTO documents (user_id, title, content) VALUES (?1, ?2, ?3)",
        params![user_id, title, body],
    )?;
    Ok(conn.last_insert_rowid())
}

/// Escape LIKE metacharacters. Useless unless the SQL carries ESCAPE '\'.
pub fn escape_like(pattern: &str) -> String {
    pattern.replace('\\', "\\\\").replace('%', "\\%").replace('_', "\\_")
}
```

Rust's type system does not stop injection on its own. `format!` into a query string is exactly as
dangerous here as anywhere else:

```rust
// Wrong: injection, regardless of the language.
let query = format!("SELECT * FROM users WHERE id = {}", id_from_request);
```

Parse first, then bind the parsed value: `let id: i64 = raw.parse().map_err(...)?;`. A parse failure
is a clean rejection at the boundary.

## Whitelisted Identifiers

```rust
const SORTABLE: &[&str] = &["id", "name", "email", "created_at"];

pub fn list_users_sorted(conn: &Connection, sort: &str, desc: bool) -> Result<Vec<User>> {
    let column = SORTABLE
        .iter()
        .find(|c| **c == sort)
        .ok_or_else(|| rusqlite::Error::InvalidParameterName(format!("unsortable: {sort}")))?;
    let direction = if desc { "DESC" } else { "ASC" };

    // Safe: both fragments are constants from this file.
    let sql = format!("SELECT id, name, email FROM users ORDER BY {column} {direction}");
    let mut stmt = conn.prepare(&sql)?;
    stmt.query_map([], |row| {
        Ok(User { id: row.get(0)?, name: row.get(1)?, email: row.get(2)? })
    })?
    .collect()
}
```

Equality against a constant list, and the direction from a `bool` rather than from a caller-supplied
string. `sort_order.to_uppercase()` compared against `["ASC", "DESC"]` with an `unwrap_or` fallback
is the same idea done loosely — it accepts anything and quietly sorts ascending, so a typo in the
caller looks like working code.

## Migrations

```rust
use rusqlite::{Connection, Result};

struct Migration {
    version: i32,
    name: &'static str,
    up: &'static str,
}

const MIGRATIONS: &[Migration] = &[
    Migration {
        version: 1,
        name: "create_users",
        up: "CREATE TABLE users (
                 id INTEGER PRIMARY KEY,
                 name TEXT NOT NULL,
                 email TEXT NOT NULL UNIQUE,
                 created_at TEXT NOT NULL DEFAULT (datetime('now'))
             );",
    },
    Migration {
        version: 2,
        name: "create_documents",
        up: "CREATE TABLE documents (
                 id INTEGER PRIMARY KEY,
                 user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                 title TEXT NOT NULL,
                 content TEXT
             );
             CREATE INDEX idx_documents_user ON documents(user_id);",
    },
];

pub fn migrate(conn: &mut Connection) -> Result<()> {
    conn.execute_batch(
        "CREATE TABLE IF NOT EXISTS schema_migrations (
             version INTEGER PRIMARY KEY,
             name TEXT NOT NULL,
             applied_at TEXT NOT NULL DEFAULT (datetime('now'))
         );",
    )?;

    let current: i32 = conn.query_row(
        "SELECT COALESCE(MAX(version), 0) FROM schema_migrations",
        [],
        |row| row.get(0),
    )?;

    for migration in MIGRATIONS.iter().filter(|m| m.version > current) {
        let tx = conn.transaction()?;
        tx.execute_batch(migration.up)?;
        tx.execute(
            "INSERT INTO schema_migrations (version, name) VALUES (?1, ?2)",
            rusqlite::params![migration.version, migration.name],
        )?;
        tx.commit()?;
    }
    Ok(())
}
```

`Connection::transaction` takes `&mut self` and gives you a guard that rolls back on drop — which is
what you want. `unchecked_transaction` exists to work around the borrow checker on a shared
connection and gives up that compile-time guarantee; reach for it only when the alternative is
worse, and never in a loop where an early `?` would skip the rollback.

Bind the version as an integer. `migration.version.to_string()` writes the number into an INTEGER
column as text, and SQLite's type affinity will usually convert it — until the column is one where
it does not.

## Rebuilding a Table

The order matters, and the two easy mistakes are doing it with foreign keys enabled and skipping the
check before commit.

```rust
pub fn rebuild_users(conn: &mut Connection) -> Result<()> {
    conn.execute_batch("PRAGMA foreign_keys = OFF")?; // must be outside the transaction

    let result = (|| -> Result<()> {
        let tx = conn.transaction()?;
        tx.execute_batch(
            "CREATE TABLE users_new (
                 id INTEGER PRIMARY KEY,
                 full_name TEXT NOT NULL,
                 email TEXT NOT NULL UNIQUE,
                 status TEXT NOT NULL DEFAULT 'active'
             );
             INSERT INTO users_new (id, full_name, email, status)
                 SELECT id, name, email, COALESCE(status, 'active') FROM users;
             DROP TABLE users;
             ALTER TABLE users_new RENAME TO users;
             CREATE INDEX idx_users_email ON users(email);",
        )?;

        let violations: i64 =
            tx.query_row("SELECT count(*) FROM pragma_foreign_key_check", [], |r| r.get(0))?;
        if violations > 0 {
            return Err(rusqlite::Error::InvalidQuery);
        }
        tx.commit()
    })();

    conn.execute_batch("PRAGMA foreign_keys = ON")?; // restored on both paths
    result
}
```

`DROP TABLE users` with foreign keys still on fires `ON DELETE CASCADE` across every child table.
That is why the PRAGMA comes first — and why turning it back on has to happen even when the
transaction failed.

## Connection Pool

```rust
use r2d2::{Pool, PooledConnection};
use r2d2_sqlite::SqliteConnectionManager;
use rusqlite::OpenFlags;
use std::path::Path;

pub struct DatabasePool {
    pool: Pool<SqliteConnectionManager>,
}

impl DatabasePool {
    pub fn new(path: &Path, size: u32) -> Result<Self, r2d2::Error> {
        let manager = SqliteConnectionManager::file(path)
            .with_flags(
                OpenFlags::SQLITE_OPEN_READ_WRITE
                    | OpenFlags::SQLITE_OPEN_CREATE
                    | OpenFlags::SQLITE_OPEN_NO_MUTEX,
            )
            .with_init(|conn| {
                conn.execute_batch(
                    "PRAGMA journal_mode = WAL;
                     PRAGMA foreign_keys = ON;
                     PRAGMA busy_timeout = 5000;
                     PRAGMA synchronous = NORMAL;
                     PRAGMA cache_size = -64000;",
                )
            });

        Pool::builder().max_size(size).min_idle(Some(2)).build(manager).map(|pool| Self { pool })
    }

    pub fn get(&self) -> Result<PooledConnection<SqliteConnectionManager>, r2d2::Error> {
        self.pool.get()
    }
}

pub fn list_users(pool: &DatabasePool) -> Result<Vec<User>, String> {
    let conn = pool.get().map_err(|e| e.to_string())?;
    let mut stmt = conn
        .prepare("SELECT id, name, email FROM users")
        .map_err(|e| e.to_string())?;
    stmt.query_map([], |row| {
        Ok(User { id: row.get(0)?, name: row.get(1)?, email: row.get(2)? })
    })
    .map_err(|e| e.to_string())?
    .collect::<Result<Vec<_>, _>>()
    .map_err(|e| e.to_string())
}
```

`with_init` is what makes the pool correct: without it, a connection recycled from the pool is a
connection with foreign keys off. `SQLITE_OPEN_NO_MUTEX` says each connection is used by one thread
at a time, which the pool guarantees and you must not defeat by cloning a connection out of it.

Sizing the pool does not buy write throughput — SQLite has one writer for the whole database.
Extra connections queue on the same lock. Size for readers.

Converting every error to `String` at the boundary, as `list_users` does, keeps driver text out of
whatever calls it — but log the real error before you flatten it, or you have thrown away the only
diagnostic.

## Runtime-Assembled Queries with `sea-query`

```rust
use sea_query::{Expr, Iden, Query, SqliteQueryBuilder};
use sea_query_rusqlite::RusqliteBinder;

#[derive(Iden)]
enum Users {
    Table,
    Id,
    Name,
    Email,
    Status,
}

pub fn search(
    conn: &Connection,
    name: Option<&str>,
    status: Option<&str>,
    limit: u64,
) -> Result<Vec<User>> {
    let mut query = Query::select();
    query.columns([Users::Id, Users::Name, Users::Email]).from(Users::Table);

    if let Some(name) = name {
        query.and_where(Expr::col(Users::Name).like(format!("%{}%", escape_like(name))));
    }
    if let Some(status) = status {
        query.and_where(Expr::col(Users::Status).eq(status));
    }
    query.limit(limit);

    let (sql, values) = query.build_rusqlite(SqliteQueryBuilder);
    let mut stmt = conn.prepare(&sql)?;
    stmt.query_map(&*values.as_params(), |row| {
        Ok(User { id: row.get(0)?, name: row.get(1)?, email: row.get(2)? })
    })?
    .collect()
}
```

The builder's value is that column names come from the `Iden` enum — an identifier that does not
exist is a compile error rather than a runtime string. Values still become bound parameters.

Note the `escape_like` call: a query builder binds the value but has no opinion about the `LIKE`
metacharacters inside it. That is still yours. If you need `ESCAPE`, express it in the builder or
write that predicate by hand.

## FTS5 Maintenance

```rust
pub fn optimize_fts(conn: &Connection) -> Result<()> {
    conn.execute("INSERT INTO docs_fts(docs_fts) VALUES('optimize')", [])?;
    Ok(())
}

pub fn rebuild_fts(conn: &Connection) -> Result<()> {
    conn.execute("INSERT INTO docs_fts(docs_fts) VALUES('rebuild')", [])?;
    Ok(())
}

/// integrity-check returns no rows; it reports by failing.
pub fn fts_is_consistent(conn: &Connection) -> bool {
    conn.execute("INSERT INTO docs_fts(docs_fts) VALUES('integrity-check')", [])
        .is_ok()
}
```

`query_row` against an `INSERT` never yields a row, so an integrity check written that way always
takes its error path — and a version that swallows the error with `unwrap_or("ok")` reports every
database as healthy, including a corrupt one. `execute` plus `is_ok` is the check.

## Testing

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use rusqlite::Connection;

    fn test_db() -> Connection {
        let mut conn = Connection::open_in_memory().unwrap();
        conn.execute_batch("PRAGMA foreign_keys = ON").unwrap();
        migrate(&mut conn).unwrap();
        conn
    }

    #[test]
    fn payload_round_trips_as_data() {
        let conn = test_db();
        let payload = "'; DROP TABLE users; --";
        conn.execute(
            "INSERT INTO users (name, email) VALUES (?1, ?2)",
            rusqlite::params![payload, "payload@example.test"],
        )
        .unwrap();

        let stored: String = conn
            .query_row("SELECT name FROM users WHERE email = ?1", ["payload@example.test"], |r| {
                r.get(0)
            })
            .unwrap();
        assert_eq!(payload, stored, "value was interpreted rather than bound");
    }

    #[test]
    fn search_payload_matches_nothing() {
        let conn = test_db();
        let found = search_users(&conn, "' OR 1=1--", "active").unwrap();
        assert!(found.is_empty(), "payload matched rows it should not");
    }

    #[test]
    fn unsortable_column_is_rejected() {
        let conn = test_db();
        assert!(list_users_sorted(&conn, "name; DROP TABLE users", false).is_err());
    }
}
```

`assert!(result.is_ok())` is not an injection test — a query that safely matched nothing and a query
that returned the whole table both satisfy it. Assert on the rows and on the row count.

In-memory databases are per-connection: `Connection::open_in_memory()` twice gives two unrelated
databases, and a pool of in-memory connections gives each one an empty schema. Use one connection
per test, or a temporary file when the code under test needs a pool.
