# Migration

Read this before porting from Cocos2d-x or moving between Axmol major lines.

## A Cocos2d-x port inherits a broken build

**Cause:** Axmol forked Cocos2d-x v4.0 but its CMake and platform files have diverged. A maintainer's
recommended community path is to generate an Axmol project, then move code and resources into it.

**Replace:** start from the template matching the pinned Axmol line. Reapply project-specific CMake,
Android, and Apple changes deliberately; do not copy generated Cocos project files wholesale.

Use `axmol-migrate` only as an aid for a Cocos2d-x v4.0 codebase. The official guide warns that 3.x
and older may not work at all. The compatibility `cocos2d.h` can get the first build running, but
replace its old namespace and type mappings over time so the port does not depend on a permanent
compatibility layer.

**Prove:** build every shipped platform from a clean generated directory, then run a representative
scene. A successful namespace replacement does not validate rendering, audio, or platform files.

## A v2-to-v3 estimate misses most input work

**Cause:** v3 replaces separate touch and mouse APIs with pointer events and also replaces keyboard,
IME, text-field, and label entry points. Counting this as a version bump hides the number of handlers
and widgets affected.

**Replace:** inventory these seams before estimating:

| v2 surface | v3 direction |
|---|---|
| `EventListenerTouch*`, `EventListenerMouse` | `PointerEventListener` |
| `Touch`, `EventTouch`, `EventMouse` | `PointerEvent` |
| `EventListenerKeyboard` | `KeyboardEventListener` |
| `IMEDispatcher`, `IMEDelegate` | `InputSystem`, `InputDelegate` |
| `TextFieldTTF`, UI text fields | `InputField` |
| label-specific create factories | unified `Label::create()` |

Funnel input through a small application-owned interface before the migration. Then the engine API
change lands in adapters instead of every scene and widget.

**Prove:** enumerate every include and constructor for the removed types, migrate one vertical slice,
and test pointer down/move/up/cancel/scroll, keyboard, and text entry. Compile against the pinned v3
headers; callback return types and later pointer APIs have continued to change across v3 PRs.

## Roadmap intent is mistaken for a contract

**Cause:** the v3 roadmap mixes completed work, planned work, and incomplete subsystems. Its C++23,
RHI, physics, platform, and removal bullets are useful warnings but not release guarantees.

**Replace:** use the roadmap to find risk, then confirm each relied-on feature in the pinned commit,
its migration guides, and runnable `cpp-tests`. For a stable production baseline, the official v3 RHI
page still directs users to v2 while v3 is in active development.

**Prove:** record the exact commit, build the feature on every target backend, and keep the migration
separate from unrelated changes so failures have a narrow cause.

After switching the engine commit, re-run its `setup.ps1`; otherwise an axslcc mismatch can masquerade
as a shader regression.

See [the source basis](sources.md#migration) for the official guides and practitioner discussion.
