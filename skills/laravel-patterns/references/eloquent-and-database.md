# Eloquent and the database

Read this when writing or reviewing models, queries, migrations, or anything that touches data.

## Turn silent bugs into exceptions

The single highest-value line in a Laravel application. In `AppServiceProvider::boot()`:

```php
use Illuminate\Database\Eloquent\Model;

public function boot(): void
{
    Model::preventLazyLoading(! $this->app->isProduction());
    Model::preventSilentlyDiscardingAttributes(! $this->app->isProduction());
}
```

- `preventLazyLoading` throws `LazyLoadingViolationException` on any lazy-loaded relationship, which
  is how N+1 gets caught in development instead of in a slow-query log.
- `preventSilentlyDiscardingAttributes` throws when you fill an attribute missing from `$fillable` —
  otherwise the write is silently dropped and the bug surfaces as "the field never saves."

Guard both on `! isProduction()` so a missed case degrades rather than takes the site down. To log
instead of throw, use `Model::handleLazyLoadingViolationUsing(...)`.

## N+1 and eager loading

```php
// ❌ one query per book
$books = Book::all();
foreach ($books as $book) { echo $book->author->name; }

// ✅ two queries
$books = Book::with('author')->get();

// ✅ nested, and constrained
$books = Book::with(['author.contacts', 'reviews' => fn ($q) => $q->latest()->limit(3)])->get();

// ✅ already have the models
$books->load('author');
```

- **Count without loading:** `Post::withCount('comments')` gives `comments_count`. Loading the
  relationship to call `->count()` on it reads every row for a number.
- **Existence without loading:** `Post::has('comments')`, `whereHas`, `doesntHave`. `whereHas` with a
  heavy closure is a correlated subquery — check the plan on large tables.
- **Selecting columns on an eager load:** Laravel warns you "should always include the `id` column
  and any relevant foreign key columns," or the relationship cannot be matched back up.
- **`$with` on the model** always loads a relationship. Useful for a relationship genuinely always
  needed; a trap when it is not, because it taxes every query in the application.
- **Cross-database relationships:** "Eloquent does not currently support querying for relationship
  existence across databases."

## Iterating large result sets

| Method | Memory | Eager loading | Use when |
|---|---|---|---|
| `get()` | all rows | yes | the set is bounded and small |
| `chunk(n)` | one chunk | yes | batch processing, **not** modifying the filtered column |
| `chunkById(n)` | one chunk | yes | batch processing that **updates the column being filtered** |
| `lazy()` | one chunk | yes | streaming with relationships |
| `cursor()` | one model | **no** | streaming, no relationships, still bounded by PDO buffering |

Two documented traps:

- **`chunk` while updating the filter column** skips rows. Laravel: using `chunk` in these scenarios
  "could lead to unexpected and inconsistent results." Use `chunkById`.
- **`cursor()` cannot eager load** — "since the `cursor` method only ever holds a single Eloquent
  model in memory at a time, it cannot eager load relationships." It also still buffers raw results
  in PDO, so it is not unbounded; `lazy()` is the safer default.

`chunkById` and `lazyById` add their own `where` clauses, so group your own conditions in a closure:

```php
Flight::where(fn ($q) => $q->where('delayed', true)->orWhere('cancelled', true))
    ->chunkById(200, fn ($flights) => $flights->each->update(['departed' => false]), column: 'id');
```

## Choosing how to read a set — the decision that matters most

Before writing any query, answer: **how large can this get?** Not how large it is today.

