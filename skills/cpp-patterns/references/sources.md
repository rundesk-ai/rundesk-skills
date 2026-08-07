# C++ source basis

This package is a Rundesk synthesis of the C++ Core Guidelines, the standard-library reference, the
toolchain's own documentation, and failures recorded during real C++ game development. Use this file
to audit or update a claim.

**Read in this order of authority.** The standard and cppreference say what the language does; the
Core Guidelines say what to do about it; the sanitizer and lint catalogs record what people actually
get wrong; project experience supplies the traps no document lists. Verified in **August 2026**.

## The language

- [cppreference](https://en.cppreference.com/) — the practical reference. Specifically
  [undefined behavior](https://en.cppreference.com/w/cpp/language/ub),
  [object lifetime](https://en.cppreference.com/w/cpp/language/lifetime),
  [initialization](https://en.cppreference.com/w/cpp/language/initialization),
  [the One Definition Rule](https://en.cppreference.com/w/cpp/language/definition),
  [RAII](https://en.cppreference.com/w/cpp/language/raii),
  [move semantics](https://en.cppreference.com/w/cpp/utility/move), and the per-container
  [iterator invalidation rules](https://en.cppreference.com/w/cpp/container).

## Guidelines

- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines) — Stroustrup and
  Sutter. Sixteen sections; the ones this package leans on are **P** (philosophy), **I** (interfaces),
  **F** (functions), **C** (classes), **R** (resource management), **ES** (expressions and
  statements), **Con** (constants), **CP** (concurrency), **Per** (performance) and **SF** (source
  files). Rules cited by ID: **P.8** don't leak any resources · **I.1** make interfaces explicit ·
  **I.2** avoid non-const globals · **I.4** precisely and strongly typed · **I.11** never transfer
  ownership by a raw pointer or reference · **F.15** conventional parameter passing · **C.20** rule of
  zero · **C.21** rule of five · **C.35** virtual destructor on a polymorphic base.
- The zero-overhead principle — "what you don't use, you don't pay for" — is the reasoning behind
  several of the performance rules.

## Build

- [CMake documentation](https://cmake.org/cmake/help/latest/) — especially
  [`target_include_directories`](https://cmake.org/cmake/help/latest/command/target_include_directories.html)
  and [`include_directories`](https://cmake.org/cmake/help/latest/command/include_directories.html),
  which carries the warning that directory-level commands make every target below inherit the
  property and "increase the chance of hidden dependencies."
- [Effective Modern CMake](https://gist.github.com/mbinna/c61dbb39bca0e4fb7d1f73b0d66a4fd1) — the
  target-based model, and why setting the standard through `CMAKE_CXX_FLAGS` breaks.
- [Modern CMake](https://cliutils.gitlab.io/modern-cmake/) ·
  [Professional CMake](https://crascit.com/professional-cmake/) — Craig Scott, the reference text
  (the domain rejects automated requests, so this link cannot be link-checked; it is a book
  recommendation, not a claim-bearing citation) ·
  [cmake-examples](https://github.com/pr0g/cmake-examples).
- [Ninja manual](https://ninja-build.org/manual.html) ·
  [ctest](https://cmake.org/cmake/help/latest/manual/ctest.1.html) — output capture, which is why a
  printing probe is silent on success.

## Tooling

- [AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html) ·
  [UndefinedBehaviorSanitizer](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html) ·
  [ThreadSanitizer](https://clang.llvm.org/docs/ThreadSanitizer.html) ·
  [MemorySanitizer](https://clang.llvm.org/docs/MemorySanitizer.html). UBSan's check list doubles as a
  catalog of undefined behaviour worth knowing.
- [The complete C/C++ sanitizers handbook](https://gist.github.com/MangaD/3b46e4c5ef4c63e44a21bed39ae64093)
  and [cpp-sanitizers](https://github.com/Toxe/cpp-sanitizers) — flag combinations, and runnable
  demonstrations per bug class.
- [clang-tidy](https://clang.llvm.org/extra/clang-tidy/) and its
  [check list](https://clang.llvm.org/extra/clang-tidy/checks/list.html) — like every lint catalog, a
  record of what people actually get wrong rather than a style opinion.
- [clang-format](https://clang.llvm.org/docs/ClangFormat.html) ·
  [Include What You Use](https://include-what-you-use.org/) ·
  [LLDB command map](https://lldb.llvm.org/use/map.html).

## Axmol

- [Axmol](https://github.com/axmolengine/axmol) — C++20 requirement, supported platforms and render
  backends, v2 LTS versus the v3 development branch.
- [Axmol FAQ](https://github.com/axmolengine/axmol/wiki/FAQ) — **reference counting with no smart
  pointers planned**, `setup.ps1` and axslcc troubleshooting, the `AXLOGD`-family logging change at
  v2.1.3, glob regeneration when adding a source file, and the Android multi-touch gesture
  interception.
- [Cocos2d-x migration guide](https://github.com/axmolengine/axmol/wiki/Cocos2d%E2%80%90x-migration-guide) —
  the `ax` namespace, `USING_NS_AX`, renamed types, deprecated Cocos types in favour of the standard
  library, and the `axmol-migrate` tool's v4.0-only scope.
- [Axmol vs Cocos2d-x](https://github.com/axmolengine/axmol/wiki/Axmol-vs-Cocos2d%E2%80%90x) ·
  [Axmol manual](https://axmol.dev/manual/latest/) ·
  [DevSetup](https://github.com/axmolengine/axmol/blob/dev/docs/DevSetup.md).
- [Apple: Launch Services](https://developer.apple.com/documentation/coreservices/launch_services) —
  bundle-identifier registration, the mechanism behind the duplicate-bundle trap.

## Recorded project experience

Several items here are not in any vendor document. They were recorded during development of two
independent 2D games on **Axmol v2.11.x** with CMake and Ninja on macOS, and are carried here
generalized, without project identifiers:

- **Ninja is not concurrency-safe on one build directory** — corrupted dependency logs causing full
  rebuilds, reconfigure loops from inconsistent stamps, and zero-byte archives from concurrent `ar`.
- **Duplicate application bundles share a bundle identifier**, and macOS Launch Services resolves by
  identifier globally, so `open` can launch a different copy than the path given — presenting as "I
  rebuilt and it comes up old."
- **`cmd | tail` reports the pipe's exit status**, and **`ninja -n` does not execute side-effect
  edges**, so both can report success or a small step count for a build that did neither.
- **Rapid edit/revert cycles on a widely-included header can leave translation units compiled against
  different header states** — an ODR violation surfacing as failures in unrelated suites.
- **A `ClippingNode` nested inside another `ClippingNode` blanks the surrounding UI**, and camera,
  HUD and hit-testing must share one full-frame rect rather than `getVisibleSize()`. Both were hit
  independently in **both** projects, which is why this package states them as engine behaviour.
- **Four Xcode-only Axmol build settings must be reproduced** in the project's own CMake for a Ninja
  build on macOS to compile and launch.
- **`EventListenerMouse` callbacks return `bool`** in v2.11.x.
- **A shader's `#version` must be the first line**, and duplicated shader logic drifts unless shared
  through `#include`, which axslcc supports.
- **A header owning containers of private incomplete types needs all used special members declared
  out of line**, not only the destructor.

## What this package deliberately does not cite

- Tutorials written against C++98/03 idioms without saying so. Most bad C++ advice online is age, not
  error.
- Benchmark posts with no published method or build type.
- Style opinions presented as correctness. Where this package takes a position it says so and gives
  the failure it prevents.
- Engine documentation for Cocos2d-x, except where the migration path is the subject — the APIs have
  diverged.
