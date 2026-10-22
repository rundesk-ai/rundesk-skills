---
name: writing-task-tickets
description: Use when writing, rewriting, trimming or scoping a task ticket, story or epic in a tracker such as Jira or Linear that stakeholders read to understand what needs doing and why — including turning a stated problem into a ticket, cutting a long or process-heavy one down, or deciding whether one should be split. It supplies a four-section shape, outcome-level pass-or-fail requirements, and what to leave out. Do not use for a bug report, a GitHub issue, an implementation plan or build steps, or a full product requirements document.
---

# Writing task tickets

A task tells a stakeholder — someone who decides, funds, tracks or is affected by the work — what
needs doing, why it is worth doing, and how they will know it is done, in about a minute. Engineers
and agents plan the build from it themselves, so it carries outcomes, never a plan: a pre-planned
task is one the stakeholder cannot read and the builder does not need.

## The shape

```markdown
**Title:** <the outcome>

**Problem**
<What is wrong today and what it costs. Two sentences at most.>

**Goal**
<What is true once this is handled. One sentence.>

**Done when**
- <One outcome per line that someone can check>

**Not included:** <What a reader might assume is part of this but is not. Omit when nothing needs saying.>
```

- **Title** names the outcome: "Stop privacy emails landing in spam", not "Fix DNS records".
- **Problem** is two sentences: what happens today, then what it costs — money, risk, time,
  customers. A problem with no cost reads as optional. Use a real number when one is known; never
  invent one — write "[cost?]" and ask. Name a group rather than listing its members.
- **Done when** is the requirements. Read [Requirements](references/requirements.md) before
  writing the list; it holds the rules that make each line an outcome that passes or fails.
- **Not included** records limits the person set or the context makes plain — never a choice
  nobody made, which decides the build.

## Procedure

1. **Read what you were given:** the request, the conversation, an old task, the project's docs or
   code. Do not ask for what you can already see.
2. **Ask when there is no problem to state.** A request naming only an area and a vague word —
   "better reporting" — states no problem, and research cannot supply one: code shows what exists,
   never what the person finds wrong with it. Ask one to three questions (what goes wrong, for whom,
   what should be true after) and stop without a draft.
3. **Scope it.** One task holds one outcome that can finish on its own; a task carrying two gets
   half-done. Propose a split when the material holds unrelated problems, the requirements fall
   into groups serving different goals, one part can finish while another waits on a decision, or
   the Goal needs "and" to join two outcomes. Many requirements serving one goal is still one
   task. Propose it even when the person asked for one task — "put it all in one ticket" is said
   before anyone weighs the cost. Write each task in full, lead with one line saying why; the
   person decides.
4. **Write, then cut** every sentence a stakeholder would not miss.
5. **Add the notes** and hand over.

## Notes after the task

Up to four bullets, one sentence each, under a **Notes** heading — and nothing after them. Each
carries something the person must know or decide: a line you added and why, a smaller first
version, what already exists, a gap to fill, what a rewrite dropped. Plain words; no nested lists,
file paths or code. Never mention what you did not do or could not file; the person did not ask,
and it buries the notes that matter.

## Wording

- **No people's names.** Name the role or place. Assignment is a tracker field, and a name in the
  body goes stale when the work changes hands.
- **Plain words** for someone outside the project; expand an acronym or drop it. Short active
  sentences, no hedging. Say each thing once.

## Leave out

| Leave out | Because |
|---|---|
| Numbered requirements with matching acceptance criteria | The same points twice; **Done when** is both. |
| History, source documents, versions, meeting timestamps | Link them in the tracker. |
| Evidence lists, rollout, readiness, approval gates | Process the team already follows; **Not included** marks the edge. |
| Dependencies and blockers | The tracker's blocked-by link. |
| Solutions, estimates, technical guarantees — formats, retries, mappings, test suites | The implementation planning derives them from the outcome. |

## Check before handing over

- One outcome? If not, propose the split.
- Problem in two sentences, the second its cost?
- Notes four bullets or fewer, one sentence each, and nothing after them?
- Every **Done when** line an outcome a stakeholder would miss, traced to the request or to context
  that requires it, and one two people would agree passed?
- Any person's name, or a sentence there for the writer's protection? Remove it.

Read [Examples](references/examples.md) when rewriting a long task or proposing a split, and
[Sources](references/sources.md) when auditing or changing a rule here.
