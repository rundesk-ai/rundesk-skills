# Build loop traps

Read this when a build result does not make sense: a change with no effect, a rebuild that recompiles
the world, a failure in code you did not touch, or a binary that behaves like an older one.

**The governing rule: in C++, a surprising result is a build artifact until proven otherwise.** The
compile-link-run loop has more places to go stale than most ecosystems, and every hour spent
debugging a stale binary is spent on a bug that is not there.

## Contents

- [One writer per build directory](#one-writer-per-build-directory)
- [Exactly one artifact](#exactly-one-artifact)
- [Trusting an exit code](#trusting-an-exit-code)
- [Phantom failures and the ODR](#phantom-failures-and-the-odr)
- [When the cache is corrupt, reset it](#when-the-cache-is-corrupt-reset-it)
- [A probe that prints is invisible](#a-probe-that-prints-is-invisible)
- [The stale-build checklist](#the-stale-build-checklist)

## One writer per build directory

**Ninja is not concurrency-safe on a single build directory.** Two builds at once — a developer's dev
loop, a background build, an agent, a CI runner sharing a volume — corrupt it in three distinct ways:

- `.ninja_deps` / `.ninja_log` are corrupted, producing `ninja: warning: premature end of file;
  recovering`. Ninja then does not know what is built and **recompiles everything**, turning a
  one-second rebuild into a full one.
- Stamp files end up inconsistent — a glob-verification file newer than `build.ninja` — so CMake
  re-runs on **every** build, invalidating everything each time. A reconfigure loop.
- Two `ar` invocations on one archive truncate it to zero bytes. The link then fails with something
  like `file is empty in lib/libFoo.a`, which reads as a corrupt dependency rather than a race.

**Rules:**

- One build per build directory, enforced rather than agreed. A lock file around the dev-loop script
  makes a second concurrent build fail fast instead of corrupting the cache.
- Never start a background build against the directory a human may be using.
- If another actor must build, give it **its own throwaway directory** — never the shared one.
- Healthy rebuild check: a no-op build reports no work in about a second. If it starts compiling the
  dependency tree, the cache is already corrupt.

## Exactly one artifact

**More than one build directory producing a runnable application is a trap, not a convenience.**

On macOS this is at its worst: every bundle built from the same project carries the same
`CFBundleIdentifier`, and **Launch Services registers applications by bundle id globally**. So `open`
can launch a *different* copy than the path you gave it — including `open -n /full/path/App.app`. The
symptom is brutal and misleading: you rebuild, you launch, and you get an old binary. Every fix
"makes no difference." The bug looks like it is in your code and it is in your launcher.

**Rules:**

- Exactly one build directory produces the application. Everything else — headless tests, sanitizer
  builds, single-file compile checks — must produce **no** runnable bundle.
- **First diagnostic for "I rebuilt but it comes up old":** search the tree for the artifact.
  More than one hit is the bug.
- Clean up: kill the running process, delete every stray build directory, then flush and re-register:

```sh
find . -name 'App.app' -maxdepth 4        # expect exactly one
rm -rf build-verify build-agent*          # never the shared dev directory
LSREG=/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister
"$LSREG" -kill -r -domain local -domain user
"$LSREG" -f path/to/the/one/App.app
```

- A stray bundle left behind is a landmine for the **next** session, not this one. Clean up before
  you stop.

## Trusting an exit code

```sh
cmake --build build | tail -60          # reports tail's status — ALWAYS success
```

A pipe replaces the exit code with the last command's. A build that failed at the link step reports
success, and you go on to debug a binary that was never produced.

```sh
cmake --build build > build.log 2>&1; echo "exit=$?"    # trust this
grep -cE '^\[' build.log                                 # step count, for diagnosing over-rebuilds
```

The same applies to a chained background command: `cmd; tail` reports `tail`'s status. Run the
command whose result you care about alone.

**`ninja -n` (dry run) also lies** when the build has side-effect edges. It does not execute the
glob-recheck or reconfigure edges, so it cannot see the rebuild they trigger — it will report two
actions where a real build does hundreds. To answer "why does this rebuild so much," time a real
build and count its steps.

## Phantom failures and the ODR

**A failure in a suite your change cannot reach is a build artifact until proven otherwise.**

The mechanism: a widely-included header is edited, the build runs, the edit is reverted, the build
runs again — several times within a few seconds, as happens when probing whether a test has teeth.
Ninja decides by mtime, and cycles that fast can leave some translation units compiled against the
old header and some against the new. Inline functions then disagree across TUs — an **ODR violation**,
which is undefined behaviour, and it surfaces as nonsense failures wherever it happens to trip.

The tells: a failure that **moves between runs**, or one that **survives a full restore** of every
file you touched.

**Confirm with a clean-room build, not by re-running.** Configure a scratch build directory and build
every TU against one header state:

```sh
cmake -B /tmp/cleanroom -G Ninja -DHEADLESS_ONLY=ON && cmake --build /tmp/cleanroom
```

Two caveats that keep this honest:

- **Do not wipe the shared build directory** to "clean" it. Use a scratch path.
- **This does not license blaming a stale build for a real bug.** The claim is allowed only with the
  clean-room result as evidence. Without it, assume the bug is yours.

When a teeth-proving pass needs many rapid edit/revert cycles, prefer probing a header few TUs
include, or accept the rebuild cost.

## When the cache is corrupt, reset it

There is a strong temptation to theorise — regenerated headers, glob mismatches, dependency scanning.
Resist it. When a build directory behaves impossibly (a dry run and a real build disagree, stamps are
inconsistent, an archive is empty), the answer is almost always that its **state** is bad, not its
**configuration**:

```sh
pkill -x App 2>/dev/null
rm -rf build/dev build/.dev.lock
cmake -B build/dev -G Ninja && cmake --build build/dev
```

A from-scratch configure writes all stamps consistently, which is what breaks a reconfigure loop.
If an identical configuration works elsewhere, the difference is state.

## A probe that prints is invisible

**`ctest` captures stdout and replays it only for failures.** A temporary test that *prints* the
value you want to see is silent when it passes — and the silence reads as "my probe never ran" or
"the state is fine." Both wrong; you have learned nothing.

- To read probe output, **run the test binary directly** with its filter, not through the ctest
  wrapper. Or pass `--output-on-failure` / `-V`.
- **Better: make the probe assert rather than print.** A wrong value then fails and ctest prints it
  for free — and the probe is already the shape the regression test needs, so nothing is thrown away.
- **A probe can pass for the wrong reason.** Before trusting a green probe, confirm it actually
  reached the state you meant to exercise.

## The stale-build checklist

Run this before debugging any surprising result:

1. Did the build actually succeed? Check the exit code, unpiped.
2. Is there exactly one artifact? Search for it.
3. Is the binary newer than the source you changed? Compare timestamps.
4. Did the file you edited get compiled? Check `compile_commands.json` and the build log.
5. Are you running the binary you just built, by full path?
6. Does a clean-room build in a scratch directory behave the same?

Only after all six does the code become the leading suspect.

## Sources

- [Ninja manual](https://ninja-build.org/manual.html) — the build log and dependency database
- [CMake `--build`](https://cmake.org/cmake/help/latest/manual/cmake.1.html) · [`file(GLOB CONFIGURE_DEPENDS)`](https://cmake.org/cmake/help/latest/command/file.html#glob) — why a glob re-check edge exists
- [ctest](https://cmake.org/cmake/help/latest/manual/ctest.1.html) — output capture and `--output-on-failure`
- [cppreference: One Definition Rule](https://en.cppreference.com/w/cpp/language/definition) — why mismatched TUs are UB rather than a link error
- [Apple: Launch Services](https://developer.apple.com/documentation/coreservices/launch_services) — bundle-identifier registration, the mechanism behind the wrong-binary trap
- The concrete failures on this page were recorded during CMake/Ninja game development on macOS. The
  mechanisms are general to any Ninja + CMake project, and the bundle trap to any macOS application
  build. Engine-specific traps from the same projects are in `axmol-patterns`.
