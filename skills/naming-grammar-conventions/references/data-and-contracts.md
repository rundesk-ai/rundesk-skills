# Data and contract naming

Read this when a name is stored, serialized, queried, emitted, or consumed outside one process.
Use `database-design` to choose the schema model and ecosystem-specific database conventions; this
reference keeps the meaning stable after those decisions are made.

## Schemas

Name tables and fields for domain facts, not storage mechanics. Follow the database and repository
convention for singular or plural tables, casing, timestamps, foreign keys, and constraints. Those
forms differ across ecosystems; consistency within the schema matters more than a universal choice.

State units in numeric field names when callers could confuse them: `duration_seconds`,
`size_bytes`, `amount_cents`. Document currency and precision separately when one suffix cannot carry
the full contract.

## APIs and events

Apply the API's protocol and ecosystem conventions. Semantic consistency does not require an API
field to expose a database column name or internal structure.

- Keep one stable name for the same public concept within an API version.
- Use distinct names when cardinality, authority, lifecycle, or meaning differs.
- Keep secrets, private identifiers, and internal topology out of public names and examples.

## Renames

Classify the boundary before changing a name:

| Boundary | Default |
|---|---|
| Private local identifier | Rename atomically with its callers and tests. |
| Stored field | Add or migrate under the database's safe migration pattern; prove data preservation. |
| Published API or event | Add the replacement, support the old contract for the promised window, migrate consumers, then remove it in an allowed breaking change. |
| Metric or log field | Preserve dashboards, alerts, and queries or provide an explicit transition. |
| Visible label | Change independently only when the underlying meaning and accessibility contract stay stable. |

Do not hide cross-layer drift with display aliases alone. Record the canonical concept and the
intentional boundary mappings so later changes do not invent another synonym.

## Review

- Search migrations, fixtures, clients, event consumers, analytics, dashboards, and documentation.
- Verify case sensitivity and reserved-word behavior in the actual engine or protocol.
- Test old and new readers during a compatibility window.
- Inspect serialized output; passing internal tests does not prove the public name.
