# Undefined behavior

Read this when behavior changes with optimization, differs by compiler, or appears impossible. Run
the relevant sanitizer before relying on inspection; see [tooling](tooling.md).

Undefined behavior does not promise a crash or a diagnostic. The optimizer may assume it cannot
occur, so the visible failure can be far from its cause.

## Lifetime and containers

Use-after-free, use-after-return, double deletion, and dangling views are lifetime defects. Moved-
from objects are not inherently UB: standard-library objects remain valid but their value is usually
unspecified; respect operation preconditions.

Container mutation is unsafe only when it invalidates what the loop or later code uses. Check the
specific container and operation.

```cpp
// Bad: vector::erase invalidates it before ++it.
for (auto it = values.begin(); it != values.end(); ++it)
    if (pred(*it)) values.erase(it);

// Good: continue from the iterator erase returns.
for (auto it = values.begin(); it != values.end(); )
    it = pred(*it) ? values.erase(it) : std::next(it);
```

- `vector` growth that changes capacity invalidates all pointers, references, and iterators into it.
- `map[key]` inserts a value when the key is absent; use `contains`/`find` to test and `at` for
  checked access.
- `vector::operator[]` is unchecked before C++26 hardening and remains UB out of range when not
  hardened. `at()` always bounds-checks and throws `out_of_range`.

Proof: reproduce the mutation followed by the access under ASan; log capacity only to confirm that
the intended invalidating path executed.

## Polymorphism and definitions

| Symptom | Cause | Replace with | Proof |
|---|---|---|---|
| derived behavior disappears | object passed or stored as base by value was sliced | base reference or owning smart pointer | focused virtual-dispatch test |
| destruction crashes or leaks | delete through a base with the wrong destructor contract | public virtual destructor, or forbid base deletion with protected non-virtual destructor | `-Wnon-virtual-dtor` plus sanitizer run |
| override stops running | signature drift created a different function | mark every override `override` | compiler error on mismatch |
| unrelated translation units behave differently | definitions or class layouts differ across TUs | one definition independent of TU-local macros | clean build and compare preprocessing/commands |

Virtual calls in constructors and destructors dispatch to the currently constructed or destructed
class, not a more-derived override. This is defined behavior but often violates intent; use a
non-virtual helper or a factory that calls virtual work after construction.

The dangerous One Definition Rule case is different definitions of the same inline entity in
different translation units. It is not required to produce a linker error. Inspect macros, generated
headers, and compile commands, then confirm with a clean scratch build.

## Arithmetic and initialization

- Signed overflow, integer division or remainder by zero, and invalid shift counts are UB. Check
  before arithmetic; use unsigned only when modular arithmetic is intended.
- Mixed signed/unsigned comparison converts operands under the usual arithmetic rules. Prefer a
  common appropriate type or C++20 `std::cmp_*`; `-Wsign-compare` finds suspicious cases.
- Initialize built-in locals before reading them. MSan diagnoses executed uninitialized reads.
- Members initialize in declaration order, regardless of initializer-list order. Match those orders;
  `-Wreorder` exposes mismatches.
- Non-local static initialization across translation units is only partially ordered. Prefer a
  function-local static when first-use initialization fits the lifetime model.
- Brace initialization rejects narrowing, but an `initializer_list` constructor gets priority.
  Choose braces for narrowing protection, not as an unexplained universal rule.

## Concurrency

A data race—conflicting unsynchronized accesses to the same memory—is UB. `volatile` does not supply
atomicity or ordering; use `atomic` for the appropriate single-object operation or a lock for a
compound invariant.

```cpp
// Bad: the check and insertion are one decision but separately synchronized or not synchronized.
if (!cache.contains(key)) cache[key] = compute();

// Good: protect the whole decision, or use a concurrent structure with that compound operation.
std::scoped_lock lock(cache_mutex);
if (!cache.contains(key)) cache[key] = compute();
```

Proof: run the reproducer under TSan in a separate configuration. A quiet run proves only that no
executed access triggered a report.

## Confirm, do not infer

1. Reproduce under ASan plus UBSan; use TSan separately for races.
2. Confirm the suspect path executed.
3. Reduce to the invalid operation and record the diagnostic.
4. Compare optimization levels only as a clue. A difference raises suspicion; it does not prove UB.

See [the source basis](sources.md#undefined-behavior-and-diagnostics) for the language, container,
ODR, and sanitizer contracts.
