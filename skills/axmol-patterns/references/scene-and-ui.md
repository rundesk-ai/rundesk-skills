# Scene graph and UI

Read this for nodes, layout, resolution, input, and the interface layer. Almost every layout bug on
this engine is one of two things: **the wrong rect**, or **a stencil conflict**.

## Contents

- [Resolution: the rect you must use](#resolution-the-rect-you-must-use)
- [Clipping](#clipping)
- [Node lifecycle](#node-lifecycle)
- [Drawing vector UI](#drawing-vector-ui)
- [Input](#input)
- [Physics and content size](#physics-and-content-size)
- [Diagnosing a layout bug](#diagnosing-a-layout-bug)

## Resolution: the rect you must use

**`Director::getVisibleSize()` returns the design resolution rect, not the window.**

When a design resolution policy such as SHOW_ALL is pinned for stable metrics, the actual window can
be **wider than** that rect, and its origin can be **negative** — the letterbox inverted into design
space. So on an ultra-wide display, or after certain resizes:

- A camera frustum widened to the physical frame is larger than `getVisibleSize()`. Zoom limits and
  pan clamps computed from the design size then permit positions that show void past the world edge.
- HUD placement, world camera, and hit-testing computed from *different* rects disagree, and clicks
  land somewhere other than where the user aimed.

**Rules:**

- **Decide one full-frame rect and use it for the camera, the HUD, and hit-testing alike.** Three
  systems and two rects is the bug. Compute it once and pass it.
- Clamp zoom and pan against the **actual** camera rect. Do not assume origin zero.
- **Never make the design resolution track the live window frame.** It reads as the obvious fix for a
  layout that is wrong at one size, and it breaks HUD docking at scene start, because the frame is not
  final when the scene builds.
- On Retina/HiDPI, the content scale factor breaks pixel-exact sprite tiling. Handle it explicitly
  rather than nudging offsets until one scale looks right.

**"Wrong on first paint, correct after a resize" means state captured too early** — not a formula
error. Measure when the value is actually available. Resist theorising about the arithmetic; log the
rect at each stage and find where it is still provisional.

## Clipping

**A `ClippingNode` nested inside another `ClippingNode` blanks the surrounding UI.** The inner clip's
stencil masks everything drawn *after* it: the inner content appears and the rest of the interface
vanishes.

The case that produces it is entirely ordinary — a region clipped to a shape (a dock silhouette or a
panel with a curved edge) containing a widget that needs its own rounding (a rounded minimap, an
avatar, a progress ring).

**Fix: self-clipping content goes in a sibling overlay, never inside a region clip.** Position the
overlay to match, and keep the two clips as siblings so neither stencil sees the other.

For a plain rectangular clip, prefer **`ClippingRectangleNode`** — it uses the scissor rect rather
than the stencil buffer, so it does not participate in this conflict at all.

## Node lifecycle

- `init()` runs at construction; `onEnter()` when the node joins a running scene; `onExit()` when it
  leaves; `onEnterTransitionDidFinish()` after a scene transition completes.
- **Do not assume the frame or parent size is final in `init()`.** It frequently is not, which is the
  root of the first-paint problem above. Measure in `onEnter` or later.
- `scheduleUpdate()` registers a per-frame `update(float dt)`. Unschedule in `onExit`, or use
  `scheduleOnce`/`schedule` with an explicit key you can cancel.
- Anything you schedule, listen for, or retain must be undone when the node leaves. A listener
  outliving its node fires into a destroyed object.
- **Z-order is per-parent**, so a high local Z does not lift a node above a sibling subtree. Reparent
  instead of fighting it.

## Drawing vector UI

- **`DrawNode` has no anti-aliasing.** Vector UI drawn with it has jagged edges, and the fix is
  **MSAA**, not more segments. Adding segments costs vertices and does not fix the aliasing.
- Watch for **coincident vertices** — the triangulator rejects them, and the failure presents as a
  shape that silently does not draw.
- For anything reusable, a nine-patch sprite or a texture beats generated geometry: it batches, it
  anti-aliases for free, and it is art-directable without a rebuild.

## Input

- **Event listener signatures are version-specific.** In v2.11.x, `EventListenerMouse` callbacks
  (`onMouseMove`, `onMouseDown`, `onMouseUp`, `onMouseScroll`) return **`bool`**, not `void` — a lambda
  written against the older signature will not compile. Return `false` for "not consumed", `true` for
  "consumed", and never fall off the end.
- **The whole input system is replaced in v3** — `EventListenerTouch` and `EventListenerMouse` give
  way to a unified `PointerEventListener`. See [`migration.md`](migration.md) before writing input
  code you intend to carry forward.
- Remove listeners in `onExit`, or use the node-bound registration so the engine does it.
- **Android multi-touch**: with three or more simultaneous points the system may intercept the
  gesture, so `touchEnd`/`touchCancel` never fires. Do not build state that assumes a matching end
  event — time it out or reconcile on the next down.
- Decide deliberately between owner-driven hit-testing and native widget clicks. Mixing them is what
  makes a modal that does not actually block the layer underneath.

## Physics and content size

If you use the physics integration, one documented constraint governs the scene graph:

> **"The content size of a sprite cannot be changed after the physics object is set on a node."**

So `setContentSize()` with different dimensions after attaching a body is prohibited, and **animation
frames must be the same size**. Scaling, rotating and translating are fine.

Enable with `AX_ENABLE_CHIPMUNK_INTEGRATION 1` or `AX_ENABLE_BOX2D_INTEGRATION 1`. The integration API
uses Chipmunk2D internally by default; note that direct `PhysicsSpriteChipmunk2D` use is **deprecated
and removed in v3**.

## Diagnosing a layout bug

1. **Log the rect** — design size, visible size, window frame, camera rect — at `init`, `onEnter`, and
   after the first frame. The stage where they diverge is the answer.
2. **Is it wrong only at one window size or after a resize?** A rect problem.
3. **Did an entire region disappear when you added a rounded widget?** The clipping trap.
4. **Wrong on first paint, right after a resize?** State captured too early.
5. **Clicks landing in the wrong place?** Hit-testing is using a different rect from rendering.
6. Verify against the **live window**. An offline composite cannot show any of these.

## Sources

- [Axmol FAQ](https://github.com/axmolengine/axmol/wiki/FAQ) — Android multi-touch gesture interception
- [2D physics engines](https://github.com/axmolengine/axmol/wiki/2D-Physics-Engines-Information) — the content-size constraint, quoted, and the integration flags
- [Migration guide for PR 3173](https://github.com/axmolengine/axmol/wiki/Migration-Guide-for-PR-3173) — the v3 input rewrite
- [Axmol manual](https://axmol.dev/manual/latest/) · [cpp-tests](https://github.com/axmolengine/axmol) — runnable examples of every subsystem
- The resolution-rect rule, the `ClippingNode` stencil conflict, the `DrawNode` anti-aliasing point,
  and the v2.11.x mouse-callback signature were recorded across two independent Axmol projects. The
  first two were hit in **both**, which is why they are stated as engine behaviour.
