# Where logic belongs

Read this when adding a feature, reviewing a fat class, or deciding where a piece of behaviour should
live.

## The rule

**Controllers, jobs, commands, listeners, and observers are entry points. Models are persistence.
Business logic belongs in a class that any entry point can call.**

An entry point's job is to translate the outside world into a call and a response: read input,
authorize, delegate, return. The moment it also decides *what the business does*, that decision is
reachable from exactly one direction.

The test, and it is a good one:

> Could a console command, a queued job, a test, and an HTTP request all perform this operation
> without duplicating code?

If the answer is no, the logic is in the wrong place. Logic inside a controller cannot be reached by
an Artisan command without faking a request. Logic inside a job cannot be run synchronously. Logic
inside an observer runs whether or not the caller wanted it to.

## What each layer owns

| Layer | Owns | Never |
|---|---|---|
| **Controller** | Input, authorization, delegating to one call, shaping the response | Business rules, multi-step orchestration, external API calls, mail |
| **Form request** | Validation rules, `authorize()` | Persistence, side effects |
| **Service / action** | The actual business operation, orchestration, transactions | Knowing about HTTP, `$request`, or a queue |
| **Model** | Table mapping, relationships, casts, scopes, accessors | Orchestration, HTTP calls, sending mail, cross-aggregate rules |
| **Job** | Transport: *run this operation later, with retries* | The operation itself |
| **Event / listener** | Genuinely passive reactions other parts may opt into | Anything required for the operation to be correct |
| **Observer** | Narrow, always-true persistence concerns (slugs, `uuid`) | Business rules, notifications, anything surprising |
| **API resource** | Output shape | Fetching, computing, authorizing |

## The refactor

```php
// ❌ Everything in the controller: validation, persistence, files, mail, notification
public function store(Request $request)
{
    $data = $request->validate([...]);
    $user = User::create($data);
    if ($request->hasFile('avatar')) {
        $user->update(['avatar' => $request->file('avatar')->store('avatars')]);
    }
    Voucher::create(['user_id' => $user->id, 'code' => Str::random(8)]);
    Mail::to($user)->send(new Welcome($user));
    foreach (User::where('is_admin', true)->get() as $admin) {
        $admin->notify(new NewUser($user));
    }
    return redirect()->route('users.index');
}
```

```php
// ✅ Controller: input, authorization, one call, a response
public function store(StoreUserRequest $request, RegisterUser $registerUser)
{
    $registerUser->handle(UserData::from($request->validated()));

    return redirect()->route('users.index');
}

// ✅ Action: the operation, callable from anywhere
final class RegisterUser
{
    public function __construct(private AvatarStorage $avatars) {}

    public function handle(UserData $data): User
    {
        $user = DB::transaction(function () use ($data) {
            $user = User::create($data->attributes());
            $user->vouchers()->create(['code' => Voucher::mintCode()]);

            return $user;
        });

        UserRegistered::dispatch($user);   // after commit; mail and admin notices listen

        return $user;
    }
}
```

What moved and why:

- **Validation → form request.** The controller stops knowing the rules, and the rules become
  reusable and testable on their own.
- **Persistence + orchestration → action.** Now a seeder, an import command, and a test can register a
  user. This is the whole point.
- **Slow side effects → queued listeners.** The response no longer waits on mail.
- **The transaction wraps only the database work**, and the event fires after it commits.

## Service or action?

Both are ordinary classes. The difference is granularity, and it does not matter much:

- **Action** — one operation, one class, an obvious name: `RegisterUser`, `CancelSubscription`,
  `ImportPriceList`. Usually one public method. Best default; the class name documents the operation.
- **Service** — several closely-related operations that genuinely share dependencies or state:
  `PaymentGateway`, `AvatarStorage`. Reach for it when three actions would all take the same three
  constructor arguments.

Do not create both layers by reflex. `Controller → Service → Action → Repository` for a CRUD form is
four files to write one insert, and every one of them has to be read to answer a question.

**A `Repository` wrapping Eloquent is usually not worth it.** Eloquent is already the data-access
abstraction; a repository over it re-exposes the query builder through a hand-written interface, and
the "we could swap the ORM" benefit is one nobody collects. Wrap a *third-party API*, not your own
database.

## Jobs are transport

```php
// ❌ The operation lives in the job — unreachable synchronously, awkward to test
class ImportPriceList implements ShouldQueue
{
    public function handle(): void { /* 150 lines */ }
}

// ✅ The job is a wrapper
class ImportPriceListJob implements ShouldQueue
{
    public function __construct(public Supplier $supplier) {}

    public function handle(ImportPriceList $import): void
    {
        $import->handle($this->supplier);
    }
}
```

The action can now be called inline from a command, tested without the queue, and reused by a
different trigger. The job keeps what is genuinely its own: retries, backoff, uniqueness, timeouts.
See [`queues-and-jobs.md`](queues-and-jobs.md).

## Models: rich, but not omniscient

A model may hold relationships, casts, scopes, accessors, and small predicates about its own
state — `$order->isRefundable()` belongs on `Order`. What does not belong:

- Charging a card, calling an API, sending mail.
- Anything spanning several aggregates — that is an action's job.
- Static "do the whole use case" methods. `User::registerWithVoucherAndEmail()` is a service wearing a
  model's name.

## Observers and events: the hidden-logic trap

The honest caution, and it comes from practitioners rather than the framework: observers **hide logic
from anyone reading the controller**. Somebody tracing "what happens when a user is created" sees the
action, not the four observers that also fired.

Use them for:

- Narrow, always-true persistence concerns — generating a slug or UUID, touching a counter.
- Genuinely optional reactions that other parts of the system opt into, via events.

Do not use them for:

- Anything required for the operation to be correct. If registration is broken without it, put it in
  the action where a reader will find it.
- Anything that must not run during seeding, imports, or tests — observers fire for those too.
- Anything triggered by a mass update or delete, because **those do not fire model events at all**.
  See [`eloquent-and-database.md`](eloquent-and-database.md).

## Where the transaction goes

In the action, around the database work only — not in the controller, and not spanning an HTTP call.
Dispatch jobs and fire events with external side effects **after** commit.

## The honest caveat

Laravel mandates none of this. Its documentation says the default structure is a starting point and
"you are free to organize your application however you like," and the most-cited community refactor
walkthrough opens with the same point in capitals. A three-route admin tool does not need an action
layer, and adding one is cost with no return.

The rule earns its keep when **an operation has more than one trigger, more than one step, or a side
effect that can fail**. At that point the question stops being style and starts being whether the
behaviour is reachable and testable. Apply it there, and say plainly when a piece of code is small
enough not to need it.

## Sources

- [Restructuring a Laravel controller using services, events, jobs, actions, and more](https://laravel-news.com/controller-refactor) — Laravel News; the worked refactor, the observer caution, and the "you are free to structure your project however you want" caveat
- [Spatie: Laravel & PHP guidelines](https://github.com/spatie/guidelines.spatie.be/blob/master/content/code-style/laravel-php.md) — keep controllers to CRUD verbs, extract a new controller rather than bloating one, follow the framework's documented way
- [Queueable actions in Laravel](https://stitcher.io/blog/laravel-queueable-actions) — Brent Roose on actions as the unit of business logic
- [Controllers](https://laravel.com/docs/13.x/controllers) — single-action controllers
- [Service container](https://laravel.com/docs/13.x/container) — how actions and services get their dependencies
- [Directory structure](https://laravel.com/docs/13.x/structure) — "Laravel imposes almost no restrictions on where any given class is located"
