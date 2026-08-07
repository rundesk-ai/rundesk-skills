---
name: laravel-patterns
description: Use this skill when the user asks to build, review, debug, refactor, or advise on a Laravel application or API — routing, controllers, middleware, validation, authorization, Eloquent and queries, migrations, queues and jobs, caching, configuration, testing, deployment — or on an Inertia.js frontend built on Laravel, including props, shared data, partial reloads, forms, SSR, and asset versioning. It supplies version-accurate rules, the failure each convention prevents, and the documented warnings that are easy to miss. Do not use it for Livewire-specific or Blade-only frontend work with no Inertia involved.
---

# Laravel and Inertia patterns

Follow the framework's own conventions and its documented warnings. Most Laravel bugs that reach
production are not exotic — they are a documented `WARNING` block somebody had not read.

## Establish the version before advising

Advice that was correct two majors ago is the main source of wrong Laravel guidance. Read the actual
versions first:

```sh
php artisan --version
php artisan about
composer show laravel/framework inertiajs/inertia-laravel 2>/dev/null
cat package.json | grep '@inertiajs'
```

| Release | Date | PHP | Bug fixes until | Security until |
|---|---|---|---|---|
| Laravel 11 | 12 Mar 2024 | 8.2–8.4 | 3 Sep 2025 | 12 Mar 2026 — **ended** |
| Laravel 12 | 24 Feb 2025 | 8.2–8.5 | 13 Aug 2026 | 24 Feb 2027 |
| **Laravel 13** | 17 Mar 2026 | 8.3–8.5 | Q3 2027 | 17 Mar 2028 |
| Inertia v2 | — | — | 26 Sep 2026 | 26 Mar 2027 |
| **Inertia v3** | 26 Mar 2026 | — | current | — |

Laravel 11 is out of support entirely. Laravel 12 leaves bug-fix support on **13 August 2026** and
is security-only after that; flag it when you see it.

## The skeleton is not what older guides describe

Since Laravel 11 there is **no `app/Http/Kernel.php` and no `app/Exceptions/Handler.php`**.
Middleware, exception handling, and routing are configured in **`bootstrap/app.php`**:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->web(append: [EnsureUserIsSubscribed::class]);
    $middleware->alias(['subscribed' => EnsureUserIsSubscribed::class]);
})
```

`app/` contains only `Http`, `Models`, and `Providers` by default; every other directory appears
when a `make:` command creates its first class. `routes/` holds `web.php` and `console.php` —
`api.php` and `channels.php` are installed with `php artisan install:api` and `install:broadcasting`.
Do not scaffold directories nobody asked for, and do not tell somebody to edit a Kernel that is not
there.

## Work in this order

1. **Read the real code before advising.** Read the model, the migration, and the controller
   together; Laravel's behaviour depends on all three and none of them is inferable from the others.
2. **Use the framework's own solution.** If there is a documented way, use it. Deviating needs a
   stated reason — that is Spatie's rule and it is the right one.
3. **Put the logic where every caller can reach it.** Controllers, jobs, commands, and observers are
   entry points; business logic belongs in a service or action they all call. See
   [`where-logic-belongs.md`](references/where-logic-belongs.md).
4. **Make failures loud in development.** `Model::shouldBeStrict()` in a non-production environment
   turns three classes of silent bug into exceptions.
5. **Prove it with a test.** Laravel's testing surface is good enough that "I could not test it" is
   almost always a design problem.

## Rules that always hold

- **Never call `env()` outside `config/`.** After `config:cache` the `.env` file is not loaded and
  `env()` returns only real system variables — so the call returns `null` in production and nowhere
  else. Read `config('...')` everywhere else.
- **`APP_DEBUG=false` in production**, always. Laravel: "you risk exposing sensitive configuration
  values to your application's end users."
- **Validate, then persist only `validated()`.** `$request->all()` includes everything the client
  sent. Keep `$fillable` set as well — validation and mass-assignment protection are two layers, not
  one choice.
- **Never pass user input to `Rule::unique()->ignore()`.** Laravel: "otherwise, your application will
  be vulnerable to an SQL injection attack."
- **Business logic never lives in a controller, a model, a job, or an observer.** Those are entry
  points and persistence. Put the operation in a service or action so a command, a job, a test, and a
  request can all reach it.
- **Eager load, or turn lazy loading into an exception.** N+1 is the default failure mode of an ORM.
- **Never load an unbounded result set.** `Model::all()` and `->get()` on a growing table are time
  bombs. Paginate what a user sees; `chunkById()` or `lazy()` what a job processes. Choosing wrong
  here is the difference between a job that runs and a worker killed by the memory limit.
- **Dispatch after commit.** A job dispatched inside a transaction can run before the transaction
  commits, against rows that do not exist yet.
- **Everything in Inertia props reaches the browser.** Inertia: "all data returned from the
  controllers will be visible client-side, so be sure to omit sensitive information."
- **Authorize on the server.** Props that say what a user may do are for rendering, never for access
  control.

## Read the reference the task needs

| Area | Read for |
|---|---|
| [Where logic belongs](references/where-logic-belongs.md) | Controllers vs services vs actions vs jobs vs observers; the fat-controller refactor |
| [Eloquent and the database](references/eloquent-and-database.md) | Models, strictness, N+1, chunking, query performance, mass assignment, transactions, migrations |
| [HTTP layer](references/http-and-validation.md) | Routing, controllers, Laravel 13 attributes, form requests, validation, gates and policies, API resources |
| [Queues and jobs](references/queues-and-jobs.md) | Serialization, transactions, uniqueness, timeouts, batches, chains — the documented warnings |
| [Inertia](references/inertia.md) | The mental model, responses, forms, validation, security, SSR, versioning, testing |
| [Inertia data loading](references/inertia-data-loading.md) | Shared data, once, deferred, optional, partial reloads, prefetching, polling, infinite scroll |
| [Performance and deployment](references/performance-and-deployment.md) | Caches, the optimize command, drivers, Octane, indexes, what to measure |
| [Anti-patterns](references/anti-patterns.md) | The consolidated do / don't list, and the failure each one prevents |
| [Sources](references/sources.md) | The citation basis, to audit or update any claim above |

## Review output shape

```text
[HIGH] Job dispatched inside a transaction without afterCommit
Location: app/Actions/CreateOrder.php:38
Evidence: DB::transaction() wraps Order::create() and ProcessOrder::dispatch(); the queue
connection in config/queue.php does not set after_commit.
Why: the worker can pick the job up before the commit and load a row that does not exist yet.
Fix: set 'after_commit' => true on the connection, or dispatch()->afterCommit().
Check: a test that dispatches inside a transaction and asserts the job sees the committed row.
```

Name the failure, not just the rule. A recommendation whose reason is "best practice" is one nobody
can evaluate.
