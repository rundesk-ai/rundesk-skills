# Migration

Read this before an engine bump, or when porting from Cocos2d-x.

## Version status

| Line | State |
|---|---|
| **v2 LTS** | Maintenance. **2.11.x is the final v2 release.** No new features |
| **v3** | Development. Rewrites the input system — see below |

Sitting on 2.11.x is a defensible choice: it is the settled end of a line rather than an abandoned
middle. But it does not receive features, so plan the v3 evaluation deliberately rather than
discovering the input rewrite during an upgrade.

## Cocos2d-x → Axmol

Axmol forked Cocos2d-x v4.0 in November 2019 and has diverged since.

- **The namespace is `ax`.** `USING_NS_CC` becomes `USING_NS_AX`.
- A **compatibility header** maps old names, which eases the port. Treat it as a ramp, not a
  destination — update to Axmol naming over time or you carry the mapping forever.
- **Cocos types that duplicate the standard library are deprecated.** `std::string`, not `CCString`.
  This is most of the "renamed types" work.
- **`axmol-migrate`** automates part of the conversion, but only for **v4.0** projects. Cocos2d-x 3.x
  and older "may not work at all" — those are a rewrite of the affected layers, not a migration.
- Rendering, audio, and platform support have genuinely diverged: Metal/Vulkan/D3D12 backends, HiDPI,
  an OpenAL Soft audio refactor, and modularised extensions. Cocos2d-x documentation is useful for
  concepts and unreliable for APIs.

A port is worth scoping by *layer*: your simulation should port unchanged if it never included an
engine header, which is the argument in [`architecture.md`](architecture.md) arriving in a different
form.

## v2 → v3: the input system is replaced

**This is the largest single item in a v3 upgrade, and it is easy to miss** because it reads as a
refactor rather than a feature. Touch and mouse are unified into a pointer model.

**Removed, and what replaces each:**

| Removed | Replacement |
|---|---|
| `Touch.h`, `EventTouch.*`, `EventMouse.*` | `PointerEvent.h` |
| `EventListenerTouch.*`, `EventListenerMouse.*` | `PointerEventListener.h` |
| `IMEDispatcher.*` | `InputSystem.h` + `InputDelegate.h` |
| `TextFieldTTF.*`, `UITextField.*`, `UITextFieldEx.*` | `InputField.h` |

**What changes in your code:**

- `EventListenerTouchOneByOne::create()` and `EventListenerMouse::create()` become
  `PointerEventListener::create()`, with unified callbacks: `onPointerDown`, `onPointerMove`,
  `onPointerUp`, `onPointerCancel`, `onPointerScroll`.
- `EventListenerKeyboard` becomes `KeyboardEventListener`, whose callback takes a single
  `KeyboardEvent*` rather than separate `KeyCode` and `Event*` parameters.
- `IMEDispatcher::getInstance()->dispatchInsertText()` becomes
  `InputSystem::getInstance()->dispatchInsertText()`, and you implement `InputDelegate` instead of
  `IMEDelegate`.
- **`Label::create()` is unified** — `createWithTTF()`, `createWithSystemFont()` and
  `createWithBMFont()` collapse into one entry point.

**Planning implication:** every input handler and every text field is touched. If input is scattered
across scenes and widgets, that is the cost of the upgrade — and a reason to funnel input through a
small number of your own types now, so the v3 change lands in a handful of files rather than
everywhere.

Related: in **v2.11.x**, `EventListenerMouse` callbacks return `bool` rather than `void`. That
signature is itself version-specific, and the class it belongs to is the one v3 removes.

## What else v3 removes

The input rewrite is the biggest item, but the roadmap discussion lists more removals. Anything below
that your code touches is upgrade work:

- **Chipmunk physics and its tests** — gone. Plan for Box2D; the roadmap reimplements 2D physics on
  **Box2D v3**, and notes physics 2D is not yet production-ready there.
