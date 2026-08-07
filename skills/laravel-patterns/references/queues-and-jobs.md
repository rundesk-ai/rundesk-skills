# Queues and jobs

Read this before writing, reviewing, or debugging queued work. Almost everything here is a `WARNING`
block from Laravel's own documentation, quoted, because each one describes a bug that is invisible
until production load.

## The transaction trap

The most common serious queue bug in Laravel applications:

> When dispatching a job within a transaction, it is possible that the job will be processed by a
> worker before the parent transaction has committed. When this happens, any updates you have made to
> models or database records during the database transaction(s) may not yet be reflected in the
> database. In addition, any models or database records created within the transaction(s) may not
> exist in the database.

It presents as a job that fails intermittently with "model not found," worse under load, unreproducible
locally where the queue is `sync`.

Three fixes, in order of preference:

```php
// 1. Connection-wide, in config/queue.php — the right default
'redis' => ['driver' => 'redis', 'after_commit' => true],

// 2. Per dispatch
ProcessPodcast::dispatch($podcast)->afterCommit();

// 3. Opt out where you deliberately want the old behaviour
ProcessPodcast::dispatch($podcast)->beforeCommit();
```

Setting `after_commit` "also affects queued event listeners, mailables, notifications, and broadcast
events" — which is usually what you want, and worth knowing before you flip it.

## Serialization

Jobs are serialized to the queue, so what you put in the constructor matters.

- `SerializesModels` stores only the model's key and re-fetches on execution. That means the job sees
  the row **as it is when the worker runs**, not as it was at dispatch. Usually right; occasionally
  the source of "the job used the new value."
- **Loaded relationships are serialized too**, which quietly makes payloads enormous. Strip them:

```php
$this->podcast = $podcast->withoutRelations();
$this->podcast = $podcast->withoutRelation('comments');

#[WithoutRelations]                      // per-property or on the class
public function __construct(public Podcast $podcast) {}
```

- Collections or arrays of models **do not** have relationships restored on deserialization, by
  design, "to prevent excessive resource usage."
- A deleted model makes the job fail on deserialization. `$deleteWhenMissingModels = true` if that is
  the correct outcome.
- Binary data must be base64-encoded: "otherwise, the job may not properly serialize to JSON."
- **Never use `$this` in a chain, batch, or `catch` callback.** Those callbacks are serialized and run
  later; Laravel warns about it for chains, batches, and closure dispatch separately.

## Timeouts, retries, and failure

> A job's "timeout" value should always be less than its "retry after" value. Otherwise, the job may
> be re-attempted before it has actually finished executing or timed out.

That is the setting pair that produces duplicate side effects — two charges, two emails — because the
queue released the job while the first attempt was still running. `timeout` also requires the PCNTL
extension, and has no effect with `queue:work --once`.

- Set `$tries` and `$backoff`, or Laravel 13's `#[Tries]`, `#[Backoff]`, `#[Timeout]`,
  `#[FailOnTimeout]` attributes.
- By default a timed-out job consumes an attempt and is released; `FailOnTimeout` makes it fail
  outright instead of retrying.
- Implement `failed(Throwable $e)` for anything with a user-visible consequence. A job that fails
  silently into `failed_jobs` is a feature nobody knows is broken.
- Monitor the failed-jobs table. It is the closest thing a queue has to an error log.

## Making jobs safe to run twice

A queue is at-least-once. Write jobs so a second run is harmless.

- **`ShouldBeUnique`** prevents duplicate dispatch, and requires a lock-capable cache driver —
  `memcached`, `redis`, `dynamodb`, `database`, `file`, `array`. Two more documented limits: "unique
  job constraints do not apply to jobs within batches," and with multiple servers "you should ensure
  that all of your servers are communicating with the same central cache server."
- **`WithoutOverlapping`** prevents concurrent execution of the same key, and needs the same lock
  support.
- **Debounced jobs and unique jobs are mutually exclusive** — "a job using the `DebounceFor` attribute
  should not implement `ShouldBeUnique`."
- Beyond that, make the work itself idempotent: check state before acting, key external calls with an
  idempotency token.

## Chains and batches

```php
Bus::chain([new ProcessPodcast, new OptimizePodcast])
    ->catch(fn (Throwable $e) => /* no $this here */)
    ->dispatch();
```

- **`$this->delete()` inside a job does not stop the chain.** "The chain will only stop executing if a
  job in the chain fails."
- Batched jobs are wrapped in transactions, so "database statements that trigger implicit commits
  should not be executed within the jobs."
- With Horizon, remember it manages Redis queues only — a `database` failover queue needs its own
  `queue:work database` process.

## Configuration and operations

- **The `database` queue driver is not suitable for production** — Laravel's deployment guidance names
  Redis, SQS, or Beanstalkd, and notes the database driver's known deadlock issues.
- `block_for => 0` makes workers block indefinitely and "will also prevent signals such as `SIGTERM`
  from being handled until the next job has been processed" — which breaks graceful deploys.
- The `serializer` and `compression` Redis options are not supported by the `redis` queue driver.
- **Restart workers on every deploy** (`queue:restart`). A long-running worker holds the old code in
  memory indefinitely.
- **No queued jobs are processed during maintenance mode.** They resume afterwards.
- Separate queues by latency requirement and run dedicated workers, so a slow report job cannot
  starve password-reset emails.

Laravel 13 adds central routing so a job's connection and queue are declared in one place:

```php
Queue::route(ProcessPodcast::class, connection: 'redis', queue: 'podcasts');
```

## What belongs on a queue

Anything slow or failable that the response does not need: third-party API calls, email and
notifications, file and image processing, imports and exports, search indexing, expensive
aggregation. Doing them inline is the most common cause of a slow Laravel endpoint.

## Sources

- [Queues](https://laravel.com/docs/13.x/queues) — every quoted warning above
- [Deployment](https://laravel.com/docs/13.x/deployment) — production driver guidance
- [Configuration](https://laravel.com/docs/13.x/configuration#maintenance-mode) — queues during maintenance mode
- [Cache: atomic locks](https://laravel.com/docs/13.x/cache#atomic-locks) — which drivers support the locks unique and overlapping jobs need
- [Laravel 13 release notes](https://laravel.com/docs/13.x/releases) — `Queue::route`, job attributes
