# Undefined behavior and the trap catalog

Read this when behaviour changes with optimisation level, differs between compilers, or is
"impossible."

**Why this matters more in C++ than elsewhere.** The optimiser is entitled to assume undefined
behaviour never happens. So UB does not reliably crash — it deletes your null check, reorders your
code, or works perfectly in `-O0` and fails in `-O2`. The symptom appears far from the cause, which
is why "it works on my machine" is a genuine outcome rather than a joke.

**Do not debug suspected UB by reading.** Build with sanitizers first; see [`tooling.md`](tooling.md).

## Contents

- [Lifetime](#lifetime)
- [Containers and iterators](#containers-and-iterators)
- [Inheritance](#inheritance)
- [Integers and arithmetic](#integers-and-arithmetic)
- [Initialization](#initialization)
- [Multiple definitions and the ODR](#multiple-definitions-and-the-odr)
- [Concurrency](#concurrency)
- [Everyday sharp edges](#everyday-sharp-edges)

## Lifetime

The largest category, covered in [`ownership-and-lifetime.md`](ownership-and-lifetime.md). In UB
terms: use-after-free, use-after-return, double free, and reading a moved-from object. AddressSanitizer
finds all of them **when the path executes**, which is why a test that reaches the code matters more
than a test that asserts about it.

## Containers and iterators

**Iterator invalidation is the classic.** Mutating a container while iterating it is undefined:

```cpp
// Bad: erase invalidates it; ++it is then UB
for (auto it = v.begin(); it != v.end(); ++it)
    if (pred(*it)) v.erase(it);

// Good: erase returns the next valid iterator
for (auto it = v.begin(); it != v.end(); )
    it = pred(*it) ? v.erase(it) : std::next(it);

// Better for a vector: one pass, one move
std::erase_if(v, pred);                       // C++20
```

- `vector::push_back` past capacity invalidates **every** iterator, pointer, and reference into it.
- `operator[]` on a `std::map` **inserts** a default-constructed value when the key is absent. Use
  `.at()` to throw, `.find()` to test, `.contains()` (C++20) to ask.
- `operator[]` on `vector` does not bounds-check. `.at()` does. Neither is checked in a release build
  unless you enable hardening.
- Indexing past the end, or dereferencing `end()`, is UB with no diagnostic.

## Inheritance

**Object slicing** — assigning a derived object to a base by value silently discards the derived
part, and the result is not polymorphic:

```cpp
Derived d;
Base b = d;          // sliced; b is a Base, virtual dispatch is gone
Base& r = d;         // fine — a reference does not slice
```

Prevent it: make polymorphic bases non-copyable, and pass by reference or smart pointer.

**Deleting through a base pointer without a virtual destructor is UB.** `-Wnon-virtual-dtor`.

**Calling a virtual function from a constructor or destructor** dispatches to the base version, not
the override — the derived object does not exist yet, or no longer does. Not UB, but almost never
what was intended.

**`override` on every override.** Without it, a signature that drifts from the base silently becomes
a new function and the override stops being called.

## Integers and arithmetic

- **Signed overflow is UB.** Unsigned wraps (defined), signed does not. `INT_MAX + 1` licenses the
  optimiser to assume the addition never overflows, which is how a bounds check disappears.
- **Shifting by ≥ the width, or by a negative amount, is UB.**
- **Mixed signed/unsigned comparison** converts the signed operand to unsigned:
  `-1 < 0u` is **false**. `-Wsign-compare` catches it; C++20 `std::cmp_less` does it correctly.
- **`size()` is unsigned**, so `for (int i = 0; i < v.size(); ++i)` is a signed/unsigned comparison,
  and `v.size() - 1` on an empty vector is a very large number.
- **Integer division truncates toward zero**, and division by zero is UB — not an exception.
- **Narrowing conversions lose data silently.** `-Wconversion`; brace initialization `{}` refuses
  narrowing at compile time, which is one good reason to prefer it.

## Initialization

- **A local of built-in type is uninitialized**, and reading it is UB. `int x;` then `if (x)` may do
  anything. Always initialize: `int x = 0;` or `int x{};`.
- **Members are initialized in declaration order**, not in the order of the initializer list. Listing
  them out of order compiles and misleads; `-Wreorder` catches it.
- **The static initialization order fiasco**: the order of construction of non-local statics across
  translation units is unspecified, so one using another may see it unconstructed. Use a function-local
  static (initialized on first use, and thread-safe since C++11):

```cpp
Registry& registry() { static Registry r; return r; }
```

- **Prefer brace initialization** — it refuses narrowing. Know the one surprise: for a type with an
  `initializer_list` constructor, braces prefer it, so `std::vector<int> v{5}` is one element with
  value 5, while `std::vector<int> v(5)` is five zeros.

## Multiple definitions and the ODR

The One Definition Rule is unenforced across translation units and the failures are bizarre.

- A non-inline function or variable defined in a header, included twice, is a link error — the easy
  case.
- **The dangerous case: two TUs seeing *different* definitions of the same inline function or class.**
  That is UB, and the linker picks one arbitrarily. Symptoms appear in code you did not touch.
- This happens for real when a header changes between the compilation of two TUs — see the phantom
  failure in [`build-loop-traps.md`](build-loop-traps.md) — and when a macro or `#ifdef` makes a class
  layout differ per TU.
- Keep header-defined functions `inline` or `constexpr`, define class members in one place, and never
  make a type's definition depend on a macro that only some TUs set.

## Concurrency

- **A data race is UB.** Two threads, same memory, at least one writing, no synchronisation. Not
  "occasionally wrong" — undefined.
- `volatile` is not for threading. It means "this memory may change outside the program" (hardware
  registers). Use `std::atomic`.
- **A read-modify-write is not atomic** because each half is. `if (!cache.count(k)) cache[k] = f();`
  from two threads runs `f` twice and can corrupt the container. One lock around the whole decision.
- ThreadSanitizer finds races the tests execute. It cannot find one nothing runs.

## Everyday sharp edges

| Trap | What happens |
|---|---|
| `strlen`/`strcpy` on non-terminated data | Reads past the buffer |
| Returning `c_str()` of a temporary `std::string` | Dangles immediately |
| `printf("%d", someLong)` | Format/argument mismatch is UB. Prefer `std::format`, or a fmt-style logger |
| `memcpy` into a non-trivially-copyable type | UB. Check `std::is_trivially_copyable` |
| Comparing unrelated pointers with `<` | Unspecified |
| Reading a union member you did not write | UB in C++ (unlike C). Use `std::variant` |
| `reinterpret_cast` then dereference | Strict-aliasing violation. Use `std::bit_cast` (C++20) or `memcpy` |
| `assert` in a release build | Compiled out by `NDEBUG` — never put a required check in one |
| Recursion or a large array on the stack | Stack overflow, which ASan reports only sometimes |

## How to confirm

1. Build with `-fsanitize=address,undefined -fno-omit-frame-pointer -g` and run the reproduction.
2. If it is a race, `-fsanitize=thread` — separately; TSan and ASan do not combine.
3. If the sanitizers are silent, the path may not be executing. Confirm the test reaches the code
   before concluding it is clean.
4. Compare `-O0` and `-O2`. A difference is strong evidence of UB.

## Sources

- [C++ Core Guidelines — ES: Expressions and statements](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-expr) · [Con: Constants and immutability](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-const) · [CP: Concurrency](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-concurrency)
- [cppreference: undefined behavior](https://en.cppreference.com/w/cpp/language/ub) · [One Definition Rule](https://en.cppreference.com/w/cpp/language/definition) · [object lifetime](https://en.cppreference.com/w/cpp/language/lifetime) · [initialization](https://en.cppreference.com/w/cpp/language/initialization)
- [UndefinedBehaviorSanitizer](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html) — the check list is itself a UB catalog
- [AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html) · [ThreadSanitizer](https://clang.llvm.org/docs/ThreadSanitizer.html)
- [cppreference: container invalidation](https://en.cppreference.com/w/cpp/container)
