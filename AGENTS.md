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
