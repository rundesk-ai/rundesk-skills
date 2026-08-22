---
name: laravel-patterns
description: Use when building, reviewing, debugging, or refactoring a Laravel application, API, scheduled task, or behavior-bearing Blade feature, including controllers, validation, authorization, Eloquent, migrations, queues, caching, outbound HTTP, events, mail, testing, and deployment. It supplies version-aware Laravel defaults and source-backed replacements for common production traps. Use `inertia-patterns` alongside it at an Inertia boundary. Do not use for visual-only changes with no Laravel behavior; use `frontend-design`.
---

# Laravel patterns

Prefer the application's established Laravel pattern, then the framework's documented path. Do not
introduce a second style for the same job unless the existing one causes a correctness or security
failure; name that failure when deviating.

## Inspect before changing

```sh
php artisan --version
php artisan about
composer show laravel/framework
```

Then read the changed files, sibling implementations, configuration, and relevant tests. Check the
installed major before using versioned APIs; do not copy a current-doc example into an older
application. Prefer the project's documentation search or installed source when available.

New Laravel 11+ applications use the streamlined `bootstrap/app.php` configuration, but upgraded
applications may retain `app/Http/Kernel.php` and `app/Exceptions/Handler.php`. Inspect the actual
skeleton and extend its existing boundary. Generate only the directories the change needs.

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

## Rule index

Map every affected concern before editing. Start with the compact do/don't pairs, then read the
deeper reference only for the concerns the change touches. Cross-cutting work often needs several
rows.

| Concern | Compact rules | Deeper reference |
|---|---|---|
| Query count, eager loading, indexes, large datasets | [Database performance](references/rule-index.md#database-performance) | [Eloquent and database](references/eloquent-and-database.md) |
| Subqueries, aggregates, complex ordering, query plans | [Advanced queries](references/rule-index.md#advanced-queries) | [Eloquent and database](references/eloquent-and-database.md) |
| Models, relationships, scopes, casts | [Eloquent](references/rule-index.md#eloquent) | [Eloquent and database](references/eloquent-and-database.md) |
| Authentication, authorization, input safety, secrets, uploads | [Security](references/rule-index.md#security) | [HTTP and validation](references/http-and-validation.md) |
| Form requests and validation rules | [Validation](references/rule-index.md#validation) | [HTTP and validation](references/http-and-validation.md) |
| Controllers, route binding, resources, middleware | [Routing and controllers](references/rule-index.md#routing-and-controllers) | [HTTP and validation](references/http-and-validation.md) |
| Schema changes, foreign keys, indexes | [Migrations](references/rule-index.md#migrations) | [Eloquent and database](references/eloquent-and-database.md) |
| Jobs, retries, uniqueness, batches, Horizon | [Queues and jobs](references/rule-index.md#queues-and-jobs) | [Queues and jobs](references/queues-and-jobs.md) |
| Cache lifetime, invalidation, locks, memoization | [Caching](references/rule-index.md#caching) | [Performance and deployment](references/performance-and-deployment.md) |
| Outbound requests, retries, timeouts, fakes | [HTTP client](references/rule-index.md#http-client) | [Outbound HTTP and errors](references/outbound-http-and-errors.md) |
| Exceptions, reporting, rendering, log context | [Error handling](references/rule-index.md#error-handling) | [Outbound HTTP and errors](references/outbound-http-and-errors.md) |
| Events and notifications | [Events and notifications](references/rule-index.md#events-and-notifications) | [Events, mail, and scheduling](references/events-mail-and-scheduling.md) |
| Mailables and mail assertions | [Mail](references/rule-index.md#mail) | [Events, mail, and scheduling](references/events-mail-and-scheduling.md) |
| Scheduled tasks and overlap protection | [Scheduling](references/rule-index.md#scheduling) | [Events, mail, and scheduling](references/events-mail-and-scheduling.md) |
| Collections, lazy iteration, bulk operations | [Collections](references/rule-index.md#collections) | [Framework utilities](references/framework-utilities.md) |
| Blade components, attributes, composers | [Blade and views](references/rule-index.md#blade-and-views) | [Testing and views](references/testing-and-views.md) |
| Environment values and application configuration | [Configuration](references/rule-index.md#configuration) | [Performance and deployment](references/performance-and-deployment.md) |
| Pest/PHPUnit patterns, factories, fakes | [Testing](references/rule-index.md#testing) | [Testing and views](references/testing-and-views.md) |
| Naming, helpers, file boundaries, PHP style | [Style](references/rule-index.md#style) | [Framework utilities](references/framework-utilities.md) |
| Actions, services, dependencies, application structure | [Architecture](references/rule-index.md#architecture) | [Where logic belongs](references/where-logic-belongs.md) |

Read [`anti-patterns.md`](references/anti-patterns.md) when triaging a review. Read
[`sources.md`](references/sources.md) when auditing or strengthening a claim. The compact rules are
defaults, not text-match findings: confirm the failure mechanism and the installed Laravel version.

Use `inertia-patterns` alongside this skill for props, shared data, forms, partial reloads, SSR, or
adapter-version changes. Authorize on the server even when an Inertia prop controls what the UI
shows. Use `testing-code` alongside this skill when selecting test layers, designing regressions, or
auditing coverage.

## Verify the mapped behavior

Run the narrowest relevant test first, then the project's formatter and static analysis. Re-read the
diff against every mapped reference and confirm the failure path, not only the happy path. Run the
broader suite when the changed boundary or repository policy requires it.

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
