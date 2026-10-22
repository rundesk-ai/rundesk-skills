---
name: writing-bug-tickets
description: Use when writing, rewriting or reviewing a bug ticket or defect report — in Jira, Linear or a GitHub issue — that people read to understand what broke, how to see it, and how they will know it is fixed, including turning notes, a support complaint or test results into a report, or cutting a long one down. It supplies the report's shape, reproduction and evidence rules, keeping what was tested apart from what is guessed, and when to split or ask. Do not use for finding or fixing the cause of a failure, or for a request for something new.
---

# Writing bug tickets

A bug ticket lets someone who was not there see the failure, judge how much it matters, and know
when it is fixed. The team reads it to decide; whoever fixes it plans from it. It records what was
observed and tested — never the fix, and never a guess presented as a finding, because a wrong
cause written as fact sends the fix to the wrong place.

## The shape

```markdown
**Title:** <the symptom, and where it happens>

**Problem**
<What goes wrong and for whom, then what it costs. Two sentences.>

**Steps to reproduce**
1. <From a known starting state, one action per step>

**Expected:** <what should happen>
**Actual:** <what happens instead, with the exact error>

**Tested**
- <Where it fails, where it does not, and how often>

**Done when**
- <The steps above now give the expected result>

**Not included:** <Only what a reader might assume is part of this fix. Omit when nothing needs saying.>
```

- **Title** names the symptom and where: "Quote form loses answers on Back in mobile Safari", not
  "Form bug" or "Fix history state".
- **Problem** says who is hit and what it costs — lost customers, support load, compliance risk.
  Use a real number when one is known; never invent one.
- **Steps to reproduce** are the smallest set that shows the failure from a known starting state,
  with only the setup that matters: account type, data, environment. Steps nobody ran are not steps:
  when the failure has not been reproduced, say so — "Seen twice in production; not yet
  reproduced" — rather than writing steps from a guess.
- **Expected** and **Actual** are observable. Quote the exact error; "it breaks" tells nobody what
  to look for.
- **Tested** is what scopes the fix: where it fails and where it does not ("fails on iPhone Safari
  18; works on Chrome desktop and Android"), how often (every time, 3 of 10, once), and when it
  started if known (first seen, last version that worked). An intermittent failure usually has a
  pattern; record the conditions of each occurrence rather than calling it random.
- **Done when** passes or fails. The first line is always the reproduction giving the expected
  result; add a line only for a scope the ticket names, such as each environment listed as failing.
  "Add tests" or "refactor the handler" is the build, not the outcome.

## Procedure

1. **Read what you have:** notes, a complaint, logs, test results, the conversation.
2. **Ask when you cannot see the failure.** Without what was done, what was expected and what
   happened instead, there is no bug to write — and the code cannot tell you what the person saw.
   Ask for whichever is missing, at most three questions, and stop without a draft.
3. **One failure per ticket.** Failures the reporter can tell apart — different symptoms, screens or
   conditions — get separate tickets; one fix rarely closes both, and a combined ticket stays open
   until the slower one lands. Propose the split, write each in full, and let the person decide. A
   request for something new that arrives with the bug is not part of it; name it in a note.
4. **Write, then check** that every statement is something observed, or is marked otherwise.
5. **Add the notes** and hand over.

## Facts, not theories

- A suspected cause goes in a note beginning "Suspected:", never in the Problem or the Done when.
- A gap stays a gap: "[version?]", "[how often?]" — and ask for it in a note. Never fill it with a
  plausible value.
- Describe impact — who, how many, whether there is a workaround — and leave severity and priority
  to whoever triages; they weigh it against everything else.
- Logs and screenshots are attached, not pasted; quote only the line that shows the failure, with
  customer data and secrets removed. Use a test account in the steps, never a real customer's.

## On GitHub

A GitHub issue keeps the format its filing workflow sets — the repository's issue template, or the
fallback bug form when there is none. This skill supplies what goes into it: the same steps,
expected and actual results, Tested lines and pass-or-fail outcomes, placed in that format's fields.
The shape above is for Jira and Linear.

## Notes after the ticket

Up to four bullets, one sentence each, under a **Notes** heading — and nothing after them: a gap to
fill, a suspected cause, a proposed split, something new that came with the report, what a rewrite
dropped. Never mention what you did not do or could not file.

## Wording

- **No people's names.** Name the role or the account type. Assignment is a tracker field.
- **Plain words**, short active sentences, each thing said once.

## Check before handing over

- Could someone who was not there reproduce it from the steps alone?
- Is every statement observed, or marked as suspected or unknown?
- One failure? Tested lines saying where it does and does not happen?
- Every **Done when** line pass or fail, with the reproduction first?
- No person's name, customer data or secret?

Read [Examples](references/examples.md) when turning rough notes into a ticket or splitting a
report, and [Sources](references/sources.md) when auditing or changing a rule here.
