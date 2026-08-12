---
name: designing-games
description: Use when defining, designing, balancing, or critiquing a game, including its intended player experience, rules, mechanics, meaningful choices, core and nested player loops, challenge, fairness, progression, rewards, or in-game economy. It supplies an evidence-backed workflow for translating an audience-specific experience hypothesis into testable gameplay systems. Do not use it for the technical frame/update loop, production scheduling, level layout alone, or playtest study execution.
---

# Designing games

Design for a named player experience, not an abstract promise that the game will be fun. Treat every
mechanic as a hypothesis about behavior; only representative play can show whether that behavior and
experience emerge.

## Write the experience contract

Before proposing features, record:

1. **Audience and context:** intended players, prior genre knowledge, platform and input, session
   context, social setting, and accessibility needs.
2. **Player fantasy:** who the player imagines they are, what they repeatedly do, and why those
   actions matter inside the game.
3. **Experience pillars:** a small, ranked set of specific qualities such as tense improvisation,
   expressive construction, shared discovery, or deliberate mastery. Define a visible player
   behavior that would support and contradict each pillar.
4. **Constraints:** genre promises, content and production limits, business model, safety, rating,
   fairness, and non-goals.
5. **Evidence:** the smallest prototype or playtest observation that could change the design team's
   belief.

Do not use `engaging`, `immersive`, `addictive`, or `fun` as an unqualified pillar. Different players
seek different experiences, and one game can intentionally combine or prioritize several.

## Translate experience through the system

Reason in both directions:

```text
designer: intended response <- observed dynamics <- mechanics and content
player:   available action  -> system response   -> perceived consequence
```

Use MDA vocabulary precisely:

- **Mechanics** are rules, actions, data, algorithms, and content that the team builds.
- **Dynamics** are behaviors that emerge when mechanics interact with players and each other.
- **Aesthetics** are the intended emotional or experiential responses—not visual art direction.

Start from the intended response, predict the dynamics required to create it, and then select the
minimum mechanics that could produce those dynamics. Trace proposed mechanics back upward before
keeping them. A feature without a supported pillar or necessary production purpose is scope, not
value.

Write each important rule as a contract:

```text
player state and information
available action and cost
system resolution, uncertainty, and timing
feedback the player can perceive
state change and new decision created
intended experience and failure hypothesis
```

## Design nested player loops

Model a player loop as **action -> system response -> readable feedback -> changed state -> next
decision**. Do not confuse it with the technical runtime loop that samples input and advances the
simulation; use `programming-gameplay` for that implementation boundary.

Map the loops that actually exist:

- **Moment-to-moment loop:** the repeated verbs and decisions through which the player exercises
  skill or expression.
- **Encounter or objective loop:** how local pressure, resources, success, failure, and recovery
  change the next situation.
- **Session loop:** how a play period begins, develops, reaches a natural stopping point, and lets
  the player resume without losing intent.
- **Progression or metagame loop:** how knowledge, capability, relationships, world state, or
  authored content changes across sessions.

For every loop, identify its entry condition, player goal, decisions, costs, feedback, state
change, exit condition, and connection to the next loop. A reward is not a complete loop: it must
change what the player can understand, choose, attempt, express, or pursue.

Use `designing-player-experience` for the detailed feedback and onboarding treatment. Use
`playtesting-games` to test whether players notice the state, form the intended goal, and choose
without prompting.

## Make decisions consequential and legible

A decision earns attention when the player can distinguish alternatives, anticipate a meaningful
tradeoff, and observe a consequence. Preserve uncertainty when it serves the experience, but expose
enough information for the player to form a model and learn from the outcome.

Check each repeated choice:

- Does the current state make more than one option plausible for the intended audience?
- Do alternatives differ in risk, timing, resource use, information, expression, or downstream
  possibility rather than only presentation?
- Can the player connect the result to the decision, including when randomness is involved?
- Does one option dominate across the states that matter? If so, redesign the relationship, make
  the dominance intentional and temporary, or remove the false choice.
- Does failure expose a learnable cause and a reasonable way to retry, adapt, or leave?

Do not require strategic choice in a game whose intended experience is contemplation, sensation,
performance, or authored drama. Meaningful choice is a design instrument, not a definition of every
good game.

## Tune challenge and fairness for the contract

Define challenge in terms of what the player must perceive, decide, execute, remember, coordinate,
or tolerate. Difficulty is experienced relative to player skill, knowledge, ability, equipment,
context, and motivation; one numerical curve cannot serve every audience.

Make the tested skill clear, establish its prerequisites, and define how challenge relationships and
fairness serve the experience. Route selectable difficulty and assist settings, accidental-barrier
removal, communication, and affected-player validation to `designing-player-experience`.

Fairness does not require symmetry or equal outcomes. Define it for the game: consistent rules,
legible causes, comparable opportunity, counterplay, recoverability, or intentionally asymmetric
roles. Verify player perception as well as the underlying math.

Read [systems-progression-and-economies.md](references/systems-progression-and-economies.md) when
designing balance relationships, power curves, randomness, rewards, progression, resources, item
flows, currencies, or a persistent economy.

## Protect player agency

Optimize for the promised experience and sustainable value to the player, not time spent, return
frequency, conversion, or spending in isolation. Do not manufacture urgency, obscure real-money
cost, disguise purchases as ordinary play, make cancellation or refunds harder than purchase, or
use variable rewards to exploit players who cannot evaluate the risk.

For monetized or child-accessible games, identify the applicable platform, consumer-protection,
privacy, age-design, and gambling-like-mechanic rules before implementation. Legal conclusions are
jurisdiction- and product-specific; current qualified review owns them.

Keep play voluntary and interruptible. Show material costs and consequences before commitment,
provide deliberate confirmation for purchases, preserve a clear exit, and measure regret,
complaints, unintended purchases, and player harm beside commercial outcomes.

## Deliver a testable design

Produce:

1. the audience, player fantasy, ranked pillars, constraints, and non-goals;
2. an experience-to-dynamics-to-mechanics trace;
3. the nested player-loop map and system state contracts;
4. the decision, challenge, fairness, progression, and economy models that matter;
5. known exploits, dominant strategies, runaway feedback, accessibility barriers, and ethical
   risks;
6. prototype and playtest hypotheses with observable supporting and contradicting behavior; and
7. decisions to keep, change, remove, or investigate, with evidence still missing.

```text
Good: "We expect cautious players to spend scarce information to avoid a fight; test whether they
      understand both costs and deliberately choose between them."
Bad:  "Add a scan currency and more combat because choices and content increase engagement."

Good: model how every resource enters, changes, and leaves the system; test representative paths
      and edge states before tuning values.
Bad:  tune reward values in isolation until the average session length rises.

Good: show the price and consequence, require an intentional purchase action, and make recovery
      discoverable.
Bad:  reuse a familiar gameplay button for an immediate purchase and hide the refund path.
```

The evidence and limits behind these lessons are mapped in
[sources.md](references/sources.md).
