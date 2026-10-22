# Requirements

The **Done when** list is what a stakeholder checks to know the work is finished, and what the
builder plans from. Every line costs someone work, so the best list is the shortest one that meets
the goal and lets nobody argue about whether it was met.

## Each line

- **An outcome a stakeholder would notice** if it were missing: "Both SMS vendors' results can
  be compared stage by stage." The guarantees that make it trustworthy — formats, versions, retries,
  duplicates, mappings, response codes — are the build, and the implementation planning derives
  them. A line naming a component, a technology or a test case is describing the build.
- **Direct and short.** A present-tense fact of about ten words: "Brokers see the partner's reason
  on each returned lead." Past fifteen words it is usually two lines or carrying detail.
- **Passes or fails.** Two people checking it reach the same answer, or the task never closes.
  *Clear, easy, fast, reliable, better, properly, nicely, user-friendly* pass nobody's test; write
  what someone would see instead — "the error says the text was not sent and why". When the bar
  needs a number the person did not give, mark the gap — "Results load within [time?]" — and ask in
  a note; never invent one.
- **One requirement per line**, as many lines as the work holds; merge lines that say the same thing.
- **Conditions that must not change** get a line only when a stakeholder would care if they broke:
  "Recipients are unchanged."

## What belongs on the list

- **Only what was asked.** A line nobody requested reads as agreed scope, and gets built. Add one
  only when the context — the conversation, an old task, the code — shows the requested outcome
  fails without it, and say why in a note: staging gains "never sends to live partners" because
  the code defaults to live partner addresses. Work *beyond* the outcome, however sensible, is a
  note suggesting a separate job, not a line.
- **Not the common sense.** "Use test data", "keep keys out of the task", "don't touch production
  while testing" are things nobody competent would do; stating them buries the lines that matter.
  Keep one only when this work makes the mistake likely, and say why.
- **The smallest complete list.** Judge each requested line by whether the goal fails without it.
  Keep requested extras — the person decides — but name the smaller first version in a note. A line
  the system already satisfies is not new work: drop it, and say what already exists. Word each line
  at the lowest bar that meets the goal: "the customer receives the quote" leaves the cheap route
  open; "delivery is tracked in real time" forces a bigger build.
- **Never trim** compliance (consent, opt-out, Do Not Call), security, data loss or accessibility.

## Rewriting a technical task

Collapse its requirements into the few outcomes they serve. Translating them one for one produces
the old spec in plainer words — accurate, and still unreadable to a stakeholder. Apply the same
filter to what the original excluded: carry its real scope limits into **Not included**, and drop
its common-sense ones ("no real consumer data", "no production credentials") like any other.
