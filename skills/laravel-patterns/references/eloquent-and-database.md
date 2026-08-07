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

- Do not rewrite a migration already applied outside disposable local environments; add a new
  migration so deployed state has a forward path.
- Make rollback behavior honest. Implement `down()` when reversal is safe; document an intentionally
  irreversible data migration instead of pretending it can restore deleted data.
- On populated large tables, inspect the database engine's locking and online-DDL behavior before
  adding an index or changing a column.
- Use `EXPLAIN` and observed query shapes to choose indexes. Avoid blanket indexing rules that ignore
  write cost and composite-index order.

The exact source mapping for every pair and version boundary is in [`sources.md`](sources.md).
