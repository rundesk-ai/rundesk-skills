# Axmol source basis

This package is a Rundesk synthesis of the Axmol engine's own documentation plus failures recorded
during real development on it. Use this file to audit or update any claim.

**Read in this order of authority.** The engine wiki states what the engine does; GitHub Discussions
is where problems get solved; recorded project experience supplies the traps no page lists.

**Version facts, checked against the
[releases API](https://api.github.com/repos/axmolengine/axmol/releases) on 7 August 2026** rather than
against documentation prose:

| Fact | Value |
|---|---|
| Latest v2 release | **v2.11.4**, published 2026-07-06 |
| Preceding | v2.11.3 (2026-02-23), v2.11.2 (2026-01-15), v2.11.1, v2.11.0 (2025-12-19) |
| Line status | v2 is LTS in maintenance; **2.11.x is its final minor**. v3 is the development branch |

Re-check with:

```sh
curl -sS 'https://api.github.com/repos/axmolengine/axmol/releases?per_page=5' \
  | python3 -c 'import sys,json;[print(r["tag_name"], r["published_at"][:10]) for r in json.load(sys.stdin)]'
```

Where a claim below is marked as recorded experience rather than documentation, treat it as evidence
from practice — strong where it was reproduced independently, weaker where it was seen once.

## Engine documentation

- [Axmol](https://github.com/axmolengine/axmol) — what the engine is, C++20 requirement, supported
  platforms (Windows, macOS, Linux, iOS, Android, tvOS, Xbox/UWP, WebAssembly), render backends
  (Metal, Vulkan, D3D11/12, OpenGL), and the v2 LTS versus v3 development split.
- [Axmol wiki](https://github.com/axmolengine/axmol/wiki) — the documentation index.
- [FAQ](https://github.com/axmolengine/axmol/wiki/FAQ) — `setup.ps1` and the PowerShell execution
  policy, axslcc troubleshooting after a branch switch, reference counting kept for historical
  reasons with standard smart pointers not planned for the engine API, the `AXLOG` → `AXLOGD` change
  at v2.1.3, glob regeneration with `-f`, and Android intercepting 3+ point gestures so
  `touchEnd`/`touchCancel` never fires.
- [Memory Management](https://github.com/axmolengine/axmol/wiki/Memory-Management) — **the most
  important page for a newcomer.** `retain`/`release` pairing, the autorelease pool draining once per
  main-loop cycle, `create()` conventions, parents retaining children, the documented leak and
  dangling scenarios, `ax::RefPtr<T>`, `ax::Vector`/`ax::Map`, the `AX_SAFE_*` macros, and
  `AX_REF_LEAK_DETECTION` with `Object::printLeaks()`.
- [Shaders in Axmol 2.x](https://github.com/axmolengine/axmol/wiki/Shaders-in-Axmol-2.x) — axslcc as a
  `glslcc` fork, ESSL v310 / GLSL v450, the `.vsh`/`.fsh` → `_vs`/`_fs` naming, the `custom/` prefix
  and `ProgramManager::loadProgram`, **both uniform constraints** (all non-sampler uniforms in a
  block; one block per stage for Metal), and **custom shaders disabling auto-batching** unless
  `ProgramState::updateBatchId()` is called.
- [Shaders in Axmol 3](https://github.com/axmolengine/axmol/wiki/Shaders-in-Axmol3) — the v3 pipeline.
- [Sprite Sheets: Tools and Formats](https://github.com/axmolengine/axmol/wiki/Sprite-Sheets-Tools-and-Formats) —
  PLIST v3, the `SpriteSheetLoader` interface, the recommended packers, and the requirement that frame
  names be unique across atlases with prefixing or subdirectories as the fix.
- [SDF text rendering](https://github.com/axmolengine/axmol/wiki/SDF-text-rendering) — the outline
  ranges and that spread lives in `FontFreeType.cpp` while the scale lives in the shader, so changing
  one means changing both.
- [2D Physics Engines](https://github.com/axmolengine/axmol/wiki/2D-Physics-Engines-Information) — the
  three options, the `AX_ENABLE_*_INTEGRATION` flags, the deprecation and v3 removal of
  `PhysicsSpriteChipmunk2D`, and the constraint that content size cannot change after a physics body
  is attached.
- [Extensions](https://github.com/axmolengine/axmol/wiki/Extensions) — the full list with default
  states, the 2.1.3 all-off-then-opt-in change, per-extension CMake flags, and DragonBones and the
  legacy GUI extension being deprecated.
- [Particle System](https://github.com/axmolengine/axmol/wiki/Particle-System) ·
  [Tiled](https://github.com/axmolengine/axmol/wiki/Tiled) ·
  [Media Player](https://github.com/axmolengine/axmol/wiki/Media-Player) ·
  [Protecting image assets](https://github.com/axmolengine/axmol/wiki/Protecting-image-assets).
- [DevSetup](https://github.com/axmolengine/axmol/blob/dev/docs/DevSetup.md) ·
  [Axmol manual](https://axmol.dev/manual/latest/).

## Migration

- [Cocos2d-x migration guide](https://github.com/axmolengine/axmol/wiki/Cocos2d%E2%80%90x-migration-guide) —
  `ax` namespace and `USING_NS_AX`, the compatibility header, renamed types, deprecated Cocos types in
  favour of the standard library, and `axmol-migrate` targeting v4.0 only with 3.x and older possibly
  not working at all.
- [Migration Guide for PR 3173](https://github.com/axmolengine/axmol/wiki/Migration-Guide-for-PR-3173) —
  **the largest v3 change.** The complete removal table: `Touch`/`EventTouch`/`EventMouse` →
  `PointerEvent`, the listener classes → `PointerEventListener`, `IMEDispatcher` → `InputSystem` +
  `InputDelegate`, `TextFieldTTF`/`UITextField` → `InputField`, `EventListenerKeyboard` →
  `KeyboardEventListener`, and `Label::create()` unified.
- [Axmol vs Cocos2d-x](https://github.com/axmolengine/axmol/wiki/Axmol-vs-Cocos2d%E2%80%90x) ·
  [SpriteKit to Axmol](https://github.com/axmolengine/axmol/wiki/SpriteKit-to-Axmol) ·
  [Update guide to v2.3.0 for Android](https://github.com/axmolengine/axmol/wiki/Update-guide-to-v2.3.0-for-Android).

## Community: where problems get solved

**[GitHub Discussions](https://github.com/axmolengine/axmol/discussions) is the engine's designated
place for questions**, and it is where several things live that the wiki does not cover. Search it
before assuming a problem is yours.

- [Axmol build time improvement (#1814)](https://github.com/axmolengine/axmol/discussions/1814) —
  iOS builds of 7–15 minutes with a full rebuild on a one-line change; **ccache reported to bring
  that to 52 seconds to ~1m20**. Maintainers declined to bundle it (not Axmol-specific, maintenance
  burden) and agreed to document it as a workaround. The maintainer also narrows the full-rebuild
  behaviour to **Xcode builds specifically** — "it does not happen when creating Windows or Android
  builds."
- [Axmol v3 roadmap (#2650)](https://github.com/axmolengine/axmol/discussions/2650) — the removals
  and platform moves summarized in [`migration.md`](migration.md): Chipmunk, GLES 2.0, `Color3B`,
  tolua, `ghc::filesystem`; C++23, Box2D v3, JoltPhysics, D3D12/Vulkan, OpenXR, ARM64. A discussion
  thread, so intent rather than contract — but it tells you what not to build new code against.
- [Using Axmol as a replacement engine (#1129)](https://github.com/axmolengine/axmol/discussions/1129) —
  a practitioner account of migrating from Cocos2d-x 3.17.2, and how different the build system is.

## Community and learning resources

The engine's own [Tutorials page](https://github.com/axmolengine/axmol/wiki/Tutorials) is the curated
index. The individual resources, linked directly:

- [Introduction to Game Dev using Axmol](https://github.com/axmolengine/axmol/wiki/Introduction-to-Game-Dev-using-Axmol) —
  the beginner entry point.
- **Code & Web** — third-party tutorials written against Axmol specifically:
  [Axmol + TexturePacker](https://www.codeandweb.com/texturepacker/tutorials/axmol) ·
  [a physics-enabled game with PhysicsEditor](https://www.codeandweb.com/physicseditor/tutorials/how-to-create-a-physics-enabled-game-with-axmol-engine) ·
  [animations and sprite sheets](https://www.codeandweb.com/texturepacker/tutorials/animations-and-spritesheets-in-axmol-engine) ·
  [2D dynamic light effects](https://www.codeandweb.com/spriteilluminator/tutorials/how-to-use-light-effects-with-axmol-engine).
- [How to port a Cocos2d-x game to Axmol](https://anivalegames.com/2023/03/04/how-to-port-cocos2d-x-game-to-axmol-game-engine/) —
  Anivale Games. A first-hand porting account rather than a guide.
- [Android Studio setup walkthrough](https://www.youtube.com/watch?v=cr_lJovFaDI) — Real Gear Inc.
- [Options for handling EGL context loss on Android](https://github.com/axmolengine/axmol/wiki/Options-for-handling-EGL-Context-loss-on-Android) —
  a platform failure mode worth reading before it happens rather than after.
- [Adding external libraries and frameworks](https://github.com/axmolengine/axmol/wiki/Adding-External-Libraries-and-Frameworks).
- [AxmolSteamInput](https://github.com/rudiHammad/AxmolSteamInput) — a community integration.
- [cpp-tests as a WebAssembly build](https://axmol.netlify.app/wasm/cpp-tests/cpp-tests), with source
  in the repository. **The most useful reference in practice**, because every subsystem has a runnable
  example you can read and diff against your own.
- For the surrounding skills the page recommends [LearnCpp](https://www.learncpp.com/),
  [cppreference](https://en.cppreference.com/), the
  [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines), the CMake
  tutorials, and [The Book of Shaders](https://thebookofshaders.com/). Those belong to `cpp-patterns`.

## Recorded project experience

Not in any engine document. Recorded during development of two independent 2D games on **Axmol
v2.11.x** with CMake and Ninja on macOS, carried here generalized:

**Reproduced in both projects — stated as engine behaviour:**

- **A `ClippingNode` nested inside another `ClippingNode` blanks the surrounding UI.** The inner
  stencil masks everything drawn after it. Reached from an ordinary case: a shaped region containing
  a widget that needs its own rounding.
- **`Director::getVisibleSize()` is the design rect, not the window.** Camera, HUD and hit-testing
  must share one full-frame rect, which can be wider than the design size and have a negative origin.

**Recorded once:**

- **Four Xcode-only build settings must be reproduced** in the project's own CMake for a Ninja build
  on macOS to compile and launch: the vendored `AXSLCC_EXE` path, `-fobjc-weak` on the engine core,
  the `soft_oal.framework` embed plus ad-hoc codesign and `CFBundleIdentifier` stamp, and
  `-Wno-deprecated-declarations` scoped to the game target.
- **`EventListenerMouse` callbacks return `bool`** in v2.11.x, not `void`.
- **A shader's `#version` must be the first line** — a leading comment breaks compilation.
- **Shader logic duplicated across `.frag` files drifts**; share it with `#include`.
- **Guard colour transforms by texel coverage under premultiplied alpha**, or edges halo.
- **Nearest filtering muddies detailed icons** — choose the filter per texture class.
- **Design resolution must not track the live window frame**; it breaks HUD docking at scene start.
- **"Wrong on first paint, correct after resize" is state captured too early**, not a formula error.
- **`DrawNode` has no anti-aliasing** — the fix is MSAA, not more segments; watch for coincident
  vertices.
- **Verify against the live window, never an offline composite**, and **enumerate a combinatorial
  surface rather than sampling it** — scene-sampled seam verification never converges.
- **A valid atlas with a drifting manifest schema still becomes the fallback** — generate the loader
  contract alongside the asset.

Build-loop failures from the same projects — Ninja concurrency, duplicate macOS bundles, piped exit
codes, ODR from rapid header edits, ctest hiding a passing test's stdout — are in `cpp-patterns` →
`build-loop-traps.md`, because they are general to CMake and Ninja rather than specific to this
engine.

## What this package deliberately does not cite

- Cocos2d-x documentation for APIs. Useful for concepts; the APIs have diverged.
- Tutorials predating the v2 line without saying so.
- Performance claims with no measurement.
