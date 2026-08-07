# Scene graph and UI

Read this for resolution policies, layout timing, clipping, input, and physics-sized nodes.

## HUD, camera, and hit tests disagree

**Cause:** frame size is in physical pixels while the scene normally works in design coordinates.
`getVisibleSize()` also depends on the resolution policy: in Axmol v2.11.4 it returns the design size
for policies other than `NO_BORDER`; `NO_BORDER` computes a cropped visible size and origin.

**Replace:** choose the resolution policy deliberately and use the resulting `getVisibleRect()` as
the scene-space contract. Convert input into that same space. Do not mix `getFrameSize()` values into
camera clamps or UI placement without an explicit conversion.

```cpp
const auto rect = director->getRenderView()->getVisibleRect();
layoutHud(rect);
camera.setBounds(rect);
```

**Prove:** log policy, frame size, design size, visible rect, and converted pointer coordinates at
startup and after resize on each aspect ratio. The earlier blanket rule that `getVisibleSize()` was
always the design rect and could have a negative origin was incorrect; the v2.11.4 implementation is
the authority.

## Adding a clip hides unrelated UI

**Cause:** `ClippingNode` uses stencil state, so failures can be backend-, ordering-, or stencil-depth
specific. Axmol's implementation and `NestedTest` explicitly support nested clipping; nesting alone
is not a valid diagnosis.

**Replace:** reduce the scene against the engine's nested clipping test. Use
`ClippingRectangleNode` for an axis-aligned rectangle because it uses scissoring rather than stencil;
otherwise inspect stencil order, inversion, alpha threshold, and available stencil bits.

**Prove:** run the reduced nested case on the failing backend, then restore siblings one at a time.
Do not replace evidence with a universal ban on nested `ClippingNode`.

## Input or scheduled work reaches a departed node

**Cause:** an externally owned listener or callback outlives the node it captures.

**Replace:** prefer scene-graph-priority listeners tied to the node. Explicitly remove fixed-priority
listeners and application-owned schedules during exit/teardown. Keep registration and removal next
to each other.

For v2.11.4, all `EventListenerMouse` callbacks return `bool`; return whether the event was consumed.
Do not copy a signature from another Cocos/Axmol release—read the pinned header. v3 replaces this API
with `PointerEventListener`; see [Migration](migration.md).

On Android, three or more simultaneous touches may be intercepted before Axmol receives an end or
cancel. Reconcile active-touch state on later input and add a timeout; do not require one matching end
for every down.

**Prove:** leave and re-enter the scene, then exercise mouse/touch cancellation and multi-touch. No
old callback should fire, and gesture state must recover without a terminal event.

## Animation changes the size of a physics sprite

**Cause:** Axmol documents that a sprite's content size cannot change after a physics body is
attached; differently sized animation frames violate that contract.

**Replace:** normalize animation frame sizes before attaching the body. Move, rotate, or scale the
node instead of calling `setContentSize()` afterward.

**Prove:** assert equal content sizes for every animation frame and exercise the complete animation
with physics enabled.

See [the source basis](sources.md#scene-input-and-physics) for the v2.11.4 implementation, engine
tests, FAQ, and physics guidance.
