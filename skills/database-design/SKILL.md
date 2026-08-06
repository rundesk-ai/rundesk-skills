---
name: database-design
description: "Apply engine-independent data modelling — normalization, keys, relationship shapes, polymorphic associations, hierarchies, temporal history, audit trails, soft delete, optimistic locking, and keyset pagination. Use when designing a new schema or reviewing one someone proposed, modelling a many-to-many or parent-child relationship, deciding where a nullable column or a JSON blob belongs, keeping historical versions of a row, recording who changed what and when, choosing between deleting and retiring a record, handling two users editing the same row, or paginating a list that will get long."
---

# Database Design

Modelling decisions that are true before an engine is chosen: what the tables are, what identifies a
row, which relationships exist, and how time and deletion are represented. These outlive the
engine — a schema you regret survives every migration you run on it, because the application is
written against its shape.

## Scope

This skill owns the model. It does not own engine tuning, and does not restate it:

| Question | Skill that owns it |
|---|---|
| PostgreSQL indexes, planner behaviour, RLS, pooling, `EXPLAIN` | `postgres-patterns` |
| MySQL/InnoDB indexes, locking, online DDL, replication, connection limits | `mysql-patterns` |
| SQLite PRAGMAs, WAL, FTS5, table rebuilds, the single-file hazards | `sqlite-patterns` |

When a modelling decision below has an index or a locking consequence, this skill names the
consequence and points you at whichever of those three you are running. What index type serves it,
and what the planner does with it, is their answer, not this one's.

## How to Use

Read the reference for the pattern at hand — not both, and not all of either.

| Read | When |
|---|---|
| [references/advanced-patterns.md](references/advanced-patterns.md) | Polymorphic associations and inheritance, hierarchies (adjacency list, materialized path, closure table), temporal and bitemporal history, JSON columns, denormalization and summary tables, keyset pagination, and the shape of a safe schema change |
| [references/security-examples.md](references/security-examples.md) | Storing credentials or PII, multi-tenant isolation, roles and permissions tables, audit logs, immutable records, optimistic locking, retention and anonymization, and constraints that encode a business rule |

Both reference files write their DDL in SQLite dialect, because it is the smallest and every engine
reads it. The *shapes* are portable; the spellings are not — `datetime('now')` is `now()` in
PostgreSQL and `NOW()` in MySQL, `TEXT` timestamps are `timestamptz` and `DATETIME`, and
`INTEGER PRIMARY KEY` is `bigserial`/`BIGINT AUTO_INCREMENT`. Translate through the engine skill you
are using.

## Normalization

- **Start at 3NF.** Every non-key column depends on the key, the whole key, and nothing but the key.
  Anything else is a claim you will have to keep true by hand.
- **Denormalize from a measurement, not a prediction.** A duplicated column is a second source of
  truth, and the trigger or job that keeps it current is code that can be wrong. Pay that only when
  a profile shows the join is the problem.
- **A repeating group is a table.** `tag1, tag2, tag3` and `tags TEXT -- "a,b,c"` are the same
  mistake: you cannot index them, constrain them, or join through them.
- **Under-normalizing is the common failure, not over-normalizing.** The usual real symptom is one
  wide table carrying several entities' worth of columns, most of them null for most rows.

## Keys and Identity

- **Every table has a primary key.** A table without one has no way to name a row, so no update or
  delete can be trusted to hit exactly one.
- **Separate the surrogate key from the business key.** The surrogate identifies the row forever;
  the business key (an email, an SKU, an invoice number) is what people mean, and it changes. Give
  the business key a `UNIQUE` constraint and never make it the target of a foreign key.
- **Prefer narrow, monotonic surrogates.** Every foreign key and index carries a copy of it. Random
  UUIDs as the clustered key cost write locality on MySQL/InnoDB and PostgreSQL both — see those
  skills for the mechanics, and keep the UUID in a unique column if an external identifier is
  required.
- **A composite primary key is right for a pure junction table** — `(document_id, tag_id)` — and
  wrong once that relationship acquires attributes of its own.
- **Null means "unknown", not "none" and not "zero".** A nullable column with three meanings is
  three columns, or an enum, in disguise.

## Relationships

- **One-to-many** is a foreign key on the many side. Choose the `ON DELETE` action deliberately:
  `CASCADE` when the child cannot exist alone, `RESTRICT` when the delete should be refused,
  `SET NULL` when the link is optional. The default — no action — is the one nobody chose.
- **Many-to-many** is a junction table, always. Give it its own columns when the relationship has
  attributes (a role, a position, a joined-at), and a surrogate key at that point.
- **One-to-one** is usually one table. It earns a second when the columns have a different lifetime,
  a different access pattern, or a different sensitivity — a credential row apart from a profile row.
- **Self-referential** relationships are hierarchies, and how you store them decides which queries
  are cheap. Adjacency list, materialized path, and closure table are in
  [references/advanced-patterns.md](references/advanced-patterns.md).
- **Index the child side of every foreign key.** No engine here does it for you on the referencing
  column, and an unindexed one turns a parent delete into a scan. The index syntax and what the
  planner does with it belong to `postgres-patterns`, `mysql-patterns`, or `sqlite-patterns`.

