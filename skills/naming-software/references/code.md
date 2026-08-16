# Code naming

Read this when choosing or reviewing source-code identifiers. Treat language and framework style as
the casing authority; these rules govern meaning.

## Values and collections

Name a value with a noun that says what it contains.

| Avoid | Prefer | Failure prevented |
|---|---|---|
| `data`, `result`, `tmp` | `normalized_address`, `invoice` | The reader must reconstruct meaning from assignments. |
| `user_list`, `carrier_array` | `users`, `carriers` | The name duplicates a type that can change. |
| `timeout`, `size`, `amount` | `timeout_seconds`, `size_bytes`, `amount_cents` | Callers silently mix units. |
| `records_by_key` | `invoices_by_id` | Neither the element nor key has a domain meaning. |

Use singular nouns for one value and plurals for collections. Name mappings by the relationship when
it matters, such as `invoices_by_id` or `rates_by_region`.

## Conditions and states

Make a boolean read as a condition in the local language's idiom. `is_active`, `has_consent`, and
`can_retry` are useful defaults, not a cross-language law. Prefer positive conditions when callers
would otherwise accumulate double negatives.

Replace a boolean with a state type when `true` and `false` no longer describe every legal state.
Do not add adjacent flags that permit impossible combinations.

## Functions, types, and modules

Name an operation with a verb and its subject: `normalizeAddress`, `archiveInvoice`, `findAccount`.
Avoid verbs that only say code runs: `process`, `handle`, `manage`, `do`.

Use the repository's established verb vocabulary. If `find` may return nothing and `get` must return
one value, preserve that distinction rather than alternating them for variety.

Name a type for the concept it represents. Avoid `Helper`, `Manager`, `Util`, or `Service` when the
type has a narrower responsibility. Split a type whose only accurate name is a grab bag.

## Errors and events

Keep a stable machine classification separate from audience-specific prose:

- code and API clients need a stable error type or code;
- logs need diagnostic context without secrets;
- interface text needs the affected subject and a recovery action.

Name events as facts that occurred and commands as actions requested. Follow the project's event
syntax instead of imposing one punctuation or tense convention.

## Configuration and tests

Name configuration by the behavior it controls and include units where ambiguity is possible. Do
not encode secrets in names, examples, or defaults.

Name tests after observable behavior in the repository's test style. A test name should distinguish
the contract it protects, not narrate its implementation.

## Review

- Read the language's official style guide before introducing a casing or prefix rule.
- Search callers before renaming a public identifier.
- Check generated clients, serialization keys, reflection, templates, and configuration references.
- Prefer a staged compatibility change over a mixed old/new vocabulary.
