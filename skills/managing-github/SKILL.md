---
name: managing-github
description: Use this skill when asked to prepare, create, edit, inspect, or verify GitHub issues, pull requests, or releases. It provides guarded GitHub CLI workflows that select the correct account and repository, honor repository rules, limit external changes to authorized actions, and prove stored results. Do not use it for local Git work, GitHub Actions, or repository administration.
---

# Manage GitHub

Use one shared safety contract, then load only the reference for the requested operation.

## Shared contract

GitHub mutations affect other people. Inspect freely, but create, edit, push, tag, publish, or
request review only when the owner requested that action. A specific request is authorization;
otherwise prepare a draft or plan and stop before changing GitHub.

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
templates override these fallbacks. Before sending public text, remove credentials, private
URLs, customer data, private conversations, internal hostnames, personal identifiers, and
unrelated logs. Use placeholders and retain only evidence needed for the task.

After every mutation, read the stored object back from GitHub and compare its identity, content,
and state with the request. A successful exit status is not proof that the intended result was
stored. If `gh` is missing, unauthenticated, or unauthorized, stop with the prepared content and
exact blocker; do not use a different account or publication route.

## Choose the operation

- [Issues](references/issues.md): draft, file, edit, or triage an issue; search duplicates;
  select templates, labels, issue types, and security routes.
- [Pull requests](references/pull-requests.md): prepare, open, edit, or inspect a PR; select its
  base and head, explain the diff, link issues, and verify checks.
- [Releases](references/releases.md): choose a SemVer version; prepare, draft, publish, verify,
  or recover a GitHub Release, its exact tag, notes, and artifacts.

Read multiple references only when the request genuinely spans those operations.
