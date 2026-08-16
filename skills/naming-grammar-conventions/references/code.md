# Code naming

Read this when choosing or reviewing source-code identifiers. Treat language and framework style as
the casing authority; these rules govern meaning.

## Values and collections

Name a value with a noun that says what it contains.

| Avoid | Prefer | Failure prevented |
|---|---|---|
| `data`, `result`, `tmp` | `normalized_address`, `invoice` | The reader must reconstruct meaning from assignments. |
| `user_list`, `invoice_array` | `users`, `invoices` | The name duplicates a type that can change. |
| `records_by_key` | `invoices_by_id` | Neither the element nor key has a domain meaning. |

Use singular nouns for one value and plurals for collections. Name mappings by the relationship when
it matters, such as `invoices_by_id` or `rates_by_region`.

## Functions, types, and modules

As a catalog conclusion, name an operation for its observable outcome: `normalizeAddress`,
`archiveInvoice`, `findAccount`. A generic verb such as `process` or `handle` forces the reader to
reconstruct the outcome from the body.

Use the repository's established verb vocabulary. If `find` may return nothing and `get` must return
one value, preserve that distinction rather than alternating them for variety.

Name a type for the concept it represents and follow the repository's existing type vocabulary.

## Review

- Read the language's official style guide before introducing a casing or prefix rule.
- Search callers before renaming a public identifier.
- Check generated clients, serialization keys, reflection, templates, and configuration references.
- Keep secrets and private identifiers out of names, examples, logs, and defaults.
- Prefer a staged compatibility change over a mixed old/new vocabulary.
