---
name: laravel-patterns
description: Use when building, reviewing, debugging, or refactoring a Laravel application or API, including controllers, validation, authorization, Eloquent, migrations, queues, caching, testing, and deployment. It supplies version-aware Laravel defaults and source-backed replacements for common production traps. Do not use for Livewire- or Blade-only frontend work; use `inertia-patterns` alongside it at an Inertia boundary.
---

# Laravel patterns

Prefer Laravel's documented path. Deviate only when the codebase or measured behavior supplies a
reason.

## Inspect before changing

```sh
php artisan --version
php artisan about
composer show laravel/framework
```

Then read the route, request, controller, model, migration, configuration, and tests involved. Check
the installed major before using versioned APIs; do not copy a current-doc example into an older
application.

For Laravel 11+, configure middleware and exceptions in `bootstrap/app.php`; the minimal skeleton has
no `app/Http/Kernel.php` or `app/Exceptions/Handler.php`. Generate only the directories the change
needs.

## Apply these defaults

| Avoid | Prefer | Failure prevented |
|---|---|---|
| `env()` outside `config/` | Read `config('...')` | `config:cache` stops loading `.env`, so local-only success becomes a production `null` |
| `APP_DEBUG=true` in production | `APP_DEBUG=false` | Debug pages can expose configuration values |
| Persisting `$request->all()` | Validate, authorize, then persist `validated()` into an explicitly fillable model | Extra client fields crossing the write boundary |
| User input in `Rule::unique()->ignore(...)` | Pass the resolved model or its system-generated key | Laravel documents the former as an SQL-injection vector |
| Lazy-loading relations in loops | Eager load and enable non-production strictness | N+1 queries stay visible during development |
| `all()` / unbounded `get()` on growing data | Paginate user views; use `lazy()` or `chunkById()` for batch work | Memory growth tracks table growth |
| Dispatching inside a transaction | Enable `after_commit` or call `afterCommit()` | A worker can run before the row exists |
| Queue `timeout >= retry_after` | Keep timeout several seconds shorter | The same job can run twice concurrently |

These are framework-documented failure modes, not style preferences. The references give the exact
conditions and sourced good/bad pairs.

## Place behavior where callers can reach it

Keep a small CRUD action in its controller. Extract an action or service when an operation has
multiple entry points, multiple coordinated steps, or side effects. Jobs transport an operation;
observers should not hide work required for correctness. Read
[`where-logic-belongs.md`](references/where-logic-belongs.md) before introducing or reviewing those
layers.

## Make silent ORM failures loud

In non-production environments, enable the strictness needed by the project:

```php
Model::preventLazyLoading(! app()->isProduction());
Model::preventSilentlyDiscardingAttributes(! app()->isProduction());
```

This catches accidental lazy loads and discarded attributes during development without turning a
missed eager load into a production outage.

## Read only the needed depth

- Read [`eloquent-and-database.md`](references/eloquent-and-database.md) for relationship loading,
  large result sets, aggregates, mass operations, transactions, and migrations.
- Read [`http-and-validation.md`](references/http-and-validation.md) for route binding, form
  requests, file validation, policies, and API resources.
- Read [`queues-and-jobs.md`](references/queues-and-jobs.md) before writing or debugging queued work.
- Read [`performance-and-deployment.md`](references/performance-and-deployment.md) for configuration
  caches, slow requests, data caches, Octane, and long-running workers.
- Read [`anti-patterns.md`](references/anti-patterns.md) when triaging a review; it routes suspicious
  code to the reference that owns the fix.
- Read [`sources.md`](references/sources.md) when auditing or updating a claim or example.

Use `inertia-patterns` alongside this skill for props, shared data, forms, partial reloads, SSR, or
adapter-version changes. Authorize on the server even when an Inertia prop controls what the UI
shows.

## Report findings as failures

```text
[HIGH] Job can run before its transaction commits
Location: app/Actions/CreateOrder.php:38
Evidence: ProcessOrder is dispatched inside DB::transaction(); after_commit is false.
Impact: the worker may query an order that has not committed.
Replacement: enable after_commit or append ->afterCommit().
Verification: cover the dispatch boundary and the job's lookup in a queue-backed test.
```

Separate correctness and security defects from structure preferences. Never call a recommendation
"best practice" without naming the failure it prevents.
