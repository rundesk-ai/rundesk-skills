# Eloquent and the database

Read this for relationship loading, growing result sets, bulk writes, transactions, or migrations.

## Catch lazy loads and discarded writes

```php
// Good: fail during development, not under production traffic.
Model::preventLazyLoading(! app()->isProduction());
Model::preventSilentlyDiscardingAttributes(! app()->isProduction());
```

The first exposes accidental relationship queries; the second exposes attributes missing from the
model's fillable set. Keep production behavior deliberate: Laravel also supports logging lazy-load
violations when throwing would be unsafe.

## Load relationships deliberately

```php
// Bad: one author query per book.
$books = Book::all();
foreach ($books as $book) {
    echo $book->author->name;
}

// Good: books and authors are loaded in two queries.
$books = Book::with('author')->get();
```

Use `withCount`, `withSum`, or `withExists` when only an aggregate is needed. When selecting columns
on an eager load, include the related key and relevant foreign key or Eloquent cannot match the
results. A model-level `$with` is a tax on every query; reserve it for relationships every caller
needs.

Laravel 11+ supports a per-parent `limit()` inside eager-load constraints. On older applications,
use a version-compatible solution; native support came from the community
`eloquent-eager-limit` package through framework PR #49695.

Use local scopes for constraints reused across callers. Reserve global scopes for conditions that
truly apply to every query, including admin, reporting, queue, and maintenance paths; a hidden
`published` filter is difficult to diagnose when one caller needs drafts. Define casts for domain
types such as booleans, dates, enums, arrays, and encrypted values, following the model convention
used by the installed Laravel version.

## Ask SQL for the value you need

Do not eager load a has-many collection only to read one aggregate or latest value. Prefer
`withCount`, `withSum`, `withExists`, an `ofMany` relationship, or a correlated `addSelect()`
subquery when it expresses the required value. For several conditional totals over the same rows, a
single conditional-aggregate query can replace several independent counts.

These are candidates, not automatic wins. Compare `EXPLAIN` plans and representative timings before
replacing `whereHas()` with a join, `whereIn()` subquery, or multiple-query strategy; database
statistics and indexes decide the winner. When both sides of an already-loaded relationship are
needed, `setRelation()` can point each child at the existing parent and prevent a reverse N+1 without
another query.

## Bound every growing read

Choose by eventual size, not today's row count:

| Need | Prefer | Avoid |
|---|---|---|
| Human-visible page | `paginate()`, `simplePaginate()`, or `cursorPaginate()` | `all()` |
| Batch with eager-loaded relations | `lazy()` | `cursor()` |
| Batch that changes its filter column | `chunkById()` or `lazyById()` | `chunk()` or `lazy()` |
| Count, sum, or existence | SQL `count()`, `sum()`, or `exists()` | Loading a collection first |

```php
// Bad: transfers and hydrates every paid order to obtain one number.
$count = Order::where('status', 'paid')->get()->count();

// Good: the database returns the aggregate.
$count = Order::where('status', 'paid')->count();
```

Laravel documents two easy-to-miss failures:

- Updating the column used to filter `chunk()` or `lazy()` can skip or repeat rows; advance by an
  immutable key with `chunkById()` or `lazyById()`.
- `cursor()` cannot eager load and PDO still buffers raw results, so use `lazy()` for a very large
  relationship-aware stream.

Group custom `orWhere` conditions before `chunkById()` because it adds its own conditions:

```php
Flight::where(fn ($query) => $query
        ->where('delayed', true)
        ->orWhere('cancelled', true))
    ->chunkById(200, fn ($flights) => $flights->each->update(['departed' => false]));
```

## Keep writes explicit

```php
// Bad: unvalidated client fields and every future column are writable.
protected $guarded = [];
$user->update($request->all());

// Good: the request and model each enforce the write boundary.
protected $fillable = ['name', 'email'];
$user->update($request->validated());
```

Validation and mass-assignment protection solve different failures; keep both. Enable
`preventSilentlyDiscardingAttributes` outside production so a missing fillable attribute is not
silently dropped.

Use `insert()` or `upsert()` when model hydration and events are not required. Confirm the database
has the primary or unique index `upsert()` needs; MySQL and MariaDB use table indexes rather than the
method's `uniqueBy` list to detect conflicts.

## Treat mass operations as eventless

```php
// Bad when correctness depends on an updated observer: no model is hydrated, so no event fires.
Post::where('expired', true)->update(['status' => 'archived']);

// Good: make the required side effect explicit and keep the batch bounded.
Post::where('expired', true)->chunkById(500, function ($posts) {
    $ids = $posts->modelKeys();
    Post::whereKey($ids)->update(['status' => 'archived']);
    SearchIndex::rebuildPosts($ids);
});
```

Eloquent mass updates and deletes do not dispatch the corresponding model events. Do not hang audit,
index, or notification correctness on an observer when the application also uses mass operations.
If per-model events are required, deliberately hydrate and save each model and accept the extra work.

## Keep transactions narrow

Use `DB::transaction()` for related database writes and pass a retry count when deadlock retries are
appropriate. Do not hold locks while calling an external service. Queue jobs, mail, and other
external effects after commit so rollback does not leave the outside world ahead of the database.

## Review migrations as production operations

- Generate migration filenames with `php artisan make:migration --no-interaction`; the timestamp and
  naming stay compatible with the application's tooling.
- Do not rewrite a migration already applied outside disposable local environments; add a new
  migration so deployed state has a forward path.
- Make rollback behavior honest. Implement `down()` when reversal is safe; document an intentionally
  irreversible data migration instead of pretending it can restore deleted data.
- On populated large tables, inspect the database engine's locking and online-DDL behavior before
  adding an index or changing a column.
- Use `EXPLAIN` and observed query shapes to choose indexes. Avoid blanket indexing rules that ignore
  write cost and composite-index order.
- Use `foreignId()->constrained()` when its conventions match the schema. Name the table and actions
  explicitly when they do not; a concise helper must not conceal the wrong delete behavior.
- Mirror a database default in a model only when unsaved model instances must expose that same
  value. Otherwise two defaults create two places that can drift.

The exact source mapping for every pair and version boundary is in [`sources.md`](sources.md).
