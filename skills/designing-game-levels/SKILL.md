---
name: designing-game-levels
description: Use when planning, blocking out, implementing, critiquing, or iterating a game's levels, maps, spaces, routes, encounters, puzzles, checkpoints, wayfinding, gating, or spatial pacing. It supplies an engine-neutral workflow that derives geometry and content from player, camera, movement, challenge, and progression metrics, then validates the space before art polish. Do not use it for procedural-generation algorithms, asset production, world lore alone, or gameplay rules with no spatial delivery.
---

# Design game levels

Make space deliver the game's intended decisions and rhythm. A level is not a decorated container;
its dimensions, routes, visibility, encounter state, resources, and recovery rules shape what the
player can perceive, choose, execute, and learn.

## Establish the spatial contract

Start from the audience, experience pillars, player verbs, camera, controls, movement model, enemy or
puzzle capabilities, session target, progression state, and content constraints. Record measured or
prototype-derived metrics rather than designing from visual scale alone:

```text
player/collision dimensions and traversal distances
speed, acceleration, jump, turn, aim, interaction, and recovery envelopes
camera framing, sightline, occlusion, and screen-space needs
enemy, hazard, puzzle, cover, and resource ranges
checkpoint, failure, reset, and revisit behavior
performance, accessibility, and production constraints
```

Use `designing-game-cameras-and-controls` when the view or input contract is unresolved and
`designing-games` when the rules or intended challenge are unresolved. Geometry cannot compensate
for an undefined mechanic.

Keep unknown dimensions as relationships to measured movement and view envelopes. If a graybox needs
an initial number before evidence exists, label it as a disposable assumption and define the traversal
or playtest that will replace it; false precision makes an arbitrary layout look validated.

## Map intent before geometry

Write a beat map for the expected experience: entry state, goal, decision or skill, pressure,
information, resources, change, recovery, and exit. Mark critical, optional, secret, return, escape,
and inaccessible paths. Explain why each branch exists and how the player can infer it.

Use landmarks, composition, lighting, motion, sound, topology, and repeated visual grammar to support
wayfinding, but preserve intentional uncertainty when it serves exploration. A critical route should
not depend on one fragile cue or color alone.

Control pacing through meaningful changes in decision density, pressure, traversal, information,
reward, safety, and spectacle—not by inserting empty distance or constant enemy escalation. Give
players space to perceive and apply a new concept before combining it with additional demands.

## Block out with gameplay metrics

Build the cheapest playable graybox that can answer reachability, timing, sightline, framing,
navigation, encounter, puzzle, and recovery questions. Keep art modular or absent until major spatial
changes are cheap.

```text
Good: derive a jump gap and landing view from tested movement/camera metrics, then observe failures.
Bad:  sculpt the finished vista first and tune movement until the player can cross it.
```

Exercise extremes and transitions: shortest/tallest avatar states, slow/fast movement, alternate
routes, backtracking, moving targets, camera collision, edge positions, multiplayer occupancy when
applicable, accessibility assists, and low-performance conditions. Verify spawn and checkpoint state,
not only the first clean traversal.

## Build encounters and puzzles as state machines

For each encounter or puzzle, define initial state, player information, valid approaches, pressures,
resources, escalation, success, partial progress, failure, recovery, reset, exit, and downstream
state. Place enemies, hazards, interactables, cover, and rewards to create the intended decisions—not
to fill space or meet a content count.

Teach a concept in a readable state, let the player practice it with limited interference, then test
transfer or combination. Do not make “teach, practice, test” a rigid three-room formula; observe what
the defined audience already knows and where they form the wrong model.

```text
Good: expose a mechanic safely, observe its use, then combine it after players demonstrate a model.
Bad:  label three rooms teach/practice/test without checking what players perceive or learn.
```

Preserve counterplay and recovery. A failure should be attributable to a learnable decision or
execution demand unless confusion is itself the intended experience. Avoid checkpoints that force
players to repeat mastered low-risk work before retrying the actual challenge.

## Validate before decoration and at final fidelity

Run designer walkthroughs for contracts, automated traversals for reachable bounds and state
invariants, and representative playtests for navigation, challenge, pacing, and interpretation.
Record the route players take, what they look at, hesitation, deaths/failures, retries, resource
state, and where intervention becomes necessary. A heatmap or completion rate identifies a location;
it does not explain the cause.

Re-test after art, lighting, audio, effects, collision, optimization, and narrative dressing because
final presentation can hide affordances, change scale, block sightlines, or alter performance and
timing.

Deliver the spatial contract and metrics, beat/route map, blockout assumptions, encounter/puzzle
state contracts, checkpoint and recovery design, accessibility and performance risks, playtest
hypotheses, observed evidence, and remaining changes. Route human research to `playtesting-games`,
automated proof to `testing-code`, and asset creation to `creating-design-assets`.

The evidence, good/bad mappings, and limits are in [sources.md](references/sources.md).
