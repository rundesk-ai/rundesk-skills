# Laravel do/don't index

Use these pairs as a fast review and implementation checklist. They are conditional defaults, not
automatic findings: preserve a sound local convention, verify version-sensitive APIs, and read the
linked deeper reference before changing behavior.

## Database performance

| Don't | Do | Why |
|---|---|---|
| Access an unloaded relation in a loop | Eager load the relations the response uses | Prevents N+1 queries |
| Eager load every relation by default | Load only what this caller needs | Avoids hidden query and hydration cost |
| Select every column for a narrow result | Select the required columns and relationship keys | Reduces transfer without breaking relation matching |
| Load rows to count, sum, or test existence | Use SQL aggregates or `exists()` | Avoids needless hydration |
| Read an unbounded growing table | Paginate, `lazy()`, or `chunkById()` | Bounds memory and response size |
| Add indexes by reflex | Use observed filters, joins, sorts, and `EXPLAIN` | Preserves write cost and useful index order |
| Query from Blade or an API resource | Prepare data before rendering or serialization | Makes query count visible and testable |

Read [Eloquent and database](eloquent-and-database.md).

## Advanced queries

| Don't | Do | Why |
|---|---|---|
| Hydrate a has-many relation for one scalar | Use `withCount()`, `withExists()`, `ofMany()`, or `addSelect()` | Asks SQL for the actual value |
| Run several independent counts over the same rows | Consider one conditional-aggregate query | Can remove repeated scans |
| Reload a parent for every already-loaded child | Reuse the parent with `setRelation()` when appropriate | Prevents a reverse N+1 |
| Assume `whereIn`, `whereHas`, a join, or a subquery always wins | Compare representative plans and timings | The engine and indexes decide |
| Add a composite index without matching the query | Order columns from actual equality, range, and sort use | Makes the index usable for the target plan |
| Force one complex query when two bounded queries are clearer | Measure both and keep the simpler adequate plan | Complexity is also a cost |

Read [Eloquent and database](eloquent-and-database.md).

## Eloquent

| Don't | Do | Why |
|---|---|---|
| Model the wrong cardinality | Choose the relationship that matches the schema keys | Preserves query and persistence semantics |
| Duplicate a reusable constraint | Use a local scope with a domain name | Keeps callers aligned |
| Hide a conditional product view in a global scope | Reserve global scopes for constraints every caller needs | Avoids surprising admin, job, and report queries |
| Treat booleans, dates, enums, arrays, or encrypted values as raw strings | Define explicit casts | Keeps domain types stable |
| Compare a relationship key manually when Eloquent expresses it | Use helpers such as `whereBelongsTo()` when supported and clearer | Preserves relationship intent |
| Hardcode table names throughout model queries | Prefer qualified model columns or relationships where practical | Reduces rename drift |

Read [Eloquent and database](eloquent-and-database.md).

## Security

| Don't | Do | Why |
|---|---|---|
| Persist `$request->all()` | Authorize, validate, then persist `validated()` into an explicit write boundary | Blocks extra client fields |
| Concatenate input into SQL | Use bindings, Eloquent, and trusted identifiers | Prevents injection |
| Render user HTML with `{!! !!}` | Escape with `{{ }}` or sanitize at a deliberate boundary | Prevents XSS |
| Disable CSRF protection application-wide | Exclude only the exceptional route | Preserves request-forgery protection |
| Rely on hidden UI controls | Authorize every server-side action | The client is not a security boundary |
| Validate uploads by extension alone | Check size, MIME/content, storage, and delivery policy | Extensions are attacker-controlled |
| Store secrets in code or read `env()` in application classes | Resolve secrets through configuration or an approved secret store | Supports caching and secret rotation |
| Expose sensitive attributes because they are encrypted | Combine encryption, serialization hiding, and authorization | Each control solves a different leak |
| Leave login or public-write endpoints unbounded | Apply a named rate limiter derived from abuse and product needs | Limits brute force and resource exhaustion |
| Skip dependency auditing | Run the repository's supported audit in CI or release checks | Finds known vulnerable packages |

