# Organization

Read this when creating a header, splitting code, or defining dependency boundaries.

## Keep headers contractual and self-contained

A header should expose only what callers need to compile. Extra includes and implementation details
increase coupling and rebuild cost.

- Use the project’s existing include-guard convention. `#pragma once` is widely implemented but is
  not standard; portable libraries may require macro guards.
- Never put `using namespace` at header scope; it changes every includer’s lookup environment.
- Define templates where instantiation can see them. Define non-template implementation out of line
  unless callers need it inline or during constant evaluation.
- Give header-defined non-template functions and variables the required `inline` semantics to avoid
  multiple definitions.
- Put translation-unit-only helpers in an anonymous namespace in the source file.

Include what the file names; do not rely on transitive includes. Put a source file’s matching header
first so missing dependencies in that header fail immediately:

```cpp
#include "project/grid.h"

#include <algorithm>
#include <vector>

#include <fmt/format.h>

#include "project/tile.h"
```

Avoid umbrella headers for convenience: changing any dependency then recompiles every consumer.

## Forward declarations and PIMPL

Use a forward declaration when a declaration is sufficient and hiding the definition has a real
coupling or ABI benefit. Include the definition when allocating, dereferencing, inheriting, or
otherwise requiring a complete type.

For `unique_ptr<Impl>` PIMPL, declare operations that invoke deletion out of line, where `Impl` is
complete:

```cpp
// widget.h
class Widget {
public:
    Widget();
    ~Widget();
    Widget(Widget&&) noexcept;
    Widget& operator=(Widget&&) noexcept;
private:
    struct Impl;
    std::unique_ptr<Impl> impl_;
};
```

The default `unique_ptr` deleter requires a complete `Impl` when deletion is instantiated, including
the owner’s destructor, move assignment, and reset paths. Define the special members the class uses
in the source file after `Impl`; do not expose `Impl` merely to silence the error.

## Make boundaries compile-time facts

Keep pure domain logic independent of frameworks and I/O; place translation in adapters and wiring
in the application target. Enforce the direction with target links, not prose.

```text
core <- adapters <- app
  ^
tests
```

If a core test fails to link after a framework include appears, remove the dependency. Linking the
framework into the test target makes the forbidden edge permanent.

## Design interfaces that expose intent

| Avoid | Prefer | Failure avoided |
|---|---|---|
| primitive ids with the same type | domain types and `enum class` | swapped arguments and implicit integer conversion |
| ignored status or handle results | `[[nodiscard]]` when ignoring is a defect | silently discarded failure or resource |
| stateful “interface” base | narrow abstract interface or composition | coupled implementations and slicing risk |

For polymorphic bases, choose either a public virtual destructor or a protected non-virtual one
according to whether callers may delete through the base. Mark overrides `override` so signature
drift fails at compile time.

Follow the repository’s naming convention. If none exists, choose one consistent rule; reserve
`ALL_CAPS` for macros so constants do not look like preprocessors.

See [the source basis](sources.md#source-files-interfaces-and-pimpl) for guideline rules, IWYU, and
the incomplete-type contract.