- **GLES 2.0 support** — dropped, on the basis that Android 5.1+ devices support GLES 3.0.
- **`Color3B`** — migrating to `Color32`/`Color4B`.
- **Deprecated `StringUtils::format`**, all deprecated stubs, and the **tolua** dependency.
- **`ghc::filesystem`** — removed, since C++17 `std::filesystem` suffices.

And the platform/standard moves that come with it: **ISO C++23**, Lua 5.5.x, 3D physics from
BulletPhysics to **JoltPhysics**, D3D11/D3D12/Vulkan backends, OpenXR, Linux and Windows ARM64, high
DPI on Windows/Linux/WebAssembly, and Wayland.

Treat the roadmap as intent rather than a contract — it is a discussion thread, and dates move. But
the *direction* is reliable, and it tells you which APIs not to build new code against.

## Other version-gated items

- **Logging.** From v2.1.3, use `AXLOGD` / `AXLOGI` / `AXLOGW` / `AXLOGE` — fmtlib-style, no
  `.c_str()` needed. The older `AXLOG` required `.c_str()` for `std::string` and `.data()` for
  `std::string_view`.
- **Extensions.** From 2.1.3 you can disable all extensions and opt back in individually; earlier
  versions need them disabled one at a time.
- **Physics.** `PhysicsSpriteChipmunk2D` is **deprecated and removed in v3**. Use the integration API,
  which uses Chipmunk2D internally by default.
- **Deprecated extensions.** DragonBones and the legacy GUI extension are no longer recommended.
- **Android**, updating to v2.3.0 or later, has its own guide — check it rather than assuming a
  Gradle bump suffices.
- **Shaders** differ between the 2.x and 3.x pipelines; there are separate wiki pages for each.

## How to do the bump

1. **Read the release notes and the migration pages for every version you are crossing**, not just the
   target. The input rewrite is documented in a PR-specific page, which is easy to miss.
2. Bump the submodule to the tag and **re-run `setup.ps1`** — a tools/branch mismatch produces shader
   errors that look like shader bugs.
3. Build the **headless core first**. If it does not compile, an engine header has leaked into it, and
   you should fix that before anything else.
4. Then the app. Expect the four Xcode-only CMake fixes to still be needed, and check whether the
   engine has changed what they compensate for.
5. Run on **every platform you ship**. Backends differ, and a Metal-only uniform-block violation
   compiles fine on GL.
6. Keep the bump its own commit with nothing else in it. When something breaks a week later, you want
   to revert one pointer.

## Sources

- [Cocos2d-x migration guide](https://github.com/axmolengine/axmol/wiki/Cocos2d%E2%80%90x-migration-guide) — the `ax` namespace, renamed and deprecated types, the compatibility header, `axmol-migrate` and its v4.0-only scope
- [Migration guide for PR 3173](https://github.com/axmolengine/axmol/wiki/Migration-Guide-for-PR-3173) — the complete input-system replacement table above
- [Axmol vs Cocos2d-x](https://github.com/axmolengine/axmol/wiki/Axmol-vs-Cocos2d%E2%80%90x) · [Axmol](https://github.com/axmolengine/axmol) — v2 LTS and v3 status
- [Update guide to v2.3.0 for Android](https://github.com/axmolengine/axmol/wiki/Update-guide-to-v2.3.0-for-Android)
- [Axmol FAQ](https://github.com/axmolengine/axmol/wiki/FAQ) — the `AXLOG` → `AXLOGD` change at v2.1.3
- [2D physics engines](https://github.com/axmolengine/axmol/wiki/2D-Physics-Engines-Information) — Chipmunk2D sprite deprecation and v3 removal
- [Extensions](https://github.com/axmolengine/axmol/wiki/Extensions) — the 2.1.3 opt-in change, deprecated extensions
- [SpriteKit to Axmol](https://github.com/axmolengine/axmol/wiki/SpriteKit-to-Axmol) — if porting from Apple's engine
