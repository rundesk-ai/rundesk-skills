---
name: reviewing-code
description: Use when asked to review a diff, change set, commit, branch, merge or pull request, file set, or completed implementation for defects, regressions, security, reliability, maintainability, performance, test gaps, or repository-rule violations. It supplies a language-, platform-, provider-, and version-control-neutral workflow for establishing scope, tracing changed contracts, proving material findings, and issuing a defensible readiness verdict. Do not use merely to explain code or implement fixes.
---

# Review code

Judge the change against intended behavior and repository rules, not personal preference. Seek
material problems; perfection is not the bar.

Treat review as read-only unless the user also asks for fixes. Do not post comments, approve, request
changes, merge, deploy, or mutate an external system without explicit authorization.

## Set the subject and scope

1. Read repository rules, the requirement, and relevant design decisions.
2. Resolve the artifact, intended outcome, and effective base. Ask the review system what it compares;
   do not infer a default branch, revision, or workspace state.
3. Enumerate the scope, including local staged, unstaged, and untracked work when applicable. Check
   hidden or truncated files and generated, dependency, schema, configuration, and documentation
   changes. State exclusions, sampling, and unavailable evidence.

If the repository uses Git, select the command matching the named artifact:

```sh
git status --short
git diff
git diff --cached
git show <commit>
git diff <base>...<head>
```

Use the repository's native comparison otherwise. A precise review of the wrong comparison is still
the wrong review.

## Trace behavior beyond the patch

1. Read the reason, history, and primary entry points; scan the complete change for boundaries,
   surprises, and high-risk operations.
2. Inspect every in-scope human-authored line and enough whole-file context to understand its
   contract.
3. Search changed names, interfaces, schemas, formats, flags, and invariants through callers,
   consumers, persistence, configuration, failure paths, and rollout.
4. Inspect tests, documentation, migrations, generated outputs, and operational changes that prove
   or carry the behavior.

Follow risk: correctness, boundaries, data integrity, trust, authorization, validation, privacy,
concurrency, compatibility, recovery, observability, and resource bounds. Check whether proof exercises
the changed behavior. Flag complexity or performance only for a concrete cost or defect risk.

Apply repository rules as authoritative. Report style only when it violates those rules, obscures
behavior, or creates material maintenance risk.

## Avoid known review traps

These pairs distill the evidence in [references/sources.md](references/sources.md), which should be
read when auditing or revising a rule. Angle brackets below are placeholders, not fabricated defects.

| Bad | Do instead |
|---|---|
| Review the convenient diff. | Name the artifact and effective base first. |
| Inspect changed lines only. | Trace contracts through unchanged callers and consumers. |
| `Green means correct.` | Show the check exercises the change and fails when it breaks. |
| `This might break` or `This looks unsafe.` | Show `<trigger> -> <behavior> -> <impact>` and the missing or bypassed safeguard. |
| Inflate uncertain concerns. | Rank reachable impact; mark uncertainty unverified. |
| Promote preference or analyzer output. | Require policy or a reachable failure. |
| Report each symptom. | Report one root cause and its affected paths. |
| Sample, then declare readiness. | Name scope; use `Cannot conclude` when omissions block judgment. |

## Prove and rank findings

Require **location -> trigger -> behavior -> impact -> missing safeguard**. Confirm callers and tests
do not resolve it and it was introduced by or blocks the change. Ask, mark unverified, or omit when
proof is incomplete. Keep unrelated pre-existing problems out of change findings.

Assign severity from impact:

- **Blocking:** likely compromise, data loss, outage, or fundamental correctness failure; prevents
  readiness.
- **Important:** reachable regression, contract break, or material operational risk; normally
  prevents readiness.
- **Optional:** worthwhile improvement that does not affect readiness. Keep these few and separate.

When permitted, run the smallest prescribed check that tests a material concern. Do not change code
during review-only work. Record commands, discovered counts, skips, and failures; separate observation
from inference. One green suite is never exhaustive.

## Report a defensible decision

Put findings first, ordered by severity and impact:

```text
[severity] Concise title — path/to/file:line
Trigger: <input, state, or sequence>
Impact: <observed behavior and consequence>
Evidence: <trace, check, and missing safeguard>
Direction: <small correction, without redesigning the change>
```

Then list only decision-relevant assumptions, questions, checks not run, or exclusions. End with one
verdict:

- **Ready:** no material finding blocks the fully stated scope.
- **Changes requested:** name the findings that prevent readiness.
- **Cannot conclude:** name the missing context or excluded risk that prevents a defensible verdict.

If there are no findings, say `No material findings` and name any material area not validated. This
means no demonstrated defect was found in scope; it does not prove correctness.
