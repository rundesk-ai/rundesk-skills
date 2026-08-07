# Rundesk Skills

Rundesk's depended collection of general-purpose, guidance-only Agent Skills. It contains complete
skill packages and has no service integration commands, credentials, or shared state.

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

## Included skills

- `axmol-patterns`
- `cpp-patterns`
- `database-design`
- `debugging-code`
- `frontend-design`
- `inertia-patterns`
- `laravel-patterns`
- `managing-github`
- `mysql-patterns`
- `pdf-creation`
- `postgres-patterns`
- `python-patterns`
- `reviewing-code`
- `seo`
- `sqlite-patterns`
- `testing-code`
- `vue-patterns`
- `writing-plans`

## Manifest contract

`manifest.json` is the repository contract. Rundesk reads its `schema`, `name`, `version`, and
`description`, then discovers complete packages under `skills/`. The `skills` array remains this
repository's maintained catalog index and is checked against the Included skills list by repository
validation; Rundesk does not need it to discover packages.

The catalog name is the install and update unit; each skill name remains the grant and revoke unit.
This repository uses semantic versions for publication, but Rundesk compares source content rather
than trusting the version to decide whether an update exists.

Script-backed skill catalogs use this same manifest format and live in separate repositories,
including
[rundesk-skills-apple](https://github.com/rundesk-ai/rundesk-skills-apple) and
[rundesk-skills-integrations](https://github.com/rundesk-ai/rundesk-skills-integrations).

Rundesk checks this repository after every successful `rundesk update`. Changed content replaces
the installed catalog atomically, including same-version changes and local drift; identical content
stays in place. Catalog namespaces let repositories carry the same skill name. Use `--as <name>`
when one agent must hold two grants that would otherwise share a name. See
[RELEASING.md](RELEASING.md) for the version, tag, validation, and GitHub Release process
maintainers use.
