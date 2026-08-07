# Memory

Read this before storing a pointer to any engine object. This is the largest adjustment for a
developer arriving from modern C++, and getting it wrong produces leaks and use-after-free that the
usual tools describe unhelpfully.

## The model

Axmol inherits Cocos2d-x's intrusive reference counting, itself inherited from Cocos2d-iphone's
Objective-C model. Objects deriving from `ax::Object` (historically `Ref`) carry a reference count.

The engine's own rule, quoted:

> **"A `retain()` must always be matched with a `release()`."**

- `new` gives a reference count of 1.
- `retain()` increments, `release()` decrements, and at zero the object deletes itself.
- **Never call `delete` on an engine object.** Use `release()`.

## Autorelease and the pool

`autorelease()` adds the object to a pool that calls `release()` on it **once per main-loop cycle** —
at the end of the current frame. This is what lets a factory return an object nobody has claimed yet
without leaking it.

> **"If you call `autorelease()` more than once in the SAME main-loop cycle, then there must be 1
> reference for each call to `autorelease()`."**

The practical consequence: **an autoreleased object you did not retain is gone at the end of the
frame.** Storing that pointer in a member and using it next frame is a use-after-free.

## `create()` is the convention

Engine classes provide a static `create()` that constructs the object and calls `autorelease()` on it.
Follow the convention in your own `Node` subclasses — a constructor that returns a non-autoreleased
object breaks every caller's expectation.

```cpp
MyNode* MyNode::create() {
    auto* n = new MyNode();
    if (n && n->init()) { n->autorelease(); return n; }
    AX_SAFE_DELETE(n);
    return nullptr;
}
```

## The scene graph owns its children

> **"All sub-classes of Node will automatically call `retain()` and `release()` on child nodes."**

`addChild()` retains; removal releases. So for anything that lives in the tree, **let the tree own
it** and do not manage the count yourself.

The leak this prevents, and the one the wiki documents:

```cpp
auto* sprite = new Sprite();   // refCount = 1  — never autoreleased
addChild(sprite);              // refCount = 2
// scene destructs → release() once → refCount = 1 → never freed
```

## When you hold a reference yourself

> **"If we need to hold a reference to an `ax::Object` object for some particular reason, then we must
> call `retain()` when we store the reference, and `release()` when we no longer require it."**

Release in the destructor. And prefer not to be in this position at all: reach for the node through
its parent rather than caching a raw pointer across frames. A node removed from its parent may be
destroyed immediately, so a cached raw pointer is a dangling pointer with no diagnostic.

## The RAII helpers — use them

The FAQ's line that no smart pointers are planned refers to the **standard** smart pointers in the
engine's own API. The engine does ship RAII helpers, and they remove nearly all manual counting:

| Helper | Does |
|---|---|
| `ax::RefPtr<T>` | Retains on assignment, releases on destruction. The `unique_ptr`-shaped answer for a held reference |
| `ax::Vector<T*>` | Retains on insert, releases on removal |
| `ax::Map<K, T*>` | The same, keyed |
| `AX_SAFE_RETAIN(p)` | Retain if not null |
| `AX_SAFE_RELEASE(p)` | Release if not null |
| `AX_SAFE_RELEASE_NULL(p)` | Release and null the pointer |

**Prefer `ax::RefPtr<T>` to a raw `T*` member with hand-written retain/release.** It costs a little
and it makes the destructor correct by construction — which is the same argument as `unique_ptr` in
ordinary C++, and it applies here for the same reason.

Use `ax::Vector`/`ax::Map` for collections of engine objects rather than `std::vector<Node*>`; the
standard container will happily hold pointers to objects that have already died.

## Leak detection

```cpp
#define AX_REF_LEAK_DETECTION 1     // development builds
```

Then `Object::printLeaks()` at shutdown reports objects still alive. It also catches a `release()`
that leaves the count wrong, which is how a dangling reference is found before it crashes.

Turn this on in the development configuration and read its output before a release. A leak here does
not show up as growth in a short session — it shows up after an hour of play.

## Your own types stay modern

**The reference-counting model belongs at the engine boundary and nowhere else.** Simulation types,
value objects, data structures, and services should be ordinary modern C++ with `std::unique_ptr`,
RAII, and no `Ref` in sight. See [`architecture.md`](architecture.md).

Two models in one codebase is fine when the boundary is sharp. It becomes unmanageable when `Ref`
leaks inward, because then every type has manual lifetime and nothing composes.

## Sources

- [Axmol: Memory Management](https://github.com/axmolengine/axmol/wiki/Memory-Management) — every quoted rule, `RefPtr`, `ax::Vector`/`Map`, the `AX_SAFE_*` macros, and `AX_REF_LEAK_DETECTION`
- [Axmol FAQ](https://github.com/axmolengine/axmol/wiki/FAQ) — reference counting is kept for historical reasons and standard smart pointers are not planned for the engine API
- `cpp-patterns` → `ownership-and-lifetime.md` for the model your own types should use
