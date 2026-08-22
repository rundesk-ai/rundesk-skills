---
name: laravel-patterns
description: Use when building, reviewing, debugging, or refactoring Laravel backend behavior, including controllers, validation, authorization, Eloquent, migrations, queues, caching, outbound HTTP, events, mail, schedules, Blade behavior, testing, and deployment. It supplies version-aware, example-driven Laravel rules and production traps. Use `inertia-patterns` alongside it at an Inertia boundary. Do not use for visual-only work with no Laravel behavior; use `frontend-design`.
---

# Laravel Best Practices

Best practices for Laravel, organized as an index of rule files. Each rule file teaches what to do
and why. For exact API syntax, verify with `search-docs`.

Read only the files mapped to the current task. If `search-docs` is unavailable, verify
version-sensitive APIs against the installed framework or official versioned documentation.

## Consistency First

Before applying any rule, check what the application already does. Laravel offers multiple valid
approaches, and the best choice is the one the codebase already uses, even if another pattern would
be theoretically better. Inconsistency is worse than a suboptimal pattern.

Check sibling files, related controllers, models, or tests for established patterns. If one exists,
follow it. Don't introduce a second way. These rules are defaults for when no pattern exists yet,
not overrides.

## How to Apply

1. Check the changed files, nearby code, project configuration, and relevant tests for established
   patterns. Deviate only for a correctness or security defect, and call the deviation out.
2. Map every affected concern to the rule index below. Read each mapped rule file before editing.
   Skip unrelated rule files.
3. Make the smallest coherent change. Keep the application's architecture and naming instead of
   introducing a second pattern for the same job.
4. Verify version-sensitive Laravel APIs for the installed version with `search-docs`, or inspect
   the installed framework when it is unavailable.
5. Run the narrowest relevant tests first, then the project's formatting and static-analysis checks
   when the change warrants them.
6. Re-read the diff against every mapped rule before finishing.

## Rule Index

Cross-cutting changes often need more than one rule file.

| Concern | Read |
| --- | --- |
| Query count, eager loading, indexes, large datasets | [`references/rules/db-performance.md`](references/rules/db-performance.md) |
| Subqueries, aggregates, complex ordering and query plans | [`references/rules/advanced-queries.md`](references/rules/advanced-queries.md) |
| Models, relationships, scopes, casts | [`references/rules/eloquent.md`](references/rules/eloquent.md) |
| Authentication, authorization, input safety, secrets, uploads | [`references/rules/security.md`](references/rules/security.md) |
| Form Requests and validation rules | [`references/rules/validation.md`](references/rules/validation.md) |
| Controllers, route binding, resources, middleware | [`references/rules/routing.md`](references/rules/routing.md) |
| Schema changes, columns, foreign keys, indexes | [`references/rules/migrations.md`](references/rules/migrations.md) |
| Jobs, retries, uniqueness, batches, Horizon | [`references/rules/queue-jobs.md`](references/rules/queue-jobs.md) |
| Cache lifetime, invalidation, locks, memoization | [`references/rules/caching.md`](references/rules/caching.md) |
| Outbound requests, retries, timeouts, fakes | [`references/rules/http-client.md`](references/rules/http-client.md) |
| Exceptions, reporting, rendering, log context | [`references/rules/error-handling.md`](references/rules/error-handling.md) |
| Events and notifications | [`references/rules/events-notifications.md`](references/rules/events-notifications.md) |
| Mailables and mail assertions | [`references/rules/mail.md`](references/rules/mail.md) |
| Scheduled tasks and overlap protection | [`references/rules/scheduling.md`](references/rules/scheduling.md) |
| Collections, lazy iteration, bulk operations | [`references/rules/collections.md`](references/rules/collections.md) |
| Blade components, attributes, composers | [`references/rules/blade-views.md`](references/rules/blade-views.md) |
| Environment values and application configuration | [`references/rules/config.md`](references/rules/config.md) |
| Pest/PHPUnit patterns, factories, fakes | [`references/rules/testing.md`](references/rules/testing.md) |
| Naming, helpers, file boundaries, PHP style | [`references/rules/style.md`](references/rules/style.md) |
| Actions, services, dependencies, application structure | [`references/rules/architecture.md`](references/rules/architecture.md) |
| Production caches, Octane, deploy transitions, workers | [`references/rules/deployment.md`](references/rules/deployment.md) |
| Code-review triage across Laravel concerns | [`references/rules/review-triage.md`](references/rules/review-triage.md) |

## Decision Rules

- Prefer framework features and existing application abstractions over new helpers or dependencies.
- Avoid speculative abstractions. Extract code when it creates a clear domain boundary, removes
  meaningful duplication, or makes behavior independently testable.
- Keep database access out of Blade views and prevent hidden N+1 queries across controllers,
  resources, jobs, and serialization.
- Check the installed framework version before using a rule's version-sensitive API. New Laravel
  11+ applications use streamlined configuration, while upgraded applications may retain older
  kernel and exception-handler boundaries.
- Use `inertia-patterns` alongside this skill for props, shared data, forms, partial reloads, SSR,
  or adapter-version changes. Authorize every request on the server.
- Use `testing-code` alongside this skill when choosing test layers or auditing coverage.
- Read [`references/sources.md`](references/sources.md) only when auditing or changing a factual
  claim or example.