## Constraints

Constraints are the last line, and the only line that holds when a second application, a migration
script, or a person with a SQL prompt writes to the table.

- `NOT NULL` on everything that is genuinely required. Retrofitting it means backfilling.
- `UNIQUE` on every business key, including the composite ones.
- `CHECK` for enumerations, ranges, and cross-column rules — an `end_date >= start_date` is one line
  and removes a class of bug permanently.
- `FOREIGN KEY` wherever a column holds another table's key, even when the application "always" sets
  it correctly.

A constraint that only exists in application code is a convention. Conventions do not survive the
second writer.

## Polymorphism and Inheritance

One relationship, several possible target types. Three shapes, and the choice is about where the
nulls and the integrity go:

- **Single table** — every type in one table with type-specific nullable columns. Simplest, but the
  table fills with nulls and no constraint stops an email-only column from being set on an SMS row
  unless you write it.
- **Class table** — a base table plus one table per type. Every column is meaningful and every
  foreign key is real; reading a full object needs a join.
- **Separate nullable foreign keys** with a `CHECK` that exactly one is set — real referential
  integrity, and it stops scaling around the fourth or fifth type.

Worked out, with the constraints and partial indexes each needs, in
[references/advanced-patterns.md](references/advanced-patterns.md).

## History and Time

- **A row that is updated in place has no history.** If anyone will ask what the price was in March,
  the current value is not enough, and reconstructing it later is not possible.
- **Versioned rows (SCD Type 2)** carry `valid_from`/`valid_to` with the current version open-ended.
  Enforce "one current version" with a partial unique index on the business key where the row is
  open — a plain `UNIQUE(business_key, valid_to)` does **not** do it, because nulls do not collide.
- **Bitemporal** separates when something was true from when you recorded it. Real for finance,
  contracts, and anything with retroactive corrections; overkill everywhere else.
- **An audit log answers "who changed this", which is a different question** from "what did it say
  then". A log of changes is not a version history, and a version history has no actor. Decide which
  one you actually need; build both only if both get read.

## Deletion

- **Soft delete is a state, so model it as one.** A `deleted_at` timestamp beats a boolean: it
  records when, and it is still a clean `IS NULL` test.
- **Every query then has to remember.** Give readers a view that filters, and index for the
  filtered set — a partial or filtered index over the live rows, on whichever engine you are on.
- **Soft-deleted rows still occupy their unique constraints.** A retired user keeps their email
  address, and the next signup with it fails. Decide up front: release the value on delete, or
  include the delete marker in the uniqueness.
- **Erasure requests need real deletion or anonymization**, not a flag. Anonymizing in place
  preserves referential integrity where a hard delete would break it.

## Concurrency in the Model

- **Optimistic locking is a `version` column**, incremented on every write, checked in the `WHERE`
  clause. Zero rows affected means someone else got there first, and the application decides what to
  do about it. This is the portable answer and it costs one integer.
- Pessimistic locking — `SELECT ... FOR UPDATE`, isolation levels, deadlock ordering — is engine
  behaviour. See `postgres-patterns` or `mysql-patterns`.

## Pagination

- **Keyset pagination, not `OFFSET`,** for any list that can grow. `OFFSET 10000` makes the engine
  produce and discard ten thousand rows on every page.
- **The sort key must be total.** Order by the timestamp *and* the primary key, and carry both in
  the cursor — ties on a non-unique sort column skip and repeat rows across pages.
- **The model owes the index its shape.** Design the sort so a single index can serve it; see
  `postgres-patterns`, `mysql-patterns`, or `sqlite-patterns` for how to declare it.

## Common Mistakes

| Mistake | Instead |
|---|---|
| No primary key | Surrogate key on every table |
| A list in a column: `tags TEXT` = `"a,b,c"` | Junction table |
| Foreign key column with no constraint | `REFERENCES` with a chosen `ON DELETE` |
| Business key as the foreign key target | Surrogate as the target, `UNIQUE` on the business key |
| `is_deleted BOOLEAN` | `deleted_at` timestamp |
| `UNIQUE(key, valid_to)` for "one current row" | Partial unique index where `valid_to IS NULL` |
| Storing a money amount as a float | Integer minor units, or the engine's exact decimal type |
| Local timestamps with no zone | UTC, in the engine's timestamp-with-zone type |
| Denormalizing before measuring | Normalize, measure, then denormalize with a maintainer |
| "The table has 10M rows, so it scans" | Row count is not the cause; the missing or unusable index is |

## Guardrails

- Design from the queries. A schema nobody has written a query against is a guess.
- Say which normal form you left and why, whenever you leave one.
- Schema changes on a live table are engine-specific and are the engine skill's territory:
  `mysql-patterns` for online DDL, `sqlite-patterns` for the table rebuild procedure,
  `postgres-patterns` for lock-taking DDL.
- Get explicit human approval before any migration that drops a column, drops a table, or rewrites
  data — and before running one without a restore you have tested.
