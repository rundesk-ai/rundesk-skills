# Ownership and lifetime

Read this when designing a type that holds a resource, or when something is freed twice, leaked, or
read after it died. Most C++ defects are this page.

## Answer the ownership question first

For every object: **who owns it, and when does it die?** If the code cannot answer, no amount of
`shared_ptr` will fix it — you will have replaced a leak with a cycle.

The Core Guidelines put it as a type-level rule (I.11): **"Never transfer ownership by a raw pointer
(`T*`) or reference (`T&`)."** So the vocabulary is fixed:

| Type | Means |
|---|---|
| `T`, `T&`, `const T&` | Non-owning. The caller keeps it alive for the call |
| `T*` | Non-owning, and may be null. Never delete it |
| `std::unique_ptr<T>` | Exclusive ownership. Moving transfers it |
| `std::shared_ptr<T>` | Shared ownership, refcounted. Use when lifetime is genuinely joint |
| `std::weak_ptr<T>` | Observes a `shared_ptr` without extending it. Breaks cycles |
| A handle / index | Ownership stays with a container; the holder resolves on use |

A raw pointer in a modern codebase should mean *observer* and nothing else. Once that is consistent,
a reviewer can read ownership off the signatures.

## RAII

Every resource — memory, file, socket, lock, GPU handle, transaction — is owned by an object whose
destructor releases it. That is the whole technique, and it is what makes C++ exception-safe without
`finally`.

```cpp
// Bad: leaks on any early return or throw between the two lines
auto* buf = new std::byte[n];
process(buf, n);
delete[] buf;

// Good: released on every path out, including a throw
auto buf = std::make_unique<std::byte[]>(n);
process(buf.get(), n);
```

- `std::lock_guard` / `std::scoped_lock`, never a bare `mutex.lock()`.
- `std::fstream`, not `fopen`.
- For a C API, wrap the handle once in a small RAII type with a custom deleter, and never let the
  raw handle escape.
- **Destructors must not throw.** A throwing destructor during stack unwinding calls
  `std::terminate`. Mark them `noexcept` (they are by default) and swallow-and-log if you must.
- **Never call a virtual function from a constructor or destructor.** The dynamic type is not the
  derived one yet, or is no longer.

## The rule of zero, three, five

**Rule of zero — the default.** A class that owns no resource directly declares none of the special
members. Compose it from types that manage their own (`std::string`, `std::vector`, `unique_ptr`)
and the compiler generates everything correctly.

**Rule of five.** If you declare *any* of the destructor, copy constructor, copy assignment, move
constructor, or move assignment, you almost certainly need to consider all five. Declaring a
destructor **suppresses the implicit move operations**, which silently turns moves into copies — a
performance bug with no diagnostic.

```cpp
class Buffer {
public:
    ~Buffer();                                    // declared, so:
    Buffer(const Buffer&)            = delete;    // decide each one explicitly
    Buffer& operator=(const Buffer&) = delete;
    Buffer(Buffer&&) noexcept;
    Buffer& operator=(Buffer&&) noexcept;
};
```

Mark move operations `noexcept`. `std::vector` will copy rather than move on reallocation if the move
constructor is not `noexcept`, because it cannot otherwise give the strong exception guarantee.

**A polymorphic base needs a virtual destructor** — or deleting through a base pointer is undefined
behaviour. `-Wnon-virtual-dtor` catches it.

## Smart pointers, and which one

```cpp
auto widget = std::make_unique<Widget>(args);      // default
auto shared = std::make_shared<Session>(args);     // only if ownership is genuinely shared
std::weak_ptr<Node> parent_;                       // back-edges, to break cycles
```

- **`unique_ptr` first, always.** It is zero-overhead and it says exactly one thing.
- **`make_unique`/`make_shared`** over a bare `new`. They are exception-safe in an argument list and
  `make_shared` puts the control block and object in one allocation.
- **`shared_ptr` is not "the safe one".** It is refcounting: it costs an atomic increment per copy,
  it makes lifetime non-deterministic, and two objects that point at each other **never die**. Use
  `weak_ptr` for the back-edge.
- **Pass a smart pointer only when transferring or sharing ownership.** A function that merely uses
  the object takes `T&` or `const T&`. `const shared_ptr<T>&` as a parameter is a copy of a pointer
  the caller already owns, and it needlessly couples the signature to the ownership model.
- `unique_ptr` with a custom deleter is the right wrapper for a C handle.

## Passing parameters

| Situation | Take |
|---|---|
| Read only, cheap to copy (`int`, `string_view`, small struct) | By value |
| Read only, expensive to copy | `const T&` |
| Modify the caller's object | `T&` |
| Consume / store a copy | By value, then `std::move` into place |
| Transfer ownership | `std::unique_ptr<T>` by value |
| Optional, may be absent | `const T*`, or `std::optional<T>` for a value |

Use `std::string_view` and `std::span` for non-owning views of a sequence — and remember they are
**views**: they do not extend the lifetime of what they point at. A `string_view` to a temporary
dangles at the end of the full expression.

## Dangling: the four ways

Every one of these compiles cleanly and produces undefined behaviour.

**1. Reference to a local.**

```cpp
const std::string& name() { std::string s = build(); return s; }   // dead on return
```

**2. Iterator, pointer, or reference into a container that reallocated.** `push_back` past capacity
invalidates *everything* into a `vector`. Rules differ per container — `deque`, `list`, `map` and
`unordered_map` each invalidate differently, and this is worth checking rather than remembering.

**3. A view outliving its owner.** `string_view` and `span` into a temporary, a moved-from object, or
a container that has since been cleared.

**4. Capturing by reference in a lambda that outlives the scope.** `[&]` in a callback, a thread, or
anything stored is a dangling capture waiting to happen. Capture by value, or capture the specific
things you need and prove their lifetime.

```cpp
// Bad: `total` is gone by the time the callback runs
registerCallback([&] { report(total); });

// Good: explicit, owned
registerCallback([total] { report(total); });
```

**A cache or index derived from a data structure is part of that structure's lifetime.** When the
owner is destroyed or rebuilt, a derived view that outlives it is not a stale read — it is a
use-after-free. Rebuild or invalidate derived state at the same moment the source changes, and give
the cache the same owner.

## Move semantics

- `std::move` does not move. It casts to an rvalue reference, permitting a move.
- **A moved-from object is valid but unspecified.** You may destroy it or assign to it; do not read
  its value. Standard library types are typically left empty, but do not rely on it for your own.
- Do not `std::move` a return value of a local — that defeats copy elision, which is guaranteed for
  a returned prvalue since C++17.
- Take a sink parameter by value and `std::move` into the member. It is one form that is optimal for
  both lvalue and rvalue callers.

## Sources

- [C++ Core Guidelines — R: Resource management](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-resource) · [I.11](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Ri-raw) — never transfer ownership by raw pointer or reference · [P.8](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rp-leak) — don't leak any resources
- [F.15 and the parameter-passing table](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rf-conventional)
- [C.20 — rule of zero](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rc-zero) · [C.21 — rule of five](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rc-five) · [C.35 — virtual destructor](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rc-dtor-virtual)
- [cppreference: RAII](https://en.cppreference.com/w/cpp/language/raii) · [`unique_ptr`](https://en.cppreference.com/w/cpp/memory/unique_ptr) · [`shared_ptr`](https://en.cppreference.com/w/cpp/memory/shared_ptr) · [move semantics](https://en.cppreference.com/w/cpp/utility/move)
- [cppreference: container invalidation rules](https://en.cppreference.com/w/cpp/container) — per-container, worth reading rather than recalling
