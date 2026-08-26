# Rundesk Skills

Rundesk's depended collection of general-purpose, guidance-only Agent Skills. It contains complete
skill packages and no service integration commands, credentials, or shared state.

## Skills

- `creating-design-assets`
- `ecommerce-storefronts`
- `laravel-stripe-payments`
- `maintaining-task-briefs`
- `naming-grammar-conventions`
- `pdf-creation`
- `performance-engineering`
- `working-as-an-assistant`
- `writing-plans`

## Install

Rundesk previews a catalog before changing the install. Review the preview, confirm it, then grant
only the skills an agent needs:

```sh
rundesk skills install https://github.com/rundesk-ai/rundesk-skills
rundesk skills install https://github.com/rundesk-ai/rundesk-skills --confirm
rundesk skills grant ava rundesk-skills/writing-plans
```

Installation adds the complete catalog and grants no skills automatically. Rundesk normally fetches
this depended catalog during installation, retries when a machine was offline, and does not permit
the catalog's removal. Its namespace owns later lifecycle commands:

```sh
rundesk skills catalogs
rundesk skills update rundesk-skills
rundesk skills update rundesk-skills --confirm
rundesk skills revoke ava writing-plans
```

## Requirements

- The catalog is public and installs from its GitHub repository with the current Rundesk CLI.
- Packages are guidance-only and require no catalog runtime, credentials, dependencies, or network
  access. A skill may describe tools that have their own documented requirements.
- Rundesk is optional. Copy or symlink a complete package, including its references and assets, into
  a provider's supported skill directory. For Codex use `.agents/skills/`; for Claude Code use
  `.claude/skills/`. Review an existing same-name destination before replacing it.
- The catalog name is the install and update unit. Each skill name is the grant and revoke unit. One
  agent cannot hold two grants with the same name; use `--as <name>` only for a deliberate alias.

Before updating from an older core catalog that still carries game or C++ skills, install
`rundesk-skills-gamedev`; for each affected agent, revoke the old core grant and immediately grant
the same-named gamedev skill. Then update this catalog.

### Marketing workflow skills

The Rundesk marketing team owns research, SEO, landing-page planning, lead-compliance, and product-
requirements skills. Install its catalog in skills-only mode to use them without creating the team:

```sh
rundesk skills install https://github.com/rundesk-ai/rundesk-team-marketing
rundesk skills install https://github.com/rundesk-ai/rundesk-team-marketing --confirm
```

Before updating from a version of this catalog that still carries those packages, move each affected
agent to the marketing-owned grant. Revoke the old grant, grant its replacement, then update this
catalog:

| Previous grant | Replacement |
|---|---|
| `conversion-landing-pages` | `rundesk-team-marketing/conversion-landing-pages` |
| `lead-compliance-gates` | `rundesk-team-marketing/lead-compliance-gates` |
| `researching-topics` | `rundesk-team-marketing/researching-topics` |
| `seo` | `rundesk-team-marketing/seo` |
| `writing-prds` | `rundesk-team-marketing/writing-prds` |

```sh
rundesk skills revoke ava seo
rundesk skills grant ava rundesk-team-marketing/seo
rundesk skills update rundesk-skills --confirm
```

### Development workflow skills

The Rundesk development team owns the coding and product-design skills. Install its catalog in
skills-only mode to use them without creating the team:

```sh
rundesk skills install https://github.com/rundesk-ai/rundesk-team-development
rundesk skills install https://github.com/rundesk-ai/rundesk-team-development --confirm
rundesk skills grant ava rundesk-team-development/testing-code
```

`managing-github` ships with Rundesk CLI as `rundesk/managing-github`. Before updating an older
`rundesk-skills` catalog, move each affected agent to the new grant: revoke the old same-named grant,
grant its replacement, then update this catalog:

