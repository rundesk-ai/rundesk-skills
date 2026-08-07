# Organization

Read this when creating a header, splitting a module, or deciding where something belongs.

C++ organization is unusual in one respect: **how you split files changes your build time by orders
of magnitude**, because a header edit recompiles every translation unit that includes it. Structure
is a performance decision here, not only a readability one.

## Headers and sources

A header is a **contract**; a source file is an implementation. Put in the header only what a caller
needs to compile against, because everything else is compile time you are charging to every consumer.

- **`#pragma once`** at the top. It is universally supported and cannot be got wrong; include guards
  can be, by copy-paste.
- **Never `using namespace` at file scope in a header.** It leaks into every consumer. Inside a
  function in a source file is fine.
- **Templates and `constexpr` must be visible where instantiated**, so they live in headers. Keep
  them small, or split heavy implementation into a `_impl.h` the header includes at the bottom.
- **Anything defined in a header must be `inline`** (or a class member, or a template), or you get
  duplicate-symbol errors at link.
- Keep an **internal-linkage** helper in an anonymous namespace in the source file, not `static` at
  file scope, and never in a header.

## Include hygiene

**Include what you use.** Each file includes exactly the headers for the names *it* names, and does
not lean on a transitive include. Transitive includes break when somebody else tidies their header,
producing a failure far from the change.

Order includes so a missing include in your own header is caught:

```cpp
// grid.cpp
#include "project/grid.h"   // 1. this file's own header, FIRST — it must be self-contained
                            //
#include <algorithm>        // 2. standard library
#include <vector>
                            //
#include <fmt/format.h>     // 3. third party
                            //
#include "project/tile.h"   // 4. this project
```

Putting the matching header first proves it compiles standalone. Anything else and a missing include
in the header is masked by whatever the source happened to include earlier.

**Avoid the convenience umbrella header** that includes everything in a library. It is one line for
the author and a full rebuild for every consumer on any change.

## Forward declarations and PIMPL

**Forward declare in headers wherever possible.** A declaration is enough for a pointer, a reference,
or a function signature — you only need the full definition to allocate, dereference, or inherit.

```cpp
// grid.h
namespace project { class Tile; }        // enough for the members below

class Grid {
    std::vector<Tile*> tiles_;
    const Tile& at(int x, int y) const;
};
```

**PIMPL** hides implementation entirely, so changing it does not recompile consumers:

```cpp
// widget.h
class Widget {
public:
    Widget();
    ~Widget();                            // out of line — Impl is incomplete here
    Widget(Widget&&) noexcept;            // declare ALL of them; see below
    Widget& operator=(Widget&&) noexcept;
private:
    struct Impl;
    std::unique_ptr<Impl> impl_;
};
```

**The trap, and it is a real one:** when a header holds a container or `unique_ptr` of a **private,
incomplete** type, declaring only an out-of-line destructor is not enough. As soon as the owner is
copied, moved, or assigned, the compiler instantiates the corresponding container operations at a
point where the element type is still incomplete, and the error is confusing.

**Rule: declare and define every special member you use — destructor, copy and move constructors,
copy and move assignment — out of line in the source file, after the element type is complete.** Do
not solve it by leaking the implementation type into consumers.

## Namespaces

- One project namespace, nested for subsystems: `project::sim`, `project::render`.
- **Never open `namespace std`** except to specialize a standard template for your own type.
- An anonymous namespace for internal linkage in a source file.
- `inline namespace` only for versioning an ABI, which most projects do not need.
- Avoid deep nesting. Three levels is usually two too many for a reader.

## Layering, enforced

Decide the dependency direction, then **make the build enforce it** — a documented rule drifts, a
target that refuses to link does not.

```text
core/     pure logic — no framework, no I/O, no engine.  Fast to build, trivially testable.
adapters/ maps core concepts onto a framework, a database, a renderer.
app/      thin: wiring, entry point, configuration.
tests/    links core ALONE.
```

That last line is the mechanism. Because `tests/` links only `core`, the day a framework include
appears in `core` the test target stops linking and CI goes red. Fix that by removing the include —
never by linking the framework into tests, which disarms the tripwire permanently.

The same structure buys a **fast build**: a configuration that builds only the core and its tests
skips the heavy dependency entirely, turning a minutes-long loop into a seconds-long one.

## Interfaces

- **An abstract interface is a class with a virtual destructor and pure virtual methods, and no
  state.** If it has data members, it is a base class, and you have coupled every implementation to
  it.
- Prefer a **narrow** interface. `I.1`: make interfaces explicit; `I.4`: make them precisely and
  strongly typed.
- **Strong types over primitives.** `TileId` and `PlayerId` as distinct types cannot be swapped at a
  call site; two `int`s can, and will. An `enum class` cannot be confused with an integer.
- **`[[nodiscard]]`** on anything whose return value must not be ignored — a status, a handle, a
  reserved resource.
- Not everything needs an interface. A single implementation behind a pure virtual base is
  indirection with no second caller; add it when the second implementation exists, or when a test
  genuinely needs a seam that nothing else provides.

## Naming

Follow the project's existing convention above all else — mixed conventions cost more than any
particular choice. Absent one, be internally consistent, and:

- Distinguish types from values and members from locals in *some* consistent way (a trailing
  underscore on members is common and greppable).
- Name headers after the primary type they declare.
- **`ALL_CAPS` is for macros only**, so a constant named that way reads as a macro and may collide
  with one.
- Prefer a name that states the domain concept over one that states the mechanism.

## Sources

- [C++ Core Guidelines — SF: Source files](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-source) — self-contained headers, `#include` order, no `using namespace` in a header
- [I: Interfaces](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-interfaces) — I.1, I.2, I.4, I.11
- [C: Classes and class hierarchies](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-class)
- [cppreference: translation units and linkage](https://en.cppreference.com/w/cpp/language/translation_phases) · [`#pragma once`](https://en.cppreference.com/w/cpp/preprocessor/impl)
- [Include What You Use](https://include-what-you-use.org/) — the tool that checks the rule mechanically
- The incomplete-type special-member trap was recorded in a real project; the mechanism is standard
  and applies to any PIMPL or container-of-forward-declared-type header.
