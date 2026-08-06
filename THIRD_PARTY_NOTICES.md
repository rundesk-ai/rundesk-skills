# Third-party notices

The following skills are adapted from the
[ECC skill collection](https://github.com/affaan-m/ECC/tree/e4e4163101f162881e628f300a9ca4e6a940bcea)
at commit `e4e4163101f162881e628f300a9ca4e6a940bcea`:

- `laravel-patterns`
- `python-patterns`
- `seo`
- `vue-patterns`

The source material is licensed under the MIT License:

Copyright (c) 2026 Affaan Mustafa

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

The `frontend-design` skill is adapted from Anthropic's
[frontend-design Agent Skill](https://github.com/anthropics/skills/tree/2235be7c60b551f5de82ade908fd3816455afcda/skills/frontend-design)
at commit `2235be7c60b551f5de82ade908fd3816455afcda`. Rundesk changed the skill's
metadata, workflow, UX guidance, accessibility guidance, implementation constraints, and
verification criteria. The source and this derivative are provided under the Apache License,
Version 2.0; a copy accompanies the skill in `skills/frontend-design/LICENSE.txt`.

The `postgres-patterns` skill is adapted from
[Supabase's agent-skills collection](https://github.com/supabase/agent-skills/tree/1207767388a0ffb55f21fb4e6988fee96942431d/skills/supabase-postgres-best-practices)
at commit `1207767388a0ffb55f21fb4e6988fee96942431d`. Rundesk renamed the skill, replaced its
frontmatter with this catalog's `name` and `description` contract, restructured `SKILL.md` around
the rule categories with local reference links, and removed every Supabase-specific construct:
`auth.uid()` became an application-set session setting (`current_setting('app.current_user_id',
true)`), the `anon`/`authenticated`/`service_role` roles became ordinary roles, the hosted pooler
became PgBouncer, and Supabase documentation links became their PostgreSQL documentation
equivalents or were dropped where none exists. Rundesk did not carry across the upstream
`CHANGELOG.md`, `references/_contributing.md`, or `references/_template.md`. A copy of the license
accompanies the skill in `skills/postgres-patterns/LICENSE.txt`.

The source material is licensed under the MIT License:

Copyright (c) 2026 Supabase

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

The `mysql-patterns` skill is adapted from
[PlanetScale's database-skills collection](https://github.com/planetscale/database-skills/tree/af0ce0cfb65cca4cc21d18ca0d9cf270ca99d488/skills/mysql)
at commit `af0ce0cfb65cca4cc21d18ca0d9cf270ca99d488`. Rundesk renamed the skill, deleted the
PlanetScale hosting recommendation from `SKILL.md`, rewrote every remote
`raw.githubusercontent.com` reference link as a path inside the package, and replaced the
PlanetScale- and Vitess-specific passages in `references/online-ddl.md` and
`references/connection-management.md` with the underlying MySQL behaviour — native online DDL plus
`gh-ost`/`pt-online-schema-change`, and a generic connection proxy. A copy of the license
accompanies the skill in `skills/mysql-patterns/LICENSE.txt`.

The source material is licensed under the MIT License:

Copyright (c) 2026 PlanetScale

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

The `sqlite-patterns` and `database-design` skills are adapted from the
[claude-skills-generator collection](https://github.com/martinholovsky/claude-skills-generator/tree/1086ef25672acba2916220c6ce032a612cd9dc98)
at commit `1086ef25672acba2916220c6ce032a612cd9dc98` — `sqlite-patterns` from `skills/sqlite` and
`database-design` from `skills/database-design`, each of which supplied a `SKILL.md` and the
reference files `advanced-patterns.md` and `security-examples.md`.

Rundesk renamed both skills and replaced the upstream frontmatter — `name`, `risk_level`,
`description`, `version`, `author`, `tags`, and a pinned model identifier — with this catalog's
`name` and `description` contract. Rundesk removed the framing that scoped both skills to one
private desktop project, renumbered and reordered the sections of both `SKILL.md` files, resolved
the upstream's contradictory risk classification by dropping it, and removed a "Key Vulnerabilities"
section that named no vulnerability. In `sqlite-patterns`, Rundesk made the guidance
engine-level and language-neutral with Python worked examples, moved the upstream's Rust
(`rusqlite`, `sea-query`, `r2d2`) material into `references/rust-bindings.md`, and corrected several
technical claims: `PRAGMA mmap_size = 30000000000` is now presented as a measured tuning knob rather
than an initialization default, `PRAGMA page_size` is documented as ineffective after the first
write, the FTS5 external-content trigger set is complete rather than insert-only, the FTS5
integrity check no longer reads a row from an `INSERT`, `LIKE` escaping is paired with an `ESCAPE`
clause, and the table-rebuild procedure disables foreign keys outside the transaction and runs
`PRAGMA foreign_key_check` before committing. In `database-design`, Rundesk narrowed the scope to
engine-independent modelling and replaced the upstream's indexing, query-tuning, connection-pooling
and partitioning guidance with pointers to `postgres-patterns`, `mysql-patterns`, and
`sqlite-patterns`; it also corrected the "one current version" constraint in the temporal pattern,
which the upstream expressed as a `UNIQUE` over a nullable column that does not enforce it. A copy
of the license accompanies each skill in `skills/sqlite-patterns/LICENSE.txt` and
`skills/database-design/LICENSE.txt`.

The source material is released into the public domain under the Unlicense:

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org>

The `python-testing` skill is adapted from the
[LambdaTest Agent Skills collection](https://github.com/LambdaTest/agent-skills/tree/a7cdbf033ede0442d393a3a816507166dc196896/unittest-skill)
at commit `a7cdbf033ede0442d393a3a816507166dc196896`.

The source material is licensed under the MIT License:

Copyright (c) 2025 TestMu AI / LambdaTest

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
