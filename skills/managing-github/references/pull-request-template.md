# Fallback GitHub pull-request template

Use this only when the target repository has no applicable pull-request template. Replace every
placeholder, remove comments, preserve the six core headings, and check only claims proven for the
exact head commit. Add the conditional sections after the core template only when they materially
help review; do not add them to produce a fuller-looking body.

````md
## Problem

<!-- State the current behavior or limitation, who or what it affects, and the consequence. -->

## Proposed solution

<!-- Describe the implemented outcome, important decisions and rationale, its boundary, and preserved behavior. -->

## Evidence

<!-- Give concise before-and-after observations, source locations, measurements, or contract links that support the merge case. Distinguish evidence from validation. -->

## Acceptance criteria

- [ ] <!-- Independently checkable outcome proven by this exact head. -->

## Validation

- [ ] `<exact command or manual check>` — `<observed result>`
- [ ] Required GitHub checks pass for the exact head commit.

<!-- Use one standalone `Closes #<number>.` line per issue this PR completes. Use `Refs` for partial work. -->

## Agent

<!-- Replace the placeholder with the filing agent's display name. Do not add provider, model, tool, session, vendor link, generated-by branding, or provider-style co-author attribution. -->

🤖 by <Agent>
````

Add **Scope and compatibility** when the change affects a public contract, migration, dependency,
permission, or preserved behavior. Add **Risks and safeguards** for a material security, privacy,
data, billing, destructive-operation, or deployment risk. Add **Manual user path** when a short
representative path would help a reviewer observe a user-facing result.
