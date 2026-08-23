---
name: managing-development-work
description: Use when handling a software change from request to an approval-ready outcome, including scoping, planning, execution, delegation decisions, scope control, and validation.
---

# Manage development work

Choose the shortest safe path to the requested outcome. More agents, more files, more architecture,
and more process are costs to justify, not signs of thoroughness.

## Define the outcome before the workflow

Write one completion contract from the request:

- the behavior or artifact the owner wants;
- the observable evidence that will prove it;
- explicit constraints, exclusions, and preserved behavior;
- authority already granted and actions that need later approval; and
- material unknowns that could change scope, behavior, risk, cost, or reversibility.

Inspect repository rules, workspace state, and the smallest relevant implementation surface. Ask only
for a decision that cannot be safely discovered or reasonably inferred. A request to investigate,
plan, or advise does not authorize implementation, external delivery, or an adjacent fix.

## Choose the smallest engagement mode

Classify from observed boundaries, not from how ambitious the solution sounds.

### Direct

Use direct work for a localized documentation, copy, metadata, configuration, or similarly mechanical
change when the current owner has the skill and authority to complete and verify it safely. Keep a
short checklist in the current turn. Do not create a standalone plan or delegate it merely to follow
a workflow.

### Bounded implementation

Use one implementer for an ordinary code change with one coherent outcome, a known design boundary,
and focused proof. The owner may implement directly when it is their responsibility and capability;
otherwise give one matching development specialist the bounded assignment. The specialist follows
its own agent instructions and the exact handoff; it does not restart this management workflow.

As a default scope signal, pause before implementation if the expected change exceeds three
production files or 150 production lines, introduces a service or architectural layer, changes a
public contract, or requires a refactor to make the feature possible. These are review triggers, not
targets and not permission to fill a budget. Repository-specific stricter limits win.

### Planned delivery

Use a written plan when the accepted outcome has three or more dependent steps, crosses meaningful
component boundaries, needs staged compatibility or recovery, will be handed across agents, or
cannot be safely held in one working checklist. Apply `writing-plans`; keep each task coherent and
testable, and stop decomposition when the complete requested outcome is covered.

### Discovery before commitment

Use a read-only discovery specialist—such as a Scout—only when a sizable or unfamiliar codebase has
an unknown that materially changes the approach, scope, or risk. Give it the exact question,
inspection boundary, evidence to return, and decision the result will unlock. The owner synthesizes
the finding into the plan before an implementer—such as Forge—receives work.

Do not use discovery to restate an already understood request, and do not pass an unchecked scout
report directly to implementation. If inspection by the owner is cheaper than the handoff and
review, inspect directly.

## Increase ceremony only for observed risk

Risk changes the workflow and proof, not the requested product scope. Name the trigger and response:

- authentication, authorization, secrets, or privacy: trace trust boundaries and refusal paths;
- money, entitlements, or irreversible business state: preserve invariants and reconciliation;
- schema, migration, deletion, or persisted-state changes: define compatibility, recovery, and
  post-change checks;
- production, infrastructure, or deployment: separate implementation from rollout authority and
  define rollback and health proof;
- public APIs, formats, or integrations: identify consumers and compatibility evidence; and
- concurrency, performance, or broad blast radius: characterize the baseline and prove relevant
  limits under representative conditions.

Add an independent reviewer or QA specialist only when repository policy, owner direction, or a
named risk benefits from independent judgment. Assign the risk lens and evidence explicitly. Do not
route every ordinary change through research, implementation, review, and QA agents by default.

## Hold the scope boundary

Before approving a plan or handoff, apply this gate:

1. Does every proposed production change directly deliver the requested outcome or its necessary
   proof?
2. Can an existing boundary solve it without a new abstraction, service, generalized framework, or
   rewrite?
3. Are cleanup, modernization, deployment, and adjacent defects excluded unless explicitly
   requested or strictly necessary?
4. Is the change still inside the accepted size, risk, compatibility, and authority boundary?

If any answer fails, reduce the approach. If a materially larger boundary is genuinely necessary,
stop before implementation and ask the owner to approve the expanded outcome and impact. Explain
the smallest viable boundary, why the original boundary cannot work, expected size, risks,
alternatives, and proof. Passing tests never authorizes more scope.

Never infer a refactor from a feature or bug request. When a refactor is explicitly requested or
proved necessary, characterize preserved behavior first, split the work into reversible increments,
and avoid combining unrelated feature, cleanup, or deployment work.

When implementation reveals a new dependency, consumer, risk, or necessary file outside the
accepted boundary, freeze the affected work. Preserve valid local evidence, distinguish a mistaken
estimate from a changed outcome, and update the completion contract and downstream proof. Continue
without new approval only when the discovery remains inside the accepted outcome, risk, authority,
and scope signals. Otherwise present the expansion gate again; do not let sunk effort decide scope.

## Build the execution contract

For work that leaves the owner, apply `delegating-work` and send one bounded outcome with:

- exact included and excluded behavior;
- files or component ownership when known;
- the accepted size budget and stop conditions;
- applicable repository and specialist guidance;
- required implementation, test, and user-path evidence; and
- authority limited to local artifacts—no issue, push, pull request, merge, tag, release, publish,
  deploy, or other external delivery.

Use one implementation owner by default. Split or parallelize only independent workstreams whose
coordination cost is lower than sequential execution and whose edit boundaries do not overlap. Keep
architecture decisions, dependency order, integration, approval, and final communication with the
primary owner.

Do not grant this orchestration workflow to inbound-only development specialists merely because
they write code. Keep their shortest-path execution, testing, stop conditions, and local-artifact
return contract in their agent instructions so an accepted assignment starts with implementation
instead of another management cycle.

## Review the return, not the summary

When implementation returns:

1. Inspect the actual workspace, complete diff, changed-file count, production-line delta, and
   relevant surrounding contracts.
2. Compare every change with the completion contract and remove or reject unrelated work,
   speculative abstractions, unrequested refactors, and unnecessary dependencies.
3. Inspect the reported commands and outputs; rerun the narrowest meaningful checks on the
   integrated artifact and then the repository-required gate.
4. Exercise the affected user or system path when behavior is observable through a safe local or
   test surface. Add failure, boundary, recovery, compatibility, or rollout proof only where the
   accepted risk requires it.
5. Allow one bounded correction pass for a focused miss. If correction reveals a different design,
   larger boundary, or repeated scope failure, stop and re-scope instead of layering fixes.

A delegated answer is evidence to inspect, not completion. `Complete` means the accepted behavior,
scope, and proof all match the integrated artifact. Say `validation incomplete` or `blocked` when a
required surface or decision is unavailable.

## Prepare external delivery separately

Do not require an issue, project entry, branch, commit, or pull-request draft merely as workflow
ceremony. Create or prepare one only when the owner requests it, repository policy requires it, or
it is the smallest durable artifact needed for the accepted work. Its existence never expands the
outcome or grants GitHub authority.

Before any pull request, give the owner a compact checkpoint:

```text
Outcome: <what changed>
Scope: <production files and approximate production-line delta>
Risk: <named triggers and mitigations, or none material>
Proof: <observed checks and user-path result>
Excluded: <adjacent work intentionally left out>
```

Obtain explicit owner approval for that exact pull-request outcome and scope. The primary agent then
applies `managing-github` and owns the issue or pull request, branch push, checks, review responses,
and any separately authorized merge or release. An implementation specialist returns local artifacts
and evidence; it never performs GitHub delivery for the primary.

The evidence behind small changes, explicit risk, bounded delegation, and observed completion is
mapped in [references/sources.md](references/sources.md).
