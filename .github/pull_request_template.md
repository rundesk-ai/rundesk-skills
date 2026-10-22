## Summary

<!-- What was wrong or missing, and what is true now. One or two sentences. -->

## Changes

- <!-- One change per bullet, as someone using the catalog would notice it — not a file list. Add one bold **Breaking:** or **Risk:** line when it applies. -->

## Testing

- [ ] `python3 -m unittest discover -s tests -v`
- [ ] Every touched `SKILL.md` and `references/sources.md` was read completely.
- [ ] Every source link added or relied on was verified, or no source link changed.
- [ ] `git diff --check`
- [ ] Required GitHub checks pass for the exact head commit.

```text
# Each command or check run on this exact head, with what it showed
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
