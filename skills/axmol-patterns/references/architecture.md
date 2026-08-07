# Architecture

Read this when engine headers leak into domain code or every test requires an Axmol application.

## Keep Axmol at the presentation edge

Use a one-way dependency:

```text
game/UI -> render adapter -> simulation/domain
tests ---------------------> simulation/domain
```

The core exposes meaning—state, quantities, commands—not `Node`, `Sprite`, colors, filenames, or
`ax::Object`. The adapter maps that meaning to Axmol types.

```cpp
// Good: the core states meaning; the adapter chooses pixels.
enum class Surface { water, rock };
ax::Color4B surfaceColor(Surface value); // render layer only

// Bad: a domain header imports Axmol for a presentation choice.
#include "axmol.h"
struct Tile { ax::Color4B color; };
```

The failure is larger than compile time: importing Axmol also imports its reference-counting and
runtime-context assumptions. That makes domain tests depend on a director, event loop, or graphics
setup and lets `Ref` ownership spread through otherwise ordinary C++.

## Enforce the boundary with a target

Build the core and its tests without linking Axmol:

```cmake
add_library(simcore ${SIM_SOURCES})
target_include_directories(simcore PUBLIC sim/include)

add_executable(sim_tests ${SIM_TEST_SOURCES})
target_link_libraries(sim_tests PRIVATE simcore)
```

If that target fails after an Axmol include enters `sim/`, remove the dependency. Linking the engine
into the tests hides the breach and turns the tripwire off.

Keep engine-specific ownership in the adapter:

- Let scene nodes own children.
- Store an independent engine reference with `ax::RefPtr`, not a raw member.
- Keep core ownership under normal RAII; do not derive domain types from `ax::Object`.
- Advance simulation from one explicit input/time boundary. Do not let arbitrary node callbacks
  become the model's clock.

## Prove the separation

1. Configure and build the core test target without the engine target.
2. Run it without a window or graphics context.
3. Search public core headers for Axmol includes and types.
4. For a renderer change, show that only adapter/UI targets rebuild.

This is a catalog architecture default, not an Axmol API requirement. It combines Axmol's documented
ownership model with the decoupling and build-loop guidance in `cpp-patterns`; see
[the source basis](sources.md#architecture-and-practitioner-evidence).
