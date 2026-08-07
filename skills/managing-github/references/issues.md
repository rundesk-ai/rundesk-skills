# GitHub issues

## Discover the tracker contract

Confirm that issues are enabled:

```sh
gh repo view --repo <owner/repo> --json hasIssuesEnabled
```

If disabled, follow the repository's support or discussion route when authorized, or return a
draft. Read applicable `AGENTS.md`, `CONTRIBUTING.md`, `.github/ISSUE_TEMPLATE/`, and
`SECURITY.md`. Inspect every Markdown template and YAML issue form on the default branch. Select
the template whose stated purpose matches the report; preserve its required headings, field
order, checkboxes, and footer. Remove comments and placeholders. Never mark an unproven claim or
check complete.

For YAML forms, map each required `body` entry to a rendered heading and substantive answer.
Inspect available labels and issue types before naming either:

```sh
gh label list --repo <owner/repo> --limit 100
gh api -H 'X-GitHub-Api-Version: 2026-03-10' \
  repos/<owner>/<repo>/issue-types --jq '.[].name'
```

Do not invent a label or type. A 404 means issue types are unavailable; authentication,
permission, and other failures remain blockers.

## Route and investigate

Confirm the behavior belongs to this repository, not a dependency, integration, configuration,
or caller. Separate **observed** behavior, **expected** behavior, and **inferred** mechanisms. A
source trace is evidence, not a reproduction; state when the report is inspection-only.

Potential vulnerabilities, credentials, and exploitable paths belong in the repository's
`SECURITY.md` route or GitHub private vulnerability reporting, never a public issue.

Search open and closed issues with the symptom, exact error, component, and a plain-language
variant:

```sh
gh issue list --repo <owner/repo> --state all --search '<distinctive terms>' --limit 100
```

Read plausible matches. When one covers the same underlying problem, add only new evidence when
authorized. Do not create a duplicate merely because the existing issue is closed.

## Write a checkable issue

Keep one independently closable problem per issue. Lead with impact and current behavior, not a
preferred implementation. Use the repository template when one applies. Otherwise use the
smallest suitable fallback.

Bug:

```md
## What happened
<Who is affected, what failed, and the consequence.>

## Reproduce
<Smallest exact setup and ordered actions.>

**Expected:** <documented or intended result>
**Actual:** <observed result, trimmed to the failure>

## Environment
- version or commit: <value>
- operating system/runtime: <only relevant details>

## Evidence
- <fresh result, source location, regression range, or sanitized excerpt>

## Acceptance criteria
- [ ] <observable condition distinguishing fixed from unfixed>
```

Feature or scoped work:

```md
## Need
<Who needs what, and what is impossible or costly today.>

## Evidence
- <request, example, measurement, or current limitation>

## Scope
- <bounded capability or outcome>

## Out of scope
- <nearest tempting expansion>

## Acceptance criteria
- [ ] <observable completion condition>
```

Put optional implementation ideas under **Possible approach** so the issue survives a design
change. Apply the shared public-data hygiene before filing.

## Apply and verify

Compare the final body with the selected template line by line. Write it to a Markdown file so
shell quoting cannot alter it:

```sh
gh issue create --repo <owner/repo> \
  --title '<concise, specific title>' \
  --body-file <issue-body.md> \
  [--type '<existing type>'] \
  [--label '<existing label>']
```

For edits, inspect the current issue before changing only the requested fields with
`gh issue edit`. Then prove the stored result:

```sh
gh issue view <number> --repo <owner/repo> \
  --json url,title,body,labels,issueType,state
```

Recheck template compliance, report the URL, and distinguish drafts from filed or edited issues.
