# Anti-patterns

Read this when reviewing code, or before recommending a pattern. Each row names the failure, not just
the rule — a "best practice" nobody can evaluate is not guidance.

## Structure

| Don't | Do | Because |
|---|---|---|
| Put business logic in a controller | Put it in a service or action the controller calls | A command, job, or test cannot reach it without faking a request |
| Put the operation inside the job's `handle()` | Job wraps an action | It cannot be run synchronously or tested without the queue |
| Put business rules in an observer | Put them in the action | Observers hide logic from anyone reading the caller, and fire during seeding and imports too |
| Rely on model events for correctness | Do the work where the write happens | Mass updates and deletes fire **no** model events |
| Build `Controller → Service → Action → Repository` for a CRUD form | One action, or just the controller | Four files to run one insert, all of which must be read to answer a question |
| Wrap Eloquent in a `Repository` | Use Eloquent; wrap third-party APIs instead | Eloquent is already the abstraction; the swap-the-ORM benefit is never collected |
| Static "whole use case" methods on a model | An action class | `User::registerWithVoucherAndEmail()` is a service wearing a model's name |
| Edit `app/Http/Kernel.php` | `bootstrap/app.php` | It has not existed since Laravel 11 |

## Queries

| Don't | Do | Because |
|---|---|---|
| `Model::all()` on a growing table | `paginate()`, `chunkById()`, or `lazy()` | A time bomb with no warning until the memory limit |
| `->get()->count()` / `->get()->isNotEmpty()` | `count()` / `exists()` | Reads every row to produce one number or one boolean |
| `->get()->sum()` | `withSum()` / `sum()` | Aggregate in SQL, not in PHP |
| Lazy load in a loop | `with()`, or `preventLazyLoading()` | N+1 — the default failure mode of an ORM |
| `chunk()` while updating the filtered column | `chunkById()` | Documented: "could lead to unexpected and inconsistent results" — it skips rows |
| `cursor()` when you need relationships | `lazy()` | Documented: `cursor()` "cannot eager load relationships" |
| A loop of `create()` | `insert()` / `upsert()` | One round trip per row |
| Deep `paginate()` on a large table | `cursorPaginate()` | Offset pagination walks the skipped rows and drifts as rows are inserted |
| Leave foreign keys unindexed | Index every FK, filter, and sort column | Eloquent will not tell you; the database will, under load |
| `$guarded = []` | Explicit `$fillable` | The failure arrives when someone later adds `is_admin` |
| Persist `$request->all()` | Persist `$request->validated()` | `all()` contains whatever the client sent |

## Correctness and safety

| Don't | Do | Because |
|---|---|---|
| `env()` outside `config/` | `config('...')` | After `config:cache` the `.env` is not loaded — returns `null` in production only |
| `APP_DEBUG=true` in production | `false` | "You risk exposing sensitive configuration values to your application's end users" |
| Dispatch inside a transaction | `afterCommit()` or `after_commit => true` | The worker can run before the commit, against rows that do not exist yet |
| `timeout` ≥ `retry_after` | `timeout` < `retry_after` | The job is retried while still running — duplicate charges, duplicate emails |
| Pass user input to `Rule::unique()->ignore()` | Pass a system-generated id | Documented SQL injection vector |
| Validate a file by its extension | Combine with `mimes` / `mimetypes` | "You should never rely on validating a file by its user-assigned extension alone" |
| Allow SVG through the `image` rule casually | Know that it is off by default | XSS risk; `image:allow_svg` is an explicit decision |
| Assume a policy `before()` filter runs | Define the ability method | It "will not be called if the class doesn't contain a method with a name matching the ability" |
| HTTP calls inside a transaction | Call outside, or after commit | The lock is held for the whole round trip |
| The `database` queue driver in production | Redis, SQS, Beanstalkd | Laravel: "not suitable for production… known to have deadlock issues" |
| Closures in route files | Controllers | `route:cache` fails, so production loses route caching |
| Static arrays or container-injected singletons under Octane | Request-scoped state, resolver closures | State persists between requests; documented memory leak and stale-binding source |

## Inertia

| Don't | Do | Because |
|---|---|---|
| Submit with `fetch` or `axios` | `<Form>` or `useForm` | The response is not an Inertia response: no page update, no `errors`, no `FormData` conversion |
| Pass a whole model as a prop | `->only(...)`, a resource, or a DTO | "All data returned from the controllers will be visible client-side" — including columns added later |
| Trust a `can` prop for access control | Authorize on the server too | The route can be called without the button |
| Pile data into `HandleInertiaRequests::share()` | Page props, closures, or `Inertia::once()` | "Shared data should be used sparingly as all shared data is included with every response" |
| Bare values for expensive props | Closures | A bare value is computed on every request, even when a partial reload asked for something else |
| Poll or reload without `only` | Scope it | Every interval re-runs the whole controller |
| Skip asset versioning | Set `version()` | Clients keep the old bundle indefinitely, with no signal — "only some users have the bug" |
| Ship a shared `flash` prop | Flash data | Shared props persist in history state, so the toast reappears on back |
| Defer the thing the page is about | Defer below-the-fold data only | You have added a round trip to the critical path |
| Assume SSR works because tests pass | Enable `throw_on_error` in testing | SSR failures fall back to client rendering silently |
| Rely on history encryption over HTTP | HTTPS | It needs `window.crypto.subtle`, available only in secure contexts |
| Use `Inertia::lazy()` | `Inertia::optional()` | Renamed in v3 |

## Advice-giving

- **Do not advise without reading the version.** Laravel 11 is out of support; 12 leaves bug-fix
  support on 13 August 2026; Inertia v2 and v3 differ in named APIs. Most wrong Laravel guidance is
  right guidance for a version nobody is running.
- **Do not scaffold a directory nobody asked for.** `app/` ships with three.
- **Do not recommend a package for something the framework does.** Check the docs first.
- **Do not treat structure preferences as correctness findings.** Laravel says "you are free to
  organize your application however you like." Say which findings are bugs and which are opinions.
- **Do not report a fix as verified without running it.** A test that was never watched failing is a
  test that proves nothing.

## Sources

Every quoted line above is cited in [`sources.md`](sources.md). The heaviest sources are Laravel's own
`WARNING` blocks in [queues](https://laravel.com/docs/13.x/queues),
[configuration](https://laravel.com/docs/13.x/configuration),
[validation](https://laravel.com/docs/13.x/validation),
[eloquent](https://laravel.com/docs/13.x/eloquent) and
[authorization](https://laravel.com/docs/13.x/authorization), plus
[Inertia v3](https://inertiajs.com/docs/v3/).
