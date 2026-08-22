# Events, mail, and scheduling

Read this for events, queued listeners, notifications, mailables, or scheduled tasks.

## Choose explicit delivery semantics

Use an event when multiple independent listeners react to a fact that already happened. Call a
service or action directly when the side effect is required for the operation to succeed; hiding a
required step behind an event makes the write site look successful before its invariant is complete.

Follow the application's listener-discovery or manual-registration convention, and confirm the
effective map with `php artisan event:list`. Do not manually register a listener already discovered
by the installed skeleton.

Queue slow listeners, notifications, and mail only when the response does not need their result and
the queue's retry semantics are acceptable. Do not make every notification queued by reflex: an
in-memory or database-only channel may be part of the immediate transaction.

## Publish after commit

An event, listener, notification, or mailable dispatched inside a transaction can run before its
rows commit. Use the relevant after-commit interface or `afterCommit()` configuration when the
consumer reads those rows. A rollback must not leave an external message describing state that never
committed.

Keep each listener idempotent because a queued attempt can run more than once. Route channels to
separate queues only when their latency or capacity requirements differ; each extra queue needs an
operated worker and monitoring.

For arbitrary recipients, use on-demand notifications instead of creating placeholder models. Use
Laravel's locale preference contract when the notifiable model already owns a durable preference.

## Test transport and content separately

- Fake events, notifications, or mail at the boundary and assert the correct class, recipient, and
  queue/sent state.
- For a queued mailable, use `assertQueued()`; `assertSent()` proves only synchronous delivery.
- Instantiate a mailable or notification separately to test rendered content. Do not couple every
  content assertion to dispatch mechanics.
- Cover after-commit behavior when delivery depends on a transaction.

## Prevent schedule duplication

Apply `withoutOverlapping()` when a variable-duration task can still be running at its next tick.
Choose a lock expiration longer than the expected run and clear a stale lock deliberately after a
crash rather than disabling overlap protection.

Lock the boundary that performs the long-running work. If a scheduled command only dispatches a
queued job, its scheduler lock ends after dispatch and does not protect the job's runtime; apply the
job's uniqueness or overlap middleware when that execution must not overlap.

Use `onOneServer()` when one logical task must run once across several scheduler hosts; it requires a
shared, supported cache store. Use `runInBackground()` only for scheduled commands whose parallel
execution is safe and whose output and failures remain observable.

Restrict environment-specific tasks explicitly. Group schedule configuration when several tasks
share the same timezone, server, or maintenance policy, but preserve unique names for single-server
jobs that otherwise share a schedule expression.

Verify with `schedule:list`, a representative invocation, and the scheduler's logs or monitoring.
Configuration that looks correct but has no running scheduler, shared lock store, or failure signal
does not operate the task.

The source mapping for these contracts is in [`sources.md`](sources.md).
