# Performance and deployment

Read this for production configuration, caching, Octane, and diagnosing a slow Laravel application.

## The deployment caches

```sh
composer install --no-dev --optimize-autoloader
php artisan optimize          # config + events + routes + views
php artisan migrate --force
php artisan queue:restart
```

`optimize` runs the individual cache commands together. Each earns its place:

- **`config:cache`** collapses `config/` into one file. It also **stops `.env` being loaded**, which is
  the `env()` trap below.
- **`route:cache`** collapses route registration. **Fails if any route uses a closure** — use
  controllers.
- **`view:cache`** precompiles Blade so requests do not compile on demand.
- **`event:cache`** precomputes listener discovery.

Re-run them on every deploy. Cached config that predates the deploy is config the deploy did not
apply — and the symptom is a change that "did not take."

`--no-dev` matters beyond disk: development packages such as Ignition record queries, logs, and dumps
in memory to build friendly error pages, which is real overhead in production. `--optimize-autoloader`
generates a classmap.

## The `env()` rule

> If you execute the `config:cache` command during your deployment process, you should be sure that you
> are only calling the `env` function from within your configuration files. Once the configuration has
> been cached, the `.env` file will not be loaded; therefore, the `env` function will only return
> external, system level environment variables.

`env('SOMETHING')` in a controller, model, service, or Blade template returns `null` in production and
works perfectly everywhere else. Put the value in a `config/` file and read `config('...')`.

`APP_DEBUG=false` in production, without exception.

## Production drivers

From Laravel's own deployment guidance:

| Concern | Use | Avoid |
|---|---|---|
| Queue | Redis, SQS, Beanstalkd | **`database`** — "not suitable for production environments and is known to have deadlock issues" |
| Session | Database, Redis, Memcached, DynamoDB | `cookie` — size and security limits |
| Cache | Redis, Memcached | `file` on multi-server, `array` anywhere real |

Also ensure OPcache is enabled and configured for production (no timestamp validation), or PHP
recompiles every file on every request.

## Caching application data

```php
$stats = Cache::remember("team:{$team->id}:stats", now()->addMinutes(10), fn () => $this->compute());
Cache::flexible("feed:{$id}", [300, 3600], fn () => $this->feed());   // stale-while-revalidate
Cache::touch('key', now()->addHour());                                // Laravel 13: extend TTL
```

- **Cache the expensive derived thing, not the model.** Caching a model row usually swaps a fast
  indexed lookup for a network hop plus an invalidation problem.
- **Have an invalidation story before you add the cache.** A wrong cached value is worse than a slow
  correct one, and it lasts until the TTL.
- Tag or namespace keys so related entries can be cleared together.
- Use atomic locks (`Cache::lock()`) to prevent stampedes on an expensive rebuild.
- `Cache::flexible()` serves stale while refreshing in the background — usually what a dashboard wants.

## Octane

Octane keeps the application booted between requests, which is a large win and a new class of bug:
**state now persists.**

- **Static properties and arrays leak.** "Adding data to a statically maintained array will result in
  a memory leak." Octane restarts a worker every 500 requests to bound the damage, which hides the
  leak rather than fixing it.
- **Do not inject the container or the request into a singleton's constructor.** Documented: it "can
  lead to the container unexpectedly missing bindings that were added later in the boot cycle or by a
  subsequent request." Inject a resolver closure, or do not make it a singleton.
- Octane resets first-party framework state, but "does not always know how to reset the global state
  created by your application."
- Anything that reads request-scoped data at boot is now wrong for every subsequent request.

Test under Octane before deploying to Octane. A bug of this kind is invisible on the first request.

## Diagnosing a slow application

Measure before changing anything. In order of how often it is the answer:

1. **Query count.** N+1 is the most common cause by a wide margin. Telescope, Debugbar, or Pulse will
   show it in one page load. `Model::preventLazyLoading()` in development prevents the whole class.
2. **Missing indexes.** `EXPLAIN` the slow query. Foreign keys and any column used in `where`,
   `orderBy`, or a join need one.
3. **Work that belongs on a queue.** Third-party calls, mail, image processing, exports, indexing.
4. **Unbounded reads.** `Model::all()` on a growing table is a time bomb with no warning. Paginate.
5. **Serialization cost.** Large API resource collections and, in Inertia, oversized props — see
   [`inertia-data-loading.md`](inertia-data-loading.md).
6. **Boot cost.** Too many eagerly-registered service providers; defer what can be deferred.

Only after those does infrastructure — Octane, a bigger box, a read replica — pay off. Laravel's own
first-party monitoring is Pulse (application health) and Nightwatch; Telescope is for local and
staging, not production.

## Deployment mechanics

- Zero-downtime deploys need atomic symlink switching or a managed platform. `php artisan down` is
  real downtime, and no queued jobs process while it is on.
- Pre-render the maintenance view (`down --render="errors::503"`) so it works before dependencies
  finish installing.
- Use `down --secret` to keep a bypass route for yourself.
- Restart queue workers and, if used, the Inertia SSR server on every deploy — both hold old code in
  memory.
- Migrations run with `--force` in production. Review any migration that locks a large table before it
  runs inside a deploy window.

## Sources

- [Deployment](https://laravel.com/docs/13.x/deployment) — optimize commands, driver recommendations, `--no-dev` and Ignition
- [Configuration](https://laravel.com/docs/13.x/configuration) — the `config:cache` / `env()` warning, debug mode, maintenance mode
- [Laravel Octane](https://laravel.com/docs/13.x/octane) — memory leaks, singleton and container injection, state reset
- [Cache](https://laravel.com/docs/13.x/cache) — `remember`, `flexible`, atomic locks, `Cache::touch`
- [The ultimate performance checklist for Laravel apps](https://laravel-news.com/performance-checklist) — Laravel News
- [Pulse](https://laravel.com/docs/13.x/pulse) · [Telescope](https://laravel.com/docs/13.x/telescope)
