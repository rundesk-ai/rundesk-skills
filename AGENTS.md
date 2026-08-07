# AGENTS

Rules for agents working in this repository.

This is the depended, general-purpose guidance catalog Rundesk fetches when absent. It teaches
repeatable work; it does not run commands, call services, hold credentials, or replace provider
documentation. Script-backed work belongs in `rundesk-skills-apple` or
`rundesk-skills-integrations`. An offline install may complete without this catalog; Rundesk retries
later and does not permit its removal.

## Start here

1. Read `README.md`, then every `SKILL.md` and `references/sources.md` you will touch. Read each file
   before editing it.
2. Load the rule for the artifact:

   | Change | Follow |
   |---|---|
   | any skill | current Rundesk `writing-skills` |
   | Python or `tests/test_catalog.py` | `python-patterns` |
   | pull request | `managing-github` pull-request guidance |
   | version, tag, or release | `RELEASING.md`, then `managing-github` release guidance |

   If a governing skill is unavailable, name it in the report; do not imply compliance.
3. Search before adding a skill. Extend the existing owner instead of splitting one subject across
   packages.
4. Verify Rundesk commands and catalog behavior against the current `rundesk-cli` parser, tests, and
   bundled `writing-skills` package. Never copy syntax from memory or an older installed release.
5. Investigate an owner's concern before contradicting it. Bring evidence, not a hunch.

## A skill is researched judgment

A skill synthesizes traps, defaults, and decisions a capable agent would not reliably infer. Its
job is consistent output quality: teach the preferred practice, what not to do, what to do instead,
and the failure that choice prevents. It is not generated filler or a condensed manual.

| Do | Don't |
|---|---|
| Teach the workflow in execution order | Enumerate an API or every option |
| Give one strong default and when to deviate | Present preference as universal law |
| Name the gotcha and the failure it causes | Use unexplained `always` or `never` |
| Pair every `don't` with the better replacement | Leave the agent knowing only what to avoid |
| Show a small good/bad pair | Add background prose |
| Route conditional depth to one reference | Duplicate a rule across files |
| Link to exhaustive upstream detail | Paraphrase the manual |

Keep a rule only when it changes execution, prevents a likely failure, or routes needed depth.
Write a known trap as **symptom → cause → preferred replacement → proof**. If a source only says a
feature exists and reveals no failure or better practice, link the manual when needed; do not copy
it into the skill.

Good/bad examples are sourced evidence, not invented illustrations. Derive each pair from a cited
guideline, analyzer rule, maintainer resolution, or reproduced community failure. You may minimize
the syntax, but `sources.md` must make the lesson behind the pair traceable.

```cpp
// Good: erase returns the next valid iterator.
it = items.erase(it);

// Bad: erase invalidates `it`; incrementing it is undefined behavior.
items.erase(it);
++it;
```

Source: `skills/cpp-patterns/references/sources.md` maps this pair to cppreference's invalidation
rules.

Before shipping, ask: would a competent practitioner learn more than the docs' first page; does
each constraint name its failure; and can the agent act now? If not, research or cut it.

## Route precisely; spend context once

Use only `name` and `description` in `SKILL.md` frontmatter.

- `name` matches the directory: lowercase letters, digits, single hyphens, at most 64 characters.
- `description` is the routing instruction. Start with `Use when`, `Apply when`, or equivalent and
  name direct and indirect user goals. Follow with one short sentence naming the workflow or
  knowledge supplied. Add `Do not use` only to exclude a likely near-miss. Keep it within 1,024
  characters.
- Put every trigger in the description; the body is unavailable until the skill triggers.
- Keep core steps, defaults, and gotchas in `SKILL.md`. Put conditional depth and larger examples in
  focused references, one level down.
- Link each reference from `SKILL.md` with the exact condition for reading it. Keep one source of
  truth for each instruction.
- Do not add a table of contents to `SKILL.md` or a reference. The agent reads the complete file, so
  repeating its headings spends context without improving routing.
- Create no empty optional directory and no package README, changelog, installation guide, or
  creation diary.

