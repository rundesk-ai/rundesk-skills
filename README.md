# Rundesk Skills

Rundesk's depended collection of general-purpose, guidance-only Agent Skills. It contains complete
skill packages and has no service integration commands, credentials, or shared state.

## Install with Rundesk CLI

Rundesk CLI is the default installation path for this catalog. It manages catalog updates, skill
namespaces, and per-agent grants while preserving the repository's complete package structure.

Rundesk fetches this catalog during its own install and retries after updates when an offline
machine could not fetch it. The direct catalog commands use the same preview-and-confirm flow:

```sh
rundesk skills install https://github.com/rundesk-ai/rundesk-skills
rundesk skills install https://github.com/rundesk-ai/rundesk-skills --confirm
```

The first command previews the manifest; `--confirm` installs the complete catalog when it is not
already present. Installation makes every discovered skill available but grants none automatically.
Grant only the skills an agent needs:

```sh
rundesk skills grant <agent> rundesk-skills/python-patterns
```

The manifest's catalog name owns later lifecycle commands:

```sh
rundesk skills catalogs
rundesk skills update rundesk-skills             # preview
rundesk skills update rundesk-skills --confirm   # apply
rundesk skills revoke <agent> python-patterns
```

`rundesk-skills` is a Rundesk dependency and cannot be removed. Revoke an individual grant when an
agent no longer needs it.

## Use without Rundesk

Rundesk is not required. Each directory under `skills/` is a portable Agent Skill with its own
`SKILL.md` and supporting files. Copy or symlink the complete package directories you want; do not
copy only `SKILL.md`, because its relative references belong to the package.

For Codex, place packages in `.agents/skills/` at a repository root for project use or in
`~/.agents/skills/` for personal use. Codex also follows symlinked skill directories. For Claude
Code, place packages in `.claude/skills/` for a project or in `~/.claude/skills/` for personal use.
Restart or begin a new session if the agent does not detect a newly copied skill.

```sh
# Codex, current repository
mkdir -p .agents/skills
cp -R /path/to/rundesk-skills/skills/testing-code .agents/skills/

# Claude Code, current repository
mkdir -p .claude/skills
cp -R /path/to/rundesk-skills/skills/testing-code .claude/skills/
```

These packages follow the open Agent Skills `SKILL.md` format. Script-backed packages, where a
catalog has them, remain subject to their documented runtime, credential, and permission setup even
when copied directly. Review an existing same-name destination before replacing it so an update
cannot retain stale package files.

## Included skills

- `creating-design-assets`
- `conversion-landing-pages`
- `database-design`
- `debugging-code`
- `ecommerce-storefronts`
- `executing-development-tasks`
- `frontend-design`
- `inertia-patterns`
- `laravel-patterns`
- `laravel-stripe-payments`
- `lead-compliance-gates`
- `maintaining-task-briefs`
- `managing-github`
- `mysql-patterns`
- `naming-grammar-conventions`
- `pdf-creation`
- `performance-engineering`
- `postgres-patterns`
- `python-patterns`
- `researching-topics`
- `reviewing-code`
- `seo`
- `sqlite-patterns`
- `testing-code`
- `vue-patterns`
- `working-as-an-assistant`
- `writing-plans`
- `writing-prds`
- `writing-technical-docs`

## Manifest contract

`manifest.json` is the repository contract. Rundesk reads its `schema`, `name`, `version`, and
`description`, then discovers complete packages under `skills/`. The `skills` array remains this
repository's maintained catalog index and is checked against the Included skills list by repository
validation; Rundesk does not need it to discover packages.

The catalog name is the install and update unit; each skill name remains the grant and revoke unit.
This repository uses semantic versions for publication, but Rundesk compares source content rather
than trusting the version to decide whether an update exists.

## Rundesk Skills collection

| Catalog | Purpose |
|---|---|
| [rundesk-skills](https://github.com/rundesk-ai/rundesk-skills) | General guidance and software-development workflows |
| [rundesk-skills-gamedev](https://github.com/rundesk-ai/rundesk-skills-gamedev) | Game design, production, C++, 2D systems, and Axmol |
| [rundesk-skills-apple](https://github.com/rundesk-ai/rundesk-skills-apple) | Guarded local Apple integrations for macOS |
| [rundesk-skills-integrations](https://github.com/rundesk-ai/rundesk-skills-integrations) | Guarded service integration CLIs |

Catalog namespaces cannot transfer grants automatically, and one agent cannot hold two grants under
the same skill name. Before updating from a core catalog version that still carries game or C++
skills, install `rundesk-skills-gamedev`; for each affected agent, revoke the old core grant and
immediately grant the same-named gamedev skill. Then update the core catalog. Use `--as <name>` only
when a deliberate temporary alias is preferable to that one-at-a-time replacement.

Standalone layout details: [Codex skills](https://learn.chatgpt.com/docs/build-skills) and
[Claude Code skills](https://code.claude.com/docs/en/slash-commands).

Rundesk checks this repository after every successful `rundesk update`. Changed content replaces
the installed catalog atomically, including same-version changes and local drift; identical content
stays in place. Catalog namespaces let repositories carry the same skill name. Use `--as <name>`
when one agent must hold two grants that would otherwise share a name. See
[RELEASING.md](RELEASING.md) for the version, tag, validation, and GitHub Release process
maintainers use.
