# Briefs and daily updates

Use a brief to compress attention, not to prove how much the assistant read. Agree on the recurring
shape, then adapt it when the day has different needs.

Deliver for a phone by default: one short heading, one decision per bullet, no table, no deep
nesting, and the source at the end. Keep `Needs you`, `Today/upcoming`, and `Waiting/watching` in a
stable order so repeated reports are easy to scan. Put extended context behind a link or after the
decision summary.

## Build the standing brief contract

Record:

- delivery cadence, local timezone, quiet hours, channel, and target length;
- priority people, projects, deadlines, risk thresholds, and interruption rules;
- included sections and explicit exclusions such as promotions, routine receipts, or general news;
- whether an empty report should be a one-line all-clear or no message; and
- opted-in personal context such as birthdays, anniversaries, travel, or household appointments.

Test the agreed output once before making it recurring. A fresh scheduled session needs the full
contract, reporting window, expected sources, selection rules, format, and quiet behavior; it cannot
depend on an earlier conversation being present.

Maintain a durable recurring-brief record in the authorized canonical system:

```text
Cadence, timezone, and allowed delivery window:
State: active | paused | cancelled
Next due:
Last attempted:
Last successful delivery and reporting window:
Last reliable source snapshot and coverage gaps:
Outstanding failure or retry decision:
```

Before delivery, compare the reporting window and last successful result. Do not send the same
brief twice. Record a failed or missed run; never advance `last successful` until delivery is
verified. Creating, changing, pausing, or cancelling this record requires the corresponding
authority in the working agreement.

Do not mine personal dates from unrelated mail or social profiles. A date belongs in a brief only
when the recipient asked to track it and the source is current enough to trust.

## Choose the right update

| Update | Include | Exclude |
|---|---|---|
| Morning or start-of-day | Needs-you decisions, today's commitments, preparation, changed waiting items | Yesterday's narrative and unchanged backlog |
| Midday exception | Material change, new conflict, or action that cannot wait | A second copy of the morning brief |
| End-of-day | Unfinished commitments, completed outcomes that matter, tomorrow's first preparation | Activity log and routine completions |
| Weekly review | Priority movement, overdue/stale items, coming deadlines, waiting-ons, decisions to make | Every message or meeting from the week |
| Meeting brief | Purpose, time/location, attendees and relevant roles, decisions sought, preparation, unresolved context | Biographies and thread history unrelated to the decision |

Lead with the recipient's required action even when the source arrived in a different order. Use
links for evidence and deeper context.

```text
Good morning — [count] items need you.

Needs you
- [Decision or action] by [deadline] — [consequence]. Recommended: [next step]. [source]

Today
- [Time and event] — [preparation or decision that changes the outcome]. [calendar]

Waiting on
- [Owner]: [expected result]; follow up [date] if it has not arrived. [source]
```

```text
Bad structure
Long greeting → unread/event/task counts → yesterday's narrative → promotions and routine notices
→ required decision
```

The good form follows evidence-backed inverted-pyramid, main-message-first, call-to-action, and
concise status-update practices. The bad form spends the recipient's attention without identifying
a decision or consequence.

## Use examples as shapes, not scripts

Preserve the agent's voice and the recipient's preferences. Reuse only the information order.

```text
Coverage-gap all-clear
No material change in checked sources. [Expected source] has been unavailable since [time], so
[affected conclusion] is unknown. Still waiting on [owner]; next check [date].

Meeting brief
[Time] — [meeting and participants] [calendar]
- Goal: [outcome sought].
- Decide: [decision the recipient must make].
- Prepare: [minimum preparation]. Recommended: [next step]. [source]
- Open: [unresolved fact or dependency]. [source]

Weekly look-ahead
[Count] decisions and [count] deadlines need you next week.
- Decide by [date]: [decision] — [consequence]. Recommended: [next step]. [source]
- [Deadline]: [outcome]; waiting on [owner]. Follow up [date] if it has not arrived. [source]
```

Do not force these sections when they are empty. A useful shape remains short because it selects
what matters, not because it truncates a longer dump.

## Handle time and uncertainty

- Resolve the recipient's timezone before using `today`, `tomorrow`, or a time-of-day greeting.
- Show a timezone when participants or travel cross zones. Do not silently convert a floating or
  ambiguous time.
- Distinguish tentative holds from confirmed events and identify the authoritative calendar.
- Recheck cancellations, room or link changes, and travel time close enough to the event to matter.
- State the as-of time when a brief combines changing sources.
- Disclose a missing source when its absence could change the apparent all-clear. Do not present an
  incomplete scan as complete.

When two sources conflict, show the decision-relevant conflict in one line and recommend the safest
next verification. Do not bury the uncertainty in a footnote.

Scope an all-clear to what was actually checked: `No material change in checked sources; calendar
unavailable, so availability is unknown.` Never use an unqualified `nothing changed` when an
expected source failed.

## Use greetings deliberately

`Good morning, Sam — two items need you.` is useful at the start of a scheduled report when it
matches local time and the recipient's preferences. Within an active exchange, continue directly.
Keep the agent's established voice; this workflow does not prescribe a persona, phrasebook, or
emoji style.

## Revise from feedback

Learn from corrections: what was useful, what was noise, what deserved interruption, and what the
recipient repeatedly opened or ignored. Ask directly before changing a consequential threshold.
Never optimize only for response speed; urgency cues can pull attention toward low-importance mail.
