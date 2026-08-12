---
name: designing-game-cameras-and-controls
description: Use when designing, implementing, tuning, or reviewing a game's camera, viewpoint, aiming, movement controls, player-facing action semantics, rebinding, responsiveness promise, or motion-comfort options across 2D or 3D play. It supplies an engine-neutral workflow that derives the player's view and controls from gameplay information, spatial judgment, and accessibility needs; use the active engine skill alongside it for component and adapter APIs. Do not use it for the technical frame loop, tick-level input buffering, general input-device APIs, or cinematic editing alone.
---

# Design game cameras and controls

Treat the camera and controls as one perception-action contract. The player must see the information
needed for a decision, express the intended action, and understand the result without fighting an
automatic camera or hidden input rule.

## Start from player tasks

Record the intended audience, platform, display, input devices, player verbs, threats, targets,
navigation cues, speed, precision, multiplayer constraints, and motion/access needs. For each common
situation, name what must remain visible and what the player must judge: direction, distance, height,
velocity, timing, cover, aim, route, or another actor.

Choose first-person, third-person, side, top-down, fixed, free, or hybrid views from those information
needs and the intended relationship to the avatar. Do not choose a perspective only because it looks
cinematic or is conventional for the genre; camera choice changes information and therefore changes
challenge.

Specify the contract before tuning:

```text
player task and required information
target/composition and permitted player control
movement, rotation, zoom, and transition behavior
occlusion, collision, bounds, teleport, and reset behavior
input action, timing semantics, feedback, and remap behavior
comfort/accessibility options and test scenarios
```

Express unknown values as named tunables or relationships until movement, display, and player evidence
exists. A precise percentage or millisecond value without a local measurement is a prototype
assumption, not a best practice; label it, bound the decision it serves, and define how it will be
changed.

## Compose camera behavior in layers

Keep distinct layers for target selection, ideal framing, smoothing, constraint resolution, and
optional presentation effects. Update from committed gameplay state after the target moves; otherwise
the camera can lag by an extra frame or react to state that is later rejected.

- Use a deadzone or camera window when constant recentering would erase intentional composition.
- Add look-ahead from meaningful motion or aim intent, with bounded reversal behavior.
- Derive damping from elapsed time, not a fixed fraction per rendered frame.
- Resolve world bounds, occlusion, and collision without losing the target or trapping the view.
- Cut or reset smoothing after teleport, spawn, scene change, or a discontinuous target switch.
- Apply shake and recoil as bounded presentation offsets; do not corrupt the authoritative transform.

```text
Good: follow committed target state, solve framing and collision, then add optional shake.
Bad:  shake the gameplay transform and use one fixed per-frame lerp on every refresh rate.
```

Test composition at the actual aspect ratios and safe areas. A camera that works in an empty room can
fail near walls, overhead geometry, crowds, fast reversals, small screens, split views, or large
targets.

## Make controls semantic and responsive

Map devices to actions such as `Move`, `Aim`, `Confirm`, or `Dodge`, not directly to gameplay state.
Define the player-facing promise for press, release, held, analog, repeat, chord, grace, queueing,
pointer, and text behavior. Use `programming-gameplay` for buffer storage, tick assignment, expiry,
consumption, pause behavior, and authoritative command handling.

For analog actions, inspect center drift, deadzone shape, response curve, saturation, sensitivity,
and device variance in context. Keep camera-relative movement stable near vertical views and explain
how aim direction, avatar facing, locomotion, and target lock arbitrate.

Support rebinding and alternate devices where the target platforms permit it. Detect conflicts,
preserve required navigation and escape actions, store mappings by stable action identifier, update
prompts after remapping or device change, and provide a recoverable reset.

```text
Good: bind semantic actions, preserve their timing, and display the player's current mapping.
Bad:  hardcode physical keys in gameplay and leave tutorials showing the old binding.
```

## Preserve agency and comfort

Give players control over sensitivity and inversion where applicable. Let them reduce or disable
nonessential shake, bob, sway, blur, automatic rotation, and aggressive recentering; offer useful FOV
control when the projection and platform support it. Avoid requiring rapid presses, prolonged holds,
precise analog control, or simultaneous chords when an equivalent configurable interaction can
preserve the intended decision.

Do not claim one “comfortable” default. Test with players susceptible to motion sickness and players
who use alternative inputs. Accessibility guidance is a design starting point, not legal
certification or a substitute for affected players.

## Validate as a coupled system

Test representative traversal, combat, aiming, platforming, puzzle, menu-transition, damage, death,
respawn, teleport, tight-space, edge-of-world, low-frame-rate, high-refresh, and device-change cases.
Observe whether players lose targets, direction, depth, or control; whether the view reveals answers
the design meant to conceal; and whether assists change the intended challenge.

Deliver the task/information matrix, view decision, camera layer contract, control/action contract,
comfort options, edge-state table, tunable parameters with owners, and playtest hypotheses. Use
`playtesting-games` for human evidence, `testing-code` for automated state proof,
`performance-engineering` for frame-time investigation, and the active engine skill for APIs.

The evidence, good/bad mappings, and limits are in [sources.md](references/sources.md).
