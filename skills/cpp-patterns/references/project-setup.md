# Project setup

Read this when creating a C++ project, adding a target, or changing its build.

## Model requirements on targets

Declare what a target needs and what its consumers inherit:

```cmake
add_library(simcore STATIC src/grid.cpp src/worldgen.cpp)
target_include_directories(simcore
  PUBLIC  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/src)
target_compile_features(simcore PUBLIC cxx_std_20)
target_link_libraries(simcore PRIVATE fmt::fmt)
```

| Scope | Target uses it | Consumers inherit it |
|---|---:|---:|
| `PRIVATE` | yes | no |
| `PUBLIC` | yes | yes |
| `INTERFACE` | no | yes |

Use the narrowest correct scope. A missing public requirement breaks consumers; an unnecessarily
public one creates hidden coupling.

| Avoid | Prefer | Failure avoided |
|---|---|---|
| `include_directories()` | `target_include_directories()` | unrelated targets inherit includes |
| `add_definitions()` | `target_compile_definitions()` | configuration-dependent definitions leak across targets |
| `link_directories()` and bare names | imported targets in `target_link_libraries()` | wrong library selection and lost usage requirements |
| `CMAKE_CXX_FLAGS` for the standard | `target_compile_features(... cxx_std_N)` | compiler-specific flags and inconsistent consumers |
| directory-wide warnings | `target_compile_options(... PRIVATE ...)` | third-party noise hides project warnings |
| `file(GLOB ...)` for sources | list sources | added or removed files can evade regeneration |

CMake explicitly prefers target-specific include directories and discourages source globs. If an
existing project uses `CONFIGURE_DEPENDS`, keep its convention unless asked to migrate; the check
adds rebuild cost and is not reliable with every possible generator.

## Isolate build state

Use out-of-source directories and give each concurrent actor or incompatible configuration its own:

```sh
cmake -S . -B build/dev -G Ninja -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
cmake --build build/dev --target app
```

Do not run multiple Ninja processes against the same tree. Ninja maintainers describe that mode as
unsupported: each process computes dirtiness independently and shares its command log. Use one
Ninja invocation for parallelism, or a separate build directory.

`compile_commands.json` records per-translation-unit compile commands for supported generators
(Makefile and Ninja). Check it when a flag, define, or include path seems wrong; do not assume an IDE
and command-line build use the same command.

## Keep warnings actionable

Start with the warning set already supported by the project. Common GCC/Clang candidates are
`-Wall -Wextra -Wpedantic`; add focused warnings such as `-Wshadow`, `-Wconversion`, or
`-Wnon-virtual-dtor` only after checking the compiler and baseline. Use `/W4` for MSVC projects.

- Scope project warnings `PRIVATE`; do not impose them on dependencies.
- Make stable warnings errors in CI. Adopt noisy checks incrementally instead of creating a large
  suppression backlog.
- Record every suppression beside the code with the reason it is safe.

## Pin fetched content and enforce layers

Consume dependencies through imported targets. Pin remote `FetchContent` with a commit hash (or an
archive hash); CMake recommends hashes because mutable branch and tag names are less secure and do
not prove which content was downloaded.

Make dependency direction executable. For example, a `core` target that links no framework cannot
silently acquire a framework dependency. Keep an application target for wiring and tests that link
the narrowest production target they exercise.

Good: `tests -> core`, while `app -> core + renderer`.

Bad: link the renderer into `core` tests to make a forbidden include compile; this removes the
boundary instead of fixing the dependency.

See [the source basis](sources.md#build-and-project-structure) for the CMake contracts and community
practice behind these defaults.