```yaml
# Good: intent and boundary are discoverable before loading.
description: >
  Use when designing or reviewing SQLite schemas, transactions, WAL behavior, backups, or query
  plans. It supplies SQLite-specific defaults and failure modes for durable applications. Do not
  use it for database-engine selection or generic data modeling.

# Bad: vague and impossible to route reliably.
description: Helpful SQLite docs and reference files.
```

Treat 500 lines as a ceiling for `SKILL.md`, not a target. Every holder pays for the description on
every turn; every trigger pays for the body.

## Research first; synthesize, never invent

Never draft a technical claim from model memory and source it afterward. Research first, then write
only what evidence supports: traps people hit, approaches communities abandoned, version boundaries,
and proven defaults.

Every touched package has `references/sources.md`. Cite the specific page, discussion, rule, release,
or study and state what it establishes. Use more than one source kind:

| Source | Establishes |
|---|---|
| Official docs, specs, source, registries, releases | contracts and version facts |
| Project issues, maintainer discussions, mailing lists, authoritative Q&A | reproduced failures and resolutions |
| Linter and analyzer rule catalogs | mistakes the ecosystem automates against |
| Named practitioners and studies with methods | judgment and empirical findings |

```markdown
Good: Official docs establish the contract; a maintainer issue explains the surprise; an analyzer
rule shows the ecosystem guards against it.

Bad: Vendor docs alone, an anonymous listicle, another generated summary, or a homepage that does
not contain the cited claim.
```

- A vendor-only source list is unfinished; add reputable community or practitioner evidence.
- Verify version facts against a registry, source tag, or release page; record version and date.
- For empirical claims, record author, date, sample, and method; label correlation as correlation.
- Separate what a source states from this catalog's conclusion. Explain the failure behind local
  judgment.
- Quote only when exact wording matters; otherwise paraphrase and cite. Do not stretch a source.
- Recorded first-hand experience must be labeled, scoped, and anonymized. Never publish a person,
  customer, private project, secret, or absolute owner path.
- Verify every link before completion and report any that could not be checked.

## Package and catalog contract

```text
skills/<name>/
├── SKILL.md                   required: routing and core guidance
├── references/sources.md     required for new or touched packages
├── references/<topic>.md     optional: focused depth
└── assets/                   optional: used templates or fixtures
```

Keep a package inside its tree so catalog updates replace it atomically. No `scripts/`, executable,
`rundesk.json`, credential, service adapter, or network call belongs here.

Rundesk's manifest contract is only `schema`, `name`, `version`, and `description`; it discovers
`skills/<name>/SKILL.md` from the tree. This repository also retains a legacy `skills` index that the
CLI ignores but the repository suite requires. Keep that index, directory names, frontmatter names,
and README list aligned until an approved migration removes the redundant index.

Semantic versioning labels this repository's releases; Rundesk compares catalog content, not the
version, to decide whether an installed tree changes.

Adapted work keeps its upstream license in the package and an entry in `THIRD_PARTY_NOTICES.md` with
the upstream commit.

## Keep the public surface synchronized

- Add, remove, or rename a skill: update `manifest.json`, `README.md`, and catalog assertions in
  `tests/test_catalog.py`.
- Adapt upstream work: update `THIRD_PARTY_NOTICES.md` and retain its license.
- Change the release process: update `RELEASING.md`.
- Change install, update, grant, or revoke examples: validate against current `rundesk-cli`.
- Publish: bump `manifest.json` under `RELEASING.md`; let the workflow generate GitHub release notes.
  Do not maintain a second release ledger.

Do not duplicate deeper CLI documentation here; point to its live source of truth.

## Ask first

- Add an executable, service adapter, credential, or network behavior.
- Delete a package or a file outside the immediate task.
- Commit, tag, release, or push.
- Modify this file.

Never leave debug material, generated filler, unsupported claims, owner-specific content, or dropped
attribution in a published package.

## Validate

The only runtime is the offline Python 3.9+ catalog test:

```sh
python3 -m unittest discover -s tests -v
```

Completion requires a passing suite with discovered tests, green required CI, and every rule above
satisfied. Report any governing skill or source link that could not be loaded or verified.
