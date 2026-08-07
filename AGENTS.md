# AGENTS

Rules for every agent working in this repository. These rules are law; where they conflict with your
general habits, this file wins.

This repository publishes **Rundesk's general-purpose, guidance-only Agent Skills catalog** — the
one shipped with every Rundesk install. It teaches; it does not run anything. `README.md` is what a
person reads, `THIRD_PARTY_NOTICES.md` records what was adapted from elsewhere, and `RELEASING.md`
is how a version ships. This file defines how you build here.

## Before you work

1. **Read `README.md` and the `SKILL.md` of every package you are touching.** Read a file before
   editing it.
2. **Load the skill that governs the artifact you are about to write.** Each one is law for that
   artifact, the same as this file:

   | Writing or changing | Follow |
   |---|---|
   | any `SKILL.md` | `writing-skills` |
   | any Python in this repository | `python-patterns` |
   | `tests/test_catalog.py` | `python-patterns` (testing) |
   | a pull request | `managing-github` (pull requests) |
   | a version bump, tag, or release | `RELEASING.md`, then `managing-github` (releases) |

   An agent that does not hold one of these skills still follows the rule; say in your report which
   ones you could not load, because silence reads as compliance.
3. **Check whether an existing package already owns the subject** before adding one. A second skill
   covering the same ground splits the guidance and neither half stays current.
4. When the owner raises a concern, investigate before contradicting — evidence, not a hunch.

## A skill is not a copy of the documentation

**This is the rule the rest of the file serves.** A skill exists to help an agent *write something
well* — consistently, idiomatically, and without walking into a failure somebody else already found.
It is not a reference manual, and the reader already has the manual.

| A skill is | A skill is not |
|---|---|
| How to do the task well, in the order it is done | An enumeration of the API surface |
| The default to reach for, and when to deviate | A list of every available option |
| **Dos and don'ts, with the failure each prevents** | A restatement of what a function returns |
| The gotcha that is not obvious from the signature | A paraphrase of a doc page |
| Version facts that change the advice | A changelog |
| Judgement the documentation deliberately leaves open | An opinion presented as a rule |

Three tests before shipping a page:

1. **Would a competent practitioner learn something?** If it only tells them what they would find in
   the first paragraph of the docs, delete it.
2. **Does every rule name the failure it prevents?** "Use X" is unevaluable. "Use X, because Y silently
   produces the wrong value after a reallocation" can be judged, argued with, and applied.
3. **Could the reader act on this without the docs open?** A skill routes and decides; it links out
   for the exhaustive detail rather than reproducing it.

Copying documentation is worse than omitting it: it doubles the maintenance surface, it goes stale
invisibly, and it buries the guidance that only this package has.

## Research before writing — every claim is sourced

**Never write a skill or a reference from memory.** A model's recollection of a framework is a
snapshot of an average of old tutorials; it is confidently wrong about versions, renamed APIs, and
anything that changed recently. Research first, then write only what the research supports.

**Every package carries a `references/sources.md`** recording where its content came from, and any
claim a reader might challenge is traceable to a source from that file.

### Where the content must come from

Find the traps, gotchas, and failures **other people have already hit and solved.** That is the whole
value of a skill — not a restatement of an API, which the reader can look up.

| Source | Use it for |
|---|---|
| Official documentation | Version facts, exact APIs, and the **warnings the vendor wrote down** |
| Lint and analyser rule catalogs | What the ecosystem thinks is worth failing a build over |
| Issue trackers, GitHub Discussions, forums, mailing lists | The problem somebody already debugged, and the maintainer's answer |
| Stack Overflow, when the answer is authoritative and current | Concrete failure modes with reproductions |
| Practitioner blogs and talks by maintainers and recognized experts | Judgement the docs deliberately omit |
| Published studies and measurements | Anything empirical, quoted with its sample and date |
| Release notes, upgrade guides, deprecation schedules | What is about to break |

### Documentation grounds a package; it must not be the whole of it

**A `sources.md` that is only vendor documentation is not finished research.** Documentation says how
a thing is meant to work. It rarely says which part bites people, what the maintainer told somebody
in a thread, or which recommended approach the community abandoned. A package built only from docs
reproduces the manual and misses the reason the skill exists.

So every package cites **more than one kind of source**, and the non-documentation sources must be
reputable and identifiable — a named maintainer, a project's own discussion forum, a recognized
practitioner, a study with a method. An anonymous listicle is not a source.

