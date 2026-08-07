# Tooling

Read this before debugging suspected memory corruption, UB, races, or a native process by hand.

## Match the diagnostic to the failure

| Symptom | First tool | What success looks like |
|---|---|---|
| invalid access, lifetime, bounds | ASan | report names allocation/free and access stacks |
| arithmetic, alignment, null, invalid operation | UBSan | report names the executed UB check and location |
| data race | TSan, in a separate build | report shows both conflicting accesses and thread creation |
| uninitialized read | MSan, with instrumented dependencies | origin/use trace reaches the read |

ASan and UBSan can combine. Clang does not allow ASan, TSan, and MSan in the same program, so use
separate build directories. Sanitizers find only executed paths.

```sh
cmake -S . -B build/asan -G Ninja -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_CXX_FLAGS='-fsanitize=address,undefined -fno-omit-frame-pointer -g'
cmake --build build/asan
UBSAN_OPTIONS=print_stacktrace=1 ./build/asan/tests
```

Prefer target-scoped sanitizer options when editing CMake; both compile and link steps need the
flags. Keep debug information, follow the toolchain’s symbolizer instructions, and check platform
support before assuming optional checks such as leak or use-after-return detection are enabled.

Do not suppress a report until a minimal reproduction proves it comes from code outside the task.
Keep suppressions narrow and explain the accepted risk; broad ignore lists also hide real defects.

## Use static analysis as a ratchet

`clang-tidy` needs a compile database. Begin with correctness checks on changed project files, then
expand only after the baseline is manageable.

```yaml
Checks: >
  bugprone-*,
  clang-analyzer-*,
  performance-*
WarningsAsErrors: 'bugprone-*,clang-analyzer-*'
HeaderFilterRegex: '(^|/)(src|include)/'
```

Choose checks for the project and installed clang-tidy version; this is a starting shape, not a
portable fixed list. Filtering project headers prevents dependency diagnostics from drowning the
signal. Run changed files in CI while introducing the tool; a whole-tree gate with thousands of
legacy findings will be bypassed rather than fixed.

Use a committed `clang-format` configuration for formatting and Include What You Use for mechanical
include-hygiene checks. Each suppression should include the check name and reason.

## Debug the process state

| Symptom | Action | Proof |
|---|---|---|
| reproducible crash | run under LLDB/GDB; capture backtrace and relevant frame values | stack reaches the faulting operation |
| hang | attach and capture all thread stacks | blocked threads and held/waited resources explain the cycle |
| wrong value | conditional breakpoint at the first bad iteration | watch the value change before downstream damage |
| unknown compile flags | inspect the translation unit in `compile_commands.json` | command includes the expected define/include/standard |

Prefer debugger state to temporary prints when crashes, buffering, or timing can hide output.

## Measure performance claims

Profile an optimized build with symbols (`RelWithDebInfo` where supported) before changing code.
Use a sampling profiler appropriate to the platform, then benchmark the isolated change with the
same compiler, flags, data, and warmup. A Debug/Release comparison measures build modes, not the
optimization under review.

Check algorithmic complexity, allocation count, and data layout before rewriting a loop. For build
time, Clang’s `-ftime-trace` can identify expensive translation units and headers.

## CI baseline

1. Build supported compilers with the project’s stable warnings as errors.
2. Run fast tests, then the full relevant suite.
3. Run ASan plus UBSan.
4. Run TSan separately when shared-memory concurrency exists.
5. Ratchet clang-tidy and formatting over changed code.

See [the source basis](sources.md#undefined-behavior-and-diagnostics) for sanitizer contracts and
[tooling-and-practitioner-guidance](sources.md#tooling-and-practitioner-guidance) for analyzer,
debugger, and community practice.
