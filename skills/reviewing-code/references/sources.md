# Code-review source basis

This package synthesizes review practice; it does not copy a provider's review UI or language manual.
Use these sources to audit or revise a rule. Links and claims were checked on **2026-08-07**, except
the naming entry below, which was added and checked on **2026-08-13**.

## Review scope and judgment

- [What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html) —
  Google Engineering Practices says to inspect every assigned human-authored line, read broader file
  and system context, evaluate design and functionality, and verify that tests would fail for broken
  behavior. It also requires reviewers to state when they cover only part of a change. This supports
  the rules against diff-only review, green-suite overconfidence, and sampled-scope overclaim.
- [Navigating a change in review](https://google.github.io/eng-practices/review/reviewer/navigate.html) —
  Google starts with the change's purpose and overall design, then moves through every file without
  omission. This establishes the skill's broad-view-before-lines order.
- [The standard of code review](https://google.github.io/eng-practices/review/reviewer/standard.html) and
  [How to write code-review comments](https://google.github.io/eng-practices/review/reviewer/comments.html) —
  Google favors changes that improve code health without demanding perfection, gives technical facts
  and repository style guides precedence over preference, and labels optional comments so they are
  not mistaken for blockers. Its comment examples explain the concrete cost and preferred direction,
  which supports impact-based severity and actionable findings.
- [What to look for in a code review — Naming](https://google.github.io/eng-practices/review/reviewer/looking-for.html) —
  Google lists naming as a review dimension in its own right: "Did the developer pick good names for
  everything? A good name is long enough to fully communicate what the item is or does, without
  being so long that it becomes hard to read." This is the basis for the trap row on names that pose
  a question or name nothing, and it sets both bounds — a name that communicates nothing and a name
  that has grown into a sentence are the same failure from opposite ends. The reportable threshold
  stays the skill's own: a name is a finding when it hides what a value holds or breaks a repository
  rule, not when a reviewer would have chosen differently. [Avidan and Feitelson, ICPC 2017](https://www.cs.huji.ac.il/~feit/papers/Names17ICPC.pdf)
  supplies the impact — with 9 professional developers over 38 recorded sessions, 3 of 6 production
  methods showed no comprehension difference between their real names and names replaced by
  consecutive letters, "due to poor and even misleading variable names". The naming rule itself, its
  evidence, and its ecosystem conflicts belong to the `database-design` package and are not restated
  here.
- [GitLab code-review guidelines](https://docs.gitlab.com/development/code_review/) — this
  open-source project's practitioner guidance starts with why the change exists, requires the entire
  diff to be read, recommends local validation when appropriate, and distinguishes blocking from
  non-blocking feedback. It corroborates the workflow without making one hosting service mandatory.

## Comparison and context traps

- [Git `diff` documentation](https://git-scm.com/docs/git-diff.html) and
  [GitHub's explanation of branch comparisons](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-comparing-branches-in-pull-requests) —
  the official references distinguish working-tree, staged, direct-endpoint, and merge-base
  comparisons. They establish why a reviewer must resolve the requested artifact and effective base.
  Git is a conditional example in this skill, not a required review system.
- [The code-review checklist for engineering teams](https://sourcegraph.com/blog/code-review-checklist) —
  Matt Tanner, Sourcegraph, 2026. This practitioner guide names the changed-lines blind spot and
  recommends checking call sites, downstream consumers, contracts, configuration, migrations, and
  observability. It supports tracing a patch through unchanged context.

## Security, reliability, and proof

- [NIST SP 800-218, Secure Software Development Framework 1.1](https://doi.org/10.6028/NIST.SP.800-218) —
  PW.7 calls for human review and/or analysis of readable code to find vulnerabilities and verify
  security requirements, then for discovered issues and remediations to be documented and triaged.
  This establishes security as a risk-driven review lens rather than a language-specific checklist.
- [OWASP Secure Code Review Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secure_Code_Review_Cheat_Sheet.html) —
  manual review complements automated analysis by examining business logic, complex security
  mechanisms, and context-specific vulnerabilities. This supports validating analyzer output rather
  than promoting it directly to a finding.
- [Testing for Reliability](https://sre.google/sre-book/testing-reliability/) — Alex Perry and Max
  Luebbe, Google SRE. Passing tests reduce uncertainty but do not prove reliability; production also
  contains rollout, configuration, version, traffic, and monitoring combinations absent from a
  hermetic suite. This supports examining rollout and observability and limiting claims from green
  checks.

## Empirical evidence and catalog conclusions

- [Characteristics of Useful Code Reviews: An Empirical Study at Microsoft](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/bosu2015useful.pdf) —
  Amiangshu Bosu, Michaela Greiler, and Christian Bird, MSR 2015. The mixed-method study interviewed
  seven developers about 145 comments, built and validated a classifier, then analyzed about 1.5
  million comments across five Microsoft projects. Functional and alternate-scenario findings were
  rated useful; false positives and unrelated future work were commonly rated not useful. Useful
  comment density fell as changed-file count grew. The authors caution that all studied projects were
  mature, large-scale Microsoft projects using one tool, so this skill adopts the signal-quality and
  scope lessons without claiming universal effect sizes.

The source set does not directly prescribe this skill's exact report template. The template is the
catalog's synthesis: location plus trigger, impact, evidence, and correction makes each finding
testable and actionable. Grouping symptoms by one root cause is likewise a reporting conclusion, not
an empirical claim; retain separate findings when triggers or corrections differ.

## Excluded source patterns

- Vendor feature pages that describe a review product but offer no transferable review judgment.
- Unsourced severity scales, arbitrary line-count limits, and claims that one check proves readiness.
- Language-specific checklists presented as universal review practice.
