---
name: axmol-patterns
description: Use this skill when building, reviewing, debugging, or configuring a game on the Axmol engine — its reference-counted memory model, scene graph and node lifecycle, resolution and camera rects, event listeners, UI, sprite sheets, shaders and axslcc, physics, extensions, CMake and platform builds, or migrating from Cocos2d-x or between Axmol majors. Do not use it for general C++ questions with no engine involvement, or for another Cocos2d-x fork.
---

# Axmol patterns

Axmol is a C++20 cross-platform 2D engine — a fork of Cocos2d-x v4.0 — targeting Windows, macOS,
Linux, iOS, Android, tvOS, Xbox (UWP) and WebAssembly, over Metal, Vulkan, D3D11/12 and OpenGL.

Two things decide whether a codebase on it stays healthy: **respecting the reference-counting memory
model at the engine boundary**, and **keeping the engine out of everything that is not presentation**.
Most of this skill follows from those.

For the language underneath — RAII, lifetime, undefined behaviour, CMake, sanitizers, and the
build-loop traps that bite hardest on this stack — use `cpp-patterns`.

## Establish the version first

```sh
git -C axmol describe --tags        # the pinned engine
grep -rn 'AX_VERSION\|axmol' CMakeLists.txt | head
```

Checked against the releases API on **7 August 2026** — not against documentation prose, which lags:

| Line | Status |
|---|---|
| **v2 LTS** | Maintenance. Latest is **v2.11.4** (2026-07-06); **2.11.x is the final v2 minor** |
| **v3** | Development branch. It **replaces the entire input system** — see [`migration.md`](references/migration.md) |

**Check the pin against the latest patch.** A project sitting on an earlier 2.11.x is missing patch
releases within a line that will get no more minors — the cheapest upgrade available. Being at the end
of the v2 line is a legitimate choice; just make it knowingly, and read the v3 input changes before
planning that move, because they are larger than a version bump usually implies.

```sh
curl -sS 'https://api.github.com/repos/axmolengine/axmol/releases?per_page=5' \
  | python3 -c 'import sys,json;[print(r["tag_name"], r["published_at"][:10]) for r in json.load(sys.stdin)]'
```

## Work in this order

1. **Confirm the engine version and that `setup.ps1` has run.** A missing `axslcc` is the most common
   first-day failure, and a tools mismatch after a branch switch is the second.
2. **Decide which layer the change belongs in.** If it is not presentation, it should not include an
   engine header.
3. **Get ownership right at the engine boundary** — retain what you keep, let the scene graph own the
   rest.
4. **Verify visuals against the live window.** An offline composite proves the generator works, not
   that the engine draws it that way.
5. **Prove the build is not stale before believing a result.** See `cpp-patterns`'
   `build-loop-traps.md`, which was largely written from this stack.

## Rules that always hold

- **The engine directory is read-only.** Every engine-specific fix belongs in your own
  `CMakeLists.txt`, so an engine bump stays a tag checkout plus a pointer.
- **Never include an engine header in your simulation or domain layer.** Enforce it with a target that
  links the core alone — a documented rule drifts, a target that will not link does not.
- **Never `delete` an engine object.** `release()`, or let the scene graph do it.
- **A `retain()` must always be matched with a `release()`.** The engine's own wording.
- **`Director::getVisibleSize()` is the design rect, not the window.** Camera, HUD, and hit-testing
  must share one full-frame rect.
- **Never nest a `ClippingNode` inside another `ClippingNode`** — it blanks everything drawn after it.
- **A shader's `#version` must be the first line.** Not the first code line, the first line.
- **Verify against the live window**, never an offline render.

## Read the reference the task needs

| Area | Read for |
|---|---|
| [Setup and build](references/setup-and-build.md) | Submodule, `setup.ps1`, axslcc, Ninja on macOS, extensions, build times |
| [Memory](references/memory.md) | `Ref` counting, autorelease, `RefPtr`, `ax::Vector`/`Map`, leak detection |
| [Scene and UI](references/scene-and-ui.md) | Node lifecycle, resolution rects, clipping, `DrawNode`, event listeners |
| [Graphics](references/graphics.md) | Shaders and axslcc, uniform blocks, batching, sprite sheets, SDF text |
| [Architecture](references/architecture.md) | Keeping the engine at the edge, the tripwire target, headless tests |
| [Migration](references/migration.md) | Cocos2d-x → Axmol, and the v3 input-system rewrite |
| [Anti-patterns](references/anti-patterns.md) | The consolidated do / don't list |
| [Sources](references/sources.md) | The citation basis |

## Review output shape

```text
[HIGH] Engine header included in the simulation layer
Location: sim/include/sim/tile.h:12  — #include "axmol.h"
Why: the headless test target links simcore alone, so this breaks the tests build; more importantly
     it puts pixels in the layer that is supposed to expose meaning.
Fix: move the colour lookup into render/, and have tile.h expose the surface enum only.
Check: cmake --build build/tests — the tripwire links again.
```
