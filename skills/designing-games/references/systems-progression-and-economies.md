# Design connected systems, progression, and economies

Use this reference when a game contains interdependent numeric systems, persistent power,
randomness, rewards, crafting, items, currencies, trading, or replenishing resources. Model the
system before tuning individual numbers.

## Define what balance means here

Balance is a relationship in service of the experience contract, not equality among every option.
Choose the relevant objective:

- several strategies remain situationally viable;
- opposing players or roles have the intended opportunity and counterplay;
- challenge develops without invalidating learned skill;
- progression changes possibility without making prior content meaningless;
- randomness creates the intended uncertainty without erasing agency; or
- an economy remains understandable and useful over its intended lifetime.

State which players, skill bands, game states, modes, and time horizons the objective covers. An
aggregate win rate can hide a dominant strategy at expert play, an inaccessible option for new
players, or a matchup that is fair only after knowledge the game never teaches.

## Map relationships before values

Create a compact system model:

```text
state/resources -> available actions -> resolution -> outputs -> changed state/resources
```

Record for each resource:

- every source, sink, converter, store, cap, decay rule, exchange, and external purchase;
- who controls it and what information they have;
- the rate and variance under representative play, not only the average;
- dependencies on skill, progression, difficulty, party size, and failure; and
- what happens at empty, capped, hoarded, duplicated, interrupted, and long-idle states.

Use simulation or a spreadsheet to expose trajectories, then validate assumptions in play. A model
can show mathematical behavior; it cannot establish that the behavior is understandable, fair, or
enjoyable.

## Inspect feedback and dominant paths

Mark reinforcing loops, where advantage produces further advantage, and balancing loops, where a
change meets counter-pressure. Reinforcing loops can create satisfying mastery or bring a contest to
a conclusion; they can also make the outcome inevitable while play continues. Balancing loops can
preserve uncertainty; hidden or excessive catch-up can make success feel irrelevant.

For every powerful strategy, compare:

- opportunity cost and execution burden;
- counterplay and information required;
- reliability across common and edge states;
- effect when combined with progression or other bonuses; and
- whether the player can understand why it succeeded.

Do not flatten every difference. Preserve asymmetric identity while bringing power, risk, and
counterplay into the intended relationship.

## Separate progression dimensions

Progression can grant:

- **knowledge:** the player learns rules, spaces, patterns, or strategy;
- **skill:** the player improves perception, decision, or execution;
- **breadth:** new tools create additional approaches;
- **power:** existing actions become more effective;
- **expression:** identity, construction, appearance, or play style expands; and
- **content or world change:** new situations, relationships, or goals become available.

Prefer progression that reinforces the fantasy and opens decisions. When adding power, check old
content, multiplayer fairness, difficulty, economy rates, and the cost of switching builds. Avoid a
mandatory weak opening whose only purpose is to make later numbers feel larger.

Map the expected paths for a new player, a skilled player, a completionist, a returning player, and
a player who spends or loses resources atypically. Provide recovery from a poor early choice when
the consequence could not have been understood at the time.

## Treat rewards as information and state change

Name what a reward does: confirms mastery, teaches value, changes the next choice, opens expression,
marks progress, advances a relationship, or resolves tension. Match timing and magnitude to that
purpose. A reward delivered for every action can obscure which behavior mattered; a delayed reward
can break the perceived connection to its cause.

Variable outcomes require visible rules appropriate to the experience. Test streaks and tails, not
only expected value. Add bad-luck protection, deterministic alternatives, or exchange paths when
extreme outcomes would invalidate promised fairness or block essential progression.

## Verify the whole system

Test in layers:

1. Check invariants, bounds, state transitions, and representative trajectories with calculations
   or simulation.
2. Use automated agents only to find exploits or system states their policy can reach; do not treat
   agent behavior as player experience evidence.
3. Observe representative players at different knowledge and skill levels.
4. Segment telemetry by relevant state and cohort; averages can conceal divergent experiences.
5. Change one causal relationship at a time when possible, then recheck adjacent systems and edge
   states.

```text
Good: evaluate a weapon across matchups, skill bands, costs, counters, and combinations; define the
      experience its asymmetry serves.
Bad:  equalize its average damage because equal numbers are assumed to mean fair play.

Good: test currency sources, sinks, caps, hoarding, failure recovery, and long-run inventories as
      one flow.
Bad:  raise one price to fix excess currency without tracing which players or sources create it.
```

The source mapping for these pairs is in [sources.md](sources.md).