| Previous grant | Replacement |
|---|---|
| `database-design` | `rundesk-team-development/designing-databases` |
| `debugging-code` | `rundesk-team-development/debugging-code` |
| `executing-development-tasks` | `rundesk-team-development/managing-development-work` |
| `frontend-design` | `rundesk-team-development/designing-ui-ux` |
| `inertia-patterns` | `rundesk-team-development/using-inertia` |
| `laravel-patterns` | `rundesk-team-development/using-laravel` |
| `mysql-patterns` | `rundesk-team-development/using-mysql` |
| `postgres-patterns` | `rundesk-team-development/using-postgres` |
| `python-patterns` | `rundesk-team-development/using-python` |
| `reviewing-code` | `rundesk-team-development/reviewing-code` |
| `sqlite-patterns` | `rundesk-team-development/using-sqlite` |
| `testing-code` | `rundesk-team-development/testing-code` |
| `vue-patterns` | `rundesk-team-development/using-vuejs` |
| `managing-github` | `rundesk/managing-github` |

```sh
rundesk skills revoke ava testing-code
rundesk skills grant ava rundesk-team-development/testing-code
rundesk skills revoke ava managing-github
rundesk skills grant ava rundesk/managing-github
rundesk skills update rundesk-skills --confirm
```

Repeat the replacement for every affected grant. Installing the complete development team later
reuses the skills catalog and adds its managed agents.

This collection separates runtime and permission boundaries: general guidance lives here, game and
C++ guidance lives in
[`rundesk-skills-gamedev`](https://github.com/rundesk-ai/rundesk-skills-gamedev), guarded local Apple
integrations live in
[`rundesk-skills-apple`](https://github.com/rundesk-ai/rundesk-skills-apple), and guarded service
integrations live in
[`rundesk-skills-integrations`](https://github.com/rundesk-ai/rundesk-skills-integrations).

## Repository layout

```text
.
├── .github/
│   ├── ISSUE_TEMPLATE/
│   ├── pull_request_template.md
│   └── workflows/
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
├── LICENSE
└── manifest.json
```

`manifest.json` supplies the published catalog name and version. Rundesk discovers packages under
`skills/`; the repository's legacy manifest `skills` index remains intentionally maintained and
must match package directories, frontmatter names, and this README.

## Development

Read [AGENTS.md](AGENTS.md) before changing the repository. The complete offline gate is:

```sh
python3 -m unittest discover -s tests -v
git diff --check
```

The suite requires Python 3.9+ and checks manifest, package, README, release, contributor-template,
and guide contracts. Skill changes also require source-link verification and a realistic forward
test when the guidance materially changes.

## Creating a skill catalog

Use the
[canonical skill-catalog guide](https://github.com/rundesk-ai/rundesk-cli/blob/main/docs/catalogs.md)
for catalog boundaries, manifests, package layout, installation, and validation.

This catalog's skills are researched judgment, not condensed manuals. Every new or touched package
keeps `references/sources.md`, uses a mixed evidence base, separates source claims from local
conclusions, and keeps conditional depth in focused references. Frontmatter contains only `name` and
`description`; routing belongs in the description, and `SKILL.md` stays below 500 lines. No scripts,
credentials, service adapters, or network behavior belong here.

## Contributing

Use the repository templates to keep reports bounded and reviewable:

- [Report a reproducible bug](.github/ISSUE_TEMPLATE/bug-report.md)
- [Propose a change](.github/ISSUE_TEMPLATE/change-proposal.md)
- [Prepare a pull request](.github/pull_request_template.md)

Search before adding a skill, keep public documentation synchronized with package changes, and
include exact validation evidence. Never publish credentials, personal or customer identifiers,
private-project language, or owner-specific paths. Adapted work must retain its upstream license and
record the upstream commit in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Releases

Published skill content and behavior changes follow [RELEASING.md](RELEASING.md) and its semantic
version policy. Repository-process-only changes to agent guides, contributor templates, or tests
that enforce those files do not require a manifest version bump. Rundesk compares catalog content,
not only the version, when deciding whether an installed tree changed.

## License

This catalog is available under the [MIT License](LICENSE). Adapted packages remain subject to the
licenses recorded in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
