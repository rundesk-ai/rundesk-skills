# AGENTS

Rules for every agent working in this repository. These instructions define how to work here; where
they conflict with general habits, this file wins.

## Purpose

This repository publishes Rundesk's depended, general-purpose guidance catalog. Its skills teach
repeatable judgment and workflows; they do not run commands, call services, hold credentials, or
replace current provider documentation. Script-backed work belongs in a catalog with the matching
runtime and permission boundary, such as `rundesk-skills-apple` or
`rundesk-skills-integrations`.

An offline Rundesk install may complete without this catalog. Rundesk retries later and does not
permit its removal.

`README.md` defines the public catalog. `manifest.json` defines the published catalog metadata and
maintained package index. Each package's `SKILL.md` and references define its guidance;
`RELEASING.md` defines publication.

Use the
[canonical skill-catalog guide](https://github.com/rundesk-ai/rundesk-cli/blob/main/docs/catalogs.md)
for organization-wide catalog structure and boundaries.

## Before you work

1. Read `docs/BRIEF.md` and `docs/CODEMAP.md` for what this catalog is and where its parts are,
   then `README.md`, this file, and the complete contents of every file you may change. For skill
   work, also read that package's `SKILL.md` and `references/sources.md`.
2. Search the repository before adding or renaming anything. Reuse the established term, package,
   pattern, and source of truth.
3. Load the smallest set of available skills that applies to the task. Use the current Rundesk `writing-skills`
   guidance for skill changes and `managing-github` for pull requests or releases when available.
   When a recurring term crosses files or layers, use `naming-grammar-conventions` when available.
   If governing guidance is unavailable, preserve established conventions and report the limitation;
   do not invent another required skill.
4. Inspect the worktree before editing. Preserve unrelated work and coordinate overlapping changes.
5. Verify Rundesk commands and catalog behavior against the current `rundesk-cli` parser, tests, and
   bundled skill contract. Do not copy syntax from memory or an older installed release.
6. Investigate an owner's concern before contradicting it. Bring evidence, not a hunch.

## Repository layout

```text
.
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug-report.md
│   │   └── change-proposal.md
│   ├── pull_request_template.md
│   └── workflows/
├── docs/
│   ├── README.md                   the index
│   ├── BRIEF.md                    what this catalog is for, and what it refuses
│   └── CODEMAP.md                  where each part lives, with counts
├── skills/<name>/
│   ├── SKILL.md
│   ├── references/sources.md
│   ├── references/<topic>.md       optional
│   └── assets/                     optional, only when consumed
├── tests/test_catalog.py
├── AGENTS.md
├── CLAUDE.md
├── README.md
├── RELEASING.md
├── THIRD_PARTY_NOTICES.md
└── manifest.json
```

`AGENTS.md` and `CLAUDE.md` are the same repository guide and must remain byte-identical. Do not add
empty optional directories or package-level READMEs, changelogs, installation guides, or creation
diaries.

## Package and artifact contract

- Keep each package entirely under `skills/<name>/` so a catalog update replaces it atomically.
- Every package contains `SKILL.md`. Every new or touched package contains
  `references/sources.md`.
- `SKILL.md` frontmatter contains only `name` and `description`.
- The directory and frontmatter `name` match and use lowercase letters, digits, and single hyphens;
  names are at most 64 characters.
- The manifest contract is `schema`, `name`, `version`, and `description`. Rundesk discovers
  `skills/<name>/SKILL.md` from the tree.
- This repository retains a legacy manifest `skills` index that the CLI ignores but the catalog
  tests require. Keep it aligned with package directories, frontmatter names, and the README list
  until an approved migration removes it.
- No script, executable, `rundesk.json`, credential, service adapter, network call, or
  provider-specific agent metadata belongs in this guidance-only catalog.

## Safety and approval gates

Get explicit approval before you:

- add executable, service, credential, dependency, or network behavior;
- delete a package or any file outside the immediate task;
- change a public contract, compatibility boundary, version, tag, or release;
- commit, push, publish, deploy, or modify repository settings; or
- modify this guide outside an authorized guide-maintenance task.

The current request may supply one or more of those approvals; never expand it beyond its stated
scope.

Never publish secrets, personal or customer identifiers, private-project language, owner-specific
paths, unredacted first-hand evidence, debug material, generated filler, unsupported claims, or
dropped attribution. Inspect the complete diff and commit-visible artifacts for those failures
before publication. Preserve unrelated work; do not reset, overwrite, force-push, or otherwise undo
shared work. Keep validation offline except for explicit source and link checks. Never claim a test,
review, or source verification that you did not observe.

## Delegation

Delegate only bounded work with explicit file ownership, constraints, and observable completion
criteria. Assign non-overlapping scopes and tell collaborators not to revert or overwrite other
work. Delegation never expands the request's authority. The parent remains responsible for
decisions, integration, full-diff review, validation, privacy, and the final result. Never treat
delegated output as proof until the parent verifies it.

## Architecture and conventions

A skill is researched judgment: traps, defaults, decisions, and proof that a capable agent would not
reliably infer from a manual's first page. Teach work in execution order. Give a strong default, the
condition for deviating, the failure a trap causes, the preferred replacement, and observable proof.
Remove prose that does not change execution, prevent a likely failure, or route needed depth.

Use a known trap's structure: **symptom → cause → preferred replacement → proof**. Good/bad examples
must come from traceable evidence, not invented illustrations.

Route precisely and spend context once:

- Make `description` the complete routing instruction because the body is unavailable until the
  skill triggers. Name direct and indirect goals and exclude only likely near-misses. Keep it within
  1,024 characters.
- Keep core steps, defaults, and gotchas in `SKILL.md`. Treat 500 lines as a ceiling, not a target.
- Put conditional depth and larger examples in focused references one level down. Link each
  reference from `SKILL.md` with the exact condition for reading it.
- Keep one source of truth for each rule. Do not add a table of contents that repeats headings or
  duplicate guidance across packages.
- Search before adding a skill. Extend the existing owner instead of splitting one subject across
  packages unless the new skill has distinct triggers, decisions, workflow, and proof.

## Documentation duties

Research before drafting technical claims. Every touched `references/sources.md` must cite the
specific page, discussion, rule, release, or study and state what it establishes. Use a mixed source
base appropriate to the claim:

- official documentation, specifications, source, registries, and releases for contracts and
  version facts;
- project issues, maintainer discussions, and reproducible failures for real traps and resolutions;
- analyzer or linter rules for mistakes the ecosystem guards against; and
- named practitioners or studies with their scope, sample, method, date, and limitations.

A vendor-only list is unfinished. Separate source statements from catalog conclusions, label
correlation and heuristics, quote only when exact wording matters, and verify every relied-on link.
Anonymize and scope recorded experience.

Adding, removing, or renaming a skill updates `manifest.json`, `README.md`, and
`tests/test_catalog.py` together. Adapted work retains its upstream license and records the upstream
commit in `THIRD_PARTY_NOTICES.md`. Update `RELEASING.md` when the release process changes. Validate
CLI examples against current `rundesk-cli`; link to deeper CLI documentation instead of duplicating
it.

Keep `docs/` in its layout. Only `README.md`, `BRIEF.md`, and `CODEMAP.md` sit at its root; a home is
added when there is a page for it and never left empty. Use the `structuring-project-docs` skill
before adding a home, moving a page, or changing the shape of one. Ecosystem root files —
`README.md`, `LICENSE`, `RELEASING.md`, `THIRD_PARTY_NOTICES.md`, and the guide pair — stay at the
repository root where consumers and tooling look for them.

Update `docs/CODEMAP.md` when a count, a layer, or a file it names changes, and `docs/BRIEF.md` only
when the catalog's purpose, audience, or refusals actually move. Keep pages thin: lead with the fact,
use a table wherever the content is tabular, and never restate a package's own guidance at the
repository level.

Keep all public documentation true in the same change as the behavior or contract it describes.

## Build, test, and run

This catalog's only runtime validation is the offline Python 3.9+ suite:

```sh
python3 -m unittest discover -s tests -v
```

Run the full suite after every change and record the exact command, discovered test count, and
result. Also run `git diff --check`, verify local links and every changed external source link, and
inspect the final diff for privacy and package-boundary failures.
For substantial skill changes, forward-test a realistic raw task without giving the evaluator the
expected answer; check routing, decision quality, traps, composition, and observable proof.

## Pull requests and releases

Use `.github/pull_request_template.md` for every pull request. Preserve its headings and checklists.
Fill it with exact commands and observed results from the exact proposed head commit. Mark a check
complete only from evidence; explain anything not applicable. Required CI must pass for that exact
head before merge.

Follow `RELEASING.md` for catalog publication. Skill content changes use the documented semantic
version policy. Repository-process-only changes, including `AGENTS.md`, `CLAUDE.md`, tests that
enforce their parity or structure, and pull request templates, do not require a manifest version
bump. Never tag unmerged content, reuse a published tag, or maintain a second release ledger.

## Definition of done

Work is complete only when:

- the full requested scope is implemented without unrelated changes;
- package, manifest, README, attribution, and guide parity contracts hold;
- the full catalog suite passes with discovered tests;
- applicable source, link, forward-test, and manual user-path checks pass;
- `git diff --check` and the privacy review are clean;
- no placeholder, debug artifact, unexplained skip, or temporary file remains; and
- the pull request reports exact-head evidence and required CI is green, when publication is in
  scope.

Report every unrun check, unavailable governing skill, unverified source, failed gate, or remaining
blocker plainly.
