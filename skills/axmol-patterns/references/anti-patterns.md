# Axmol anti-patterns

Read this when reviewing Axmol code. Each row names the failure, not just the rule.

Language-level C++ anti-patterns are in `cpp-patterns`; this page is what the engine adds.

## Memory

| Don't | Do | Because |
|---|---|---|
| `delete` an engine object | `release()` | Other references still exist; the count is the truth |
| `new Sprite()` then `addChild` with no autorelease | `Sprite::create()` | Count never reaches zero — the documented leak |
| Store a raw `T*` to an engine object across frames | `ax::RefPtr<T>`, or reach through the parent | An autoreleased object you did not retain dies at end of frame |
| Hand-written `retain`/`release` in a member | `ax::RefPtr<T>` | The destructor becomes correct by construction |
| `std::vector<Node*>` of engine objects | `ax::Vector<Node*>` | The standard container will happily hold dead pointers |
| Let `Ref` types into the simulation layer | Keep them at the render seam | Two lifetime models everywhere, and nothing composes |
| Ship without ever enabling leak detection | `AX_REF_LEAK_DETECTION 1` in dev | A leak here shows after an hour of play, not in a short session |

## Scene and layout

| Don't | Do | Because |
|---|---|---|
| `getVisibleSize()` for camera or hit-testing | One shared full-frame rect | It is the design rect; the window can be wider, with a negative origin |
| Different rects for camera, HUD, hit-test | One rect, computed once, passed | Clicks land where nothing is drawn |
| Make the design resolution follow the window | Pin it | Breaks HUD docking at scene start |
| Nest a `ClippingNode` in a `ClippingNode` | Sibling overlay, or `ClippingRectangleNode` | The inner stencil blanks everything drawn after it |
| Measure layout in `init()` | `onEnter` or later | The frame is not final yet — this is "wrong on first paint" |
| Add segments to fix jagged `DrawNode` edges | MSAA | `DrawNode` has no anti-aliasing; segments cost vertices and fix nothing |
| Leave a listener or schedule registered at `onExit` | Unregister | It fires into a destroyed node |
| `setContentSize()` after attaching a physics body | Size it first; keep animation frames equal | Documented as prohibited |
| Assume a matching `touchEnd` | Time out and reconcile | Android intercepts 3+ point gestures |

## Graphics

| Don't | Do | Because |
|---|---|---|
| A comment above `#version` | `#version` on line one | Breaks compilation, with an error that does not say so |
| Non-sampler uniforms outside a uniform block | One block per stage | A spirv limit; and Metal supports only one block |
| Two uniform blocks in a stage | Merge them | Compiles on GL, fails on Metal |
| Copy shader logic between `.frag` files | `#include` — axslcc supports it | The copies drift and only one gets the fix |
| Apply a custom shader across many sprites and stop there | `ProgramState::updateBatchId()` where uniforms match | Custom shaders disable auto-batching; one draw call becomes hundreds |
| Unguarded colour transforms with premultiplied alpha | Guard by texel coverage | Transparent texels take colour — a halo at every edge |
| One global texture filter | Choose per texture class | Crisp pixel art and blurry icons in the same build |
| Reuse a frame name across atlases | Prefix or subdirectory at pack time | `SpriteFrameCache` is one namespace; one silently wins |
| Change the SDF spread without the shader scale | Change both together | They are one control split across two files |
| Verify visuals from an offline composite | Check the live window | A composite cannot show filtering, premultiply, scale factor, or batching effects |

## Build and project

| Don't | Do | Because |
|---|---|---|
| Edit anything under the engine directory | Fix it in your own `CMakeLists.txt` | An engine bump becomes a patch-reconciliation exercise |
| The Xcode generator, or `axmol build` | Ninja and plain `cmake` | Compiler detection failures, and wrapper assumptions that do not match a custom layout |
| Assume Ninja gets the Xcode-only settings | Reproduce all four in your own CMake | Fails to compile, or launches and crashes |
| Build every extension forever | Disable what you do not use | Build time, plus deprecated libraries still being archived |
| Debug a shader error after a branch switch | Re-run `setup.ps1` first | It is almost always a tools mismatch |
| Let more than one build directory produce an `.app` | Exactly one | Launch Services resolves by bundle id globally — you run the wrong binary |
| Investigate "the rebuild recompiles the engine" as a dependency problem | Reset the build directory | It is a raced or corrupted cache; see `cpp-patterns` |

## Migration

| Don't | Do | Because |
|---|---|---|
| Treat v2 → v3 as a version bump | Read the input-rewrite guide first | Touch/mouse/text-field APIs are all replaced |
| Scatter input handling across scenes | Funnel it through a few of your own types | It decides how large the v3 change is |
| Leave the Cocos compatibility header in place forever | Migrate names over time | You keep the mapping, and the divergence grows |
| Expect `axmol-migrate` to handle a 3.x project | Scope a rewrite of the affected layers | The tool targets v4.0; older "may not work at all" |
| Trust Cocos2d-x documentation for APIs | Use it for concepts only | Rendering, audio and platform support have genuinely diverged |

## Process

- **Don't verify a visual change yourself from a screenshot you composed.** The live window is the
  artifact.
- **Don't sample scenes to verify a combinatorial surface** — seams, tile pairs, adjacency. Enumerate
  the matrix and check it mechanically; sampling never converges because the untested pair is always
  the broken one.
- **Don't conclude a code bug before ruling out a stale build.** On this stack especially — see
  `cpp-patterns` → `build-loop-traps.md`.
- **Don't relitigate a rendering decision that has been proven in the live window.** Record it and
  move on.

## Sources

Every rule is cited in [`sources.md`](sources.md). The densest are the
[Axmol wiki](https://github.com/axmolengine/axmol/wiki) — memory management, shaders, sprite sheets,
physics, extensions, and the PR 3173 migration guide — plus failures recorded across two Axmol
v2.11.x projects.
