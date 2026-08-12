# Gameplay runtime contracts

Read the sections that match the runtime boundary being implemented.

## Clocks and loop ownership

Use a monotonic clock for elapsed real time. Name separate values instead of passing an ambiguous
`delta` everywhere:

```text
wall_elapsed | fixed_tick_duration | tick_index | presentation_alpha | game_time_scale
```

If an engine owns the application loop, implement the same contract inside its callbacks; do not nest
a second blocking loop. Pump host events often enough to remain responsive even when the world is
paused or turn-based.

An accumulator loop has four explicit guards:

1. clamp or classify implausible elapsed wall time after suspend, breakpoint, or stall;
2. add admitted time to the accumulator;
3. consume only whole fixed ticks up to the per-frame catch-up limit; and
4. present using the fraction left in the accumulator.

Choose a tick rate from the game's physics, control, CPU, and networking constraints. Library examples
such as 60 Hz are starting points, not a universal requirement. Measure the chosen workload with
`performance-engineering` and leave catch-up headroom.

## Pause, slow motion, and timers

Decide each subsystem's clock explicitly:

| Concern | Typical clock decision |
|---|---|
| Gameplay movement and cooldowns | Simulation ticks or scaled game time |
| Menus and pause UI | Unscaled presentation time |
| Input edges | Host samples assigned to a tick, including paused-state policy |
| Network timeout | Monotonic real time, not paused game time |
| Animation | Simulation or presentation clock according to whether it changes authority |

Do not implement pause by sending an enormous `dt` on resume or by stopping host event processing.
Reset or classify the wall-time gap, preserve input edge rules, and resume from a documented boundary.

## Input command contract

Separate four stages:

```text
device event/state -> action mapping -> tick command -> simulation result/event
```

A command should contain only simulation-relevant data: action, value or target, tick, player/source,
and sequence when needed. Validate it against current authoritative state. Record commands after
mapping but before application when the goal is replaying game decisions independent of hardware.

Define how a short press between ticks is buffered, how held state persists, how multiple changes in
one tick are ordered, and how focus loss releases controls. Never infer input edges by comparing two
render frames when simulation may run zero or several times between them.

Represent a buffered action with its semantic action, source, press sequence, assigned tick, and
expiry rule. Consume it at most once after authoritative eligibility succeeds. Decide explicitly
whether pause freezes, expires, or clears it; do not let resume synthesize a new press from held state.

## Ordered updates and structural commits

List systems in actual execution order and record their data contract. If two systems can observe
each other's partial writes, either establish the required order or introduce staged state. Do not
describe a set as parallel merely because the conceptual systems are independent; their reads,
writes, events, and reductions must prove independence and deterministic merge behavior.

During a phase, collect structural commands such as:

```text
Spawn(prefab, initial_state)
Destroy(entity_handle)
Attach(child, parent_handle)
ChangeScene(scene_id)
```

At commit, sort or otherwise define order where simultaneous requests can conflict, validate handles,
apply changes, and emit committed lifecycle events. Decide whether newly spawned entities participate
in the current or next tick. Decide whether a destroyed entity can finish the current phase. Encode
those answers once rather than letting container behavior decide them accidentally.

Where physics contacts, job results, or concurrent producers can arrive in nondeterministic order,
copy their authoritative facts into owned data and sort or deterministically reduce them before
resolution. Record any external or asynchronous result that cannot be reproduced from the initial
state and commands.

## Identity and events

A reusable slot needs a generation/version so an old reference cannot silently target a different
entity. Validate both slot and generation at resolution. Keep domain IDs separate from engine node,
physics body, audio voice, and renderer handles; adapters maintain those mappings and clear them at
commit or teardown.

Use events for facts that several consumers may observe later. Specify:

- producer phase and publication boundary;
- immutable payload and stable identities;
- within-tick ordering or explicit lack of ordering;
- queue ownership, capacity, and overflow behavior;
- whether consumers may emit future events; and
- whether the event belongs in replay, telemetry, or presentation only.

Do not allow a presentation consumer to synchronously re-enter authoritative simulation. That turns
an apparently descriptive effect into an order-dependent state mutation.

## Deterministic replay

Define the reproducibility envelope before implementation:

```text
same process | same build/platform | compatible builds | cross-platform
```

Capture inputs beyond player commands when they affect authority: owned random seeds or stream state,
procedural inputs, external responses, content version, configuration, and permitted asynchronous job
results. Use canonical ordering and serialization for checkpoint hashes; never hash padding bytes,
addresses, presentation state, or unordered container iteration.

Replay from a known initial state, compare hashes, and stop at the first mismatch with tick, command
range, and subsystem hashes. A successful replay proves only the exercised envelope and duration.

## Save boundary

Snapshot after structural commit when authoritative relationships are coherent. Store a schema and
content version, stable entity or domain IDs, durable component/state data, and explicit relationships.
On load, validate, migrate, create authoritative objects, resolve relationships, rebuild derived data,
then create engine and presentation adapters.

Copy the snapshot while the simulation owns a coherent boundary, then let a worker serialize and
write that immutable copy. A running save request waits for such a boundary; loading enters an
explicit paused/loading mode and resets clocks, input edges, transient events, and interpolation
snapshots before resuming.

Write to a temporary sibling, flush as required by the platform contract, then atomically replace the
destination where supported. Keep the previous known-good save or another recovery path when product
risk warrants it. Test interrupted writes, incompatible versions, missing optional content, repeated
load/save, and restoration on each supported storage platform.
