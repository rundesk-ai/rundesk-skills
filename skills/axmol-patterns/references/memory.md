# Memory

Read this before creating or storing an Axmol engine object. Most engine classes derive from
`ax::Object` and use intrusive reference counting, not ordinary C++ ownership.

## A child leaks after scene teardown

**Cause:** `new` starts at reference count 1 and `addChild()` retains again. Removing or destroying
the parent releases only its reference, leaving the original one alive.

**Replace:** use the class's `create()` factory. It autoreleases the initial reference while the
parent owns the child.

```cpp
auto* sprite = ax::Sprite::create(); // autoreleased
addChild(sprite);                    // parent retains
```

For your own `ax::Object` subclass, follow the same factory convention: construct, run `init()`, call
`autorelease()` only on success, and delete a failed construction.

**Prove:** in an isolated debug checkout, deliberately enable the pinned v2.11.4 source's
`AX_OBJECT_LEAK_DETECTION` gate; remove the child, tear down the scene, and confirm no instance
remains. This changes engine configuration/source and is not an ordinary runtime switch.

## A stored pointer crashes on a later frame

**Cause:** the autorelease pool releases once at the end of the current main-loop cycle. A raw pointer
with no parent or retained owner can therefore expire before its next use; removal from a parent can
also drop the last reference immediately.

**Replace:** reach through the owning parent when practical. If the reference must live
independently, store `ax::RefPtr<T>`, which retains on assignment and releases on destruction.

```cpp
ax::RefPtr<ax::Sprite> _preview; // good independent ownership
ax::Sprite* _preview;            // unsafe unless another owner is guaranteed
```

Manual `retain()`/`release()` is valid, but every retain needs one release. Never call `delete` on a
live engine object: reference holders are not notified and become dangling.

**Prove:** exercise parent removal, scene replacement, and destruction—not just the happy frame—and
run the leak detector.

## A collection contains dead engine pointers

**Cause:** `std::vector<Node*>` stores addresses but owns no engine references.

**Replace:** use `ax::Vector<T*>` or `ax::Map<K,T*>` when the collection owns engine objects; they
retain on insertion and release on removal. Use a standard container of `ax::RefPtr<T>` when its
algorithms are a better fit.

```text
Good: ax::Vector<ax::Sprite*> ownedSprites
Good: std::vector<ax::RefPtr<ax::Sprite>> orderedSprites
Bad:  std::vector<ax::Sprite*> owningSprites
```

**Prove:** remove the last external owner while the collection remains, then clear the collection;
the objects must remain valid until the clear and disappear afterward.

## Keep two ownership models separated

Use `ax::RefPtr` and Axmol containers at the engine seam. Use RAII, values, and standard smart
pointers for domain code. Deriving domain types from `ax::Object` spreads manual lifetime rules into
code that could otherwise compile and test without the engine; see [Architecture](architecture.md).

See [the source basis](sources.md#memory) for the official ownership rules and diagnostics.
