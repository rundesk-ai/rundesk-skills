# Rundesk Skills

Rundesk's curated collection of general-purpose, guidance-only Agent Skills. It is included
with every Rundesk install, contains complete skill packages, and has no service integration
commands, credentials, or shared state.

Install the repository into Rundesk's machine-wide skill library:

```sh
rundesk skills install https://github.com/rundesk-ai/rundesk-skills
rundesk skills install https://github.com/rundesk-ai/rundesk-skills --confirm
```

The first command previews the manifest; `--confirm` installs the complete catalog. Installation
makes every declared skill available but grants none automatically. Grant only the skills an
agent needs:

```sh
rundesk skills grant <agent> python-patterns
```

The manifest's catalog name owns later lifecycle commands:

```sh
rundesk skills catalogs
rundesk skills update rundesk-skills
rundesk skills remove rundesk-skills
```

Removal requires a second `--yes` invocation and is refused while any declared skill is granted.

## Included skills

- `database-design`
- `debugging-code`
- `frontend-design`
- `laravel-patterns`
- `managing-github`
- `mysql-patterns`
- `pdf-creation`
- `postgres-patterns`
- `python-patterns`
- `python-testing`
- `reviewing-code`
- `seo`
- `sqlite-patterns`
- `testing-code`
- `vue-patterns`
- `writing-plans`

## Manifest contract

`manifest.json` is the repository contract. The same format represents one skill or many:
`skills` is always a non-empty list, containing one entry for a single-skill repository and
several entries for a collection like this one.

Each entry names a complete package inside the repository. The catalog name is the install,
version, update, and removal unit; each skill name remains the grant and revoke unit. The
strict semantic `version` changes whenever installed content changes.

Script-backed skill catalogs use this same manifest format and live in separate repositories,
including
[rundesk-skills-apple](https://github.com/rundesk-ai/rundesk-skills-apple) and
[rundesk-skills-integrations](https://github.com/rundesk-ai/rundesk-skills-integrations).

Rundesk checks this repository after every successful `rundesk update`. A newer manifest version
is activated atomically, while a same-version check restores the repository's exact files to
remove local drift. A custom skill with any declared name makes the complete catalog installation
fail without overwriting that custom content. See [RELEASING.md](RELEASING.md) for the version,
tag, validation, and GitHub Release process maintainers use.
