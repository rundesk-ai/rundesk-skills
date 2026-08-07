# Status and open items

A running list is the assistant's continuity layer. It records commitments and next moves, not a
transcript of everything discussed.

## Keep one canonical item

Use the recipient's established task system when one exists. Otherwise keep a minimal record:

```text
Outcome/request:
Status: Needs you | Next | In progress | Waiting on | Watch | Parked
Owner:
Next action:
Due or review date:
Source:
Last checked:
Blocker or decision:
```

Create an item only from an explicit request, accepted commitment, authoritative record, or
confirmed follow-up. A sentence such as “we should consider a retreat sometime” is not a booked
commitment. Clarify or leave it as conversation context. Persist every state change to the
authorized canonical system; if that write is unavailable, show the proposed state change and do
not imply it will survive the session.

## Maintain state, not history

- Update the existing item when a thread changes; do not create one task per reply.
- Separate `Waiting on` from `Needs you`. Name who owes the next move and when to follow up.
- Give `Watch` and `Parked` items a trigger or review date so they do not disappear or recur forever.
- Remove completed items from routine briefs after reporting the meaningful outcome once.
- Flag stale items whose due date, owner, or next action can no longer be trusted.
- Preserve a source link and last-checked time. Close from the recipient's direct confirmation, the
  item's responsible owner, or its canonical system; treat an incidental or ambiguous claim as
  `unconfirmed` and keep the item open.

```text
Good structure
Waiting on — [owner]: [expected result]. Follow up [date] if it has not arrived. Last checked
[timestamp]. [source]

Bad structure
[Topic] — ongoing. Mentioned several times. Urgent.
```

This pair minimizes the GTD waiting-for and GitLab owner/next-step/source practices mapped in
[sources](sources.md). The good form exposes ownership and the next review point; the bad form
forces the recipient to reconstruct state and invites repeated, unactionable reminders.

## Report progress as a delta

A status update should answer:

1. What outcome changed?
2. What is the current state and confidence?
3. What happens next, by whom, and when?
4. What is blocked or needs the recipient?
5. Where is the supporting record?

Do not list routine activity as progress. `Reviewed ten messages` is an implementation detail;
`Vendor confirmed delivery for Tuesday; no action needed` is an outcome.

When nothing changed, do not restate the old update. Use `No material change in checked sources;
still waiting on Legal, next check Thursday` only if the scheduled cadence requires a visible
report, and name any expected source that could not be checked.

## Review the list

At an agreed cadence, sweep:

- overdue and due-soon actions;
- prior and upcoming calendar entries that create follow-up;
- `Waiting on` items whose check date arrived;
- active outcomes with no next action;
- parked items whose review trigger arrived; and
- duplicates, cancelled work, and commitments no source still supports.

Escalate aging only when its consequence warrants the recipient's attention. Age alone does not
turn a low-value item into an emergency.

## Hand off safely

For another assistant or a fresh session, pass the current contract, active list, source links,
approval boundaries, temporary constraints, and expirations. Do not pass a raw transcript and
expect the next agent to infer what remains authorized.
