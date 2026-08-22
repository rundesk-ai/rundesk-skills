## Problem

<!-- State the current behavior or limitation, who or what it affects, and the consequence. -->

## Proposed solution

<!-- Describe the implemented outcome, important decisions and rationale, its boundary, and preserved behavior. -->

## Evidence

<!-- Give concise before-and-after observations, source locations, measurements, or contract links that support the merge case. Distinguish evidence from validation. -->

## Scope and compatibility

- Skills changed:
- User-visible guidance:
- Preserved behavior:
- Executables, service adapters, credentials, or network behavior added: none
- Third-party source, attribution, or license changes: none

## Risks and safeguards

<!-- Cover material credential, privacy, destructive, deployment, compatibility, or other risks. State "No material risk identified" when none applies. -->

- Risk:
- Guard:

## Acceptance criteria

- [ ] <!-- Independently checkable outcome proven by this exact head. -->

## Validation

- [ ] `python3 -m unittest discover -s tests -v`
- [ ] Every touched `SKILL.md` and `references/sources.md` was read completely.
- [ ] Every source link added or relied on was verified, or no source link changed.
- [ ] `git diff --check`
- [ ] Required GitHub checks pass for the exact head commit.

```text
# Exact validation and manual verification commands with observed results
```

## Repository gates

- [ ] The diff contains no credential, customer identifier, private-project language, owner-specific path, generated filler, or unrelated artifact.
- [ ] Every skill remains guidance-only: no script, executable, `rundesk.json`, credential, service adapter, or network call was added.
- [ ] Each touched skill's name, routing description, core guidance, references, and package layout follow `AGENTS.md` and the current `writing-skills` guidance.
- [ ] Each touched `references/sources.md` maps concrete claims to verified sources, uses more than one source kind, and is not vendor-only.
- [ ] Adapted work retains its upstream license and is recorded in `THIRD_PARTY_NOTICES.md`, or no adapted work changed.
- [ ] `README.md`, `manifest.json`, `tests/test_catalog.py`, and `skills/` agree.
- [ ] Any required semantic `manifest.json` version change follows `RELEASING.md` and is stated below.

## Release

- Manifest version: `<before>` → `<after>`
- SemVer reason:
- Release or follow-up required after merge:

## Manual user path

<!-- Give the shortest representative trigger or workflow and expected agent behavior. Explain when no manual user path applies. -->

```text

```

## Agent

<!-- Replace the placeholder with the filing agent's display name. Do not add provider, model, tool, session, or generated-by branding. -->

🤖 by <Agent>
