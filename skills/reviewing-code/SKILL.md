---
name: reviewing-code
description: Use this skill when asked to review a code change—whether a diff, commit, branch, pull request, file set, or completed implementation—for defects, regressions, security, maintainability, performance, or repository-rule violations. It provides a language-agnostic process for establishing intended behavior, inspecting the full change and its context, validating material risks, and reporting prioritized, evidence-backed findings with a readiness verdict. Do not use it merely to explain code or write a pull request.
---

# Review code

Judge the change against its intended behavior and the repository's standards, not personal
preference. Seek material problems; perfection is not the bar.

Treat review as read-only unless the user also asks for fixes. Do not post comments, approve a
change, or request changes in an external system without explicit authorization.

## Establish the review contract

1. Read every applicable repository instruction, contribution guide, design note, and acceptance
   criterion.
2. Identify the exact change, its intended outcome, and the base it should be compared with. State
   any assumption that could alter the verdict.
3. Inspect repository status before judging a diff. Include staged, unstaged, and relevant untracked
   files when reviewing local work.
4. Bound the review. If any file, generated output, dependency, or risk area is excluded, say so;
   never imply exhaustive coverage after sampling.

For Git work, choose the comparison that matches the request:

```sh
git status --short
git diff --stat
git diff
git diff --cached
git diff <base>...<head>
git show <commit>
```

Do not assume the default branch or use a working-tree diff when the request names a commit, range,
or pull request.

## Understand before judging

Review in this order:

1. Read the task, issue, change summary, and commit history to learn why the change exists.
2. Scan the complete diff for shape, boundaries, unexpected files, and high-risk areas.
3. Inspect the primary entry points and design before line-level details.
4. Trace changed behavior through callers, callees, data models, interfaces, configuration, and
   failure paths. Read unchanged context where the contract lives.
5. Inspect every changed human-authored line, then the relevant proof, documentation, migrations,
   and operational changes.

A diff shows what moved, not whether the system still works. Search the repository for uses of
changed names, interfaces, schemas, flags, and assumptions before filing a finding.

## Evaluate quality by risk

Prioritize these lenses:

1. **Correctness and data integrity:** Does reachable behavior satisfy the requirement across valid,
   empty, boundary, repeated, and partial-failure cases? Can state be lost, duplicated, corrupted,
   or reported inaccurately?
2. **Security and privacy:** Are trust boundaries, authorization, validation, secrets, sensitive
   data, and command or query construction handled safely?
3. **Design and integration:** Does responsibility live in the right layer? Do callers and consumers
   still honor the changed contract? Is the solution consistent with nearby architecture?
4. **Failure and concurrency:** Are errors observable and recoverable? Consider retries, ordering,
   cancellation, timeouts, atomicity, races, and cleanup where the system makes them relevant.
5. **Compatibility and rollout:** Can APIs, stored data, configuration, migrations, and mixed
   versions move forward safely? Is rollback or partial deployment hazardous?
6. **Proof:** Do existing checks exercise the behavior that changed, including meaningful failure
   paths? Never infer correctness solely from a green suite.
7. **Maintainability:** Is the code understandable at the repository's normal level of abstraction?
   Flag duplication or complexity only when it creates a concrete cost or defect risk.
8. **Performance and operations:** Flag measurable or structurally clear impact, not hypothetical
   micro-optimization. Check logging, diagnosis, resource bounds, and user-facing documentation when
   the change affects them.

Apply repository rules as authoritative. Treat style as a finding only when it violates those rules,
obscures behavior, or creates material maintenance risk.

Validate proportionally. When permitted, use the smallest repository-prescribed check or focused
reproduction that can confirm a material concern. During a review-only request, do not change code
or add proof. Separate observed results from inference and state which relevant checks were not run.

## Prove each finding

Before reporting a problem:

- identify the smallest useful file and line location;
- name the input, state, or sequence that reaches it;
- trace the resulting behavior and concrete impact;
- confirm nearby code, callers, and existing safeguards do not resolve it; and
- give the smallest practical correction direction without redesigning the change.

Do not report speculation, generic advice, duplicate symptoms of one cause, or unrelated pre-existing
problems. If evidence is incomplete, ask a focused question or mark the concern as unverified rather
than presenting it as a defect.

Use severity consistently:

- **Blocking:** likely security, data-loss, outage, or fundamental correctness failure that must be
  resolved before the change proceeds.
- **Important:** reachable regression, contract break, or substantial maintenance or operational
  risk that should be resolved.
- **Optional:** worthwhile improvement that does not affect readiness. Keep these few and clearly
  separate from defects.

## Report the decision

Put findings first, ordered by severity and then impact. For each finding include:

```text
[severity] Concise title — path/to/file:line
Trigger and observed behavior. Explain the impact and the correction direction.
```

Then state only the assumptions or unanswered questions that affect the decision. End with one
verdict:

- **Ready:** no material finding blocks the stated change.
- **Changes requested:** list the findings that prevent readiness.
- **Cannot conclude:** name the missing context or excluded risk that prevents a defensible verdict.

If there are no findings, say `No material findings` and identify any material area not validated.
Do not claim the code is correct merely because the review found no defect.
