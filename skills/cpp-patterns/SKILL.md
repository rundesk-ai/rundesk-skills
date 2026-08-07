---
name: cpp-patterns
description: Use when writing, reviewing, debugging, organizing, or building C++: ownership and lifetime, undefined behavior, headers, CMake targets, warnings, sanitizers, or stale builds. It supplies modern C++ defaults, failure modes, and an evidence-first workflow. Do not use it for C or for another language that only links a C++ library; use `axmol-patterns` alongside it for Axmol games.
---

# C++ patterns

Make ownership visible, lifetimes defensible, and builds reproducible.

## Establish the environment

Read the build before changing source:

```sh
c++ --version
rg --files -uuu -g 'compile_commands.json'
test ! -f CMakeLists.txt || cmake --version
test ! -f CMakeLists.txt || rg 'CXX_STANDARD|cxx_std_|CMAKE_CXX_FLAGS' -g 'CMakeLists.txt'
```

Confirm the compiler, generator, standard floor, and exact command in `compile_commands.json` when
available. For a non-CMake project, inspect its active build configuration rather than translating
it into CMake. Do not introduce a newer language feature or raise the floor without approval.

## Work in this order

1. Establish who owns each resource and when it dies.
2. Reproduce the failure; confirm the edited file and launched binary belong to the same build.
3. Enable compiler warnings and the relevant sanitizer before debugging suspected lifetime, UB, or
   race failures by inspection.
4. Fix correctness, then profile before changing code for performance.
5. Run the smallest relevant test, then the wider suite.

## Defaults and failure modes

| Prefer | Avoid | Failure prevented |
|---|---|---|
| RAII and values | naked `new` / `delete` | leaks and partial cleanup on early exit or exceptions |
| `unique_ptr` for ownership; `shared_ptr` only for shared lifetime | raw owning pointers | ambiguous deletion and reference cycles |
| rule of zero; otherwise consider the full copy/move/destructor set | one ad hoc special member | accidental copies, double deletion, or disabled moves |
| `const` where mutation is not intended | mutable-by-default state | unreviewable side effects |
| target-scoped CMake properties | directory-wide flags and includes | hidden transitive build dependencies |
| separate build directories for concurrent/configuration-specific work | concurrent writers in one Ninja tree | duplicated commands and shared build-state races |
| compiler, sanitizer, or failing-test evidence | “this looks wrong” | speculative review findings |

## Read only what the task needs

- Creating targets or changing CMake: [project setup](references/project-setup.md).
- Splitting headers, source, or layers: [organization](references/organization.md).
- Designing owners, views, RAII, or moves: [ownership and lifetime](references/ownership-and-lifetime.md).
- Investigating optimizer-sensitive or impossible behavior: [undefined behavior](references/undefined-behavior.md).
- Configuring diagnostics or debugging a process: [tooling](references/tooling.md).
- Investigating stale, overbuilt, or wrong artifacts: [build-loop traps](references/build-loop-traps.md).
- Reviewing broadly: [anti-pattern checklist](references/anti-patterns.md).
- Auditing a technical claim: [source basis](references/sources.md).

For Axmol, load `axmol-patterns` too. It owns engine lifetime, scene graph, resolution, shader, and
migration guidance; this skill still owns C++, CMake, and the build loop.

## Report reproducible findings

```text
[HIGH] Dangling vector element reference
Location: src/world/Grid.cpp:88
Evidence: push_back changes capacity before the saved reference is read; ASan reports
heap-use-after-free in the reproducer.
Fix: return a value or stable handle, or resolve an index after mutation.
Check: rerun the growth case under ASan.
```

Separate defects from preferences. Report the language rule or observed diagnostic, the triggering
path, and a check for the fix.
