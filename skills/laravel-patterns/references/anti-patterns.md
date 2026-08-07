# Review triage

Read this when scanning Laravel changes. Each signal routes to the reference that owns the mechanism,
replacement, and sourced example; do not report a text match without confirming the surrounding code.

| Signal | Verify | Read |
|---|---|---|
| `env(` outside `config/` | Production uses config caching | [Performance and deployment](performance-and-deployment.md) |
| `APP_DEBUG=true` in a production environment | The value reaches the deployed environment | [Performance and deployment](performance-and-deployment.md) |
| `all()` or unbounded `get()` | The table can grow and the caller does not need every row | [Eloquent and database](eloquent-and-database.md) |
| Relationship access inside a loop/resource | The query did not eager load it | [Eloquent and database](eloquent-and-database.md) |
| `get()->count()`, `get()->sum()`, `get()->isNotEmpty()` | Collection behavior is not otherwise needed | [Eloquent and database](eloquent-and-database.md) |
| `chunk()` while changing its filter column | Updated rows can move between pages | [Eloquent and database](eloquent-and-database.md) |
| Bulk `update`, `delete`, `insert`, or `upsert` | Correctness depends on model events | [Eloquent and database](eloquent-and-database.md) |
| `$guarded = []` plus request-derived writes | A future sensitive column can cross the boundary | [Eloquent and database](eloquent-and-database.md) |
| Business operation in a controller/job/observer | Multiple callers, steps, or required side effects justify extraction | [Where logic belongs](where-logic-belongs.md) |
| Repository wrapping Eloquent | It creates a real boundary instead of mirroring the query builder | [Where logic belongs](where-logic-belongs.md) |
| Scoped route binding without authorization | Parent-child scope is mistaken for user access | [HTTP and validation](http-and-validation.md) |
| `$request->all()` at persistence | Only validated and fillable fields should cross | [HTTP and validation](http-and-validation.md) |
| Request input passed to `unique()->ignore()` | The value is not a trusted model/key | [HTTP and validation](http-and-validation.md) |
| Extension-only file validation or enabled SVG | MIME/content and sanitization policy are present | [HTTP and validation](http-and-validation.md) |
| Policy `before()` as a universal bypass | The matching ability method exists | [HTTP and validation](http-and-validation.md) |
| Job dispatched inside a transaction | Connection or dispatch is after-commit | [Queues and jobs](queues-and-jobs.md) |
| Queued model with loaded relations | The payload and reloaded relationship set are intended | [Queues and jobs](queues-and-jobs.md) |
| Queue timeout at/above `retry_after` | A second worker can start before the first stops | [Queues and jobs](queues-and-jobs.md) |
| Unique job inside a batch | Code assumes uniqueness that Laravel does not apply | [Queues and jobs](queues-and-jobs.md) |
| Mutable static/singleton request state under Octane | State survives the request that created it | [Performance and deployment](performance-and-deployment.md) |

## Review discipline

- Read the installed Laravel version before suggesting an API or skeleton path.
- Name the observed symptom and mechanism, then give the supported replacement.
- Distinguish security/correctness failures from practitioner structure preferences.
- Do not turn the table into blanket findings: bounded `get()`, intentionally eventless bulk writes,
  and small inline CRUD code can all be correct.
- Do not report a fix as verified without running the relevant test or reproduction.

Use [`sources.md`](sources.md) to trace a lesson before changing or strengthening it.
