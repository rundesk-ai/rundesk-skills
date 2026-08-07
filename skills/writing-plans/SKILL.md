---
name: writing-plans
description: Use when work needs an executable implementation plan, especially for dependent steps, cross-component changes, risky operations, handoffs, or later continuation. It supplies a provider-neutral workflow for grounding decisions, ordering coherent tasks, respecting authority, and defining observable proof. Do not use it for a small local edit whose intent and verification fit in the response.
---

# Writing plans

Write a contract a capable worker can execute with repository access and no conversation history.

## Decide scope and destination

Plan three or more dependent steps, multiple components or owners, risky transitions, or a handoff.
Split only when each outcome can leave a working, testable state; keep shared constraints together.

Choose the destination in this order:

1. Use the path the user names.
2. Follow an existing repository convention found in its rules or documentation.
3. Use an established workspace or document area available to the user.
4. Otherwise, return the complete plan in the response.

Do not invent a provider home, storage directory, or repository convention. For an otherwise
unnamed standalone plan, use `YYYY-MM-DD-<short-topic>.md`; a project convention wins.

## Ground the plan

Read the request, repository rules, implementation, tests, interfaces, migrations, and relevant
documentation. Search before proposing structure. Confirm every path, symbol, command, and tool;
never present model recall as repository fact.

Map each requirement to its owning component. For each architectural decision, record the choice,
material alternative, and repository-specific reason. Ask about unresolved choices that change
scope, behavior, data, cost, or authority; choose and state ordinary implementation details.

Label assumptions and their confirmation. If execution must discover a fact, make discovery the
first task and give the decision rule for each result. `TBD` is not a decision rule.

## Write the execution contract

Start with:

```markdown
# <Outcome> implementation plan

**Goal:** <completed behavior>
**Approach:** <design choice and why it fits this repository>
**Constraints:** <compatibility, safety, ownership, and authorization boundaries>
**Proof:** <observable checks for the complete outcome>
```

Order numbered tasks by dependency. Each must leave a coherent state and contain:

```markdown
## 1. <Testable outcome>

**Files:**
- Modify: `confirmed/path`
- Test: `confirmed/test/path`

**Change:** <behavior, interfaces, data flow, edge cases, and preserved behavior>

**Verify:** <confirmed command or observable check> — expect <specific observable result>
```

Name created, modified, and tested files. Include signatures or data shapes only when downstream
work depends on them. Use code only to resolve ambiguity; a plan is not a speculative patch.

Keep implementation and proof together. Split at independently reviewable outcomes, not file
counts. Keep setup, configuration, and documentation with the outcome they enable. Put prerequisite
interfaces or characterization tests before consumers or refactors. Make every task self-contained;
never write “same as above” when a worker may receive only that task.

```text
Good: characterize existing behavior, verify it, then refactor and rerun the targeted and required
      suites in a separate coherent task.
Bad:  "Refactor the component and add tests." This hides order, preserved behavior, and proof.

Good: `<confirmed command>` — expect rejected input, an unchanged valid path, and a passing required
      regression suite.
Bad:  "Run tests." A command without an expected observation does not prove the requirement.
```

These patterns follow the small-change and behavior-verification evidence mapped in
[references/sources.md](references/sources.md).

## Maintain execution state

When the plan drives implementation, use the tracker's status fields when available: `pending`,
`in progress`, and `completed`, or their local equivalents. Keep the current task explicit and mark
it complete only after its `Verify` result is observed. Do not turn task status into a progress
diary.

If confirmed facts invalidate the approach, revise affected decisions and downstream tasks before
continuing. Do not silently follow or diverge from a stale plan.

## Preserve authority and handoff quality

Exclude commits, pushes, deployments, destructive operations, account changes, purchases, and
messages unless authorized. If authorized, name who may act, the approval checkpoint, recovery path
where relevant, and post-action proof. A plan does not grant permission.

Before delivery:

1. Trace every requirement to a task and remove unrequested work.
2. Recheck paths, symbols, commands, terminology, interfaces, and dependency order.
3. Replace vague verbs (`handle`, `update`, `test`) with cases and expected results.
4. Confirm each task preserves existing work and stays inside the granted authority.
5. Report the destination, outcome, decisions, open choices, and first executable task.

Do not start implementation unless the request also authorizes it.
