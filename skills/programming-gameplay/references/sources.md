# Programming gameplay source map

This package independently synthesizes practitioner literature and current engine/physics contracts.
It does not adapt AAAbench or another skill package. Links were verified 12 August 2026.

## Loop, timing, and update order

- Robert Nystrom, [Game Loop](https://gameprogrammingpatterns.com/game-loop.html) — practitioner
  basis for a continuously running nonblocking input/update/render loop, time tracking, and the
  distinction between a library-owned and engine-owned loop. Its illustrative C++ is not an API or
  performance prescription.
- Nystrom, [Update Method](https://gameprogrammingpatterns.com/update-method.html) — practitioner
  basis for slicing concurrent-seeming behavior into per-update state, recognizing significant
  update order, and avoiding modification of the live object collection during traversal. The stable
  handle/deferred-removal good/bad pair in `SKILL.md` applies this documented mutation trap; the
  generation check is corroborated by Box2D's handle design below.
- Glenn Fiedler, [Fix Your Timestep](https://gafferongames.com/post/fix_your_timestep/)
  (2004) — practitioner derivation of variable, semi-fixed, and accumulator-based fixed stepping;
  interpolation; required simulation headroom; the catch-up spiral; and exact reproducibility limits.
  The fixed-step/interpolation good/bad pair in `SKILL.md` is a minimized application of this article.
  It is a foundational explanatory article, not evidence that every game needs the same tick rate.
- Erin Catto, Box2D,
  [Simulation documentation](https://box2d.org/documentation/md_simulation.html) — current official
  engine contract for fixed stepping, substeps, post-step event buffers, order-sensitive operations,
  opaque IDs, and Box2D's stated determinism properties. Its numeric timestep/substep recommendations
  are Box2D-specific and are not made universal here.

## Commands, events, identity, and replay

- Nystrom, [Command](https://gameprogrammingpatterns.com/command.html) — practitioner basis for
  mapping raw input to executable requests and enabling queued, logged, AI-generated, or replayed
  actions. The tick-command good/bad pair in `SKILL.md` applies its input indirection while adding the
  fixed-tick boundary from Fiedler; animation-after-acceptance is this catalog's state-authority
  conclusion.
- Nystrom, [Event Queue](https://gameprogrammingpatterns.com/event-queue.html) — practitioner basis
  for temporal decoupling, plus the costs of global state, queued references, feedback loops, and
  unspecified timing. The package therefore prefers direct calls for required immediate results and
  bounded events for committed facts rather than prescribing events everywhere.
- Catto, [Replay](https://box2d.org/posts/2026/06/replay/) (6 June 2026) — maintainer implementation
  account for recording initial snapshots and mutating operations, validating state hashes, using
  generation-bearing index handles, and recognizing that engine determinism does not make application
  code deterministic. The article describes Box2D v3.2 work and its own snapshot limitations; it is
  evidence for architecture tradeoffs, not a portable replay API.
- Catto, [Determinism](https://box2d.org/posts/2024/08/determinism/)
  (19 August 2024) — maintainer basis for stable ordering, compiler/floating-point considerations,
  multithreaded result ordering, and continual determinism tests. Those techniques show what a
  cross-platform claim must control; they do not establish that arbitrary engines are deterministic.

## Host engines and save boundaries

- Apple,
  [GameplayKit entities and components](https://developer.apple.com/library/archive/documentation/General/Conceptual/GameplayKit_Guide/EntityComponent.html)
  — archived official documentation corroborating engine-owned update/render cycles and deliberate
  per-component update order. It documents an Apple framework pattern, not a requirement to use ECS.
- Godot,
  [Idle and physics processing](https://docs.godotengine.org/en/stable/tutorials/scripting/idle_and_physics_processing.html)
  — current official example of an engine exposing variable presentation processing separately from
  fixed physics processing. Exact callbacks and rates are Godot-specific.
- Microsoft,
  [Save games for Xbox and Windows](https://learn.microsoft.com/en-us/gaming/gdk/docs/features/common/game-save/game-saves)
  — official platform contract illustrating asynchronous storage, synchronization, lifecycle, and
  platform-specific durability responsibilities. It supports treating save I/O as an adapter and
  checking the target platform; it is not a universal file API.
- SQLite,
  [Atomic commit](https://www.sqlite.org/atomiccommit.html) — implementation-level explanation of
  staging, flushing, and atomic replacement/journaling needed to survive interrupted writes. Filesystem
  and platform guarantees vary, so the package requires verification rather than assuming `rename`
  alone is durable everywhere.

## Local synthesis boundaries

- The technical-loop phase ordering combines Nystrom's loop/update patterns, Fiedler's accumulator,
  and Box2D's post-step/event ordering. The exact gameplay-system order remains a game-specific
  contract.
- Stable generation handles combine Nystrom's collection-mutation trap with Catto's documented
  index-and-generation replay handles.
- Save/replay separation is this catalog's architectural conclusion: the replay sources require
  execution inputs and determinism, while durable storage sources require recoverable versioned state.
