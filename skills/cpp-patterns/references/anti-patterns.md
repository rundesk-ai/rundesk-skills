# C++ review checklist

Read this for a broad review. Rank UB, lifetime, races, and wrong results above idiom or style. Each
row names the cheapest useful proof; use the focused reference when the trigger needs more depth.

## Ownership and classes

| Avoid | Prefer | Failure avoided | Proof |
|---|---|---|---|
| naked `new` / `delete` | RAII owner or value | skipped cleanup, leaks, double deletion | early-exit test under ASan/LSan |
| raw pointer that transfers ownership | value or `unique_ptr` | caller cannot know who deletes | trace creation, transfer, and deletion across call sites |
| `shared_ptr` by default | `unique_ptr`; `weak_ptr` for back edges | cycles and hidden lifetime extension | destructor or owner-count test after release |
| stored `[&]` lambda | explicit value capture or proven shared owner | callback reads a dead stack frame | invoke after creator returns under ASan |
| one custom copy/move/destructor operation | rule of zero or explicit coherent set | suppressed moves or incorrect generated copies | type traits plus copy/move/destruction test |
| wrong polymorphic base destructor contract | public virtual, or protected non-virtual | undefined deletion through base | `-Wnon-virtual-dtor` and sanitizer case |
| polymorphic value parameter | reference or owning smart pointer | object slicing | `cppcoreguidelines-slicing` or dispatch test |
| unmarked override | `override` | signature drift stops dispatch | compiler rejects the mismatched signature |
| `noexcept` that disagrees with move behavior | match it to the implementation | termination or avoidable relocation copies | throwing-path test and copy/move counters |

## Correctness and concurrency

| Avoid | Prefer | Failure avoided | Proof |
|---|---|---|---|
| read before initialization | initialize at declaration | UB or erroneous value | MSan on the executed read |
| incrementing an invalidated erase iterator | use returned iterator or `erase_if` | dangling iterator access | ASan with an erasing case |
| `map[key]` only to test membership | `contains`/`find`; `at` for checked access | accidental insertion | assert size unchanged on a miss |
| signed overflow or unchecked shift | validate range first | optimizer-exploitable UB | UBSan at boundary values |
| mixed signed/unsigned arithmetic | range loop, matching type, or `std::cmp_*` | reversed comparison or underflow | warning plus negative/empty boundary test |
| required check in `assert` | normal error handling | `NDEBUG` removes the check | release test with `NDEBUG` |
| initializer list unlike member order | match declaration order | misleading order or premature member read | `-Wreorder` and dependent-initializer test |
| `volatile` for threading | `atomic` or lock | data race; no ordering or atomicity | TSan on the concurrent path |
| separately protected check then write | one critical section or compound operation | time-of-check/time-of-use race | concurrent test verifies one computation/update |
| C-style cast | narrow named cast | hidden const removal or reinterpretation | `cppcoreguidelines-pro-type-cstyle-cast` |

## Interfaces and source structure

| Avoid | Prefer | Failure avoided | Proof |
|---|---|---|---|
| primitive ids/flags with ambiguous meaning | domain type, `enum class`, or named functions | swapped arguments and opaque calls | swapped-call compile test or call-site review |
| output parameters for ordinary results | returned value/struct/optional | unclear writes and partial-result paths | test each return/error path; inspect call sites |
| `using namespace` in a header | qualification or local using-declaration | consumer name collisions | compile a consumer declaring the colliding name |
| reliance on transitive includes | include each named dependency | unrelated header cleanup breaks compilation | standalone header compile or IWYU |
| non-inline external definition in a header | one source definition or valid inline definition | duplicate definitions / ODR failure | link two translation units that include it |

## Build, evidence, and performance

| Avoid | Prefer | Failure avoided | Proof |
|---|---|---|---|
| directory-wide CMake properties | `target_*` with narrow scope | hidden target dependencies | inspect verbose commands for unrelated targets |
| source globs | explicit sources | additions/removals evade reliable regeneration | add/remove fixture without manual reconfigure |
| concurrent Ninja runs in one tree | one invocation or directory per actor | duplicated commands and shared-state races | process list plus distinct `-B` paths |
| piped build with lost status | capture build status, then inspect bounded log | debugging an artifact that never linked | compare pipeline and build-command statuses |
| warnings imposed on dependencies | `PRIVATE` project warnings | unfixable dependency noise | verbose dependency compile command |
| performance claim from Debug or intuition | profile optimized build; benchmark like-for-like | work on a non-bottleneck | profiler trace and repeatable benchmark |
| unexplained suppression | narrow suppression with reason and scope | permanent blind spot | reproduce finding without suppression; inspect adjacent justification |
| “looks wrong” defect | reproducer plus language/tool evidence | false-positive review churn | failing test or diagnostic before the fix |

Do not modernize beyond the configured standard, reformat unrelated code, or broaden a fix while
collecting evidence. Use [ownership](ownership-and-lifetime.md), [undefined behavior](undefined-behavior.md),
[tooling](tooling.md), and [build-loop diagnostics](build-loop-traps.md) when a row triggers.

The [source basis](sources.md) maps these practices to the C++ Core Guidelines, cppreference,
toolchain documentation, analyzer catalogs, and practitioner guidance.
