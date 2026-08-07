---
name: cpp-patterns
description: Use this skill when writing, reviewing, debugging, organizing, or building C++ — headers and modules, ownership and lifetime, RAII and smart pointers, undefined behavior, const correctness, CMake targets, compiler warnings, sanitizers, or a slow or misbehaving build. Do not use it for C, or for another language that merely links a C++ library; for a game on the Axmol engine use `axmol-patterns` alongside this skill.
---

# C++ patterns

Write C++ whose ownership is obvious, whose lifetimes are provable, and whose build is reproducible.
The language will not tell you when you are wrong — the tools will, if you turn them on.

## Establish the toolchain before changing anything

Advice for the wrong standard or a different compiler is worse than no advice. Read the build, not
the source:

```sh
cmake --version && c++ --version
grep -rnE 'CXX_STANDARD|cxx_std_|CMAKE_CXX_FLAGS' CMakeLists.txt */CMakeLists.txt
cmake -B build -G Ninja -DCMAKE_EXPORT_COMPILE_COMMANDS=ON   # a compile DB is the ground truth
```

`compile_commands.json` is the authoritative record of how a file is actually compiled — every flag,
define, and include path. When behaviour disagrees with the source, read it before theorising.

Note the standard. C++20 gives you concepts, ranges, `<span>`, designated initializers and
three-way comparison; C++17 gives you structured bindings, `std::optional`, `string_view` and
`filesystem`. Do not use a feature the project's floor does not have, and do not raise the floor
without being asked.

## Work in this order

1. **Establish ownership.** Who owns this object, and when does it die? Most C++ bugs are this
   question left unanswered.
2. **Make the compiler prove what it can.** `const`, strong types, `enum class`, `[[nodiscard]]`,
   and warnings as errors move failures from runtime to build time.
3. **Turn on the sanitizers before you debug by hand.** Address and UB sanitizers find in one run
   what a week of reading does not.
4. **Fix correctness before performance.** Then measure; do not guess.
5. **Trust the build only when you have proved it is not stale.** A surprising result is a stale
   artifact until shown otherwise — see [`build-loop-traps.md`](references/build-loop-traps.md).

## Rules that always hold

- **No raw `new` / `delete`.** RAII for every resource; `std::unique_ptr` for exclusive ownership,
  `std::shared_ptr` only where ownership genuinely is shared. Core Guideline P.8: "don't leak any
  resources."
- **Never transfer ownership through a raw pointer or reference** (I.11). A raw pointer or reference
  is a non-owning observer, and that is the only thing it should ever mean.
- **A reference or pointer must not outlive its referent.** Returning a reference to a local, or
  holding a pointer into a container that later reallocates, is undefined behaviour with no
  diagnostic.
- **Undefined behaviour is not "probably fine".** The optimiser is entitled to assume it cannot
  happen, so the symptom appears somewhere else, at a different optimisation level.
- **Every resource-owning class obeys the rule of zero, three, or five** — never a subset.
- **`const` by default**, on parameters, methods, and locals. It is free and it documents intent the
  compiler enforces.
- **Warnings are errors in CI.** A warning nobody fails on is a warning nobody reads.
- **One build directory has one writer.** Concurrent builds into one directory corrupt it.

## Read the reference the task needs

| Area | Read for |
|---|---|
| [Project setup](references/project-setup.md) | CMake targets, generators, build directories, the compile database |
| [Organization](references/organization.md) | Headers vs sources, include hygiene, layering, PIMPL, ODR |
| [Ownership and lifetime](references/ownership-and-lifetime.md) | RAII, smart pointers, rule of zero/five, dangling, move semantics |
| [Undefined behavior](references/undefined-behavior.md) | The trap catalog: iterator invalidation, slicing, overflow, init order |
| [Tooling](references/tooling.md) | Sanitizers, clang-tidy, warning sets, debugging a C++ process |
| [Build loop traps](references/build-loop-traps.md) | Stale artifacts, ninja concurrency, phantom failures, trusting an exit code |
| [Anti-patterns](references/anti-patterns.md) | The consolidated do / don't list |
| [Sources](references/sources.md) | The citation basis |

Building a game on the **Axmol** engine? Use **`axmol-patterns`** alongside this skill — it covers the
engine's reference-counted memory model, scene graph, resolution rects, shaders, and migrations. This
skill still owns the language, CMake, and the build loop underneath it.

## Review output shape

```text
[HIGH] Dangling reference returned from accessor
Location: src/world/Grid.cpp:88
Evidence: getTile() returns const Tile& to an element of a std::vector that reserve() may reallocate.
Why: any push_back between the call and the use invalidates the reference; ASan reports a
     heap-use-after-free only when the reallocation happens to move the block.
Fix: return by value, or return an index/handle the caller resolves on use.
Check: build with -fsanitize=address and run the case that grows the container.
```

Prefer a finding a sanitizer or the compiler can reproduce. In C++ especially, "this looks wrong" and
"this is wrong" are different claims, and only one of them survives review.
