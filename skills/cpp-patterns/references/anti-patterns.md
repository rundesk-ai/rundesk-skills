# C++ anti-patterns

Read this when reviewing C++. Each row names the failure, not just the rule.

**Rank findings by what they cost.** Undefined behaviour and lifetime bugs are defects — they produce
wrong answers or crashes at a distance. Style and idiom are preferences. Say which is which; in C++
the gap between them is wider than in most languages.

## Contents

- [Ownership and lifetime](#ownership-and-lifetime)
- [Classes](#classes)
- [Correctness](#correctness)
- [Interfaces and types](#interfaces-and-types)
- [Build and project](#build-and-project)
- [Performance](#performance)
- [Process](#process)

## Ownership and lifetime

| Don't | Do | Because |
|---|---|---|
| Raw `new` / `delete` | `make_unique`, RAII | Leaks on every early return and every throw |
| Return `T*` meaning "you own this" | Return `unique_ptr<T>` | I.11: never transfer ownership by a raw pointer or reference |
| `shared_ptr` as the default | `unique_ptr` first | Atomic refcount per copy, non-deterministic destruction, and cycles never die |
| Two objects holding `shared_ptr` to each other | `weak_ptr` for the back-edge | A cycle is a permanent leak that no tool reports as one |
| `const shared_ptr<T>&` as a parameter | `const T&` | The function does not participate in ownership; the signature says it does |
| Return a reference to a local | Return by value | Dangling. Copy elision makes by-value free |
| Hold an iterator or reference across a `push_back` | Re-look-up, or hold an index | Reallocation invalidates everything into a `vector` |
| `[&]` capture in a lambda that is stored or queued | Capture what you need, by value | The frame is gone when it runs |
| A cache that outlives the structure it derives from | Same owner, invalidate together | Not a stale read — a use-after-free |
| `std::move` a returned local | Just return it | Defeats guaranteed copy elision |

## Classes

| Don't | Do | Because |
|---|---|---|
| Declare a destructor and nothing else | Rule of zero, or declare all five | Declaring a destructor suppresses implicit moves — every move silently becomes a copy |
| Polymorphic base with a non-virtual destructor | `virtual ~Base() = default` | Deleting through a base pointer is UB |
| Accept a polymorphic type by value | By reference or smart pointer | Object slicing; the derived part is discarded silently |
| Call a virtual from a constructor or destructor | Two-phase init, or a non-virtual helper | Dispatches to the base — the derived object does not exist yet |
| Omit `override` | `override` on every one | A drifted signature becomes a new function and stops being called |
| Move operations without `noexcept` | Mark them `noexcept` | `vector` copies instead of moving on reallocation |
| Deep inheritance to share code | Composition | The reader cannot tell where a member came from |
| A getter/setter pair per field | A meaningful interface, or a plain struct | Encapsulation theatre with none of the benefit |

## Correctness

| Don't | Do | Because |
|---|---|---|
| `int x;` then read it | `int x = 0;` / `int x{};` | Reading an uninitialized value is UB |
| Erase while iterating with `++it` | `it = v.erase(it)`, or `std::erase_if` | The iterator is invalid before you increment it |
| `map[key]` to test membership | `.contains()`, `.find()`, `.at()` | `operator[]` **inserts** a default-constructed value |
| Compare signed with unsigned | `std::cmp_less`, or make both signed | `-1 < 0u` is false |
| `for (int i = 0; i < v.size(); ++i)` | `for (auto& x : v)`, or a matching type | Signed/unsigned comparison; `size()-1` on empty is enormous |
| Rely on signed overflow wrapping | Check before, or use unsigned deliberately | Signed overflow is UB, and the optimiser assumes it cannot happen |
| `assert` for a required check | `if (…) throw` | `NDEBUG` compiles it out of the release build |
| Member init list out of declaration order | Match the declaration order | Members initialize in declaration order regardless |
| Non-local static depending on another | Function-local static | Static initialization order across TUs is unspecified |
| `volatile` for threading | `std::atomic` | `volatile` provides no atomicity or ordering |
| Unsynchronized read-modify-write | One lock around the whole decision | Two threads both see the miss |
| A macro where a function would do | `constexpr`, `inline`, template | No scope, no type checking, unreadable errors |

## Interfaces and types

| Don't | Do | Because |
|---|---|---|
| `int` for an id, a count, and an index alike | Strong types, `enum class` | Two `int` parameters will be swapped at some call site |
| Bare `enum` | `enum class` | Unscoped enumerators leak and convert to `int` implicitly |
| Output parameters | Return a value, a struct, or `optional` | The caller cannot tell what the function writes |
| A `bool` parameter | Two functions, or an `enum class` | `render(true, false)` says nothing at the call site |
| `#define` constants | `constexpr` | No type, no scope, collides |
| C-style cast | `static_cast` and friends | Hides a `reinterpret_cast` or a `const_cast` from the reader and from grep |
| `using namespace` at header scope | Qualify, or use it inside a function | Leaks into every consumer |
| An abstract interface for one implementation | Add it when the second arrives | Indirection with no second caller |

## Build and project

| Don't | Do | Because |
|---|---|---|
| `include_directories()`, `add_definitions()` | The `target_*` equivalents | Directory commands create hidden dependencies for every target below |
| `set(CMAKE_CXX_FLAGS "-std=c++20")` | `target_compile_features` | The flag differs per compiler and breaks on a newer standard |
| Warnings on vendored dependencies | Scope them `PRIVATE` to your targets | Unfixable noise trains people to ignore warnings |
| Edit a vendored dependency in place | Fix it in your own build files | An upgrade becomes archaeology |
| Two builds into one directory | One writer, enforced with a lock | Ninja corrupts its logs; `ar` truncates archives |
| Several directories producing the app | Exactly one | The wrong binary launches and every fix "does nothing" |
| `cmd \| tail` to check a build | Redirect to a file; read `$?` | The pipe reports `tail`'s status — always success |
| An umbrella header that includes everything | Include what you use | One line for you, a full rebuild for every consumer |

## Performance

| Don't | Do | Because |
|---|---|---|
| Optimize before profiling | Measure | The cost is rarely where it feels |
| Benchmark a `Debug` build | `RelWithDebInfo` / `Release` | Debug numbers can be 10× off and mislead about the ratio |
| Pass a large object by value in a loop | `const T&` | A copy per iteration |
| `push_back` in a loop without `reserve` | `reserve(n)` | Repeated reallocation and copying |
| `std::endl` in a loop | `'\n'` | `endl` flushes every time |
| A `list` or `map` because of asymptotics | Measure against a `vector` | Contiguity usually wins below very large n |
| Micro-optimize readable code | Fix the algorithm or the allocations | A rewritten loop does not repair an O(n²) |

## Process

- **Don't report "this looks wrong" as a defect.** In C++ especially, produce the sanitizer output,
  the warning, or the failing case. A plausible-sounding lifetime concern that is actually fine costs
  the reader more than silence.
- **Don't debug suspected UB by reading.** Sanitizers first.
- **Don't trust a surprising result before ruling out a stale build.** See
  [`build-loop-traps.md`](build-loop-traps.md).
- **Don't modernize past the project's standard**, and don't raise the floor unasked.
- **Don't reformat unrelated code** in a fix. It buries the change.
- **Don't leave a suppression without a reason.** `// NOLINT(check-name): why` — an unexplained
  suppression is permanent.

## Sources

Every rule here is cited in [`sources.md`](sources.md). The densest sources are the
[C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines),
[cppreference](https://en.cppreference.com/), the
[sanitizer](https://clang.llvm.org/docs/AddressSanitizer.html) documentation, and
[clang-tidy's check list](https://clang.llvm.org/extra/clang-tidy/checks/list.html), which — like
every lint catalog — is a record of what people actually get wrong.
