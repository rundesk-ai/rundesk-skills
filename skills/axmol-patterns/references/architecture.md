# Architecture

Read this when structuring a game on Axmol, or when the engine has started appearing in places it
should not.

## The one rule

**Keep the engine at the edge.** Everything that is not presentation should compile without it.

```text
sim/     pure C++ — no engine headers. Deterministic, unit-testable, seconds to build.
render/  maps simulation meaning onto engine primitives.
game/    thin: scenes, wiring, input.
ui/      widgets and layout.
tests/   links the pure core ALONE.
```

The direction is one-way: `game` → `render` → `sim`. The simulation exposes **meaning** — a surface
type, a state, a quantity — and the render layer maps meaning to pixels. No pixels, colours, sprite
names, or engine types below the render seam.

## Why this pays, concretely

**1. The test target becomes an architecture tripwire.**

Because `tests/` links only the pure core, the day an engine include appears in `sim/` the tests stop
linking and the build goes red. A rule in a document drifts; a target that will not link does not.

**Fix a red tests build by removing the offending include — never by linking the engine into tests.**
That disarms the tripwire permanently, and it is the tempting fix precisely because it is one line.

**2. The test loop is seconds, not minutes.**

A headless configuration that builds only the core and its tests compiles **no engine at all**:

```sh
cmake -B build/tests -G Ninja -DHEADLESS_ONLY=ON
cmake --build build/tests && ./build/tests/tests/core_tests
```

This is the difference between running tests on every change and running them before a commit.

**3. It produces no application bundle.**

Which sidesteps the duplicate-bundle trap entirely — on macOS, two build directories producing an
`.app` with the same bundle identifier means `open` can launch the wrong one. See `cpp-patterns` →
`build-loop-traps.md`.

**4. The simulation is testable at all.**

Engine objects need a director, a scene, a running loop, and a graphics context. Pure types need none
of that, so their tests are fast, deterministic, and runnable in CI without a display.

**5. Two memory models stay separated.**

The engine is reference-counted; your own types should be `unique_ptr` and RAII. That is workable
while the boundary is sharp and unmanageable when `Ref` leaks inward. See [`memory.md`](memory.md).

## Determinism in the simulation

If the game has a simulation worth the name, it is worth making deterministic — it makes bugs
reproducible, replays possible, and tests meaningful.

- **Seed every RNG explicitly** and thread it through; never call a global `rand()`.
- **Never let sim-affecting iteration order depend on a hash container.** `unordered_map` order varies
  between runs and platforms. Use an ordered container, or sort before iterating.
- Keep floating-point behaviour consistent, or use integers/fixed point for anything that must
  reproduce exactly across platforms.
- **No wall-clock reads in the simulation.** Time is an input the caller supplies.
- No engine calls, so no frame-rate dependence sneaking in through the render layer.

A deterministic core plus a byte-identical regeneration check is what makes a large refactor
trustworthy: regenerate, compare hashes, and the diff is the answer.

## Working with the scene graph

- Let the tree own scene-graph objects. Reach for a node through its parent rather than caching a raw
  pointer across frames.
- Give a scene one owner for its state. A node that reads another node's members through a stored
  pointer is coupling you will not be able to unpick.
- Keep scene construction declarative and short; push logic into your own types where it can be
  tested.
- Node-level `update()` is the presentation tick. **Advance the simulation with an explicit,
  fixed-size step** driven from one place, not from whichever nodes happen to be scheduled.

## Asset and content boundaries

- Runtime content and authoring artefacts are different things. Keep proofs, source art, and
  generation scratch **out of the runtime content directory** — anything under it ships, and anything
  that ships is something you have to keep working.
- Generate the loader's contract alongside the asset. A valid atlas with a drifting manifest schema
  still silently becomes the fallback, and the symptom appears far away as "the art didn't load."
- Check asset licensing before it is load-bearing. A build that depends on assets you cannot ship is a
  build that cannot ship; degrade gracefully to a placeholder so the dependency stays optional.

## Sources

- [Axmol](https://github.com/axmolengine/axmol) · [Extensions](https://github.com/axmolengine/axmol/wiki/Extensions) — what the engine brings, and what can be turned off
- `cpp-patterns` → `organization.md` for the general layering rule and how to enforce it with a target
- `cpp-patterns` → `build-loop-traps.md` for the duplicate-bundle and stale-artifact traps this layout avoids
- The tripwire target, the headless configuration, the determinism rules, and the asset-boundary
  points were recorded across two Axmol v2.11.x game projects.