Read [HTTP, validation, and authorization](http-and-validation.md).

## Validation

| Don't | Do | Why |
|---|---|---|
| Let complex rules and authorization crowd a controller | Use a form request when it clarifies the boundary | Keeps transport code focused |
| Use pipe strings when rules contain objects, regexes, or `|` values | Prefer array rule syntax | Avoids ambiguous parsing |
| Persist raw request data after validation | Use `validated()` or `safe()` | Keeps unvalidated keys out |
| Pass user input to `Rule::unique()->ignore()` | Pass the resolved model or trusted system key | Prevents SQL injection |
| Hand-build brittle conditional rule arrays | Use `Rule::when()`, `sometimes()`, or request methods when supported | Makes conditions explicit |
| Put cross-field checks in a controller after validation | Use the form request's supported after-validation hook | Keeps one validation result |

Read [HTTP, validation, and authorization](http-and-validation.md).

## Routing and controllers

| Don't | Do | Why |
|---|---|---|
| Re-query a model from a route ID | Use implicit route model binding | Centralizes lookup and 404 behavior |
| Treat scoped binding as authorization | Scope nested resources and authorize the resolved model | Ownership and access are separate checks |
| Build unrelated custom controller verbs by default | Use resource actions while they fit; split responsibilities when they do not | Keeps routes predictable |
| Put reusable orchestration or external calls in a controller | Delegate when multiple callers, steps, or side effects justify it | Makes behavior reusable and testable |
| Serialize unloaded relations from a resource | Use `whenLoaded()` and eager load at the query site | Prevents resource-level N+1 queries |
| Register middleware in a skeleton file that the app does not use | Follow the installed application's structure | Upgraded apps may retain older boundaries |

Read [HTTP, validation, and authorization](http-and-validation.md) and
[Where logic belongs](where-logic-belongs.md).

## Migrations

| Don't | Do | Why |
|---|---|---|
| Invent migration timestamps or filenames | Generate them with Artisan | Preserves framework ordering conventions |
| Rewrite a migration already deployed | Add a forward migration | Gives every environment a valid path |
| Assume `constrained()` inferred the intended table and delete action | Inspect conventions; name exceptions explicitly | Prevents the wrong foreign-key behavior |
| Add an index without the target query plan | Derive it from representative filters and ordering | Avoids useless write overhead |
| Mirror every database default in the model | Mirror only when unsaved model instances must expose the same value | Avoids two defaults that can drift |
| Promise a destructive rollback restores lost data | Make reversal honest and document intentional irreversibility | Prevents false recovery claims |
| Alter a large populated table without an operational plan | Check locking, online DDL, duration, and rollback | Avoids deployment outages |
| Mix unrelated schema changes | Keep migrations coherent and safely deployable | Simplifies diagnosis and rollback |

Read [Eloquent and database](eloquent-and-database.md).

## Queues and jobs

| Don't | Do | Why |
|---|---|---|
| Dispatch work that reads new rows before commit | Configure after-commit dispatch or call `afterCommit()` | Prevents workers racing uncommitted state |
| Set job timeout at or above `retry_after` | Leave time for the worker to terminate before redelivery | Prevents concurrent duplicate attempts |
| Retry immediately and indefinitely | Bound attempts and use dependency-aware backoff | Avoids retry storms |
| Treat retries as exactly-once delivery | Make side effects idempotent and reconcile unknown outcomes | Jobs may run more than once |
| Add `failed()` only to log boilerplate | Use it for required repair or domain signaling; monitor failures globally | Avoids duplicate noise without losing observability |
| Assume uniqueness applies inside batches | Design batch idempotency explicitly | Laravel excludes batched jobs from unique constraints |
| Choose a uniqueness interface without its lock lifetime | Use `ShouldBeUnique` through completion or `ShouldBeUniqueUntilProcessing` for early release | Matches duplicate suppression to the operation |
| Combine a retry deadline with an unverified tries limit | Check installed worker/job precedence and test the terminal boundary | Avoids premature or unbounded retries |
| Use one queue for every latency class | Separate queues only when capacity or latency needs differ | Keeps operations intentional |
| Install Horizon for every queue | Use it when Redis queues need its supervisors, balancing, or dashboard | Horizon is an operational dependency |
| Put unlimited external calls in workers | Apply shared rate limiting and client timeouts | Protects quotas and worker capacity |

