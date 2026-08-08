# Sources

Checked 2026-08-08. These sources establish the coordination and completion failures addressed by
`SKILL.md`; they do not prescribe a Rundesk directory or this exact Markdown format.

- Ken Schwaber and Jeff Sutherland's [2020 Scrum Guide](https://scrumguides.org/scrum-guide.html)
  describes the Sprint Backlog as a current, actionable picture updated as work is learned, names the
  Product Backlog as the single source of work, and requires work to meet the Definition of Done
  before it is considered part of an increment. Applied here, a brief stays subordinate to canonical
  work, records current state rather than history, and cannot close before its done criteria pass.
- NASA's [SWE-034 acceptance-criteria guidance](https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695413/SWE-034+-+Acceptance+Criteria)
  recommends lightweight criteria for small work while linking requirements, validation methods,
  status, and observed evidence. NASA's
  [traceability-completion risk](https://swehb.nasa.gov/spaces/SITE/pages/215777594/R053+-+Traceability+Completion)
  connects missing requirement-to-implementation-to-verification links with scope gaps and late
  rework. This supports the brief's compact requirement, definition-of-done, and evidence sections.
- Anthropic's June 13, 2025 engineering report,
  [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system),
  reports that workers need an objective, output format, tool or source guidance, and clear task
  boundaries; vague handoffs produced duplicated work and gaps. This supports deriving bounded
  delegation assignments from the lead brief without making another agent read the lead's home.
