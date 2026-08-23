# Sources

## GitHub repository templates

- [Using templates to encourage useful issues and pull requests](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests)
  establishes that repository maintainers can supply issue and pull-request templates to improve
  contributor submissions.
- [Configuring issue templates for your repository](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository)
  establishes the default-branch locations, Markdown/YAML forms, chooser configuration, and when a
  repository's issue templates become available.
- [Managing and standardizing pull requests](https://docs.github.com/en/pull-requests/reference/managing-and-standardizing-pull-requests)
  establishes that pull-request templates can prompt for purpose, linked issues, testing notes,
  and review checklists. This catalog concludes that a fallback should request those decisions in
  review language without forcing empty sections.
- An anonymized first-hand operating requirement recorded on 2026-08-23 establishes the template
  precedence rule: use an applicable template from the target repository before the skill's
  fallback, while preserving consistent evidence, verification, privacy, and checkable-claim
  standards across repositories.
- A provider-diverse live forward test recorded on 2026-08-23 found that an agent preserved a YAML
  issue form but marked its required Code of Conduct attestation complete without user confirmation.
  This establishes the scoped guard that drafting or filing intent is not proof of agreement; the
  attestation stays unchecked until the user explicitly confirms it.

## Issue and pull-request writing

- An anonymized first-hand operating requirement recorded on 2026-08-22 establishes the scoped
  ownership boundary that issue and pull-request writes stay with the primary or domain agent using
  this guarded workflow. Named specialists return local artifacts and evidence instead of creating,
  editing, submitting, or following up on GitHub issues or pull requests.

- Benjamin C. Haller's 2022 peer-reviewed practitioner article,
  [Ten simple rules for reporting a bug](https://pmc.ncbi.nlm.nih.gov/articles/PMC9562159/), draws
  on more than 40 years of software-development experience. It recommends the correct reporting
  channel and template, a detailed problem and expected result, a minimal reproducible example,
  relevant environment and output, and concise presentation. It is practitioner guidance rather
  than a controlled comparison; this package uses it to shape the bug-report checklist, not to
  claim a measured effect size.
- Google's Engineering Practices guide,
  [Writing good CL descriptions](https://google.github.io/eng-practices/review/developer/cl-descriptions.html),
  establishes that a change description should explain what changed and why, preserve context and
  decisions the code cannot show, disclose shortcomings, and remain useful as history. This
  package maps that judgment to the problem, proposed-solution, evidence, and boundary sections of
  a professional pull-request merge case.
- An anonymized first-hand operating requirement recorded on 2026-08-22 reports that generic
  headings such as "Need" and "What we need," repeated request text, and implementation-only PR
  bodies produce unprofessional review artifacts. It requires issue and PR writing to present the
  problem, proposed solution, evidence, and acceptance conditions. This package treats that as a
  scoped quality standard, not a universal GitHub contract.

## GitHub CLI contracts

- [`gh issue create`](https://cli.github.com/manual/gh_issue_create) establishes `--body-file`,
  `--template`, and existing issue-type selection.
- [`gh pr create`](https://cli.github.com/manual/gh_pr_create) establishes `--body-file`, explicit
  base/head selection, user-owned fork qualification, and issue-closing references in the PR body.
- [`gh release create`](https://cli.github.com/manual/gh_release_create) establishes caller-selected
  tags and titles, annotated-tag support, prereleases, `--verify-tag`, generated notes, drafts, and
  the no-new-commits guard. This catalog therefore treats a strict `v`-prefixed stable SemVer tag as
  a fallback rather than a universal GitHub contract.

## Reproduced command surface

On 2026-08-23, `gh` 2.94.0 help output and the live issue-types endpoint were checked locally for
every command shown by this package. They confirmed the issue and PR body/template flags, current
issue-types API version, PR user-qualified head behavior, and the release draft, prerelease,
notes-file, generated-notes, no-new-commits, title, and tag-verification flags. This is
command-surface proof only; repository rules and the stored GitHub object remain authoritative for
each operation.

## Deployment branch reconciliation

- [Creating a pull request](https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/creating-a-pull-request)
  establishes that the base branch receives the changes from the head branch and documents explicit
  `--base` and `--head` selection.
- [Managing a branch protection rule](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule)
  establishes that a protected branch can require pull requests, reviews, and passing status checks.
- An anonymized first-hand operating requirement recorded on 2026-08-20 establishes the scoped
  catalog conclusion: production branches used for live website deployments must be reconciled into
  `main`, while product releases originate from `main` or an intentional isolated version branch.
- An anonymized first-hand operating requirement recorded on 2026-08-23 establishes that release
  preparation and post-production branch reconciliation belong to the managing-github routing
  contract, and that a live deployment is incomplete until its production-only work returns to the
  canonical branch under repository policy.

## Review readability and accountable identity

- An anonymized first-hand operating requirement recorded on 2026-08-20 establishes that pull
  request bodies must be concise review maps rather than implementation or test transcripts, must
  use the responsible agent's display-name sign, and must omit provider, model, tool, vendor, and
  generated-by branding.
