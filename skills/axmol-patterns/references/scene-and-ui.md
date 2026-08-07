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

## A v2 desktop text field edits twice

**Cause:** in Axmol v2.11.3-v2.11.4 desktop builds, a key reaches `EventKeyboard` first. If that event
is not stopped, Backspace then reaches `IMEDelegate::deleteBackward()` and navigation, Delete, and
Escape reach `controlKey()`.

**Replace:** give each key one owner. Let Backspace fall through to the IME delegate; call
`stopPropagation()` for every control key the keyboard listener handles. Receive printable text only
through `IMEDelegate::insertText()`.

**Prove:** test Backspace, Delete, Home, End, Left, Right, and Escape at the start, middle, and end of
text; each physical press must edit or move once.

## A multiline v2 `TextFieldTTF` ends editing on Enter

**Cause:** its newline path treats `\n` as input completion and detaches from the IME unless the
delegate consumes it. The class exposes no cursor-position getter, so a delegate cannot reliably
insert that newline at the current caret.

**Replace:** use `TextFieldTTF` as a single-line field. For multiline editing, own the text, caret,
and selection in an application model behind `IMEDelegate` instead of appending in a
`TextFieldDelegate` callback.

**Prove:** place the caret mid-string, press Enter, and confirm the newline lands there while focus
remains attached.

## macOS Cmd shortcuts do nothing in a v2 desktop build

**Cause:** Axmol maps GLFW's left and right Super keys to `EventKeyboard::KeyCode::KEY_HYPER`, not a
GUI- or Command-named key.

**Replace:** track `KEY_HYPER` press and release for Cmd chords. Keep Ctrl handling separate so the
same editor can support both conventions where required.

**Prove:** exercise Cmd+A/C/X/V on macOS and verify modifier state clears after release.

## Resizing a TTF label changes its font path

**Cause:** `setSystemFontSize()` switches a label to `STRING_TEXTURE`; it is not the TTF resize API.

**Replace:** preserve the TTF configuration:

```cpp
auto cfg = label->getTTFConfig();
cfg.fontSize = size;
label->setTTFConfig(cfg);       // good: remains TTF
label->setSystemFontSize(size); // bad: switches to a system-font texture
```

**Prove:** assert `getLabelType() == LabelType::TTF` after resizing and inspect the intended typeface
in the live target.

## Animation changes the size of a physics sprite

**Cause:** Axmol documents that a sprite's content size cannot change after a physics body is
attached; differently sized animation frames violate that contract.

**Replace:** normalize animation frame sizes before attaching the body. Move, rotate, or scale the
node instead of calling `setContentSize()` afterward.

**Prove:** assert equal content sizes for every animation frame and exercise the complete animation
with physics enabled.

See [the source basis](sources.md#scene-input-and-physics) for the v2.11.4 implementation, engine
tests, FAQ, and physics guidance.
