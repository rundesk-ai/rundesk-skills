# Queues and jobs

Read this before writing or debugging queued work. Retries, serialization, transactions, and
long-running workers create failures that a local `sync` queue hides.

## Dispatch after commit

```php
// Bad: a worker may run before the order is committed.
DB::transaction(function () use ($data) {
    $order = Order::create($data);
    ProcessOrder::dispatch($order);
});

// Good: publish only after the transaction commits.
DB::transaction(function () use ($data) {
    $order = Order::create($data);
    ProcessOrder::dispatch($order)->afterCommit();
});
```

Prefer connection-wide `'after_commit' => true` when jobs, listeners, mailables, notifications, and
broadcast events should all observe committed state. Use `afterCommit()` per dispatch when that is not
the connection default. A rolled-back transaction discards after-commit dispatches.

## Keep payloads small and time-aware

`SerializesModels` stores a model identifier and re-fetches the model when the worker runs. The job
therefore sees current database state, not a dispatch-time snapshot.

```php
// Bad: loaded relations are serialized and later reloaded without their old constraints.
public function __construct(public Podcast $podcast) {}

// Good: carry the model without relations, or carry only its scalar ID.
public function __construct(
    #[WithoutRelations] public Podcast $podcast,
) {}
```

Use `$model->withoutRelations()` on versions without the attribute. Collection behavior is
version-sensitive: Laravel 13 restores eager-loaded relations for models in serialized collections,
while earlier versions did not. Remove relations explicitly when the job should reload none, and
cover the installed version's deserialized payload in a test. Base64-encode raw binary data before
queueing it, or store the blob and queue a locator.

If a deleted model should make the work irrelevant, apply Laravel 13's
`#[DeleteWhenMissingModels]`. On older versions, use the supported equivalent for that installed
major. Otherwise treat deletion as a failure rather than silently discarding the job.

## Prevent overlapping attempts

Laravel requires job timeout to be shorter than the queue connection's `retry_after`; the worker
should die before the backend releases the job for another attempt.

```php
// Bad: another worker can receive the same job while the first still runs.
$connection = ['retry_after' => 90]; // worker/job timeout: 120

// Good: leave several seconds for the worker to terminate first.
$connection = ['retry_after' => 90]; // worker/job timeout: 60
```

Also set timeouts on blocking HTTP or socket clients; process timeouts may not interrupt them. Define
tries/backoff and surface terminal failure through monitoring or `failed()` behavior.

Back off transient failures so every retry does not hit the same unhealthy dependency immediately.
Use a fixed or increasing schedule that matches the dependency's recovery and rate-limit behavior.
Implement `failed()` only when terminal failure needs local state repair or a domain signal; global
failed-job monitoring remains necessary, and a boilerplate logger on every job can duplicate noise.

Retries mean side effects can run more than once. Check state before acting and use the provider's
idempotency key for charges or other non-repeatable external calls. `ShouldBeUnique` limits duplicate
dispatch; `WithoutOverlapping` limits concurrent execution. Neither replaces an idempotent operation.

Lock-based controls need a shared lock-capable cache across all servers. Remember:

- unique constraints do not apply inside batches;
- `DebounceFor` and `ShouldBeUnique` are mutually exclusive;
- choose the same logical key everywhere that must not overlap.

Apply rate-limiting middleware when a shared external quota governs many jobs. Use Horizon only when
the application uses Redis queues and needs its dashboard, balancing, or supervisor controls; it is
an operational dependency, not a default for every queue.

## Keep chains and batches honest

- `$this->delete()` inside a chained job does not stop later jobs; only failure stops the chain.
- Do not use `$this` in chain or batch callbacks; Laravel serializes those callbacks for later.
- Batched jobs run within transactions, so avoid statements that trigger implicit commits.

These are framework warnings, not stylistic advice.

## Operate long-running workers deliberately

- Restart workers on every deploy so they load new code.
- Keep Redis `block_for` finite when workers must handle `SIGTERM` promptly; `0` blocks signal
  handling until another job arrives.
- Separate latency-sensitive work from slow imports or reports with dedicated queues/workers.
- Inspect failed jobs and queue depth. A retry policy without monitoring only delays discovery.
- Confirm maintenance-mode behavior before a deploy; normal workers pause unless explicitly forced.

Do not repeat a stale blanket rule that the database queue is forbidden in production: current
Laravel 13 deployment guidance no longer makes that claim. Choose a backend from measured throughput,
locking, durability, and operational requirements.

The exact source mapping for every pair and warning is in [`sources.md`](sources.md).