| Rows | Reading it | Writing to it |
|---|---|---|
| Bounded and small (a config table, one user's addresses) | `get()` | `save()` |
| A page a human looks at | `paginate()` / `simplePaginate()` / `cursorPaginate()` | — |
| Thousands, in a job | `lazy()` or `chunkById()` | `chunkById()` |
| Millions | `chunkById()` with a queued batch per chunk | bulk `upsert()` / `insert()` |
| Just a count or a sum | `count()`, `sum()`, `exists()` | — |

Two failures this prevents, both common:

```php
// ❌ loads every order into memory, then counts them in PHP
$count = Order::where('status', 'paid')->get()->count();
// ✅
$count = Order::where('status', 'paid')->count();

// ❌ loads every row to find out whether one exists
if (Order::where('user_id', $id)->get()->isNotEmpty()) { ... }
// ✅
if (Order::where('user_id', $id)->exists()) { ... }
```

`Model::all()` in a codebase is worth grepping for. It is correct on a lookup table and a latent
outage on anything a customer adds rows to.

**Pagination:** offset pagination (`paginate()`) gets slower the deeper the page, because the database
still walks the skipped rows, and it drifts when rows are inserted mid-browse. `simplePaginate()`
drops the total count, which is usually the expensive part. `cursorPaginate()` is stable and fast at
any depth, at the cost of no page numbers and no jumping — the right default for feeds, APIs, and
infinite scroll.

## Query performance

Diagnose before optimizing. Count the queries and read the plan; do not guess.

```php
DB::listen(fn ($q) => logger($q->sql, $q->bindings, $q->time));   // local
Model::preventLazyLoading(! app()->isProduction());               // catches N+1 as an exception
```

Telescope, Debugbar, or Pulse will show query count and duration per request in one page load. Then:

- **Index what you filter, join, and sort on.** Every foreign key, and every column in a `where` or
  `orderBy` that runs on a large table. `EXPLAIN` the query; a full scan on a large table is the
  finding. Composite indexes are ordered — the leftmost prefix rule decides whether yours is used.
- **Select only the columns you need** on wide tables, especially with `TEXT`/`JSON`/`BLOB` columns.
  When selecting columns on an eager load, always include `id` and the foreign keys.
- **Aggregate in SQL, not in PHP.** `withCount`, `withSum`, `withAvg`, and `withExists` on
  relationships; `groupBy` with aggregates on the query. Loading a collection to `->sum()` it reads
  every row for one number.
- **`whereHas` with a heavy closure is a correlated subquery.** On large tables prefer `whereRelation`
  for the simple case, or a join, and check the plan either way.
- **Bulk write instead of looping.** `insert()` for a batch, `upsert()` for insert-or-update — a loop
  of `create()` is one round trip per row. Note `upsert()` needs a unique index, and it bypasses model
  events (below).
- **Do not paginate an already-loaded collection.** `->get()->forPage()` fetched everything first.
- **Beware `orderBy` on an unindexed column with a limit** — the database sorts the whole set to
  return ten rows.
- **Cache the expensive derived result**, not the row. See
  [`performance-and-deployment.md`](performance-and-deployment.md).

### Chunking a write safely

```php
// Update in batches, with the queue doing the work
Order::where('status', 'pending')
    ->where('created_at', '<', now()->subDays(30))
    ->chunkById(500, function ($orders) {
        ExpireOrders::dispatch($orders->pluck('id'));
    });
```

Pass ids, not models, to a job — see the serialization notes in
[`queues-and-jobs.md`](queues-and-jobs.md). And use `chunkById`, never `chunk`, whenever the loop
modifies the column being filtered.

## Mass operations skip model events

This surprises people repeatedly, and it is documented in three places:

> When issuing a mass update via Eloquent, the `saving`, `saved`, `updating`, and `updated` model
> events will not be fired for the updated models. This is because the models are never actually
> retrieved when issuing a mass update.

The same applies to mass deletes and `deleting`/`deleted`. So:

- `Post::where(...)->update([...])` fires nothing. Observers, audit logs, and search indexing that
  hang off model events will not run.
- `Model::destroy($ids)` **does** load each model and fire events, which is why it is slower.
- If a side effect must always happen, do not depend on a model event — put it where the write is.

`upsert()` requires a primary or unique index on the second-argument columns on every database
except SQL Server, and MySQL/MariaDB ignore that argument entirely and use their own indexes.

## Mass assignment

Set `$fillable` explicitly. `$guarded = []` disables the protection completely and makes every
future column writable by whatever the request happened to contain — the failure only shows up when
somebody later adds `is_admin`.

Validation is the other layer: validate, then persist `$request->validated()`. Laravel says it
directly — rejecting unknown fields helps, "however, you should still configure your model's
`$fillable` / `$guarded` properties and only persist trusted, validated input."

## Transactions

```php
DB::transaction(function () use ($data) {
    $order = Order::create($data);
    $order->items()->createMany($data['items']);

    ProcessOrder::dispatch($order)->afterCommit();   // see queues-and-jobs.md
});
```

- Keep transactions short. Never make an HTTP call inside one — the lock is held for the round trip.
- `DB::transaction()` retries on deadlock if you pass an attempt count; a manual
  `beginTransaction`/`commit` does not.
- Anything with an external side effect (mail, queue, webhook) must happen **after** commit, or a
  rollback leaves the world inconsistent with the database.

## Casts, scopes, and accessors

- Cast in the `casts()` method rather than hand-converting at each call site. `AsArrayObject`,
  `AsCollection`, `AsEnumCollection`, `encrypted`, and custom `CastsAttributes` classes all beat an
  accessor that parses a string.
- Local scopes for reusable filters; keep them intention-named (`scopeActive`, not `scopeWhereX`).
- **Global scopes are invisible at the call site.** They are the right tool for tenancy and soft
  deletes and a debugging trap for anything else, because a query that returns fewer rows than the
  developer expects has no clue in it. Document every one, and remember `withoutGlobalScope()`.
- Soft deletes are a global scope: `withTrashed()`, `onlyTrashed()`, `restore()`. Unique indexes do
  not know about them — a soft-deleted row still occupies its unique slot.
- **Pruning force-deletes:** "soft deleting models will be permanently deleted (`forceDelete`) if
  they match the prunable query."

## Migrations

- One concern per migration; never edit a migration that has run anywhere but a local machine.
- Always write `down()`, or the deploy that needs a rollback is the one that cannot have it.
- **Index every foreign key**, and index the columns you filter and sort on. Eloquent will not tell
  you a query is unindexed; the database will, under load.
- Add columns nullable or with a default when the table has rows.
- On a large table, an index build or column change locks — check the engine's online-DDL story
  before running it in a deploy window.
- Keep enum-ish columns as strings with an application-level enum cast rather than a database enum,
  which requires a schema change to extend.

## Sources

- [Eloquent: Getting Started](https://laravel.com/docs/13.x/eloquent) — strictness, chunking, cursor, mass assignment, pruning, mass-operation event warnings
- [Eloquent: Relationships](https://laravel.com/docs/13.x/eloquent-relationships) — eager loading, counting, existence queries, the column-selection warning
- [Database: Query Builder](https://laravel.com/docs/13.x/queries)
- [Database: Migrations](https://laravel.com/docs/13.x/migrations)
- [Database: Transactions](https://laravel.com/docs/13.x/database#database-transactions)
- [Eloquent: Mutators and Casting](https://laravel.com/docs/13.x/eloquent-mutators)
