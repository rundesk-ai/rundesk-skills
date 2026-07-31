# AGENTS

This repository publishes guidance-only Agent Skills packages for Rundesk's development
catalog.

- Every package lives under `skills/<name>/` and follows the complete Agent Skills format.
- `SKILL.md` frontmatter names the containing directory and gives a concrete trigger description.
- Keep instructions, references, assets, and any package-local helper together in that directory.
- This catalog does not ship integration CLIs, credentials, service adapters, or shared state.
- `catalog.json` is the source of the catalog name, version, and complete skill list.
- A version change updates `catalog.json`; release tags use the same version prefixed with `v`.
- Read every skill before changing it and validate the whole catalog before publishing.