### Rules

- **Cite the specific page, not the site.** `sources.md` says what each source established.
- **Quote a rule that a reader might otherwise soften.** A vendor's own `WARNING` in its own words
  carries weight a paraphrase does not.
- **Verify every link resolves** before committing, and say so in the pull request. Report any link
  you could not verify rather than implying you did.
- **Check version facts against a registry or release page**, never against documentation prose or
  recollection. Say which version the package was verified against, and date it.
- **Label empirical claims** with sample, date, and author, and mark them correlational when they are.
  Never present a vendor's marketing figure as a finding.
- **Separate what a source states from what you concluded.** If guidance is the package's own
  judgement, say so and give the failure it prevents.
- **Recorded first-hand experience is a legitimate source** and often the most valuable, because it is
  what no document contains. Record it as such, say how strong the evidence is, and generalize it —
  never name a person, customer, private project, or owner path.

## Hard gates — require explicit approval

- **An executable, a service adapter, or anything that needs a credential.** This catalog is
  guidance only, and `tests/test_catalog.py` enforces it. Script-backed skills live in their own
  repositories — `rundesk-skills-apple` and `rundesk-skills-integrations`.
- **Deletions.** Do not delete a package or a file outside the task's immediate scope.
- **Commits.** Do not commit or push unless told to.
- **This file.** Never modify `AGENTS.md` without approval.

## Never

- **Never let the catalog's public surface drift.** Adding, removing, or renaming a skill changes
  `manifest.json`, `README.md`, and the catalog suite **in the same commit**, plus
  `THIRD_PARTY_NOTICES.md` when the package was adapted from someone else's work. A README naming
  seven skills for a catalog of eight is how a reader learns the repository cannot be trusted, and
  it hides in a diff that only adds files. `tests/test_catalog.py` enforces this, so the rule
  survives an agent who forgets it.
- **Never split a package.** Instructions, references, assets, and any package-local helper live
  together under `skills/<name>/`, because a catalog update replaces that tree atomically.
- **Never let `SKILL.md` frontmatter lie.** `name` is the containing directory, and `description`
  names the concrete situations that should trigger it — an agent chooses a skill from that line
  alone, so a vague one is a skill nobody reaches for.
- **Never drop an attribution.** Adapted material keeps its upstream license file inside the
  package and its entry in `THIRD_PARTY_NOTICES.md`, with the commit it was taken from.
- **Never name a person, a customer, a private project, or an absolute owner path.** Every skill
  here is published and read by agents that are not yours; keep it owner-neutral.

## The package contract

```text
skills/<name>/
├── SKILL.md          frontmatter `name` + `description`, then the guidance
├── references/       depth read on demand, never inlined into SKILL.md
└── assets/           templates and fixtures the guidance points at
```

`manifest.json` is the catalog name, schema, version, and complete skill list. The catalog name is
the install, update, and removal unit; each skill name is the grant and revoke unit.

## Tech stack

- **Runtime:** Python 3.9+ — the floor CI pins, because it is the oldest a fresh macOS ships.
- **Tests:** `unittest`, offline, run directly. Nothing here reaches the network.

## Build, test & run

```sh
python3 -m unittest discover -s tests -v      # the gate
```

CI runs the same command on Ubuntu with Python 3.9, and nothing else is required to publish.

## Documentation duties

Keep the documentation true in the same task that changes reality.

- A skill added, removed, or renamed → `manifest.json`, `README.md`, and the expected-skill
  assertions in `tests/test_catalog.py`.
- A package adapted from upstream work → `THIRD_PARTY_NOTICES.md` and the package's own license
  file.
- A change to the release process → `RELEASING.md`.
- Depth belongs in the package's `references/`, never inlined into `SKILL.md`. `SKILL.md` carries
  triggers, the shape of the work, and the judgment an agent could not infer.

## Definition of done

1. `python3 -m unittest discover -s tests -v` passes, and CI is green.
2. Every rule here held — nothing executable, no credential, no owner-specific content.
3. `README.md` and `manifest.json` agree with what the repository actually ships.
4. The governing skills in **Before you work** were followed, or your report names the ones you
   could not load.
5. **The research rules held.** Every package touched has a `references/sources.md`; it cites more
   than vendor documentation; every link was checked and any that could not be verified is named in
   the report; and version facts were confirmed against a registry or release page, with the date
   recorded.
