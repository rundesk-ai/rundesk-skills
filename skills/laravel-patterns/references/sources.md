# Laravel source map

Use this file to audit a lesson, not as additional workflow. Framework docs establish behavior;
maintainer and practitioner sources establish conventions Laravel intentionally leaves open.

Verified 7 August 2026 against Laravel 13 documentation and the linked source pages. Versioned
advice is marked in the owning reference instead of maintaining a patch/support ledger here.

## Core routing and skeleton

- [`SKILL.md`: inspect the installed version](https://laravel.com/docs/13.x/releases) — framework
  release notes establish feature and PHP-version boundaries; the installed Composer package remains
  the source for the application under review.
- [`SKILL.md`: Laravel 11+ minimal skeleton](https://laravel.com/docs/13.x/structure) and
  [middleware registration](https://laravel.com/docs/13.x/middleware#registering-middleware) — current
  directories and `bootstrap/app.php` configuration.
- [Spatie's Laravel/PHP guidelines](https://github.com/spatie/guidelines.spatie.be/blob/master/content/code-style/laravel-php.md#about-laravel)
  — practitioner default: follow Laravel's documented path unless the deviation has a reason.

## Where logic belongs

- [Laravel News' worked controller refactor](https://laravel-news.com/controller-refactor) — source
  for the minimized fat-controller pair, extraction options, observer visibility tradeoff, and the
  caveat that project structure is a choice.
- [Brent Roose, Queueable actions in Laravel](https://stitcher.io/blog/laravel-queueable-actions) —
  source for actions as reusable business operations and jobs as asynchronous transport.
- [Spatie's controller guidelines](https://github.com/spatie/guidelines.spatie.be/blob/master/content/code-style/laravel-php.md#controllers)
  — keep controllers to resource actions and extract a new controller when responsibilities diverge.
- [Laravel directory structure](https://laravel.com/docs/13.x/structure) — Laravel imposes few class
  location restrictions. Therefore this catalog presents actions/services as conditional
  practitioner judgment, never framework law.
- [Eloquent events](https://laravel.com/docs/13.x/eloquent#events) — mass update/delete event gaps
  establish why observers cannot guarantee behavior for every write path.

## Eloquent and database lessons

- [Strictness and lazy-loading violations](https://laravel.com/docs/13.x/eloquent-relationships#preventing-lazy-loading)
  and [discarded-attribute protection](https://laravel.com/docs/13.x/eloquent#mass-assignment-exceptions)
  — source for the non-production strictness example.
- [Eager loading](https://laravel.com/docs/13.x/eloquent-relationships#eager-loading) — N+1 example,
  eager-load key requirements, aggregates, and model-level `$with` behavior.
- [Framework PR #49695](https://github.com/laravel/framework/pull/49695) and
  [Laravel News' maintainer-sourced announcement](https://laravel-news.com/eager-load-limit) — native
  per-parent eager-load limits arrived in Laravel 11 from `eloquent-eager-limit`.
- [Chunking and lazy collections](https://laravel.com/docs/13.x/eloquent#chunking-results) and
  [cursors](https://laravel.com/docs/13.x/eloquent#cursors) — source for the filter-mutation trap,
  grouped conditions, inability to eager load with `cursor()`, and PDO buffering.
- [Aggregates](https://laravel.com/docs/13.x/queries#aggregates) — source for the
  `get()->count()` / query `count()` pair.
- [Mass assignment](https://laravel.com/docs/13.x/eloquent#mass-assignment) — fillable/guarded write
  boundary and silent-discard behavior.
- [Mass updates](https://laravel.com/docs/13.x/eloquent#mass-updates) and
  [mass deletes](https://laravel.com/docs/13.x/eloquent#deleting-models-using-queries) — model events do
  not run when models are not retrieved. The bulk-update pair is this catalog's minimized application
  of that documented failure.
- [Upserts](https://laravel.com/docs/13.x/eloquent#upserts) — unique-index requirement and MySQL /
  MariaDB `uniqueBy` behavior.
- [Transactions](https://laravel.com/docs/13.x/database#database-transactions) — automatic rollback
  and deadlock retry count. Keeping transactions clear of external calls is the catalog's lock-scope
  conclusion, not a quoted Laravel rule.
- [Migrations: online index creation](https://laravel.com/docs/13.x/migrations#online-index-creation)
  — large index builds can block reads/writes and support is database-specific.
- [Mastering Laravel: migrations during early development](https://masteringlaravel.io/daily/2024-02-20-how-we-use-migrations-during-early-product-development)
  — Joel Clermont distinguishes disposable pre-launch migrations from the new forward migrations
  used after launch. His [production `down()` rule](https://masteringlaravel.io/daily/2023-11-13-a-good-rule-around-down-migrations)
  documents why an apparently reversible migration can destroy data after users depend on the new
  schema. The owning reference therefore asks for honest reversibility instead of a universal
  `down()` rule.

## HTTP, validation, and authorization lessons

- [Scoped bindings](https://laravel.com/docs/13.x/routing#implicit-model-binding-scoping) constrain
  nested model lookup; [policy authorization](https://laravel.com/docs/13.x/authorization#authorizing-actions-using-policies)
  checks the current user. The good/bad pair combines these separate contracts; scoping is not a user
  authorization decision.
- [Validation](https://laravel.com/docs/13.x/validation#rule-unique) — exact warning against user
  input in `unique()->ignore()`. The same page's `extensions`, `image`, and array validation sections
  establish the extension-only, SVG/XSS, and permitted-key traps.
- [Spatie's validation guidelines](https://github.com/spatie/guidelines.spatie.be/blob/master/content/code-style/laravel-php.md#validation)
  — community source for array rule syntax.
- [Policy filters](https://laravel.com/docs/13.x/authorization#policy-filters) — `before()` is not
  called without a matching ability method; `null` falls through.
- [API resource conditional relationships](https://laravel.com/docs/13.x/eloquent-resources#conditional-relationships)
  and [Laravel Daily's reproduced N+1 case](https://laraveldaily.com/post/laravel-api-resources-relations-when-methods)
  — source for the `whenLoaded()` pair and the requirement to eager load at the query site.
- [CSRF protection](https://laravel.com/docs/13.x/csrf#excluding-uris-from-csrf-protection) — narrow
  route exclusion rather than application-wide disablement.
- [Laravel session flash data](https://laravel.com/docs/13.x/session#flash-data) establishes that a
  flashed value is deleted after the subsequent request. An anonymized first-hand Laravel/Inertia
  reproduction in 2026 found a redirect target consuming flash before a later workflow request, a
  failure hidden by a test that stopped after the POST. The documented lifetime establishes the
  mechanism; the reproduction supports exercising the complete request sequence in
  `http-and-validation.md`.

## Queue lessons

- [Jobs and database transactions](https://laravel.com/docs/13.x/queues#jobs-and-database-transactions)
  — before-commit race, connection-wide `after_commit`, per-dispatch `afterCommit()`, and rollback
  discard behavior.
- [Queued relationships](https://laravel.com/docs/13.x/queues#queued-relationships) — relations enlarge
  payloads and reload without prior constraints; `withoutRelations` / `WithoutRelations` are the
  documented replacement. [Class structure](https://laravel.com/docs/13.x/queues#class-structure)
  establishes identifier re-fetch, binary-data encoding, and current-state semantics.
  [Missing models](https://laravel.com/docs/13.x/queues#ignoring-missing-models) establishes Laravel
  13's `DeleteWhenMissingModels` attribute and its silent-discard behavior.
- [Timeouts](https://laravel.com/docs/13.x/queues#timeout) and
  [`retry_after`](https://laravel.com/docs/13.x/queues#job-expirations-and-timeouts) — timeout must be
  shorter or a job may be processed twice; IO clients also need their own timeouts.
- [Unique jobs](https://laravel.com/docs/13.x/queues#unique-jobs),
  [debounced jobs](https://laravel.com/docs/13.x/queues#debounced-jobs), and
  [overlap middleware](https://laravel.com/docs/13.x/queues#preventing-job-overlaps) — shared locks,
  batch exclusion, and debounce/unique incompatibility.
- [Amazon Builders' Library: retries and idempotency](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)
  — practitioner/operational basis for making externally visible retries idempotent instead of
  relying only on queue locks.
- [Job chains](https://laravel.com/docs/13.x/queues#job-chaining),
  [batches](https://laravel.com/docs/13.x/queues#defining-batchable-jobs), and
  [Redis blocking](https://laravel.com/docs/13.x/queues#blocking) — delete does not stop a chain,
  callback serialization, implicit commits, and `block_for=0` signal handling.
- [Queue workers and deployment](https://laravel.com/docs/13.x/queues#queue-workers-and-deployment) and
  [maintenance mode](https://laravel.com/docs/13.x/configuration#maintenance-mode) — worker restart
  and pause behavior.

## Performance and deployment lessons

- [Configuration caching](https://laravel.com/docs/13.x/configuration#configuration-caching) and
  [debug mode](https://laravel.com/docs/13.x/configuration#debug-mode) — exact basis for the `env()` /
  `config()` pair and production debug warning.
- [Accessing configuration values](https://laravel.com/docs/13.x/configuration#accessing-configuration-values)
  defines dots as path separators, and Laravel's current
  [`Repository::get`](https://github.com/laravel/framework/blob/13.x/src/Illuminate/Config/Repository.php)
  delegates lookup to `Arr::get`. A [community reproduction](https://stackoverflow.com/questions/51154711/laravel-5-how-to-use-array_get-method-to-access-an-attribute-with-a-dot-inside)
  shows why a literal dotted key must be indexed from its owning array. An anonymized first-hand
  Laravel 13 reproduction in 2026 confirmed the same `null` lookup and replacement used in
  `performance-and-deployment.md`.
- [Deployment optimization](https://laravel.com/docs/13.x/deployment#optimization) — framework cache
  commands. The application must still own ordering and zero-downtime mechanics.
- [Cache atomic locks](https://laravel.com/docs/13.x/cache#atomic-locks) and
  [stale-while-revalidate](https://laravel.com/docs/13.x/cache#stale-while-revalidate) — replacements
  for stampedes and refreshes that need bounded staleness.
- [Octane dependency injection](https://laravel.com/docs/13.x/octane#dependency-injection-and-octane)
  and [memory leaks](https://laravel.com/docs/13.x/octane#managing-memory-leaks) — captured request /
  container state and growing static arrays persist across requests.

## Deliberate removals

- Inertia guidance lives in `inertia-patterns`; duplicating it here creates version drift.
- Patch numbers and support countdowns were removed because they age faster than the workflow. Inspect
  the installed package and current release notes instead.
- The former claim that Laravel 13 documentation forbids the database queue in production was
  removed. Current Laravel 13 deployment and queue docs do not make that statement.
- Blanket rules to index every foreign key, always implement `down()`, forbid repositories, or ban
  business logic from every model were weakened or removed because the cited sources do not justify
  those absolutes.