Read [Queues and jobs](queues-and-jobs.md).

## Caching

| Don't | Do | Why |
|---|---|---|
| Write manual `get()` then `put()` cache-aside code | Use `remember()` when its semantics fit | Keeps lookup and population together |
| Cache without defining acceptable staleness | Choose TTL and invalidation from the owning data change | Avoids serving unexplained stale data |
| Let concurrent misses stampede an expensive rebuild | Use an atomic lock or stale-while-revalidate | Bounds duplicate work |
| Use `has()` then `put()` for create-if-absent | Use atomic `add()` | Removes the race |
| Hit the same store repeatedly in one request/job | Use `once()` or supported cache memoization when useful | Avoids redundant reads |
| Depend on tags everywhere | Use tags only on supported stores where group invalidation earns the coupling | Preserves portability |
| Add failover without defining degraded semantics | Decide whether locks, limits, and correctness can tolerate fallback | Failover can change behavior |

Read [Performance and deployment](performance-and-deployment.md).

## HTTP client

| Don't | Do | Why |
|---|---|---|
| Let a dependency own the request's entire latency budget | Set explicit connection and response timeouts | Bounds blocked workers and requests |
| Decode every response as success | Call `throw()` or branch on the expected status | Laravel does not throw on 4xx/5xx by default |
| Retry every response | Retry selected transient failures with bounded backoff | Avoids amplifying permanent failures |
| Retry an external write with a new identity | Reuse a provider-supported idempotency key and reconcile status | A timeout can leave the remote outcome unknown |
| Pool dependent requests | Run only independent calls concurrently and inspect each result | Preserves ordering and error ownership |
| Allow tests to reach unknown hosts | Fake expected requests and prevent stray requests | Keeps tests deterministic and safe |

Read [Outbound HTTP and errors](outbound-http-and-errors.md).

## Error handling

| Don't | Do | Why |
|---|---|---|
| Catch an exception and silently return a fallback | Report it or emit a deliberate metric unless it is expected | Preserves production visibility |
| Suppress a broad exception class reflexively | Use `ShouldntReport` or `dontReport()` only for expected, otherwise-observable cases | Avoids hiding incidents |
| Report the same exception instance at every layer | Use supported duplicate suppression where needed | Reduces duplicate alerts |
| Log secrets or raw personal data as context | Attach safe identifiers and redact sensitive values | Keeps diagnostics useful without leaking data |
| Depend only on ideal `Accept` headers for API errors | Configure JSON rendering for the application's API boundary | Preserves response contracts |
| Throttle noisy errors before measuring them | Preserve representative samples and metrics first | Keeps high-volume incidents detectable |

Read [Outbound HTTP and errors](outbound-http-and-errors.md).

## Events and notifications

| Don't | Do | Why |
|---|---|---|
| Hide a required invariant behind an event | Call the required operation directly; emit events for reactions to facts | Makes success semantics honest |
| Register a listener twice | Follow the app's discovery/registration convention and inspect `event:list` | Prevents duplicate handling |
| Leave discovered event metadata stale in production | Include the repository's supported event/framework cache step in deployment | Keeps the effective listener map current |
| Publish transaction-dependent work before commit | Use the appropriate after-commit interface or option | Prevents phantom notifications and missing rows |
| Queue every notification by reflex | Queue only when latency and retry semantics fit the channels | Some channels belong in the immediate operation |
| Route every channel to a new queue | Separate queues only for a real capacity or latency policy | Every queue needs workers and monitoring |
| Create placeholder users for arbitrary recipients | Use on-demand notifications | Keeps recipient modeling honest |
| Recompute a durable locale preference at every send | Use Laravel's locale preference contract when the model owns it | Centralizes recipient language choice |

