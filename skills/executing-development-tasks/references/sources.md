# Sources

Checked 2026-08-08. These sources establish the lifecycle and failure modes synthesized in
`SKILL.md`; they do not make one provider's commands or one team's ceremony universal.

## Completion and requirement traceability

- Ken Schwaber and Jeff Sutherland's [Scrum Guide](https://scrumguides.org/scrum-guide.html) defines
  the Definition of Done as the product's required quality state and says work that does not meet it
  is not part of the increment. This supports defining the completion gate before implementation and
  refusing to rename partial validation as done; the skill does not otherwise prescribe Scrum.
- NASA's [SWE-034 acceptance-criteria guidance](https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695413/SWE-034+-+Acceptance+Criteria)
  explains that documented, measurable criteria create shared expectations and an objective basis
  for readiness. NASA's [traceability completion risk](https://swehb.nasa.gov/spaces/SITE/pages/215777594/R053+-+Traceability+Completion)
  maps missing links among requirements, implementation, and verification to late functional gaps
  and rework. Applied here, a lightweight requirement-to-proof trace prevents an agent from losing
  part of the request during implementation.

## Decomposition and delegated execution

- Wei Zhang and Jessie Jie Xia's [Abstraction first](https://martinfowler.com/articles/structured-prompt-driven/abstraction-first.html)
  is practitioner guidance from Thoughtworks' AI-assisted delivery work. It identifies independent,
  testable, acceptance-ready tasks and an end-to-end-complete task chain as defenses against agents
  inventing details or generating an integrated but incomplete blob. This supports coherent phases
  and explicit completeness checks, not the article's full SPDD method.
- Anthropic's June 13, 2025 engineering report,
  [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system),
  reports that effective worker briefs need an objective, output format, tools or sources, and clear
  boundaries; vague delegation produced duplicated work and gaps. It also reports materially higher
  token use and weaker fit when work has many dependencies or little parallelism. This field report
  supports bounded delegation for substantial independent work rather than mandatory subagents for
  every task; its quantitative results are specific to Anthropic's research system.
- OpenAI's current [model guidance](https://developers.openai.com/api/docs/guides/latest-model)
  likewise limits multi-agent benefit to complex tasks that divide cleanly into independent
  workstreams. Agreement across two provider implementations supports the provider-neutral boundary;
  neither source establishes that all development tasks should be parallelized.

## Verification, review, and user-path QA

- George Pirocanac's [How Much Testing Is Enough?](https://testing.googleblog.com/2021/06/how-much-testing-is-enough.html)
  distinguishes unit, integration, and end-to-end evidence and recommends exercising critical user
  journeys as a user would use the product. It also treats accessibility, security, performance,
  privacy, localization, and usability as additional risk-dependent tiers. This supports selecting
  proof from the changed risk rather than treating one green suite or a coverage number as universal
  completion.
- Google's [What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
  says tests require human inspection to establish that they are useful and would fail when behavior
  breaks. It also asks reviewers to judge user functionality and visual changes, check documentation,
  inspect context beyond changed lines, and add qualified reviewers for specialist risks. This is the
  basis for independent review after implementation and rerunning proof after review fixes.
- W3C's [Understanding Conformance for WCAG 2.2](https://www.w3.org/WAI/WCAG22/Understanding/conformance.html)
  states that accessibility evaluation combines automated testing with human evaluation and that
  functional conformance does not by itself establish usability. Applied narrowly, this supports a
  separate rendered, interactive user-path pass for visual changes; the skill does not claim that an
  agent's manual pass replaces accessibility expertise or testing with affected users.
