# Graphics

Read this for Axmol 2 shaders, sprite batching, texture sampling, atlases, and SDF text. Axmol 3
uses a different pipeline; follow its current shader guide instead of adapting these rules.

## Shader compiles on one backend and fails on another

**Cause:** Axmol 2's axslcc accepts ESSL 310 or GLSL 450 and produces backend variants, but its SPIR-V
and Metal paths impose two non-obvious constraints.

**Replace:** put samplers outside blocks and every other uniform in exactly one uniform block per
stage. Put `#version` before every directive or code token; GLSL permits only whitespace and comments
before it. Share repeated shader functions with axslcc `#include` support.

```glsl
#version 310 es
layout(std140) uniform FragData { vec4 tint; }; // one non-sampler block
uniform sampler2D u_texture;                    // sampler stays outside
```

**Prove:** delete generated shader output, rebuild it with the pinned axslcc, then run the affected
Metal and GL targets. After an engine branch switch, re-run `setup.ps1` before changing shader code;
the FAQ identifies a branch/tool mismatch as the usual cause of sudden axslcc failures.

## A visual effect multiplies draw calls

**Cause:** Axmol 2 does not automatically batch sprites using custom shaders because it cannot know
whether separate `ProgramState` instances have identical uniform data.

**Replace:** finalize uniform values, then call `updateBatchId()` on states that are identical. Do not
call it before later uniform changes or assume differently valued instances can batch.

```cpp
programState->setUniform(location, data, size);
programState->updateBatchId();
```

**Prove:** capture draw-call counts before and after on the representative scene. Keep the change only
if measurement confirms the expected grouping; render order and program changes can still split a
batch.

## An atlas returns the wrong frame

**Cause:** `SpriteFrameCache` uses one namespace across loaded atlases, so repeated names collide.

**Replace:** prefix names or preserve subdirectories at pack time. Configure the packer not to strip
those directories.

```text
Good: inventory/ui/icon.png  and  battle/ui/icon.png
Bad:  icon.png in both atlases
```

**Prove:** load all atlases that coexist, resolve every expected frame name, and assert it maps to the
intended texture. Do this before a second atlas makes renaming expensive.

## Scaled UI icons look blocky

**Cause:** `setAliasTexParameters()` selects nearest-neighbor sampling. That preserves intentional
pixel-art edges, but scales the partial-alpha edge pixels in an antialiased raster as visible blocks.

**Replace:** choose by asset, not by scene. Use linear sampling for antialiased or vector-derived UI
sprites that scale; keep nearest sampling for pixel art whose texel grid must remain visible.

```cpp
uiTexture->setAntiAliasTexParameters(); // antialiased icon
tileTexture->setAliasTexParameters();   // pixel art
```

**Prove:** inspect the live target at every supported content scale. The source PNG cannot show the
runtime sampler, scale, blend mode, or content scale.

## SDF outlines look wrong at every size

**Cause:** the Axmol 2 SDF spread is defined in `FontFreeType.cpp`, while the shader uses a separate
scale. Changing only one makes the CPU-generated field and shader interpretation disagree.

**Replace:** keep spread and shader scale synchronized. Start within the documented `outlineSize`
ranges—0.5–2.0 for ordinary UI, 2.0–3.0 for tuned large text—and treat thicker effects as an engine
change with a larger texture/performance budget.

**Prove:** inspect small and large glyphs in the live target at each supported content scale. An
offline bitmap cannot prove the runtime filter, blend mode, content scale, or batching behavior.

See [the source basis](sources.md#graphics) for the Axmol wiki pages and v2.11.4 code used here.
