# Codemap — rundesk-skills

Where each part lives. Counts are of artifacts, so they survive a rename and go wrong visibly when
the tree moves on without this page.

A catalog is mostly one shape repeated: every package is a directory under `skills/` holding a
`SKILL.md` and the references it loads on demand. Nothing else in the repository is large.

## Packages (skills/ — 9, 31 reference files)

Each holds `SKILL.md` (routing plus core procedure) and `references/` (conditional detail).
`references/sources.md` is required in every touched package.

| Package | References |
|---|---|
| `creating-design-assets` | 5 |
| `ecommerce-storefronts` | 4 |
| `laravel-stripe-payments` | 7 |
| `maintaining-task-briefs` | 1 |
| `naming-grammar-conventions` | 5 |
| `pdf-creation` | 0 |
| `performance-engineering` | 4 |
| `working-as-an-assistant` | 4 |
| `writing-plans` | 1 |

## Catalog identity (root)

| File | What it is |
|---|---|
| `manifest.json` | schema, name, version (`6.0.0`), description, and the legacy `skills` index the CLI ignores but the tests require |
| `README.md` | the consumer contract: what the catalog is, how to install it, and every package |
| `AGENTS.md`, `CLAUDE.md` | the repository guide, byte-identical by contract |
| `RELEASING.md` | the publication contract |
| `THIRD_PARTY_NOTICES.md` | upstream licence and commit for adapted work |

## Tests (tests/ — 1 suite)

`tests/test_catalog.py` holds the repository contract: manifest and tree agree, every package is
complete and correctly named, the README lists exactly what ships, the guide pair is identical, and
the templates keep their required shape. It also names the skills that moved to other catalogs, so
one cannot return by either route.

## Automation (.github/)

Issue templates, the pull-request template, and the workflow that runs the suite.

## Documentation (docs/)

`README.md`, `BRIEF.md`, and `CODEMAP.md`. There are no other homes: each package documents itself,
and a catalog this size would be inventing directories to hold three files.
