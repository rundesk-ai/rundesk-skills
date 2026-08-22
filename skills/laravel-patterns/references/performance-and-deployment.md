# Performance and deployment

Read this for production configuration, slow requests, data caches, Octane, or long-running workers.

## Build configuration for caching

```php
// Bad: works before config caching, may become null afterward.
$region = env('BILLING_REGION');

// Good, in config/billing.php: env() is evaluated while configuration is built.
'region' => env('BILLING_REGION'),

// Good, in application code: read the cached configuration value.
$region = config('billing.region');
```

Laravel stops loading `.env` after `config:cache`; only external system variables remain available to
`env()`. Keep every `env()` call in `config/`. Set `APP_DEBUG=false` in production because debug
output can expose configuration values.

## Read literal dotted keys without path parsing

A dynamic key containing `.` can return `null` even when that literal key exists because Laravel
configuration lookups parse dots as path separators.

```php
// Bad when $version is "api.v2": Laravel looks for nested api -> v2 keys.
$schema = config("features.schemas.$version");

// Good: resolve the known path, then index the literal key with PHP.
$schemas = config('features.schemas');
$schema = $schemas[$version] ?? null;
```

Load the owning array before indexing any externally defined identifier that may contain a dot.

Run the application's documented deploy sequence rather than copying one blindly. For a conventional
Laravel deployment, install production dependencies, migrate deliberately, run `php artisan optimize`
to cache framework metadata, and restart every long-running process that holds PHP or SSR code.

## Measure before tuning

Inspect in this order because each observation points to a concrete replacement:

1. Query count: detect lazy loading and N+1 with strict mode and a query profiler.
2. Slow query plans: use `EXPLAIN`; add or reorder indexes from actual filters, joins, and sorts.
3. Unbounded reads: paginate request data and stream batch work.
4. Inline slow or failure-prone work: queue only work the response does not need.
5. Serialization and response size: select needed columns and shape resources deliberately.

Do not recommend Octane, replicas, or larger machines before locating the measured bottleneck. Those
changes add operational cost and do not fix an N+1 query or unbounded collection.

## Cache with an invalidation plan

```php
// Good: bounded staleness and one named rebuild.
$stats = Cache::remember(
    "team:{$team->id}:stats",
    now()->addMinutes(10),
    fn () => $this->computeStats($team),
);
```

- State the acceptable staleness and invalidation event before caching a result.
- Use `Cache::lock()` when concurrent misses could stampede an expensive rebuild.
- Use `Cache::flexible()` when serving stale data during refresh is acceptable.
- Namespace related keys so invalidation can target the owning data.

Use `Cache::add()` for an atomic create-if-absent value; a separate `has()` then `put()` check races.
Use cache tags only on supported stores and only when group invalidation is worth the portability
cost. On framework versions with cache memoization, `Cache::memo()` can remove repeated store reads
within one request or job without changing cross-request TTL behavior.

A failover cache store trades an outage for degraded or potentially inconsistent cached behavior.
Adopt it only after deciding whether locks, rate limits, and cache-dependent correctness may safely
fall back; do not treat a failover store as automatic production hardening.

Avoid caching an Eloquent model reflexively. It can trade an indexed lookup for serialization and a
new stale-data problem. Cache measured expensive results whose invalidation boundary is understood.

## Treat Octane as persistent state

```php
// Bad under Octane: every request grows process memory.
static $seen = [];
$seen[] = $request->id();

// Good: keep request data request-scoped.
$seen = [$request->id()];
```

Octane keeps the application in memory between requests. Static mutable data leaks across requests,
and a singleton that captures the current request or container can retain stale state. Inject a
resolver closure or resolve request-scoped dependencies at call time. Worker recycling bounds leaks;
it does not make the state safe.

Test multiple consecutive requests under Octane. The first request cannot expose cross-request state.

## Deploy as a state transition

- Rebuild framework caches after the new release is in place; otherwise workers can use stale routes
  or configuration.
- Restart queue workers and any Inertia SSR process so they load the new release.
- Review large-table migrations for locks and online-DDL support before placing them in the request
  deploy window.
- Know that normal queued jobs pause during maintenance mode; choose zero-downtime switching or an
  explicit worker policy when the queue must continue.

The exact source mapping for every pair and warning is in [`sources.md`](sources.md).
