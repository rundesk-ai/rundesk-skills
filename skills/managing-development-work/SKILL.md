---
name: managing-development-work
description: Use when planning or delivering a software change from request through verified completion, including features, bug fixes, refactors, configuration, and repository documentation.
---

# Manage development work

Choose the shortest safe path to the requested outcome. More agents, more files, more architecture,
and more process are costs to justify, not signs of thoroughness.

## Define the outcome before the workflow

Write one completion contract from the request:

- the requested behavior or artifact;
- the observable evidence that will prove it;
- explicit constraints, exclusions, and preserved behavior;
- authority already granted and actions that need later approval; and
- material unknowns that could change scope, behavior, risk, cost, or reversibility.

Inspect repository rules, workspace state, and the smallest relevant implementation surface. Ask
only for a decision that cannot be safely discovered or reasonably inferred. A request to investigate,
plan, or advise does not authorize implementation, external delivery, or an adjacent fix.

## Choose the smallest engagement mode

Classify from observed boundaries, not from how ambitious the solution sounds.

Work already scoped into an assignment you accepted is not reclassified here; execute it under that
assignment.

### Direct

Use direct work for a localized documentation, copy, metadata, configuration, or contained code
change, including a one-line fix with a confirmed cause. Keep a short checklist in the current turn.
For code, keep direct work to one file with a confirmed cause and no design choice. Do not create a
standalone plan or delegate merely to follow a workflow.

### Bounded implementation

Use one implementer for an ordinary code change with one coherent outcome, a known design boundary,
and focused proof. The responsible agent may implement directly when it has the capability;
otherwise give one matching development specialist the bounded assignment. The specialist follows
its own agent instructions and the exact handoff.

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

Use a read-only discovery specialist only when a sizable or unfamiliar codebase has an unknown that
materially changes the approach, scope, or risk. Give it the exact question, inspection boundary,
evidence to return, and decision the result will unlock. The responsible agent synthesizes the
finding into the plan before an implementer receives work.

Bound discovery to the smallest evidence set that resolves the unknown. Start at the nearest known
entry point and expand only when evidence shows another affected boundary. Stop when the unknown is
resolved—for persisted state, when the authoritative write path and its actual consumers are
identified—or an architecture decision is proved necessary. Do not create a component inventory or
matrix merely because the system is large. If direct inspection is cheaper than the handoff and
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

Add an independent reviewer or QA specialist only when repository policy, requester direction, or a
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
stop before implementation and ask the requester to approve the expanded outcome and impact. Explain
the smallest viable boundary, why the original boundary cannot work, expected size, risks,
alternatives, and proof. Passing tests never authorizes more scope.

Never infer a refactor from a feature or bug request. When a refactor is explicitly requested or
proved necessary, characterize preserved behavior first, split the work into reversible increments,
and avoid combining unrelated feature, cleanup, or deployment work.

When implementation reveals a new dependency, consumer, risk, or necessary file outside the
accepted boundary, freeze the affected work and preserve valid local evidence. A mistaken estimate
updates the size budget; a changed outcome reopens the completion contract. Continue without new
approval only when the discovery remains inside the accepted outcome, risk, authority, and scope
signals. Otherwise present the expansion gate again; do not let sunk effort decide scope.

## Build the execution contract

For delegated work, apply `delegating-work`. Add the accepted size budget and stop conditions plus
the required implementation, test, and user-path evidence to its delegation brief.

Use one implementer by default. Split or parallelize only independent workstreams whose
coordination cost is lower than sequential execution and whose edit boundaries do not overlap. Keep
architecture decisions, dependency order, integration, approval, and final communication with the
responsible agent.

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
scope, and proof all match the integrated artifact. Say `Continue` and name the missing check, or
say `Blocked`, when a required surface or decision is unavailable.

## Prepare external delivery separately

Do not require an issue, project entry, branch, commit, or pull-request draft merely as workflow
ceremony. Create or prepare one only when the requester asks for it, repository policy requires it,
or it is the smallest durable artifact needed for the accepted work. Its existence never expands
the outcome or grants GitHub authority.

Before any pull request, give the requester a compact checkpoint:

```text
Outcome: <what changed>
Scope: <production files and approximate production-line delta>
Risk: <named triggers and mitigations, or none material>
Proof: <observed checks and user-path result>
Excluded: <adjacent work intentionally left out>
```

Obtain explicit requester approval for that exact pull-request outcome and scope. The responsible
agent then applies `managing-github` and retains external delivery; an implementation specialist
returns only local artifacts and evidence.

Read [references/sources.md](references/sources.md) when challenging a threshold, risk trigger, or
ownership boundary in this workflow.