Read [Events, mail, and scheduling](events-mail-and-scheduling.md).

## Mail

| Don't | Do | Why |
|---|---|---|
| Send slow mail synchronously when the response does not need it | Queue the mailable when retries and worker delivery are acceptable | Keeps response latency bounded |
| Queue transaction-dependent mail before commit | Use `afterCommit()` or connection-wide after-commit behavior | Prevents messages about rolled-back state |
| Assert `sent` for a queued mailable | Assert it was queued | Matches the transport contract |
| Couple every content assertion to transport | Render and test content separately from dispatch | Makes failures precise |
| Replace the application's mail design by reflex | Use Markdown mailables only when their responsive HTML/text path fits | Preserves established rendering and brand conventions |

Read [Events, mail, and scheduling](events-mail-and-scheduling.md).

## Scheduling

| Don't | Do | Why |
|---|---|---|
| Let variable-duration work overlap its next tick | Use `withoutOverlapping()` with a deliberate lock expiry | Prevents duplicate concurrent runs |
| Run one logical task on every scheduler host | Use `onOneServer()` with a shared supported cache | Prevents multi-server duplication |
| Assume a scheduler lock protects a dispatched job | Put uniqueness/overlap control on the job runtime too | The scheduler lock ends after dispatch |
| Background a task whose parallel execution is unsafe | Use `runInBackground()` only for supported commands with observable failures | Preserves ordering and diagnosis |
| Scatter environment checks inside task code | Restrict the schedule with supported environment configuration | Keeps registration policy visible |
| Duplicate shared schedule configuration | Group tasks when supported while retaining unique task names | Reduces drift without lock collisions |
| Assume a long loop will stop at the right time | Use installed-version APIs plus explicit checkpoints and monitoring | Makes time bounds observable |

Read [Events, mail, and scheduling](events-mail-and-scheduling.md).

## Collections

| Don't | Do | Why |
|---|---|---|
| Use higher-order messages when they hide nontrivial logic | Use them only for simple, obvious property/method operations | Preserves readability |
| Use `cursor()` when relations must be eager loaded | Use `lazy()` for relationship-aware streaming | `cursor()` cannot eager load |
| Page by offset while changing the filter column | Use `lazyById()` or `chunkById()` | Prevents skipped or repeated rows |
| Loop an Eloquent collection for an intentionally eventless bulk write | Use `toQuery()` after confirming model type, connection, and event semantics | Reduces round trips |
| Introduce a custom collection for shape alone | Use `#[CollectedBy]` when the installed version supports it and reusable domain behavior earns it | Avoids ornamental types |

Read [Framework utilities](framework-utilities.md) and
[Eloquent and database](eloquent-and-database.md).

## Blade and views

| Don't | Do | Why |
|---|---|---|
| Replace consumer attributes in a component | Merge or compose the attribute bag | Preserves defaults and caller customization |
| Push the same asset for every component instance | Use `@pushOnce` when one registration is intended | Prevents duplicate scripts/styles |
| Use a component when a tiny intentional partial is clearer | Choose components for explicit props, slots, and reusable contracts | Avoids ceremony without hidden coupling |
| Query or authorize in a view | Prepare data in the controller, view model, or composer | Keeps rendering deterministic |
| Put page-specific data in a global composer | Use composers only for genuinely shared view data | Avoids invisible dependencies |
| Pass the same prop through many nested components manually | Use `@aware` only for a real ancestor component contract | Reduces plumbing without hiding arbitrary state |
| Adopt Blade fragments without a partial-rendering protocol | Use them when the installed version and htmx/Turbo-style flow require them | Avoids dead complexity |

Read [Testing and views](testing-and-views.md).

## Configuration

