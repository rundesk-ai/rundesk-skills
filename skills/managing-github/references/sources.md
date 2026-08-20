# Sources

## GitHub repository templates

- [Using templates to encourage useful issues and pull requests](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests)
  establishes that repository maintainers can supply issue and pull-request templates to improve
  contributor submissions.
- [Configuring issue templates for your repository](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository)
  establishes the default-branch locations, Markdown/YAML forms, chooser configuration, and when a
  repository's issue templates become available.

## GitHub CLI contracts

- [`gh issue create`](https://cli.github.com/manual/gh_issue_create) establishes `--body-file`,
  `--template`, and existing issue-type selection.
- [`gh pr create`](https://cli.github.com/manual/gh_pr_create) establishes `--body-file`, explicit
  base/head selection, user-owned fork qualification, and issue-closing references in the PR body.
- [`gh release create`](https://cli.github.com/manual/gh_release_create) establishes annotated-tag
  use, `--verify-tag`, generated notes, drafts, and the no-new-commits guard.

## Reproduced command surface

On 2026-08-18, `gh` 2.95.0 help output was checked locally for every command shown by this package.
It confirmed the issue and PR body/template flags, PR user-qualified head behavior, and the release
draft, notes-file, generated-notes, no-new-commits, and tag-verification flags. This is command-surface
proof only; repository rules and the stored GitHub object remain authoritative for each operation.

## Deployment branch reconciliation

- [Creating a pull request](https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/creating-a-pull-request)
  establishes that the base branch receives the changes from the head branch and documents explicit
  `--base` and `--head` selection.
- [Managing a branch protection rule](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule)
  establishes that a protected branch can require pull requests, reviews, and passing status checks.
- An anonymized first-hand operating requirement recorded on 2026-08-20 establishes the scoped
  catalog conclusion: production branches used for live website deployments must be reconciled into
  `main`, while product releases originate from `main` or an intentional isolated version branch.

## Review readability and accountable identity

- An anonymized first-hand operating requirement recorded on 2026-08-20 establishes that pull
  request bodies must be concise review maps rather than implementation or test transcripts, must
  use the responsible agent's display-name sign, and must omit provider, model, tool, vendor, and
  generated-by branding.
