# Testing and views

Read this for Laravel-specific database tests, framework fakes, factories, Blade escaping, or
component data boundaries. Use `testing-code` alongside it for test-layer and coverage decisions.

## Preserve the application's test stack

Match PHPUnit or Pest, base test classes, database-reset traits, and factory conventions already in
the repository. Do not convert a suite or replace `RefreshDatabase` with another trait as incidental
cleanup; database lifecycle choices affect speed, parallelism, and isolation.

Prefer factories and named states over repeated raw attribute arrays. Use `recycle()` when related
factories must share one existing model rather than create several conceptually identical parents.
Use model assertions when the question is whether a particular model exists, and database assertions
when the exact stored row or table state is the behavior under test.

## Fake after required setup

Framework fakes replace real behavior. Create any factory data that depends on model events before
calling `Event::fake()`, or scope the fake to only the events under test. Apply the same discipline to
mail, notifications, queues, and HTTP: fake the external boundary, then assert the exact dispatch or
request that matters.

Test the failure that motivated the code. Query-count assertions can protect a known N+1 boundary,
but a brittle total for an unrelated request punishes harmless implementation changes.

## Keep Blade a rendering boundary

Escape user-controlled output with `{{ }}`. Use `{!! !!}` only for content that has passed a
deliberate sanitizer appropriate to its delivery context; calling data "trusted" does not remove XSS
risk.

Keep database queries and authorization out of templates. Controllers, view models, or composers
prepare data; templates render it. Prefer components when explicit props, slots, and attribute bags
remove hidden coupling. An include remains reasonable for a small partial whose inherited variables
are intentional and documented by nearby convention.

Use `$attributes->class()` or `merge()` so component consumers can extend attributes without losing
defaults. Use `@pushOnce` when a component rendered repeatedly must register one script or style
block. Do not place page-specific data into a global view composer merely to avoid one controller
argument; shared data should actually be shared.

Render the view in a feature or component test and assert escaped output, required props, and the
absence of unexpected queries. For visual behavior, use the project's browser or frontend testing
workflow rather than treating HTML string assertions as layout proof.

The source mapping for these contracts is in [`sources.md`](sources.md).
