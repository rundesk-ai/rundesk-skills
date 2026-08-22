# Framework utilities

Read this for dependency injection, helpers, request context, deferred work, concurrency, or
collection iteration.

## Use the container at boundaries

Constructor or method injection makes dependencies visible and lets the container resolve them. Do
not call `app()` or `resolve()` deep inside domain code merely to avoid declaring a dependency. Bind
an interface when it represents a real external or architectural boundary; an interface around
every concrete class adds indirection without isolation.

Prefer an existing Laravel helper or support class when it expresses the intent and the installed
version provides it. `Str`, `Arr`, `Number`, and `Uri` can make encoding, path, formatting, and URL
behavior explicit. Do not mechanically replace clear PHP with helpers or use dot-path access for a
literal key that itself contains a dot.

## Keep style mechanical

Match sibling naming, type declarations, constructor style, and file placement. Use descriptive
domain names instead of generic `$data` or abbreviations. Run the repository's configured formatter
— commonly Pint — instead of hand-enforcing a second style guide. Format only the intended scope
when the repository provides a dirty/diff mode, then inspect the resulting diff for unrelated churn.

## Keep context scoped and safe

Laravel Context can carry correlation or tenant identifiers through logs and queued jobs. Use hidden
context for values that must propagate but must not enter logs. Do not place a secret in visible
context, and do not use Context as an invisible substitute for an explicit domain argument when the
callee's correctness depends on the value.

## Distinguish deferred, queued, and concurrent work

- Use `defer()` only for lightweight post-response work that may be lost if the PHP process exits.
- Use a queued job for work that needs durability, retries, rate control, or separate capacity.
- Use `Concurrency::run()` for independent operations after measuring that parallel execution pays
  for its process or driver overhead. Do not parallelize operations that share a transaction or must
  run in order.

These APIs are version-sensitive. Verify them against the installed framework and keep a synchronous
or queued replacement when the application runs an older major.

## Choose the collection boundary deliberately

Use collection higher-order messages only when they stay clearer than a closure. For growing
database results, choose the Eloquent iteration method from
[`eloquent-and-database.md`](eloquent-and-database.md): `cursor()` cannot eager load,
`lazy()` can, and `lazyById()` avoids offset drift while updating the filter set.

`toQuery()` performs one bulk query over an Eloquent collection's model keys. Confirm the collection
contains one model type and one connection, and remember that the bulk update or delete does not fire
per-model events. A shorter expression does not change those semantics.

The source mapping for these contracts is in [`sources.md`](sources.md).
