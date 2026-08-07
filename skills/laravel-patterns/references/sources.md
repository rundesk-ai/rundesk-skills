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

- [Inertia v3 docs](https://inertiajs.com/docs/v3/), full index at
  [llms.txt](https://inertiajs.com/docs/llms.txt).
- [Responses](https://inertiajs.com/docs/v3/the-basics/responses): **"all data returned from the
  controllers will be visible client-side"**, prop serialization, `withViewData`, and the Firefox
  16 MiB history-state limit.
- [Shared data](https://inertiajs.com/docs/v3/data-props/shared-data): **"shared data should be used
  sparingly as all shared data is included with every response"**, and flash data as the alternative
  for toasts.
- [Partial reloads](https://inertiajs.com/docs/v3/data-props/partial-reloads): the prop evaluation
  matrix, and the `errors`-are-`always` warning that an empty error bag overwrites client-side errors.
- [Once props](https://inertiajs.com/docs/v3/data-props/once-props): the API, re-send rules, and the
  **conditional-prop `null` rule** that prevents stale cached auth state.
- [Deferred props](https://inertiajs.com/docs/v3/data-props/deferred-props) · [Load when visible](https://inertiajs.com/docs/v3/data-props/load-when-visible) · [Prefetching](https://inertiajs.com/docs/v3/data-props/prefetching) · [Polling](https://inertiajs.com/docs/v3/data-props/polling) · [Merging props](https://inertiajs.com/docs/v3/data-props/merging-props) · [Infinite scroll](https://inertiajs.com/docs/v3/data-props/infinite-scroll)
- [Forms](https://inertiajs.com/docs/v3/the-basics/forms): `<Form>` vs `useForm`, the checkbox `"on"`
  trap, automatic `FormData` conversion, the password/history-state prompt, precognition debouncing and
  file exclusion, and what breaks when you submit with fetch or axios.
- [Validation](https://inertiajs.com/docs/v3/the-basics/validation) · [File uploads](https://inertiajs.com/docs/v3/the-basics/file-uploads) · [Flash data](https://inertiajs.com/docs/v3/data-props/flash-data)
- [Authorization](https://inertiajs.com/docs/v3/security/authorization): "authorization is best handled
  server-side in your application's authorization policies."
- [History encryption](https://inertiajs.com/docs/v3/security/history-encryption): the back-button
  problem, key rotation, and the `window.crypto.subtle` secure-context requirement.
- [Asset versioning](https://inertiajs.com/docs/v3/advanced/asset-versioning): mismatch behaviour, why
  background requests do not force a reload, and the failure mode when unset.
- [SSR](https://inertiajs.com/docs/v3/advanced/server-side-rendering): dev-mode SSR without a Node
  process, Node 22 requirement, browser-API errors, silent fallback to client rendering, clustering.
- [Testing](https://inertiajs.com/docs/v3/advanced/testing): `assertInertia`, `has`/`where`/`missing`/
  `etc`, `reloadOnly`, `loadDeferredProps`, flash assertions.
- [Inertia.js v3.0.0 is here](https://laravel-news.com/inertia-3-0-0) — Laravel News on `useHttp`,
  optimistic updates, layout props, and the Axios removal.

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
- [Inertia.js once props](https://jump24.co.uk/journal/inertiajs-once-props-stop-sending-the-same-data-over-and-over-again):
  Jump24 on the shared-data-bloat problem once props solve.

## What this package deliberately does not cite

- Tutorials targeting Laravel 8–11 patterns without saying so. Most stale Laravel advice online is
  version drift, not error.
- Package recommendations for behaviour the framework provides.
- Benchmark posts without a published method.
- Architecture opinions presented as framework requirements. Where this package takes a position — for
  example on where business logic belongs — it says so and gives the failure it prevents.
