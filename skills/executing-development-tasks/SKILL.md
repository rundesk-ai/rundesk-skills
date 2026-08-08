---
name: executing-development-tasks
description: Use when implementing, fixing, refactoring, or otherwise carrying a development task from request through verified completion, whether it is a small edit or complex work delegated across agents. It supplies an end-to-end workflow for requirements, task state, planning, delegation, implementation, automated proof, user-path QA, review, and a final definition-of-done audit. Do not use it for planning-only, review-only, diagnosis-only, or test-only requests, nor for research, documentation, or administrative work without authorized production implementation.
---

# Complete development tasks

Own the outcome from request to observed proof. A plausible implementation, a delegated report, or
a green command alone is not completion.

## Establish the completion contract

Before editing:

1. Read the request, repository rules, relevant implementation, tests, interfaces, and current
   workspace state. Preserve existing work and stay inside the user's authority.
2. Restate the requested outcome, constraints, explicit non-goals, and any ambiguity that changes
   behavior, scope, data, cost, or external state. Ask only for a decision that cannot be safely
   discovered or reasonably inferred.
3. Turn each requirement into a checkable item. Record its owner, expected evidence, and state in
   the available tracker or a concise working checklist.
4. Define done before implementation. Include required behavior, automated checks, user-path QA,
   review, documentation or migration work, and repository-specific gates.

Use a compact trace while working:

```text
Requirement | Work item or phase | Proof | State
R1          | <coherent outcome>  | <observable result> | pending
```

Do not create a second project-management artifact when the repository already provides a tracker.
Apply `maintaining-task-briefs` to choose and maintain the lightest useful task record, from a short
working checklist to a disk brief that survives compaction, interruption, later turns, or delegated
work. The trace prevents a polished partial result from hiding a missed requirement; it is not a
progress diary.

## Scale the workflow to the task

- For one coherent local change, keep one short checklist: understand, implement, verify, audit.
  Skip a standalone plan and delegation unless repository rules require them.
- For three or more dependent steps, multiple components, risky transitions, or a later handoff,
  apply the available implementation-planning guidance. Split work into phases only when each phase
  leaves a coherent, testable state.
- For critical-risk work, name the approval, recovery, migration, and post-action checks before the
  risky step. A task list never grants permission to deploy, delete, publish, purchase, message, or
  mutate an external system.

Keep the checklist current. Mark an item complete only after observing its stated proof. When new
evidence changes the approach, revise affected tasks and downstream verification before continuing.

## Route specialist work

Keep this skill as the execution owner; use the applicable specialist skill or repository guidance
for technique:

- use `writing-plans` for a plan artifact and dependency-level execution contract;
- use `maintaining-task-briefs` for your task scope, active state, and resumption needs;
- use `debugging-code` while an incorrect behavior has no proven cause;
- use `testing-code` to choose and construct trustworthy automated proof;
- use `frontend-design` for rendered UI, interaction, responsive, and accessibility inspection;
- use `reviewing-code` for the independent readiness judgment; and
- use the matching language, framework, database, security, or performance guidance for the change.

Do not restate a specialist's full workflow in the task checklist. Record which guidance governs the
work and keep ownership here for integration, completion state, and the final evidence trace. If a
needed specialist is unavailable, follow repository rules and report the missing review or guidance
instead of implying it was applied.

## Delegate bounded work, retain ownership

Use subagents when the environment provides them and a substantial, self-contained workstream
benefits from separate context, specialist judgment, or safe parallelism. Good candidates include
broad repository reading, research, an isolated implementation area, test coverage analysis, and
read-only review.

Keep requirements, architectural decisions, dependency order, integration, task state, and the
final definition-of-done audit in the lead context. Do not delegate a tiny task merely to satisfy a
ceremony, and do not run dependent or overlapping edits in parallel unless the environment isolates
their work.

Brief each worker with:

- the applicable repository rules and confirmed context;
- one outcome and its requirement identifiers;
- read-only or write scope, exact ownership boundaries, and prohibited changes;
- the expected artifact or report; and
- the verification and definition of done for that assignment.

Require workers to distinguish observed evidence from inference and to report changed paths,
commands, results, gaps, and unresolved risks. Inspect their artifacts and integrate their work in
the main context; never mark a requirement complete from the worker's summary alone. If delegation
is unavailable, execute the same work sequentially and report that constraint without implying a
review or parallel pass occurred.

