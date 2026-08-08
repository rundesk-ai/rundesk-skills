---
name: maintaining-task-briefs
description: Use when your owner gives you a task, you need to track work on your plate, or the work must stay coherent across compaction, interruption, later turns, or delegation. It supplies a lightweight workflow for scoping and tracking tasks, with durable briefs when needed. Do not use it for a simple informational reply with no work to track, detailed implementation plans, or as a replacement for a canonical project or task system.
---

# Maintain active task briefs

Keep the smallest current record that lets you resume the outcome without rebuilding its scope from
conversation history. A brief is active execution state, not a second task manager or a permanent
work log.

## Choose the lightest useful record

Start this workflow when your owner assigns you an outcome or you need to review the tasks on your
plate. Keep a short working checklist when the work should finish in the current turn. Create a disk
brief when the work is likely to cross a context compaction, interruption, later turn, or delegated
result, or when your owner asks you to track it internally.

Do not create one when:

- the task can finish in the current turn with a short working checklist;
- an existing canonical tracker already preserves the scope, state, next action, and proof needed to
  resume; or
- the artifact would only copy an issue, plan, transcript, or progress history.

When a canonical issue, tracker, PRD, or project document exists, link it and keep only the
execution state you need to resume but the source does not hold. Reconcile changed requirements before
continuing; a stale brief never overrides its source.

## Use the established task area

Use your home's existing `tasks/` area and read its README before writing there. Do not derive a
provider home from memory or invent a storage convention. If the environment provides no established
task area and the user or repository names none, keep the checklist in the current work surface.

Name a new brief `YYYY-MM-DD-<short-topic>.md`, using the date work starts and a concise outcome
slug. If that name already stands for different work, add the smallest numeric suffix that makes it
unique. Maintain one brief per outcome and update it in place.

## Capture the resumption contract

Start with this compact shape and omit a section only when it truly does not apply:

```markdown
# <Outcome>

**Status:** active | waiting | blocked
**Source:** <canonical link, identifier, or direct request>
**Started:** YYYY-MM-DD
**Last checked:** YYYY-MM-DD HH:MM <timezone>

## Goal
## Scope and non-goals
## Authority and constraints
## Requirements and definition of done
## Current phase
## Next action
## Blockers or decisions
## Delegations
## Observed evidence
```

Write current facts, not a narrative. Keep requirements checkable, name the evidence that will prove
done, and distinguish observed results from assumptions. Link a detailed plan rather than copying
it; apply `writing-plans` when dependency-level planning is needed.

## Checkpoint only meaningful changes

Update the brief after a completed phase, changed requirement or decision, delegation handoff or
return, new blocker, or observed proof. Before ending a turn with unfinished work, make the next
action executable and record what must be rechecked on resume.

On resume:

1. Read the source and brief; confirm both still describe the same requested outcome.
2. Reconcile any newer requirement, external state, or delegated result.
3. Verify the current phase and next action against actual files, tools, or systems before acting.
4. Continue from the first unproven requirement, not from the last activity described.

Do not append routine tool calls, status commentary, or chronological notes. They obscure the state
the next turn needs and make stale instructions look current.

## Delegate from the brief

Derive each worker assignment from the relevant goal, requirement, scope boundary, authority, output,
and proof. Send that bounded assignment directly; another agent does not read your private home.

Record who owns the delegated item and whether it is active, returned, or blocked. On return, inspect
the artifact and evidence, integrate the result, and update the lead brief. A worker report does not
complete the parent requirement by itself.

Use `executing-development-tasks` for development delivery, verification, manual QA, review, and the
final definition-of-done audit. Use `working-as-an-assistant` when maintaining the recipient's own
task system or commitments rather than your execution state.

## Close without leaving clutter

Retire the brief only after the applicable execution owner proves its definition of done or the user
cancels the outcome. Before removal:

1. Promote durable decisions, delivered paths, and final evidence to the canonical project or task
   system.
2. Close or update the canonical source when authorized.
3. Remove the brief from `tasks/`.

Do not archive completed briefs by default. Keep one only when the user requests a handoff or audit
record and there is no better canonical destination. Rundesk does not sweep your home, so a
completed brief left behind becomes misleading task state and permanent clutter.

The evidence behind active work transparency, requirement-to-proof traceability, and bounded
delegation is mapped in [references/sources.md](references/sources.md).
