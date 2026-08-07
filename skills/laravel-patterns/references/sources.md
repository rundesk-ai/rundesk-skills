# Laravel and Inertia source basis

This package is a Rundesk synthesis of the Laravel and Inertia documentation plus a small number of
practitioner sources. The operational guidance is in the other references; use this file to audit or
update any claim.

**Read in this order of authority.** Framework documentation states the rules; practitioner sources
carry conventions and judgement the docs deliberately leave open. Never present the second as the
first — Laravel says explicitly that "Laravel imposes almost no restrictions on where any given class
is located."

Verified against these sources in **August 2026**, against **Laravel 13** and **Inertia v3**. Both had
a major release in March 2026, so anything checked against an older copy of these docs is suspect.

## Version and support facts

- [Laravel release notes](https://laravel.com/docs/13.x/releases): the support table, PHP floors, and
  every Laravel 13 feature named here — the AI SDK, JSON:API resources, `PreventRequestForgery`,
  `Queue::route()`, the expanded PHP attributes (`#[Middleware]`, `#[Authorize]`, `#[Tries]`,
  `#[Backoff]`, `#[Timeout]`, `#[FailOnTimeout]`), `Cache::touch()`, and vector search.
- [Inertia v3 documentation](https://inertiajs.com/docs/v3/): v3 released 26 March 2026; v2 bug fixes
  to 26 September 2026, security to 26 March 2027.
- [Inertia upgrade guide for v3.0](https://inertiajs.com/docs/v3/getting-started/upgrade-guide): every
  rename and breaking change, the framework floors, the Axios/`qs`/`lodash-es` removals, and the
  ESM-only output.
- [Laravel starter kits](https://laravel.com/docs/13.x/starter-kits): React, Svelte, Vue on Inertia +
  TypeScript + shadcn/ui + Tailwind; Livewire on Flux UI + Volt. Breeze and Jetstream are no longer
  updated.

## Structure and configuration

- [Directory structure](https://laravel.com/docs/13.x/structure): `app/` ships with `Http`, `Models`,
  `Providers` only; `routes/` with `web.php` and `console.php`; `api.php` and `channels.php` come from
  `install:api` / `install:broadcasting`.
- [Middleware](https://laravel.com/docs/13.x/middleware): registration in `bootstrap/app.php` — there
  is no `Http/Kernel.php` — plus the default `web` and `api` groups, aliases, and priority.
- [Configuration](https://laravel.com/docs/13.x/configuration): **the `config:cache` / `env()`
  warning**, the `APP_DEBUG` warning, maintenance mode, and that queued jobs do not run during it.

## Eloquent and the database

- [Eloquent: Getting Started](https://laravel.com/docs/13.x/eloquent): `preventLazyLoading`,
  `preventSilentlyDiscardingAttributes`, chunk vs `chunkById` vs `lazy` vs `cursor` (including "cannot
  eager load relationships" and PDO buffering), mass assignment, `upsert` index requirements, pruning
  force-deletes, and the mass update/delete **event** warnings.
- [Eloquent: Relationships](https://laravel.com/docs/13.x/eloquent-relationships): eager loading,
  `withCount`, existence queries, the "always include the `id` column and any relevant foreign key
  columns" warning, and the cross-database limitation.
- [Query Builder](https://laravel.com/docs/13.x/queries) · [Migrations](https://laravel.com/docs/13.x/migrations) · [Transactions](https://laravel.com/docs/13.x/database#database-transactions) · [Mutators and casting](https://laravel.com/docs/13.x/eloquent-mutators) · [Pagination](https://laravel.com/docs/13.x/pagination)

## HTTP layer

- [Routing](https://laravel.com/docs/13.x/routing) · [Controllers](https://laravel.com/docs/13.x/controllers) · [Eloquent: API Resources](https://laravel.com/docs/13.x/eloquent-resources)
- [Validation](https://laravel.com/docs/13.x/validation): `validated()` vs `all()`, form request
  `authorize()`, array vs pipe syntax, nested and array rules, and the **`Rule::unique()->ignore()` SQL
  injection**, **SVG/XSS**, and **file-extension** warnings.
- [Authorization](https://laravel.com/docs/13.x/authorization): gates vs policies, discovery, the
  `#[UsePolicy]` and `#[Authorize]` attributes, `Response::deny`/`denyAsNotFound`, guest handling, and
  **the `before()` filter warning**. Also carries Laravel's own Inertia authorization example.
- [CSRF protection](https://laravel.com/docs/13.x/csrf): `PreventRequestForgery` in Laravel 13.

## Queues

- [Queues](https://laravel.com/docs/13.x/queues) is the single densest source in this package. Every
  quoted warning in `queues-and-jobs.md` comes from it: the **transaction/`afterCommit`** warning,
  relationship serialization and `withoutRelations`, base64 for binary data, **`timeout` <
  `retry_after`**, `FailOnTimeout` behaviour, `ShouldBeUnique` lock-driver and batch limits, the
  multi-server cache requirement, `DebounceFor` vs `ShouldBeUnique` exclusivity, `WithoutOverlapping`,
  chain `delete()` semantics, batch implicit-commit warning, `block_for => 0` and `SIGTERM`, and the
  unsupported Redis `serializer`/`compression` options.
- [Cache: atomic locks](https://laravel.com/docs/13.x/cache#atomic-locks): which drivers support the
  locks unique and non-overlapping jobs require.

## Performance, deployment, monitoring

- [Deployment](https://laravel.com/docs/13.x/deployment): the `optimize` commands, `--no-dev` and the
  Ignition overhead point, `--optimize-autoloader`, and the production driver recommendations
  including "**the database driver is not suitable for production environments and is known to have
  deadlock issues**".
- [Octane](https://laravel.com/docs/13.x/octane): the static-state memory leak, the 500-request worker
  restart, the container/request-in-singleton warning, and "Octane does not always know how to reset
  the global state created by your application."
- [Cache](https://laravel.com/docs/13.x/cache) · [Pulse](https://laravel.com/docs/13.x/pulse) · [Telescope](https://laravel.com/docs/13.x/telescope)
- [The ultimate performance checklist for Laravel apps](https://laravel-news.com/performance-checklist) —
  Laravel News.

## Inertia

Moved. The Inertia seam now has its own skill, **`inertia-patterns`**, with its own source basis — the
v3 documentation, the Ping CRM reference application, and community writing. Use it alongside this
skill.

## Practitioner sources — conventions and judgement

These carry opinion, not framework rules. Cited where the docs deliberately do not decide.

- [Spatie: Laravel & PHP guidelines](https://github.com/spatie/guidelines.spatie.be/blob/master/content/code-style/laravel-php.md): "Laravel provides the
  most value when you write things the way Laravel intended you to write… whenever you do something
  differently, make sure you have a justification." Also array validation syntax, controller naming and
  CRUD verbs, extracting a new controller rather than bloating one, early returns over `else`.
- [Restructuring a Laravel controller using services, events, jobs, actions, and more](https://laravel-news.com/controller-refactor):
  the worked fat-controller refactor, the caution that observers hide logic from a reader, and the
  explicit caveat that "you are free to structure your project however you want."
- [Queueable actions in Laravel](https://stitcher.io/blog/laravel-queueable-actions): actions as the
  unit of business logic.
- [Laravel News](https://laravel-news.com/): the ecosystem's paper of record — release coverage,
  deprecations, and the practical write-ups referenced above.
- [freek.dev](https://freek.dev/) — **Freek Van der Herten**, Spatie. Maintainer of a large part of the
  package ecosystem; the [best practices](https://freek.dev/topics/best-practices) tag is the useful
  entry point.
- [Spatie's open-source packages](https://spatie.be/open-source) — worth checking before writing
  something; several of these are the de facto answer for permissions, media, backups and health
  checks, and reading one is a fast way to see idiomatic Laravel.
- [Tighten's blog](https://tighten.com/insights/) — Matt Stauffer and team; long-form architecture and
  upgrade experience.
- [Laravel Daily](https://laraveldaily.com/) — Povilas Korop; short, concrete, heavy on the cases that
  trip people up.
- [Laracasts forum](https://laracasts.com/discuss) and the
  [Laravel GitHub discussions](https://github.com/laravel/framework/discussions) — where a behaviour
  that looks like a bug gets settled. Search before assuming.

## What this package deliberately does not cite

- Tutorials targeting Laravel 8–11 patterns without saying so. Most stale Laravel advice online is
  version drift, not error.
- Package recommendations for behaviour the framework provides.
- Benchmark posts without a published method.
- Architecture opinions presented as framework requirements. Where this package takes a position — for
  example on where business logic belongs — it says so and gives the failure it prevents.