## Execute in coherent phases

For each item or phase:

1. Confirm its inputs, dependencies, preserved behavior, and expected proof.
2. Make the smallest complete change that delivers the item. Keep tests, documentation,
   configuration, migrations, and cleanup with the behavior they enable.
3. Run the narrowest meaningful check and inspect the actual output, exit status, discovery count,
   skips, warnings, and side effects.
4. Reconcile changed interfaces and downstream consumers before starting the next dependent phase.
5. Update task state only after the phase is integrated and its proof is observed.

Do not continue mechanically when a check invalidates the plan. Isolate the cause, correct the
smallest responsible boundary, and rerun the affected checks before proceeding.

## Prove the result through the right surfaces

### Automated proof

Apply `testing-code` and the repository's required commands to select, construct, and validate the
automated evidence. This skill owns attaching the observed result to the requirement trace after
final integration. Reopen the affected work when a required check fails, and withhold completion
when required proof did not run or does not demonstrate the claimed requirement.

### User-path QA

Treat manual QA as a tool-mediated run through the changed system, not a code reread or a prose
prediction. Inspect the available browser, window or app control, screenshot, shell, HTTP client,
database, log, and artifact-rendering tools; use the ones that can exercise and observe the public
boundary. Use safe test data and a scratch or test environment when the real path could alter live
state.

Match the tool run to the product surface:

- For visual or interactive work, open the real page or app with the available browser or window
  tool, perform the affected journey, capture screenshots of the relevant states and viewports, and
  inspect the rendered result against the requirement. Apply `frontend-design` for the detailed
  visual, responsive, interaction, keyboard, and accessibility procedure.
- For an API or backend boundary, start or use the safe local or test service, send representative
  requests through the public endpoint, and inspect status, headers, body, persisted side effects,
  emitted work, and relevant logs. Exercise a material refusal or failure path as well as success.
- For a CLI, installer, migration, or job, invoke the supported command with representative inputs
  and inspect exit status, standard output and error, files or state changed, repetition, and a
  material failure path.
- For a generated document, image, report, or other artifact, open or render the actual output and
  inspect it with the available viewer instead of validating only its source or file existence.

Follow the complete affected journey as a user would, not only the happy-path function. Check the
material normal, empty, error, boundary, and recovery states that the change owns. Record the tool,
environment, input, and observation; retain screenshots or other artifacts when they make the proof
auditable. This skill owns whether the manual pass happened and whether its blocking findings were
resolved; specialist skills own the detailed technique.

Do not call manual QA complete when the required runtime, browser, device, credentials, or service
was unavailable. Report the unvalidated path and its consequence instead of converting absence of
evidence into a pass.

### Independent review

After the implementation stabilizes, apply the repository's required review policy and the smallest
additional risk lenses justified by the change. Give reviewers the requirement, raw change, and
scope; keep them read-only unless fixes are explicitly authorized. Resolve blocking findings, then
rerun affected automated and manual checks. A reviewer report supports the lead's decision; it does
not replace inspection, integration, or proof.

## Audit the definition of done

Before claiming completion:

1. Trace every requirement to the delivered behavior and observed evidence; remove unrequested
   work.
2. Confirm every checklist item and phase is complete, integrated, and reflected in documentation,
   configuration, migrations, and generated artifacts where applicable.
3. Inspect the complete change and workspace state for accidental, unrelated, debug, secret, or
   temporary material. Preserve pre-existing user changes.
4. Confirm required reviewers have no unresolved blocking findings and rerun any checks invalidated
   by review fixes.
5. Repeat the critical user journey after final integration when the task has a user-facing path.
6. Report the outcome, changed artifacts, automated commands and observed results, manual QA and
   observations, review status, and any remaining limitation.

Use precise states:

```text
Complete: every required gate has observed evidence.
Implementation complete, validation incomplete: code exists, but a required proof could not run.
Blocked: an external decision, authority, dependency, or environment prevents further progress.
```

Never compress the second or third state into “done.” The sources behind the completion,
decomposition, delegation, testing, review, and user-evaluation rules are mapped in
[references/sources.md](references/sources.md).
