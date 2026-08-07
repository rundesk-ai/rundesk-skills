# Setup and build

Read this when setting up the engine, changing the build, or diagnosing a configure failure.

## The pinned engine

Treat the engine as a **pinned submodule you never edit**.

```sh
git submodule update --init
( cd axmol && ./setup.ps1 )      # requires PowerShell (pwsh)
```

`setup.ps1` restores the engine's gitignored tools directory, which contains **`axslcc`** — the shader
compiler. Without it, configure fails with *"axslcc not found"*. Re-run it after switching branches or
bumping the engine; a tools/branch mismatch is the documented cause of most shader-compiler errors.

On Windows, a ZIP-extracted copy trips PowerShell's execution policy. `git clone` instead — files
created locally are not blocked — or set `ExecutionPolicy RemoteSigned` for the cloned repository.

**Never edit anything under the engine directory.** Every engine-specific fix belongs in your own
top-level `CMakeLists.txt`. That single rule is what keeps an engine bump to a tag checkout and a
submodule pointer, with nothing to reconcile and no patch queue.

## Generators: use Ninja

Use the **Ninja generator**, and plain `cmake` invocations.

- The **Xcode generator** has failed to detect the compiler on recent Xcode versions.
- The **`axmol build` console wrapper** hardcodes generator and target assumptions that will not match
  a custom project layout.
- Ninja is faster and behaves the same in CI as locally, which the IDE generators do not.

```sh
cmake -B build/dev -G Ninja -DCMAKE_BUILD_TYPE=Debug
cmake --build build/dev --target MyGame
```

## The Xcode-only settings a Ninja build must reproduce

**This is the part that costs a day if nobody tells you.** Axmol applies several build settings only
under the Xcode generator. Under Ninja they are simply absent, so the app fails to compile — or
configures, links, and then crashes on launch. Four fixes belong in your own `CMakeLists.txt`:

1. **Point `AXSLCC_EXE` at the vendored binary** in the engine's tools directory. A raw `cmake`
   invocation otherwise cannot find the shader compiler even though `setup.ps1` fetched it.
2. **`-fobjc-weak` on the engine core target.** The engine sets `CLANG_ENABLE_OBJC_WEAK` only via
   Xcode; without it the AVFoundation media code's `__weak` references fail to compile.
3. **Embed and ad-hoc codesign `soft_oal.framework`** into `.app/Contents/Frameworks` in a
   `POST_BUILD` step. The engine does this only via Xcode; without it, launch crashes on
   `@rpath/soft_oal.framework`. **Stamp `CFBundleIdentifier` in the same step** — under Ninja the
   plist otherwise keeps the literal `$(PRODUCT_BUNDLE_IDENTIFIER)`.
4. **`-Wno-deprecated-declarations` on your game target only.** The engine calls its own deprecated
   context-attribute initializer from a header you include. Scoping it to the game target keeps full
   warnings on your other libraries and leaves the engine's own flags untouched.

Keep all four in your own file, commented with why. They read like cruft to the next person, and
removing any of them reproduces a confusing failure.

## Extensions are modular — turn off what you do not use

Every extension is built by default. Most projects use two or three.

| Extension | Default | Note |
|---|---|---|
| FairyGUI, ImGUI | on | UI |
| Spine | on | animation |
| Live2D, Effekseer | off | animation, particles |
| Physics Nodes, Particle 3D | on | |
| Asset Manager, Inspector, Lua, Cocostudio | on | |
| DragonBones, GUI | on | **deprecated — no longer recommended** |

From 2.1.3 you can disable the lot and re-enable individually; on earlier versions set them one at a
time:

```cmake
set(AX_ENABLE_EXT_SPINE OFF CACHE BOOL "" FORCE)
```

Two reasons this matters beyond tidiness: **build time**, and the fact that a deprecated extension you
never call is still a static library being archived on every clean build — which is exactly the kind
of artifact that shows up in a truncated-archive link error when a build directory gets raced.

## Build times

The first build compiles the whole engine and takes minutes. Every rebuild after should be a fast
relink of your own code.

**If a rebuild is recompiling the engine, something is wrong** — almost always a corrupted build
directory from two concurrent builds, or a reconfigure loop from inconsistent stamps. Do not
investigate it as a dependency-scanning problem. See `cpp-patterns` → `build-loop-traps.md`, which
documents the mechanism and the reset.

**`ccache` is the community's answer to a slow loop**, and it is worth knowing that the maintainers
deliberately did not bundle it. In a discussion about iOS builds taking 7–15 minutes with a full
rebuild on a one-line change, a contributor reported ccache bringing that to **52 seconds to ~1
minute 20**. Maintainers declined to add it to the template — it is not Axmol-specific and would be
maintenance burden — and agreed to document it as a workaround instead. So wire it up yourself:

```cmake
find_program(CCACHE_PROGRAM ccache)
if(CCACHE_PROGRAM)
  set(CMAKE_CXX_COMPILER_LAUNCHER "${CCACHE_PROGRAM}")
  set(CMAKE_C_COMPILER_LAUNCHER   "${CCACHE_PROGRAM}")
endif()
```

Note the maintainer's diagnosis in that thread: the full-rebuild behaviour was **specific to Xcode
builds** and "does not happen when creating Windows or Android builds" — one more reason the Ninja
generator is the recommendation here.

Keep a **headless configuration that builds no engine at all** for the fast test loop. It turns a
minutes-long cycle into a seconds-long one, and it produces no application bundle — which avoids the
duplicate-bundle trap entirely. See [`architecture.md`](architecture.md).

## Adding a source file

A template project that globs its sources does not see a new file until CMake re-runs. The engine's
console wrapper regenerates with `-f`; with plain CMake, re-configure. A project that lists its
sources explicitly does not have this problem, which is one argument for listing them.

## Configure failures, by message

| Message | Cause |
|---|---|
| `axslcc not found` | `setup.ps1` has not run, or ran on a different branch |
| Shader compile errors after a branch switch or bump | Tools/branch mismatch — re-run `setup.ps1` |
| `@rpath/soft_oal.framework` not loaded at launch | The framework embed step is missing (fix 3) |
| `__weak` compile failure in media code | `-fobjc-weak` missing (fix 2) |
| Bundle id is the literal `$(PRODUCT_BUNDLE_IDENTIFIER)` | The plist stamp is missing (fix 3) |
| Compiler not detected | The Xcode generator — switch to Ninja |
| `file is empty in lib/libFoo.a` | Two builds raced the same directory; see `cpp-patterns` |
| Rebuild recompiles the engine every time | Corrupted build directory or a reconfigure loop |

## Sources

- [Axmol](https://github.com/axmolengine/axmol) — platforms, backends, C++20
- [Axmol FAQ](https://github.com/axmolengine/axmol/wiki/FAQ) — `setup.ps1`, axslcc troubleshooting, PowerShell execution policy, glob regeneration with `-f`
- [Extensions](https://github.com/axmolengine/axmol/wiki/Extensions) — the table above, default states, the 2.1.3 opt-in change, and the deprecated extensions
- [DevSetup](https://github.com/axmolengine/axmol/blob/dev/docs/DevSetup.md)
- The four Ninja/macOS fixes were recorded across two independent Axmol v2.11.x projects; they are not
  in the engine documentation.
