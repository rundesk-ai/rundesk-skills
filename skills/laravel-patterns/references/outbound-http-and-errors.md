# Outbound HTTP and errors

Read this for external requests, retries, HTTP fakes, exception reporting, rendering, or log context.

## Bound every external request

Laravel's HTTP client has finite defaults, but a default that is acceptable for one dependency can
hold another request open far too long. Set response and connection timeouts from the caller's
latency budget.

```php
$response = Http::connectTimeout(2)
    ->timeout(8)
    ->get($endpoint)
    ->throw();
```

Laravel does not throw for 4xx or 5xx responses unless the caller asks it to. Call `throw()` when any
unsuccessful status is exceptional, or branch on `successful()`, `notFound()`, and related methods
when the product has explicit fallback behavior. Do not decode an error body as if it were success.

## Retry only repeatable failures

Use `retry()` for transient connection failures or selected server responses. Bound attempts and
back off between them. Do not retry every 4xx, and do not retry a payment or other externally visible
write unless the operation has a stable provider idempotency key.

A timeout can leave the provider outcome unknown: the remote write may have succeeded after the
caller stopped waiting. Persist the attempt and idempotency key, retry with that same key when the
provider contract permits it, and reconcile from the provider's status instead of issuing a blind
new write.

```php
$response = Http::retry(
    [100, 500, 1_000],
    when: fn (Throwable $error) => $error instanceof ConnectionException,
)->timeout(8)->get($endpoint);
```

Concurrent pooling helps only when requests are independent. Preserve response-to-request identity,
inspect every result, and compare measured latency before accepting the added error-handling surface.

## Make tests closed to the network

```php
Http::preventStrayRequests();
Http::fake([
    'inventory.example/*' => Http::response(['available' => true]),
]);
```

Assert the important request method, URL, headers, and payload with `Http::assertSent()`. Cover the
timeout, connection failure, exhausted retry, and product fallback paths. A broad `Http::fake()`
without `preventStrayRequests()` can let an unexpected URL hit the network or hide a missing fake,
depending on how the test is configured.

## Keep exception policy observable

Laravel supports central reporting/rendering in `bootstrap/app.php` and `report()` / `render()`
methods on exception classes. Follow the application's established location. Keep domain exceptions
specific enough to attach useful context without logging secrets:

```php
public function context(): array
{
    return ['order_id' => $this->orderId];
}
```

- Implement `ShouldntReport` or configure `dontReport()` only when the exception is expected and
  already observable through the response or another signal.
- Enable `dontReportDuplicates()` when the same exception instance can be reported at several
  layers. It deduplicates one instance, not all exceptions of that type.
- Throttle noisy exception classes only after preserving enough samples and metrics to detect the
  incident.
- Override JSON rendering when route semantics require it; do not depend solely on every client
  sending the ideal `Accept` header.

Verify the rendered status and payload, the reporting decision, and redaction of secrets or personal
data. A caught exception that returns a fallback without reporting or a metric becomes a silent
production failure.

The source mapping for these contracts is in [`sources.md`](sources.md).
