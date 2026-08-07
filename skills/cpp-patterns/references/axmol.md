# Axmol

Read this when working on a game built on the Axmol engine.

Axmol is a C++20, multi-platform 2D engine — a fork of Cocos2d-x v4.0, launched November 2019,
targeting Windows, macOS, Linux, iOS, Android, tvOS, Xbox (UWP) and WebAssembly, with Metal, Vulkan,
D3D11/12 and OpenGL backends.

**Version reality:** the **v2 line is LTS and in maintenance, with 2.11.x as its final release**; v3
is the development branch. A project pinned to v2.11.x is pinned to the end of that line — a
deliberate, stable place to be, but plan a v3 evaluation rather than expecting further v2 features.

## Contents

- [Setup and the pinned engine](#setup-and-the-pinned-engine)
- [Building with Ninja on macOS](#building-with-ninja-on-macos)
- [Memory: reference counting, not smart pointers](#memory-reference-counting-not-smart-pointers)
- [Resolution, and the rect you must use](#resolution-and-the-rect-you-must-use)
- [Scene graph traps](#scene-graph-traps)
- [Shaders and axslcc](#shaders-and-axslcc)
- [Logging](#logging)
- [Coming from Cocos2d-x](#coming-from-cocos2d-x)
- [Keep the engine out of your core](#keep-the-engine-out-of-your-core)

## Setup and the pinned engine

Treat the engine as a **pinned submodule you never edit**.

```sh
git submodule update --init
( cd axmol && ./setup.ps1 )      # needs PowerShell (pwsh)
```

`setup.ps1` fetches the gitignored tools directory, including **`axslcc`**, the shader compiler. A
fresh clone without it fails to configure with *"axslcc not found"* — the single most common
first-day error.

**Never edit anything under the engine directory.** Every engine-specific fix belongs in your own
top-level `CMakeLists.txt`. That is what keeps an engine bump to a tag checkout plus a pointer, with
nothing to reconcile. Re-run `setup.ps1` after switching branches; a branch/tool mismatch is a
documented source of axslcc errors.

## Building with Ninja on macOS

**Use the Ninja generator**, not Xcode and not the `axmol build` console wrapper — the wrapper
hardcodes generator and target assumptions that will not match a custom project layout, and the Xcode
generator has failed to detect the compiler on recent Xcode versions.

The catch: **Axmol applies several build settings only under the Xcode generator.** Under Ninja they
are missing, so the app fails to compile or configures and then crashes on launch. Four fixes belong
in your own `CMakeLists.txt`:

1. **Point `AXSLCC_EXE` at the vendored binary** in the engine's tools directory, or a plain `cmake`
   invocation cannot find the shader compiler.
2. **`-fobjc-weak` on the engine core target.** The engine sets `CLANG_ENABLE_OBJC_WEAK` only via
   Xcode; without it the AVFoundation media code's `__weak` fails to compile.
3. **Embed and ad-hoc-codesign `soft_oal.framework`** into `.app/Contents/Frameworks` in a
   `POST_BUILD` step — the engine does this only via Xcode, and without it launch crashes on
   `@rpath/soft_oal.framework`. Stamp `CFBundleIdentifier` in the same step: under Ninja the plist
   otherwise keeps the literal `$(PRODUCT_BUNDLE_IDENTIFIER)`.
4. **`-Wno-deprecated-declarations` on your game target only** — the engine calls its own deprecated
   context-attribute initializer from a header you include. Scope it to the game target so your other
   libraries keep full warnings and the engine's flags are untouched.

The first build compiles the whole engine and takes minutes; every rebuild after is a fast relink of
your own code — provided the build directory is not being raced. See
[`build-loop-traps.md`](build-loop-traps.md), which is largely written from this stack.

## Memory: reference counting, not smart pointers

**This is the biggest adjustment for a modern C++ developer.** Axmol inherits Cocos2d-x's
`Ref`-derived intrusive reference counting, and the engine's FAQ is explicit that **no smart pointers
are planned**. So inside the engine's object graph you are in a manual lifecycle, not RAII.

The model:

- `create()` factory methods return an **autoreleased** object — it will be released at the end of
  the current frame unless something retains it.
- `addChild()` retains. Removing from the parent releases.
- Holding an engine object as a member beyond the frame means `retain()`, and a matching `release()`
  in your destructor.
- A `Node*` you stored and did not retain may be dead. A node removed from its parent may be
  destroyed immediately.

The practical discipline:

- **Let the scene graph own scene-graph objects.** Add them as children and reach for them through the
  parent, rather than caching raw `Node*` across frames.
- **Where you must cache, retain — and pair every retain with a release.**
- **Keep your own domain types out of this model entirely.** Your simulation, data structures, and
  logic should be ordinary modern C++ with `unique_ptr` and RAII; only the presentation layer touches
  `Ref`. That boundary is what stops the engine's memory model spreading through the codebase.
- Never `delete` an engine object.

## Resolution, and the rect you must use

The single most productive source of layout bugs.

`Director::getVisibleSize()` returns the **design** resolution rect. When a design resolution policy
(such as SHOW_ALL) is pinned for stable metrics, the actual window can be **wider than** that rect
and its origin can be **negative** — the letterbox inverted into design space.

So on an ultra-wide window, or after some resizes:

- Camera frustum, zoom limits, and pan clamps computed from `getVisibleSize()` permit positions that
  leave visible void past the world edge, because the real camera rect is larger.
- HUD placement, world camera, and hit-testing computed from *different* rects disagree, so clicks
  land in the wrong place.

**Rules:**

- **Decide one full-frame rect and use it for the camera, the HUD, and hit-testing alike.** Three
  systems using two rects is the bug.
- Clamp zoom and pan against the *actual* camera rect, not the design size, and do not assume origin
  zero.
- **Never make the design resolution track the live window frame.** It reads as the obvious fix for a
  layout that is wrong at one size, and it breaks HUD docking at scene start, because the frame is not
  final when the scene builds.
- **"Wrong on first paint, correct after a resize" means state captured too early** — not a maths
  error. Measure when the value is actually available rather than theorising about the formula.
- On Retina/HiDPI, content scale factor breaks pixel-exact sprite tiling. Account for it explicitly
  rather than nudging offsets until it looks right at one scale.

## Scene graph traps

**A `ClippingNode` nested inside another `ClippingNode` blanks the HUD.** This one is worth stating
loudly because it has been hit independently in more than one project. The inner clip's stencil masks
everything drawn *after* it: the inner content appears and the rest of the interface vanishes.

The case that produces it is ordinary — a region clipped to a shape (a dock silhouette), containing a
widget that needs its own rounding (a rounded minimap).

**Fix: self-clipping content goes in a sibling overlay, never inside a region clip.** Consider
`ClippingRectangleNode` for the simple rectangular case; it does not use the stencil buffer.

Other node-level traps:

- **`DrawNode` has no anti-aliasing.** Vector UI drawn with it has jagged corners, and the fix is
  MSAA, not more segments. Watch for coincident vertices, which the triangulator rejects.
- **Nearest-neighbour filtering muddies detailed icons.** Choose the filter per texture class:
  nearest for pixel art, linear for icons and photographic content.
- **Event listener signatures are version-specific.** In v2.11.x, `EventListenerMouse` callbacks
  (`onMouseMove`, `onMouseDown`, `onMouseUp`, `onMouseScroll`) return **`bool`**, not `void` — a
  lambda written against the older signature fails to compile. Return `false` for "not consumed",
  `true` for "consumed", and never fall off the end.
- **Android multi-touch**: with three or more simultaneous points, the system may intercept the
  gesture, so `touchEnd`/`touchCancel` never fires. Do not build state that assumes a matching end.

## Shaders and axslcc

- **`#version` must be the first line of a shader.** Not the first *code* line — the first line. A
  leading comment breaks compilation.
- **`axslcc` supports `#include`.** Use it. Shader logic duplicated across `.frag` files **will**
  drift; the copies diverge and only one gets the fix.
- **Guard colour transforms by texel coverage under premultiplied alpha**, or transparent texels pick
  up colour and the sprite grows a halo.
- Shader-compiler errors after a branch switch or engine bump are usually a tools mismatch: re-run
  `setup.ps1`.
- Verify visual output **against the live window**, never an offline composite. A composite proves
  the generator works, not that the engine draws it that way.

## Logging

Since v2.1.3, use the fmtlib-style macros — `AXLOGD`, `AXLOGI`, `AXLOGW`, `AXLOGE` — which format
directly and need no `.c_str()` conversion. The older `AXLOG` required `.c_str()` for `std::string`
and `.data()` for `std::string_view`.

## Coming from Cocos2d-x

- The namespace is **`ax`**; `USING_NS_CC` becomes `USING_NS_AX`.
- A compatibility header maps old names, which eases migration but should not be a destination —
  update to Axmol naming over time.
- Cocos2d-x types that duplicate the standard library are deprecated: use `std::string`, not `CCString`.
- An official `axmol-migrate` tool exists for Cocos2d-x **v4.0** projects. Older 3.x projects may not
  convert at all.
- Adding a new source file to a template project that globs its sources needs a regenerate
  (`axmol build … -f`) before it appears; a project with explicitly listed sources does not.

## Keep the engine out of your core

The structural rule that makes everything above manageable:

```text
sim/    pure C++ — no engine headers. Deterministic, unit-testable, fast to build.
render/ maps simulation meaning onto engine primitives.
game/   thin: wiring, scenes, input.
tests/  links the pure core alone.
```

Two payoffs, both large:

1. **The test target is an architecture tripwire.** Because `tests/` links only the pure core, the day
   an engine include leaks into it the tests stop linking and the build goes red. Fix that by removing
   the include, **never** by linking the engine into tests.
2. **A headless configuration builds no engine at all**, so the test loop is seconds rather than
   minutes, and it produces no application bundle — which avoids the duplicate-artifact trap in
   [`build-loop-traps.md`](build-loop-traps.md).

Keep pixels, colours, sprite names, and engine types out of the core; the core exposes *meaning* and
the render layer maps meaning to pixels.

## Sources

- [Axmol](https://github.com/axmolengine/axmol) — C++20, platforms, backends, v2 LTS and v3 status
- [Axmol FAQ](https://github.com/axmolengine/axmol/wiki/FAQ) — reference counting with no smart pointers planned, axslcc troubleshooting, `AXLOGD`-family logging, glob regeneration, Android multi-touch
- [Cocos2d-x migration guide](https://github.com/axmolengine/axmol/wiki/Cocos2d%E2%80%90x-migration-guide) — the `ax` namespace, renamed types, deprecated Cocos types, `axmol-migrate`
- [Axmol vs Cocos2d-x](https://github.com/axmolengine/axmol/wiki/Axmol-vs-Cocos2d%E2%80%90x) · [Axmol manual](https://axmol.dev/manual/latest/) · [DevSetup](https://github.com/axmolengine/axmol/blob/dev/docs/DevSetup.md)
- The Ninja/macOS build fixes, resolution-rect, `ClippingNode`, `DrawNode`, mouse-callback and shader
  items were recorded across two independent Axmol v2.11.x game projects during development. The
  `ClippingNode` stencil trap and the full-frame-rect rule were each hit in **both**, which is why
  they are stated as engine behaviour rather than project quirks.
