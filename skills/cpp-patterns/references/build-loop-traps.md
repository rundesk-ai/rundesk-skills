# Build-loop traps

Read this when a change has no effect, an incremental build does too much, a failure moves between
runs, or the launched binary looks stale.

## Diagnose the artifact before the source

| Symptom | Likely cause | Preferred replacement | Proof |
|---|---|---|---|
| edit has no effect | edited file is absent from the target or a different binary launched | inspect compile database and run the built path directly | build log contains the file; process path/hash matches artifact |
| two builds repeat or interfere | concurrent Ninja processes share one build tree | one invocation, or a build directory per actor | process list and distinct `-B` paths |
| build repeatedly regenerates | CMake input, glob check, or generated file is newer/changing | use `ninja -d explain` and inspect timestamps/input changes | explanation names the dirty edge |
| unrelated failure survives a revert | stale or mixed objects, or a real pre-existing failure | compare with a fresh scratch build | scratch result separates build state from source state |
| probe prints nothing under CTest | passing output is captured | assert the condition, run binary directly, or use verbose/output-on-failure mode | test discovery plus visible assertion/output |
| failed build appears successful | pipeline status came from the last command | capture the build’s own status or enable `pipefail` deliberately | recorded status is nonzero at the failing command |

Treat these as hypotheses, not excuses. A clean scratch build that reproduces the failure makes the
source or configuration the leading suspect again.

## One writer per Ninja tree

Multiple Ninja instances in one build directory are unsupported. Each process computes dirty edges
from its startup view and writes shared build logs; duplicate commands can race on the same outputs.
Let one Ninja invocation provide parallelism. Give background agents, CI jobs, sanitizer variants,
and incompatible configurations separate build directories.

Good:

```sh
cmake -S . -B build/dev -G Ninja
cmake -S . -B build/asan -G Ninja -DENABLE_SANITIZERS=ON
```

Bad: a human and background task both run `cmake --build build/dev` concurrently. Agreement is not a
guard; use the project’s existing lock or fail-fast coordination when a shared script can overlap.

## Preserve the status you need

In shells without `pipefail`, a pipeline’s status is the last command’s status:

```sh
# Bad: reports tail's status, not necessarily the build's.
cmake --build build/dev 2>&1 | tail -60

# Good: keep the build command's status and inspect its bounded log afterward.
cmake --build build/dev > build.log 2>&1
build_status=$?
tail -60 build.log
test "$build_status" -eq 0
```

Do not label the bad form “always successful”: `tail` can also fail, and shells with `pipefail`
behave differently. The trap is losing the status of the command under investigation.

## Compare with fresh state safely

Do not erase a shared build tree to test a theory. Configure a temporary scratch directory, preserve
its log, and remove it only after resolving the exact path and confirming it is disposable.

```sh
scratch_build=$(mktemp -d "${TMPDIR:-/tmp}/cpp-cleanroom.XXXXXX")
cmake -S . -B "$scratch_build" -G Ninja
cmake --build "$scratch_build" > "$scratch_build/build.log" 2>&1
```

If scratch succeeds while the normal tree fails with identical inputs, inspect build state and
generation differences. If both fail, keep the source/configuration failure and stop blaming cache.

## Verify what ran

Before source-level debugging, answer:

1. Did the build command itself exit successfully?
2. Does `compile_commands.json` contain the edited translation unit with expected flags?
3. Is the launched executable the artifact just built? Use its explicit path; inspect duplicate
   artifact paths when identity is unclear.
4. Does the smallest relevant test actually reach the changed path?
5. Does a fresh scratch build behave the same?

For CTest, passing output is normally suppressed unless verbose output is requested. Prefer an
assertion that fails with the observed value; it both proves reachability and starts the regression
test.

See [the source basis](sources.md#build-loop-diagnostics) for Ninja maintainer guidance, CMake/CTest
contracts, and pipeline status semantics.
