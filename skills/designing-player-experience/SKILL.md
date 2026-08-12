---
name: designing-player-experience
description: Use when designing, implementing, or reviewing a game's onboarding, tutorials, HUD, feedback, game feel, difficulty and assist options, error recovery, menus during play, readability, or sensory and cognitive accessibility. It supplies an evidence-backed workflow for making state, cause, consequence, and recovery perceivable without overwhelming or manipulating the player. Do not use it for camera and control design, level geometry, visual-asset creation, or playtest methodology alone.
---

# Design player experience

Make the intended game state understandable and actionable. Polish should clarify what happened,
why it mattered, and what the player can do next; it cannot rescue rules, controls, or challenges
that do not support the promised experience.

## Define the experience and information contract

For each representative player state, record:

```text
player goal and likely prior knowledge
information needed now, soon, and on request
available action and consequence
signals across visual, audio, haptic, text, and spatial channels
failure, recovery, pause, and resume behavior
accessibility options and evidence needed
```

Rank information by decision urgency. Keep critical state persistent or reliably recallable; reveal
secondary detail on demand. Do not make the player read the HUD while the world demands attention or
repeat the same low-value signal in every channel.

Do not invent precise timing, completion, or comfort thresholds to make a specification look
measurable. Declare an initial hypothesis from local baseline or pilot evidence, identify the
population and decision, and revise it from observed distributions and material harm.

## Teach through relevant action

Teach the minimum prerequisite near the situation where it becomes useful, let the player attempt
it, show the consequence, and provide a low-cost retry. Test whether help is needed: field experiments
have found that tutorial effects depend on game complexity and presentation, not that more mandatory
instruction universally improves learning or retention.

Preserve choice where the game allows it. Let experienced players skip, accelerate, revisit, or
practice instruction; keep a reference for forgotten controls and rules. Do not teach an obsolete
binding, hide required information in one-time text, or measure tutorial success only by completion.

```text
Good: introduce one needed concept in context, let the player act, then observe transfer later.
Bad:  front-load every rule and lock the player into prompts because tutorials improve retention.
```

## Make feedback causal and proportional

Start with functional feedback: input acknowledged, action accepted or rejected, target and effect,
state change, and recovery. Then layer animation, sound, VFX, camera, haptics, timing, and UI according
to event importance and the experience pillar.

Keep authoritative gameplay separate from optional presentation. Effects may anticipate or amplify a
committed event, but a hidden animation marker should not become the only owner of damage, inventory,
or another durable state. Provide intensity controls or alternatives for shake, flashes, repeated
motion, loud transients, and haptics.

```text
Good: use coordinated, scalable signals to clarify a committed high-importance event.
Bad:  add shake, flash, hit-stop, particles, loudness, and haptics to every successful input.
```

More “juice” is not automatically more readable or enjoyable. Excess layers can mask timing, obscure
hazards, create fatigue, or become an accessibility barrier.

## Keep the HUD and menus task-focused

Give every persistent element an owner, update rule, priority, and hide/show condition. Use stable
placement and redundant cues for critical state; do not depend on color alone. Preserve focus,
back/cancel, current selection, safe areas, text scaling, localization growth, and device changes.

Explain unavailable actions and destructive consequences before commitment. Preserve progress and
settings through interruption where the game's state model permits it. An error should state what
happened, what remains safe, and a valid recovery action—not blame the player or silently discard
their work.

## Separate intended difficulty from barriers

Describe what each challenge tests: perception, knowledge, planning, memory, timing, precision,
coordination, or endurance. Remove accidental difficulty caused by illegibility, inaccessible input,
unclear rules, camera obstruction, or lost progress before tuning enemy health or damage.

Offer changeable options that target the burden where possible: timing windows, game speed, aim or
navigation assistance, information detail, retries, penalty, puzzle bypass, or input demands. Explain
effects without judgment. Do not assume one easy/normal/hard scalar preserves every experience or
secretly alter difficulty while asking players to trust their performance.

## Validate with affected players

Use heuristic review to find candidates, automated checks for programmatic contracts, and human
playtests for comprehension and access. Include players with relevant disabilities; a checklist or
nondisabled proxy cannot establish their experience. Observe success, hesitation, errors, recovery,
prompt dependence, fatigue, discomfort, and use of settings—not only self-reported liking.

Deliver the information hierarchy, onboarding sequence and hypotheses, feedback map, HUD/menu state
contract, difficulty/assist matrix, accessibility settings, error/recovery paths, and validation
evidence. Use `designing-game-cameras-and-controls` for view/input behavior, `frontend-design` for
general interface implementation, `creating-design-assets` for production assets, and
`playtesting-games` for human-study design.

The evidence, pair mappings, and limits are in [sources.md](references/sources.md).
