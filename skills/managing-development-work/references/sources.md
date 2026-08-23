# Sources

Checked 2026-08-23. These sources establish the delivery failures and safeguards synthesized in
`SKILL.md`; they do not prescribe named Rundesk roles, fixed file limits, or one universal ceremony.

## Small changes and controlled scope

- Google's [Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html)
  recommends self-contained changes that address one issue, explains that smaller changes are easier
  to review and roll back, and distinguishes a complete small change from splitting required tests
  away from behavior. This supports one-outcome increments and resisting unrelated cleanup; the
  skill's numeric pause signals are local defaults, not Google's rules.
- The [Principles behind the Agile Manifesto](https://agilemanifesto.org/principles) favors
  simplicity—maximizing the amount of work not done—and frequent delivery of working software.
  Applied here, the workflow adds planning, agents, and validation surfaces only when the outcome or
  observed risk requires them.

## Planning, risk, and proof

- NASA's [SWE-013 Software Plans](https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695397/SWE-013+-+Software+Plans)
  says software plans should identify work, commitments, and risks and remain complete, workable,
  consistent, and verifiable as conditions change. This supports executable plans for dependent or
  risky work, decision rules for discovery, and re-scoping when evidence invalidates the approach.
  Its scope is NASA aerospace software assurance; this workflow borrows plan completeness, not that
  assurance level.
- NASA's [SWE-034 Acceptance Criteria](https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695413/SWE-034+-+Acceptance+Criteria)
  recommends documented, measurable criteria that give stakeholders a shared basis for readiness.
  This supports defining observable proof before implementation and refusing to treat a plausible
  report as completion. Its scope is NASA aerospace software assurance; this workflow borrows
  measurable readiness criteria, not that assurance level.

## Delegated work

- Anthropic's engineering report, [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system),
  reports that clear objectives, output formats, tool or source guidance, and task boundaries reduce
  duplication and gaps, while multi-agent coordination consumes substantially more tokens and fits
  poorly when work has many dependencies. This field report supports bounded read-only discovery
  and one implementer by default rather than mandatory multi-agent ceremony; its quantitative
  results are specific to Anthropic's research system.
- NIST [SP 800-218, Secure Software Development Framework 1.1](https://doi.org/10.6028/NIST.SP.800-218)
  calls for risk-based practices, review or analysis, and retained evidence across secure software
  development. Applied here, independent review and additional proof respond to a named risk instead
  of becoming unconditional ceremony.

## Local synthesis

- Three production files and 150 production lines are review triggers chosen for this workflow, not
  empirical universal thresholds. A repository's own limits or a clearly higher-risk boundary wins.
- The six risk triggers and responses are this workflow's taxonomy, generalized from NIST's
  risk-based practice requirement; NIST does not enumerate them.
- Requiring requester approval for scope expansion while the responsible agent integrates returns
  and retains GitHub delivery is an operating boundary for accountable handoffs. The sources support
  small increments, explicit authority, and inspected evidence; they do not name those roles or tools.
