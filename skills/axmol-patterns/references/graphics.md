# Graphics

Read this for shaders, sprite sheets, batching, and text rendering.

## Shaders and axslcc

Axmol 2.x compiles shaders at **build time** through `axslcc` (a fork of `glslcc`), producing
Desktop GL, GLES3, GLES2 and Metal variants from one source.

**Authoring rules:**

- Write in **ESSL v310 or GLSL v450**. Extensions: `.vert`/`.vsh` for vertex, `.frag`/`.fsh` for
  fragment.
- **`#version` must be the first line.** Not the first *code* line — the first line. A leading comment
  breaks compilation, and the error does not say so.
- Custom shaders live in `{project_root}/Source/shaders/`, compile into
  `${CMAKE_BINARY_DIR}/runtime/axslc/custom`, and are referenced with a `custom/` prefix. The names
  change: `MyEffect.vsh` → `MyEffect_vs`, `MyEffect.fsh` → `MyEffect_fs`.

```cpp
auto* program = ProgramManager::getInstance()
    ->loadProgram("custom/MyEffect_vs", "custom/MyEffect_fs");
```

Built-in shaders skip the prefix and have constants in `Shaders.h`.

**The two uniform constraints, quoted, because they are not obvious and the errors are opaque:**

> **"All non-sampler uniforms must in uniform block, because glslcc(spirv) limits."**

> **"Only write 1 uniform block per shader stage"** — the Metal backend does not support more.

So: samplers stand alone, everything else goes in a single block per stage. A shader that compiles on
GL and fails on Metal is usually this.

**Share shader code with `#include`** — axslcc supports it. Logic duplicated across `.frag` files
**will** drift: the copies diverge and only one of them gets the fix. Put the common function in one
file and include it.

**Guard colour transforms by texel coverage under premultiplied alpha**, or transparent texels pick up
colour and the sprite grows a halo at its edges.

If shader compilation breaks after a branch switch or an engine bump, it is a tools mismatch — re-run
`setup.ps1` before debugging the shader.

## Batching and draw calls

**A custom shader disables automatic sprite batching by default.** This is the performance trap of the
graphics layer: a small visual effect applied across many sprites quietly turns one draw call into
hundreds.

The engine gives you the way back:

```cpp
programState->updateBatchId();   // on instances that share identical uniform data
```

Call it on instances whose uniforms match, and they batch again. Instances with genuinely different
uniforms cannot batch — which is an argument for pushing per-instance variation into vertex
attributes or a texture rather than uniforms, when it is on the hot path.

Otherwise the usual rules apply: draw calls come down by sharing a texture (an atlas), sharing a
program, and avoiding state changes between nodes. Measure before restructuring.

## Sprite sheets

- **PLIST v3** is the default format. Custom formats are possible via the `SpriteSheetLoader`
  interface, registered with `SpriteFrameCache::registerSpriteSheetLoader()`.
- Tools the engine points at: **spright**, **SpriteSheet Packer** (polygon packing), **Free Texture
  Packer**, **Free Sprite Sheet Packer**, and **TexturePacker** commercially.
- **Frame names must be unique across every loaded atlas.** `SpriteFrameCache` is one global
  namespace, so two atlases each containing `icon.png` collide and one silently wins.

The documented fix is to make names unique at pack time — either prefix them (`scene1_image1.png`) or
use subdirectories (`scene1/image1.png`), **ensuring the packer does not strip the subfolder**. Decide
this convention before the second atlas exists; retrofitting it means renaming every reference.

Unload atlases you are done with (`removeSpriteFramesFromFile`) rather than letting the cache grow for
the session.

## Texture filtering

**Nearest-neighbour filtering muddies detailed icons.** Choose the filter per texture class rather
than globally:

- **Nearest** for pixel art, and for anything drawn at exact integer scale.
- **Linear** for icons, photographic content, and anything scaled or rotated.

A single global default is why crisp pixel art and blurry UI icons show up in the same build.

## Text and SDF

Signed-distance-field text renders crisply at any scale and supports outlines. It is the right choice
for UI text that scales, and for high-DPI displays.

The documented outline ranges:

| Outline | Use |
|---|---|
| 0.5 – 2.0 | UI text: buttons, labels, high-DPI. **Safe** |
| 2.0 – 3.0 | Headings and large fonts, with tuning |
| 3.0 – 6.0 | Special effects, needs engine modification |
| > 6.0 | Not recommended |

The mechanism is split across two places: `FontFreeType.cpp` defines a spread (default 6.0) and the
shader applies a scale factor (1.5). **Changing the default means changing both, in sync** — a CPU-side
value that disagrees with the shader produces outlines that look wrong at every size and nobody can
find why.

Tradeoffs: a thicker outline needs more SDF texture resolution; a large outline on a small font
reduces legibility; and dense text increases fragment-shader load.

## Verifying visual work

**Verify against the live window, never an offline composite.** A composite proves the generator
produced the image; it does not prove the engine draws it that way, at that scale, with that filter,
under that blend mode. Several classes of bug — premultiplied-alpha halos, filtering choice, content
scale factor, batching-related z-order changes — are invisible in a composite and obvious in the
window.

For a seam or tiling problem, do not sample scenes and eyeball them. **Enumerate the pair matrix and
check it mechanically** — scene-sampled verification of a combinatorial surface never converges,
because the pair you have not looked at is always the broken one.

## Sources

- [Shaders in Axmol 2.x](https://github.com/axmolengine/axmol/wiki/Shaders-in-Axmol-2.x) — axslcc, ESSL/GLSL versions, file naming, the `custom/` prefix, both uniform constraints quoted, and `updateBatchId()`
- [Shaders in Axmol 3](https://github.com/axmolengine/axmol/wiki/Shaders-in-Axmol3) — for the v3 pipeline
- [Sprite sheets: tools and formats](https://github.com/axmolengine/axmol/wiki/Sprite-Sheets-Tools-and-Formats) — PLIST v3, `SpriteSheetLoader`, the tool list, and the unique-name requirement
- [SDF text rendering](https://github.com/axmolengine/axmol/wiki/SDF-text-rendering) — the outline ranges and the CPU/shader coupling
- [Particle system](https://github.com/axmolengine/axmol/wiki/Particle-System) · [Tiled](https://github.com/axmolengine/axmol/wiki/Tiled) · [Protecting image assets](https://github.com/axmolengine/axmol/wiki/Protecting-image-assets)
- [The Book of Shaders](https://thebookofshaders.com/) — the engine's own recommended fragment-shader primer
- The `#version`-first-line rule, `#include` sharing, premultiplied-alpha guarding, filtering-per-class
  and the pair-matrix verification point were recorded during Axmol v2.11.x development.
