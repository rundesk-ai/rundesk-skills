---
name: playtesting-games
description: Use when planning, running, or interpreting playtests with human players; testing comprehension, usability, appeal, difficulty, or accessibility; recruiting representative players; moderating sessions; designing playtest telemetry or surveys; or turning player evidence into game changes. It supplies a hypothesis-led games user research workflow. Do not use for automated software tests, QA defect verification, or bot-only simulation; use testing-code for those.
---

# Playtest games

Use players to answer a defined design question, not to approve the game or design it for the team.

## Frame the decision

1. Name the decision the team will make after the study.
2. State the intended player experience and the observable behavior that would support or challenge
   it.
3. Write a bounded research question and the competing explanations the study must distinguish.
4. Record the build, content, platform, controls, session context, and known incomplete behavior.

```text
Good: Can first-time strategy players identify a defensible move before the timer expires, and what
information do they use?
Bad:  Is the tutorial fun?
```

The good question creates observable evidence and a decision. The bad question combines an undefined
construct with no population, context, or action.

Do not make one session answer comprehension, balancing, appeal, onboarding, and market demand. A
broad test produces ambiguous evidence and invites the team to select whichever anecdote confirms its
preference.

## Recruit for the question

Define participants by experience and capabilities that can change the result: genre familiarity,
platform and input familiarity, prior exposure to the build, play context, and relevant access needs.
Recruit from the intended audience or state exactly how the available sample differs. Friends,
developers, expert players, and an existing community can expose problems, but their familiarity or
investment makes them poor stand-ins for every target player.

Choose the sample from the method and decision. Small qualitative rounds discover and explain
problems; estimates, comparisons, and subgroup claims need a quantitative sampling and analysis plan.
Do not apply a universal participant count.

Do not invent a participant count, success percentage, completion time, or pass threshold before the
recruitment population, baseline or pilot evidence, practical consequence, and analysis are known.
When the team needs a planning assumption, label it as provisional and define the evidence and owner
that will replace it before outcomes are inspected.

Include players with relevant disabilities when evaluating accessibility. A checklist or
nondisabled proxy cannot establish how a barrier affects the people who encounter it.

## Match evidence to the question

- **Observation** reveals what players do, where they hesitate, fail, recover, or invent a different
  strategy.
- **Interviewing** probes the understanding, expectation, or reasoning behind observed behavior.
- **Telemetry** counts precisely defined behavior across sessions; it does not by itself explain
  intent, frustration, or enjoyment.
- **Surveys** compare reported constructs at scale when the instrument and sample support that use.

Combine methods only when each answers a named part of the question. Read
[methods and analysis](references/methods-and-analysis.md) before choosing measures, instrumenting a
build, comparing variants, or synthesizing a mixed-method study.

When using a validated measure, preserve its items, response scale, administration, and scoring.
Changing them creates a new instrument; do not compare its scores with the validated benchmark.

## Protect the session

Obtain informed consent for participation, observation, telemetry, notes, and each kind of recording.
Explain purpose, data use, access, retention, withdrawal, and observers in language the participant
can use. Collect only needed personal data and protect it under the applicable organization and
jurisdiction rules. Obtain the required guardian and participant permissions before research with
minors or other protected populations.

Pilot the full protocol: install and launch the exact build, reset accounts and saves, verify
controllers and accessibility settings, trigger telemetry, capture recordings, and rehearse recovery
from a blocking defect. Mark assisted or corrupted tasks; do not blend them with unassisted results.

Give realistic goals without naming the expected route or control. During play, observe before
intervening and record the event before interpreting it.

```text
Good: "What do you think is happening now?" then "What made you think that?"
Bad:  "Did you notice the glowing dodge indicator?"
```

The bad question reveals both the intended cue and action, changing the evidence it seeks. Help only
for safety, distress, or an acknowledged build gap; record the intervention and what remains untested.
Tell participants that the game—not their skill—is being evaluated.

## Preserve evidence, then interpret it

For each notable moment, keep these separate:

```text
context -> observed action/result -> participant explanation -> researcher interpretation
```

Use stable participant codes and timestamps so notes, video, and telemetry can be reconciled without
putting identity in gameplay events. Instrument descriptions of behavior at the finest useful grain
with build, content, session, tick/time, and relevant state—not inferred emotions.

```text
Good: tutorial_step=parry; action=attack; attempts=3; prompt_visible=true
Bad:  player_confused=true
```

The bad event hides an interpretation as data and cannot explain what occurred.

## Turn findings into another test

1. Review all sessions before deciding; preserve confirming, conflicting, and successful evidence.
2. Group observations by one underlying player problem only when one change could plausibly address
   them.
3. Describe each finding as audience and context, observed evidence, player impact, confidence and
   limits—not the loudest participant's proposed feature.
4. Prioritize by obstruction to the intended experience and decision risk. Keep frequency visible,
   but do not call an uncommon progression blocker harmless.
5. Choose the smallest design change that tests the causal explanation. State what should change in
   the next round if the explanation is right.
6. Re-test with fresh representative players when prior exposure would teach the answer.

Report what the study supports, what it cannot support, build and participant limits, assisted or
failed sessions, and the next decision. Route automated regression coverage, deterministic harnesses,
and QA checks to `testing-code`; human play evidence does not replace them.

Read [the source map](references/sources.md) when auditing or changing these rules.