| Don't | Do | Why |
|---|---|---|
| Call `env()` outside configuration files | Read `config()` in application code | Works with configuration caching |
| Commit or casually share plaintext environment files | Use the approved secret store or supported encrypted environment workflow | Protects credentials |
| Compare raw environment strings throughout the app | Use application environment helpers at true environment boundaries | Centralizes environment semantics |
| Scatter unexplained domain strings and numbers | Use an enum, value object, configuration, or named constant that owns the concept | Prevents magic-value drift |
| Put user-facing text in constants | Use language files for translatable copy | Preserves localization |
| Look up an externally defined literal dotted key as a config path | Load the owning config array, then index the literal key | Avoids dot-path misinterpretation |
| Enable debug output in production | Keep `APP_DEBUG=false` | Prevents configuration disclosure |

Read [Performance and deployment](performance-and-deployment.md).

## Testing

| Don't | Do | Why |
|---|---|---|
| Replace the repository's Pest/PHPUnit or database lifecycle incidentally | Follow its existing test stack and reset traits | Preserves isolation and parallel behavior |
| Repeat opaque factory attribute arrays | Use named states and sequences for domain cases | Makes setup intentional |
| Create duplicate parents across related factories | Use `recycle()` when one existing relationship is intended | Preserves the modeled identity |
| Fake events before event-dependent setup | Create setup first or fake only the relevant events | Avoids breaking factories and observers |
| Disable exception handling just to observe reporting | Use the installed version's exception fake/assertions when the response should complete | Tests reporting without changing response behavior |
| Fake broad boundaries without assertions | Assert the exact dispatch, recipient, URL, payload, or failure | Proves the behavior that matters |
| Use a raw database assertion when the domain question is model existence | Prefer model assertions when they express the intent | Keeps tests aligned with the model |
| Treat HTML assertions as visual proof | Use the project's browser workflow for layout behavior | Separates rendering contracts from appearance |

Read [Testing and views](testing-and-views.md).

## Style

| Don't | Do | Why |
|---|---|---|
| Introduce a second naming or file-placement dialect | Match sibling code and Laravel conventions | Keeps the codebase predictable |
| Enforce style by hand | Run the repository's configured formatter, commonly Pint | Makes formatting mechanical |
| Replace clear PHP with helpers by reflex | Use `Str`, `Arr`, `Number`, `Uri`, or helpers when they clarify semantics | Avoids novelty without payoff |
| Use byte-oriented string functions for user text where character semantics matter | Use the appropriate multibyte-safe operation | Prevents corrupted length and slicing |
| Add comments that narrate syntax | Name the code clearly; comment constraints and non-obvious reasons | Keeps explanations durable |
| Hide page behavior in scattered inline JS/CSS | Follow the application's asset/component boundary | Preserves testability and content policy |

Read [Framework utilities](framework-utilities.md).

## Architecture

| Don't | Do | Why |
|---|---|---|
| Extract every small CRUD action | Keep it local until reuse, coordination, side effects, or testability earns extraction | Avoids speculative layers |
| Put a reusable operation only in a controller or job | Extract one named action/service and let entry points delegate | Makes behavior callable from multiple transports |
| Resolve dependencies deep inside domain code | Use constructor or method injection at visible boundaries | Makes dependencies testable and reviewable |
| Add an interface for every class | Introduce contracts at real substitution or external boundaries | Avoids empty indirection |
| Wrap Eloquent only to promise a future ORM swap | Add a repository only for a real persistence boundary | Preserves framework capabilities |
| Use process-local state as a distributed lock | Use Laravel atomic locks on a shared supported cache | Prevents cross-worker races |
| Use `defer()` for work that must survive process loss | Queue durable work; reserve `defer()` for lightweight post-response tasks | Matches durability needs |
| Put secret or correctness-critical arguments in visible Context | Use hidden context for propagated metadata and explicit parameters for invariants | Avoids leaks and invisible dependencies |
| Parallelize dependent operations | Use concurrency only for independent measured work | Preserves ordering and transaction semantics |
| Prefer newest-first ordering without a product requirement | Make default ordering explicit from caller needs | Avoids accidental behavior changes |

Read [Where logic belongs](where-logic-belongs.md) and
[Framework utilities](framework-utilities.md).
