---
name: managing-github
description: Use when asked to prepare, create, edit, inspect, or verify GitHub issues, pull requests, or releases, or to reconcile a production deployment branch into its canonical branch. It provides guarded GitHub CLI and release workflows that honor repository rules, limit external changes to authorized actions, and prove stored results. Do not use it for local Git work, GitHub Actions, or repository administration.
---

# Manage GitHub

Use one shared safety contract, then load only the reference for the requested operation.

## Shared contract

GitHub mutations affect other people. Inspect freely, but create, edit, push, tag, publish, or
request review only when the owner requested that action. A specific request is authorization;
otherwise prepare a draft or plan and stop before changing GitHub.

The primary or domain agent responsible for the outcome owns every GitHub write. Never delegate
issue or pull-request creation, editing, submission, or follow-up to a named specialist, even when
that specialist prepared the implementation or investigation. The specialist returns local
artifacts and evidence, such as the branch, commit, diff, issue draft, PR draft, and verification.
The responsible agent loads this skill, re-establishes the account and repository itself, performs
the authorized GitHub action, and proves the stored result. If you are acting as the named
specialist, stop at the handback instead of using a GitHub mutation command.

Establish the active account, repository, default branch, remotes, branch, and worktree:

```sh
gh auth status --active
gh repo view --json nameWithOwner,url,defaultBranchRef
git remote -v
git branch --show-current
git status --short --branch
```

When the owner names a repository, pass `--repo <owner/repo>` to every `gh` command. Never infer
a target from a nearby directory, an issue or PR number alone, or a remembered remote. Do not
silently switch accounts, hosts, repositories, forks, remotes, or branches.

Read the repository instructions named by the operation reference. Repository rules and
templates override these fallbacks. For issues and pull requests, inspect the target repository's
templates on its default branch before drafting. When one applies, its structure, field order, and
required prompts take precedence; keep this skill's standards for evidence, verification, privacy,
and checkable claims within that structure. Use the bundled fallback only when no repository
template applies. Never force fallback headings into a repository template merely to make projects
look identical.

Before sending public text, remove credentials, private URLs, customer data, private conversations,
internal hostnames, personal identifiers, and unrelated logs. Use placeholders and retain only
evidence needed for the task.

After every mutation, read the stored object back from GitHub and compare its identity, content,
and state with the request. A successful exit status is not proof that the intended result was
stored. If `gh` is missing, unauthenticated, or unauthorized, stop with the prepared content and
exact blocker; do not use a different account or publication route.

## Choose the operation

- [Issues](references/issues.md): draft, file, edit, or triage an issue; search duplicates;
  select templates, labels, issue types, and security routes.
- [Pull requests](references/pull-requests.md): prepare, open, edit, or inspect a PR; select its
  base and head, explain the diff, link issues, and verify checks.
- [Releases](references/releases.md): follow the repository's release workflow; choose its version
  and tag or the fallback SemVer convention; prepare, publish, verify, or recover a GitHub Release;
  and reconcile a live deployment branch into its canonical branch.

Read multiple references only when the request genuinely spans those operations.

Read [references/sources.md](references/sources.md) when auditing or changing these GitHub workflow
rules.
