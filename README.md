# Rundesk Skills

Rundesk's curated collection of general-purpose, guidance-only Agent Skills. It contains
complete skill packages and no service integration commands, credentials, or shared state.

Install the repository into Rundesk's machine-wide skill library:

```sh
rundesk skills install https://github.com/rundesk-ai/rundesk-skills
```

Installation makes every declared skill available but grants none automatically. Grant only
the skills an agent needs:

```sh
rundesk skills grant <agent> python-patterns
```

## Included skills

- `frontend-design`
- `laravel-patterns`
- `pdf-creation`
- `python-patterns`
- `python-testing`
- `seo`
- `vue-patterns`

## Manifest contract

`manifest.json` is the repository contract. The same format represents one skill or many:
`skills` is always a non-empty list, containing one entry for a single-skill repository and
several entries for a collection like this one.

Each entry names a complete package inside the repository. The catalog name is the install,
version, update, and removal unit; each skill name remains the grant and revoke unit. The
strict semantic `version` changes whenever installed content changes.

Script-backed skill catalogs use this same manifest format, but they will live in separate
repositories rather than this general collection.
