# C++ source basis

Audited 2026-08-07. This package uses language/library references for contracts, tool vendors for
diagnostic behavior, and maintainer or practitioner guidance for defaults and recurring traps. It
does not treat a source homepage, anonymous summary, or unsupported project anecdote as evidence.

## Ownership, lifetime, and classes

- The [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines) establish
  the practices synthesized here: P.8 resource safety; I.11 ownership transfer; F.15/F.16–F.21
  parameter passing; C.20/C.21 special members; C.35 base destruction; C.66 nonthrowing moves; and
  R.20/R.21 preferring smart owners and `unique_ptr` unless ownership is shared.
- cppreference documents the contracts for [RAII](https://en.cppreference.com/w/cpp/language/raii),
  [`unique_ptr`](https://en.cppreference.com/w/cpp/memory/unique_ptr),
  [`shared_ptr`](https://en.cppreference.com/w/cpp/memory/shared_ptr),
  [`std::move`](https://en.cppreference.com/w/cpp/utility/move), and per-container
  [invalidation](https://en.cppreference.com/w/cpp/container). These support cleanup on scope exit,
  incomplete-type limits, cycles, valid-but-unspecified moved-from standard objects, and the rule to
  check invalidation per operation.
- Abseil’s practitioner guidance adds concrete review defaults: [TotW 180](https://abseil.io/tips/180)
  on dangling references, [TotW 234](https://abseil.io/tips/234) on parameter contracts, and
  [TotW 77](https://abseil.io/tips/77) on copies and moves.

## Source files, interfaces, and PIMPL

- Core Guidelines [SF: Source files](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-source)
  supports self-contained headers, matching-header-first order, and avoiding namespace directives in
  headers; [I: Interfaces](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-interfaces)
  supports strong, explicit interfaces and PIMPL for stable library ABI.
- cppreference documents [`#pragma once` as non-standard](https://en.cppreference.com/w/cpp/preprocessor/impl),
  the [ODR and inline requirements](https://en.cppreference.com/w/cpp/language/definition), and the
  [PIMPL incomplete-type constraint](https://en.cppreference.com/w/cpp/language/pimpl).
- [Include What You Use](https://include-what-you-use.org/) supplies the community tool and rationale
  for direct includes rather than accidental transitive dependencies.

## Build and project structure

- CMake documents target usage requirements in
  [`target_include_directories`](https://cmake.org/cmake/help/latest/command/target_include_directories.html),
  [`target_compile_features`](https://cmake.org/cmake/help/latest/command/target_compile_features.html),
  and its [usage-requirements tutorial](https://cmake.org/cmake/help/latest/guide/tutorial/Adding%20Usage%20Requirements%20for%20a%20Library.html).
  Its [`include_directories`](https://cmake.org/cmake/help/latest/command/include_directories.html)
  page prefers target scope, and [`file(GLOB)`](https://cmake.org/cmake/help/latest/command/file.html#glob)
  explicitly discourages source globs and states the cost and generator caveat of `CONFIGURE_DEPENDS`.
  [`FetchContent`](https://cmake.org/cmake/help/latest/module/FetchContent.html) recommends commit
  hashes for remote Git content because they are more secure and verify expected content.
- [`CMAKE_EXPORT_COMPILE_COMMANDS`](https://cmake.org/cmake/help/latest/variable/CMAKE_EXPORT_COMPILE_COMMANDS.html)
  defines the compile-database content and its Makefile/Ninja generator boundary.
- [Modern CMake](https://cliutils.gitlab.io/modern-cmake/) and
  [Effective Modern CMake](https://gist.github.com/mbinna/c61dbb39bca0e4fb7d1f73b0d66a4fd1)
  are community/practitioner sources for target-scoped design and avoiding global compiler flags.

## Undefined behavior and diagnostics

- cppreference maps the language contract for [undefined behavior](https://en.cppreference.com/w/cpp/language/ub),
  [object lifetime](https://en.cppreference.com/w/cpp/language/lifetime),
  [initialization](https://en.cppreference.com/w/cpp/language/initialization), and the
  [One Definition Rule](https://en.cppreference.com/w/cpp/language/definition). The specific
  [`vector` invalidation table](https://en.cppreference.com/w/cpp/container/vector),
  [checked `at()`](https://en.cppreference.com/w/cpp/container/vector/at), and
  [unchecked `operator[]`](https://en.cppreference.com/w/cpp/container/vector/operator_at) support
  the container guidance without generalizing all mutations.
- Clang documents what [ASan](https://clang.llvm.org/docs/AddressSanitizer.html),
  [UBSan](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html),
  [TSan](https://clang.llvm.org/docs/ThreadSanitizer.html), and
  [MSan](https://clang.llvm.org/docs/MemorySanitizer.html) detect, their platform limits, and the
  instrumentation required. The [Clang user manual](https://clang.llvm.org/docs/UsersManual.html)
  states that address, thread, and memory sanitizers cannot be combined in one program.
- [cpp-sanitizers](https://github.com/Toxe/cpp-sanitizers) provides community-maintained runnable
  examples for the sanitizer configurations rather than prose-only claims.

## Build-loop diagnostics

- A [Ninja maintainer discussion](https://groups.google.com/g/ninja-build/c/4VP7whvWSH8)
  states that concurrent Ninja instances in one build directory are unsupported and explains the
  independent dirty graphs and shared `.ninja_log`. This supports separate directories; it does not
  support claiming that every concurrent run corrupts Ninja’s own logs.
- The [Ninja manual](https://ninja-build.org/manual.html) documents `-d explain`, dependency/build
  logs, and incremental decisions. CMake documents the [`--build`](https://cmake.org/cmake/help/latest/manual/cmake.1.html)
  wrapper and [CTest output modes](https://cmake.org/cmake/help/latest/manual/ctest.1.html).
- The [Bash pipeline manual](https://www.gnu.org/software/bash/manual/html_node/Pipelines.html)
  establishes last-command status by default and the `pipefail` exception.

## Tooling and practitioner guidance

- [clang-tidy](https://clang.llvm.org/extra/clang-tidy/) and its
  [versioned check catalog](https://clang.llvm.org/extra/clang-tidy/checks/list.html) support
  compile-database analysis; [clang-format](https://clang.llvm.org/docs/ClangFormat.html) and
  [LLDB’s command map](https://lldb.llvm.org/use/map.html) support formatting and debugger actions.
- [C++ Best Practices](https://github.com/lefticus/cppbestpractices), maintained by Jason Turner and
  contributors, is the practitioner basis for introducing warnings, analyzers, sanitizers, and
  optimized-build measurement as a coherent quality ratchet.
