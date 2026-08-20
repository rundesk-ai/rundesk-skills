# GitHub pull requests

## Discover the PR contract

Read applicable `AGENTS.md`, `CONTRIBUTING.md`, pull-request templates, and workflows defining
required checks. Inspect every template on the default branch and select the one matching the
change. Preserve its headings, order, questions, checklists, and footer; remove comments and
placeholders; support every checked item with fresh evidence.

Map the target repository to an explicit `<base-remote>` and the branch destination or fork to
an explicit `<push-remote>`:

```sh
git remote get-url <base-remote>
git remote get-url <push-remote>
```

Resolve the base from repository rules or its default branch. Confirm the current branch is not
the base or an unrelated worktree. If the worktree is dirty, determine whether those changes
belong before continuing; never omit, discard, or rewrite them to make a branch appear ready.

Check for an existing PR from the same branch and owner:

```sh
gh pr list --repo <owner/repo> --state all \
  --head <branch> --json number,state,url,title,headRepositoryOwner
```

`--head` accepts the branch name, not `owner:branch`. Inspect `headRepositoryOwner` before
deciding whether to update an existing PR or create one.

## Inspect the reviewable change

Fetch the selected base and inspect the merge-base range reviewers will see:

```sh
git fetch <base-remote> <base>
git log --oneline <base-remote>/<base>..HEAD
git diff --stat <base-remote>/<base>...HEAD
git diff --check <base-remote>/<base>...HEAD
git diff <base-remote>/<base>...HEAD
```

Confirm one coherent change, no secrets or generated clutter, and no unrelated edits. Follow the
repository's validation commands. Report only results observed in the current session; name each
required check that was not run and why. Never convert an unrun check into a checked box.

## Write the merge case

A PR body is a scan-friendly review map, not an implementation diary, design document, or test
transcript. It explains why the change should merge and what the diff cannot. Use the repository
template when one applies. When none applies, read and complete the
[fallback pull-request template](pull-request-template.md).

Keep the merge case proportionate:

- State the outcome and user or system impact in one or two lines.
- Give the root cause, then three to six high-value implementation bullets covering decisions and
  boundaries. Link to code, contracts, issues, or artifacts instead of pasting algorithms,
  chronology, full matrices, every edge case, or repeated diff details.
- Name only material risk and blast radius. Group exact validation commands with their observed
  results; do not paste complete test lists, mutation catalogs, logs, or CI transcripts.
- Give the shortest representative manual path, normally no more than five steps. Put blockers and
  readiness state where a reviewer can see them immediately.
- Preserve required template headings, questions, and checklists, but remove optional unused
  sections when the repository permits it.

Every PR body must identify the filing agent. Preserve a repository's stricter identity block;
otherwise append exactly:

```md
## Agent

🤖 by <Agent display name>
```

Do not add provider, model, tool, session, vendor link, `Generated with` footer, or provider-style
co-author attribution to the PR body. Agent identity is the relevant review and ownership signal.

Follow the repository's title convention. With none, use a concise imperative title; use
Conventional Commits only when that repository does.

Use one full closing reference per issue the PR completes. A bare `#12` does not close an issue,
and `Closes #12 and #13` closes only the first. GitHub applies closing keywords automatically
only when the PR targets the default branch. Use `Refs` or `Related` for partial work or a staging
base.

## Open, update, and verify

Recheck the base, head, diff, template, and validation immediately before mutation. Use a body
file to preserve Markdown:

```sh
git push -u <push-remote> <branch>
gh pr create --repo <owner/repo> \
  --base <base> \
  --head <branch> \
  --title '<title>' \
  --body-file <pr-body.md> \
  [--draft]
```

For a user-owned fork, use `--head <user>:<branch>`. GitHub CLI does not support an organization
name in that qualified form; stop rather than creating from another repository. For an existing
PR, inspect it before using `gh pr edit`, and change only requested fields. Do not add reviewers,
assignees, projects, labels, or merge settings unless requested or required.

Read the stored PR and current checks:

```sh
gh pr view <number> --repo <owner/repo> \
  --json url,title,body,baseRefName,headRefName,headRepository,headRepositoryOwner,isDraft,closingIssuesReferences
gh pr checks <number> --repo <owner/repo>
```

Verify the base, head, owner, body, agent sign, absence of provider branding, draft state, issue
links, URL, and template compliance. Report the URL and any pending or failing checks; do not claim
readiness from creation alone.
