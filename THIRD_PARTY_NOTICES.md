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
