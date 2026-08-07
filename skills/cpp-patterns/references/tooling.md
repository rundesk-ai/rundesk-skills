# Tooling

Read this before debugging C++ by hand. The tools find in one run what reading finds in a week, and
several classes of bug are effectively undiagnosable without them.

## Contents

- [Sanitizers](#sanitizers)
- [Static analysis](#static-analysis)
- [Warnings that earn their place](#warnings-that-earn-their-place)
- [Debugging a running process](#debugging-a-running-process)
- [Performance](#performance)
- [A working CI shape](#a-working-ci-shape)

## Sanitizers

Compiler instrumentation that catches at runtime what the language does not check. **This is the
first move for any suspected memory or UB bug**, not the last.

```sh
cmake -B build/asan -G Ninja -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_CXX_FLAGS="-fsanitize=address,undefined -fno-omit-frame-pointer -g"
cmake --build build/asan && UBSAN_OPTIONS=print_stacktrace=1 ./build/asan/tests
```

| Sanitizer | Finds | Cost |
|---|---|---|
| **ASan** (`address`) | Heap/stack/global overflow, use-after-free, use-after-return, leaks | ~2× slower, ~3× memory |
| **UBSan** (`undefined`) | Signed overflow, bad shifts, misaligned access, null deref, bad casts | Small |
| **TSan** (`thread`) | Data races | ~5–15× slower, ~5× memory |
| **MSan** (`memory`) | Reads of uninitialized memory | Needs an instrumented stdlib; hardest to adopt |

Rules that make them work:

- **ASan and UBSan combine. TSan combines with neither** — run it as a separate configuration.
- Build with **`-g` and `-fno-omit-frame-pointer`** or the traces are unreadable, and make sure
  `llvm-symbolizer` is on `PATH`.
- Use **`RelWithDebInfo`** or `Debug`; sanitizer output from a stripped release build is noise.
- **`UBSAN_OPTIONS=print_stacktrace=1`** — without it UBSan prints a one-line complaint and no
  location, which is the difference between a lead and a shrug.
- **They only find what executes.** A silent run means the path was not reached *or* the code is
  clean; confirm which before concluding.
- Keep a sanitizer build directory permanently configured. The friction of setting one up mid-bug is
  why people skip the step that would have solved it.

## Static analysis

**`clang-tidy`** reads `compile_commands.json` and finds bugs, modernization opportunities, and
guideline violations without running anything.

```yaml
# .clang-tidy
Checks: >
  bugprone-*,
  clang-analyzer-*,
  cppcoreguidelines-*,
  modernize-*,
  performance-*,
  readability-*,
  -modernize-use-trailing-return-type,
  -readability-magic-numbers
WarningsAsErrors: 'bugprone-*,clang-analyzer-*'
HeaderFilterRegex: '^(src|include)/'
```

- **`HeaderFilterRegex` matters.** Without it you get findings from every third-party header you
  include, and the signal is gone.
- Adopt incrementally: turn on `bugprone-*` and `clang-analyzer-*` as errors first, the rest as
  warnings, and tighten.
- Run it on **changed files** in CI, not the whole tree, or it becomes a job people skip.
- `clang-format` with a committed `.clang-format` ends formatting arguments; run it in a pre-commit
  hook so it never appears in a review.
- **`include-what-you-use`** checks the include-hygiene rule mechanically.

## Warnings that earn their place

```
-Wall -Wextra -Wpedantic
-Wshadow                  a local hiding a member is a real bug source
-Wnon-virtual-dtor        deleting through a base pointer is UB
-Wold-style-cast          C casts hide reinterpret_cast
-Wconversion              silent narrowing
-Wsign-compare            -1 < 0u is false
-Wreorder                 members initialize in declaration order, not list order
```

MSVC: `/W4 /permissive-`.

Scope them **`PRIVATE`** to your own targets — a vendored dependency compiled with your warning set
produces noise you cannot fix and will learn to ignore. Make them errors in CI rather than locally.

## Debugging a running process

| Situation | Tool |
|---|---|
| Crash with a core dump | `lldb ./app -c core` / `gdb ./app core`, then `bt` |
| Reproducible crash | Run under `lldb`/`gdb`; `bt`, `frame select`, `p expr` |
| Hang or deadlock | Attach and get **all** thread stacks: `lldb -p <pid>` then `thread backtrace all` |
| Wrong value, no crash | A conditional breakpoint on the iteration that goes wrong |
| Memory growth | `leaks` (macOS) / `valgrind --leak-check=full`, or ASan's leak detector |
| "Which flags built this file?" | `compile_commands.json` |

`thread backtrace all` on a hung process is the highest-value single command in this table — a
deadlock is visible immediately as two threads each holding what the other wants.

Conditional breakpoints beat print statements for the same reason as in every language: you get
everything in scope, not only what you thought to print. And a print from a crashed or buffered
process may never appear at all, which reads as "the line never ran."

## Performance

**Measure first.** The Core Guidelines' performance section opens with exactly this, and C++ makes it
especially easy to optimise something that was never the cost.

- `perf` (Linux), Instruments (macOS), VTune. A sampling profiler tells you where time goes;
  intuition does not.
- Benchmark with something that handles warmup and statistics, not a wall-clock delta.
- Compare like with like — always `RelWithDebInfo` or `Release`. A `Debug` measurement is
  meaningless, sometimes by 10×.
- Before micro-optimising: check the algorithm, the allocations, and the cache behaviour. Contiguous
  data beats clever code far more often than the reverse.
- Build time is performance too. `-ftime-trace` (Clang) shows which headers dominate a compile.

## A working CI shape

1. **Build** with warnings as errors, on every supported compiler.
2. **Test** — the fast, dependency-free suite first.
3. **ASan + UBSan** over the test suite.
4. **TSan** over the test suite, separately, if there are threads.
5. **clang-tidy** on changed files.
6. **clang-format** check.

Steps 3 and 4 are what make the difference. A test suite that passes without sanitizers proves the
code produced the right answer on this run, not that it is correct — and in C++ that distinction is
the whole game.

## Sources

- [AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html) · [UndefinedBehaviorSanitizer](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html) · [ThreadSanitizer](https://clang.llvm.org/docs/ThreadSanitizer.html) · [MemorySanitizer](https://clang.llvm.org/docs/MemorySanitizer.html)
- [The complete C/C++ sanitizers handbook](https://gist.github.com/MangaD/3b46e4c5ef4c63e44a21bed39ae64093) — flags, combinations, and what each catches
- [cpp-sanitizers examples](https://github.com/Toxe/cpp-sanitizers) — runnable demonstrations per bug class
- [clang-tidy](https://clang.llvm.org/extra/clang-tidy/) · [check list](https://clang.llvm.org/extra/clang-tidy/checks/list.html) · [clang-format](https://clang.llvm.org/docs/ClangFormat.html)
- [Include What You Use](https://include-what-you-use.org/)
- [C++ Core Guidelines — Per: Performance](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-performance) — measure before optimizing
- [LLDB command map](https://lldb.llvm.org/use/map.html) — lldb/gdb equivalents
