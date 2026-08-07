# Project setup

Read this when creating a C++ project, adding a target, or changing how it builds.

## Contents

- [Think in targets, not directories](#think-in-targets-not-directories)
- [The commands that replaced the old ones](#the-commands-that-replaced-the-old-ones)
- [Build directories](#build-directories)
- [The compile database](#the-compile-database)
- [Warnings and standard](#warnings-and-standard)
- [Dependencies](#dependencies)
- [A layout that scales](#a-layout-that-scales)

## Think in targets, not directories

Modern CMake is target-based. A target declares what *it* needs and what its *consumers* need, and
CMake propagates the difference. Directory-level commands are the old model and they leak.

CMake's own documentation is explicit: directory-level commands mean "all targets defined on that
level inherit those properties, which increases the chance of hidden dependencies. It's better to
operate on the targets directly."

```cmake
add_library(simcore STATIC src/grid.cpp src/worldgen.cpp)

target_include_directories(simcore
    PUBLIC  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>   # consumers see this
    PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/src)                          # only this target does

target_compile_features(simcore PUBLIC cxx_std_20)
target_link_libraries(simcore PRIVATE fmt::fmt)
```

The three keywords are the whole model:

| Keyword | Applies to the target | Propagates to consumers |
|---|---|---|
| `PRIVATE` | yes | no |
| `PUBLIC` | yes | yes |
| `INTERFACE` | no | yes |

Get these right and a consumer needs to know nothing about your internals. Get them wrong and
either the build breaks or every target in the tree quietly depends on everything.

## The commands that replaced the old ones

| Don't | Do | Because |
|---|---|---|
| `include_directories()` | `target_include_directories()` | Every target below the directory inherits it, so a target compiles only by accident of where it sits |
| `add_definitions()` | `target_compile_definitions()` | A define that changes a class layout, applied unevenly, is an ODR violation |
| `link_directories()` | `target_link_libraries()` with an imported target | A bare path finds the wrong library or none, and carries no usage requirements |
| `set(CMAKE_CXX_FLAGS "-std=c++20 …")` | `target_compile_features(t PUBLIC cxx_std_20)` | The flag differs per compiler and is not satisfied by a newer standard |
| `set(CMAKE_CXX_FLAGS "-Wall …")` | `target_compile_options()` | Vendored dependencies inherit your warnings and drown the signal |
| `file(GLOB …)` for sources | List sources explicitly | A glob is evaluated at configure time, so a new file silently is not built |

On the standard specifically: setting `-std=c++20` in `CMAKE_CXX_FLAGS` "will break in the future
because those requirements are also fulfilled in other standards… and the compiler option is not the
same on old compilers." `target_compile_features` lets CMake choose the flag.

On globbing: a glob is evaluated at configure time, so a new file does not appear until something
re-runs CMake. `CONFIGURE_DEPENDS` makes it re-check, at the cost of a glob check on every build —
and a glob-verification step is one of the things that can make a build re-run CMake in a loop when
its stamps get inconsistent. Engine templates often glob; if yours does, know that is why adding a
file sometimes needs a reconfigure.

## Build directories

Always out-of-source. Beyond that, two rules that cost real time when broken:

- **One writer per build directory.** Ninja is not concurrency-safe on a single build dir. Two
  builds at once corrupt `.ninja_deps`/`.ninja_log`, which makes ninja forget what it built and
  recompile everything; concurrent `ar` can truncate a static archive to zero bytes, producing a
  link error like `file is empty in lib/libFoo.a`. If your dev loop can be run by more than one
  actor, take a lock. See [`build-loop-traps.md`](build-loop-traps.md).
- **Separate directories for separate purposes**, and make sure only one of them produces a
  runnable artifact. A headless test configuration that builds no application avoids a whole class
  of "I ran the wrong binary" failure.

```sh
cmake -B build/dev   -G Ninja -DCMAKE_BUILD_TYPE=Debug
cmake -B build/tests -G Ninja -DCMAKE_BUILD_TYPE=Debug -DHEADLESS_ONLY=ON
cmake --build build/dev --target app
```

Prefer **Ninja** over Makefiles for speed, and over IDE generators for predictability — an IDE
generator can apply settings that a command-line build does not, so a project that only works in the
IDE has flags hiding in the IDE.

## The compile database

```cmake
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
```

`compile_commands.json` records the exact command for every translation unit. It is what
`clang-tidy`, `clangd`, and every editor integration read, and it is the fastest way to answer "is
this file actually compiled with the flag I think?" — including verifying a single file compiles
without touching the shared build directory.

## Warnings and standard

```cmake
target_compile_features(mylib PUBLIC cxx_std_20)

target_compile_options(mylib PRIVATE
    $<$<CXX_COMPILER_ID:GNU,Clang>:-Wall -Wextra -Wpedantic -Wshadow
                                   -Wnon-virtual-dtor -Wold-style-cast -Wconversion>
    $<$<CXX_COMPILER_ID:MSVC>:/W4 /permissive->)
```

- Scope warnings **to your targets**, `PRIVATE`. A third-party or vendored dependency compiled with
  your warning set produces noise you cannot fix and will learn to ignore.
- Make them errors in CI, not locally — a local build that refuses to compile over an unused
  variable interrupts thinking.
- `-Wconversion` and `-Wold-style-cast` are noisy on an existing codebase. Add them on new targets
  and work backwards, rather than turning them on everywhere and suppressing.
- Where a vendored dependency emits deprecation warnings through a header you include, scope the
  suppression to *your* target rather than patching the dependency.

## Dependencies

In rough order of preference:

1. **A system or package-manager package** found with `find_package()`, consumed as an imported
   target.
2. **`FetchContent`** for a small dependency you want pinned to a commit.
3. **A git submodule pinned to a tag**, when the dependency is large, must be built with the project,
   or is patched. Record the pin.

Whichever you choose: **never edit a vendored dependency in place.** Every fix you need belongs in
your own build files, so upgrading stays a pointer change with nothing to reconcile. That rule is
what keeps an engine or library bump from becoming an archaeology exercise.

## A layout that scales

```text
project/
├── CMakeLists.txt          top level: options, dependencies, add_subdirectory
├── cmake/                  helper modules
├── include/project/        public headers — one directory per library
├── src/                    implementation
├── tests/
└── third_party/            or a submodule, pinned
```

Keep public headers in a directory named for the project so an include reads
`#include <project/grid.h>` and cannot collide. Give each library its own `CMakeLists.txt` and let
it declare its own dependencies — that is what makes a target movable.

**Make the layering mechanical.** If a lower layer must not depend on a higher one, the way to
enforce it is a target that links only the lower layer: the day the forbidden include appears, that
target stops linking and the build goes red. A rule in a document is a rule that drifts; a target
that will not link is a rule that cannot.

## Sources

- [CMake `target_include_directories`](https://cmake.org/cmake/help/latest/command/target_include_directories.html) · [`include_directories`](https://cmake.org/cmake/help/latest/command/include_directories.html) — the directory-level warning, quoted
- [Effective Modern CMake](https://gist.github.com/mbinna/c61dbb39bca0e4fb7d1f73b0d66a4fd1) — the target-based model and the `CMAKE_CXX_FLAGS` standard argument
- [Modern CMake](https://cliutils.gitlab.io/modern-cmake/) — the community introduction
- [Professional CMake](https://crascit.com/professional-cmake/) — Craig Scott; the reference text
- [CMake tutorial: usage requirements](https://cmake.org/cmake/help/latest/guide/tutorial/Adding%20Usage%20Requirements%20for%20a%20Library.html)
- [`CMAKE_EXPORT_COMPILE_COMMANDS`](https://cmake.org/cmake/help/latest/variable/CMAKE_EXPORT_COMPILE_COMMANDS.html)
