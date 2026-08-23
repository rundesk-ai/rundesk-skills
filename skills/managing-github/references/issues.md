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
check complete. Treat agreement, policy, search, and other attestation checkboxes as user claims:
mark one complete only when the user explicitly confirmed it. A request to draft or file the issue
is not confirmation; leave the box unchecked and name the required confirmation as a blocker.

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
preferred implementation. Use the repository template when one applies. When none applies, read
[the fallback issue templates](issue-templates.md) and select the bug or change-proposal form.

Write for the person who must decide whether the work is valid and complete. Before filing, confirm
that the body answers these review questions with concrete, non-repeated content:

- **Problem:** What observable behavior or limitation exists, who or what it affects, and what
  consequence makes it worth changing?
- **Proposed solution:** For a change proposal, what outcome should replace the current state and
  where does its boundary stop? For a bug, prefer expected behavior over prescribing an
  implementation.
- **Evidence:** Which reproduction, output, source location, measurement, or documented contract
  supports the claim? Label inspection and inference instead of presenting either as reproduction.
- **Acceptance criteria:** Which independently checkable outcomes distinguish complete from
  incomplete? State observable behavior, not implementation tasks or phrases such as "works as
  expected."
- **Verification:** For a change proposal, which automated checks and representative user path
  will prove those outcomes? Keep proof methods here instead of disguising test commands as
  acceptance criteria.

Do not use headings such as **Need**, **What we need**, **Context**, **Notes**, or **Summary** as a
substitute for a claim. A short issue is good when it is specific; a generic heading followed by a
restatement of the title is not. Remove chronology, advocacy, speculative root causes, and repeated
background that do not help reproduce, decide, or accept the work.

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
