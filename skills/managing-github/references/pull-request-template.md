# Fallback GitHub pull-request template

Use this only when the target repository has no applicable pull-request template. Replace every
placeholder, remove comments, preserve all eight headings, and check only claims proven for the
exact head commit.

````md
## Summary

<!-- State what changes and why in one or two lines. -->

-

## Scope and compatibility

- Changed surface:
- User-visible effect:
- Preserved behavior:
- Compatibility or migration impact:

## Critical risk

<!-- Cover credentials, privacy, destructive operations, persisted data, billing, deployment, or another critical risk. Write "None" when none applies. -->

- Risk:
- Guard:

## Validation

- [ ] `<exact command or manual check>` — `<observed result>`
- [ ] Required GitHub checks pass for the exact head commit.

```text
# Exact validation commands and observed results
```

## Repository gates

- [ ] Repository instructions and applicable contribution guidance were followed.
- [ ] The diff contains no credential, private data, owner-specific path, debug output, generated clutter, or unrelated artifact.
- [ ] Documentation, tests, and compatibility notes agree with the changed behavior.

## Release

- Version: `<before>` → `<after>`
- SemVer reason:
- Release or follow-up required after merge:

## Manual user path

<!-- Give the shortest representative user path and expected result. State why none applies when the change has no user-facing path. -->

```text

```

<!-- Use one standalone `Closes #<number>.` line per issue this PR completes. Use `Refs` for partial work. -->

## Agent

<!-- Replace the placeholder with the filing agent's display name. Do not add provider, model, tool, session, or generated-by branding. -->

🤖 by <Agent>
````
