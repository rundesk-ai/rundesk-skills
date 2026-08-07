# Where logic belongs

Read this before extracting actions or services, or when a controller, job, model, or observer has
become hard to reuse or test.

## Use the reuse test

Ask whether an HTTP request, command, queued job, and direct test can perform the operation without
duplicating it or fabricating another transport. If multiple callers need it, extract the operation
into an ordinary class they can all call.

Do not turn this preference into a framework law. Laravel deliberately permits different structures,
and a small CRUD endpoint may be clearest inline. Extraction earns its cost when the operation has
multiple callers, coordinated steps, or side effects.

## Keep entry points thin

| Entry point | Keep here | Move out when it grows |
|---|---|---|
| Controller | Translate input, authorize, delegate, respond | Business orchestration and external calls |
| Form request | Validation and request authorization | Persistence and side effects |
| Job | Queue policy and a call to the operation | The reusable operation itself |
| Observer | Narrow persistence invariants | Required or surprising business work |
| API resource | Output shape | Queries and authorization |

This is the community pattern demonstrated by Laravel News' controller refactor and Stitcher's
queueable actions: entry points invoke a callable operation; they do not own it.

```php
// Bad: registration exists only as an HTTP workflow.
public function store(Request $request)
{
    $user = User::create($request->validate(['name' => ['required']]));
    Mail::to($user)->send(new Welcome($user));
}

// Good: the controller delegates; another entry point can call the same action.
public function store(StoreUserRequest $request, RegisterUser $register): RedirectResponse
{
    $register->handle($request->validated());

    return to_route('users.index');
}
```

The pair is minimized from Laravel News' worked controller refactor; it preserves that article's
reason for extraction without copying its full example.

## Choose one useful abstraction

- Prefer an **action** for one named operation such as `RegisterUser` or `CancelSubscription`.
- Use a **service** when several closely related operations genuinely share dependencies or state.
- Do not build `Controller -> Service -> Action -> Repository` by reflex. Each layer must remove a
  real duplication or boundary.
- Do not wrap Eloquent merely to promise a future ORM swap. Introduce a repository only when the
  application has a real persistence boundary that Eloquent cannot express cleanly.

These are practitioner judgments, not Laravel requirements. State the local payoff when recommending
them.

## Keep jobs as transport when reuse matters

```php
// Bad: 150 lines of import behavior are reachable only through a worker.
final class ImportPriceListJob implements ShouldQueue
{
    public function handle(): void { /* operation */ }
}

// Good: the job owns retries and delegates the reusable operation.
final class ImportPriceListJob implements ShouldQueue
{
    public function handle(ImportPriceList $import): void
    {
        $import->handle($this->supplierId);
    }
}
```

Keep queue-specific timeout, backoff, and uniqueness policy on the job. Read
[`queues-and-jobs.md`](queues-and-jobs.md) for those traps.

## Do not hide required work in observers

Observers are difficult to see from the write site and mass updates or deletes dispatch no model
events. Therefore:

- keep required side effects next to the operation that performs the write;
- use observers only for narrow behavior that should run for every model-level write;
- do not depend on an observer for imports or bulk updates unless the chosen write path actually
  hydrates models and dispatches events.

Put the transaction around database work inside the operation. Dispatch external effects after the
commit; holding a transaction open across an HTTP call extends locks for the whole round trip.

The exact source mapping for both examples and each judgment is in [`sources.md`](sources.md).
