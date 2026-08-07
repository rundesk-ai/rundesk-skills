# Patterns, backgrounds, and delivery

## Prove the repeat, not the tile

Define the tile geometry, spacing, overlap, palette, density, and target scales. Use a documented
pattern or tile control when available; the exported tile still requires inspection.

```text
Good: Sparse two-color fern repeat on a square tile. Motifs cross each edge continuously. Preview
multiple copies and inspect every edge and corner before scaling the pattern as a whole.

Bad: Beautiful seamless fern wallpaper; approve one tile, then crop or upscale it.
```

Render several copies in both directions. Check seams, corners, accidental clusters, directional
lines, moiré, and repetition that becomes obvious only at scale. Keep the approved source tile;
cropping or resampling it after validation can break the seam.

## Design backgrounds for their content

A background is not finished in an empty artboard. Specify target aspect ratios, focal placement,
quiet zones, contrast ceiling, safe crops, and whether the image is meaningful or decorative. Test
realistic text and controls over the least favorable area.

For responsive use, decide whether the composition may crop, needs alternate art direction, or must
preserve a subject. Do not shrink a wide composition and assume it remains useful on a narrow canvas.
The consuming layout and its accessibility remain `frontend-design` concerns.

Use one neutral, themeable texture source when color is not part of the material and the destination
can apply approved tokens. Produce separately art-directed light and dark assets when lighting,
depth, contrast, or color interaction changes the image itself; verify both against the same visual
grammar.

## Verify transparency and formats

Transparency is an alpha-channel requirement, not a checkerboard motif. Use a model or tool's
documented background control and an alpha-capable format. Inspect edge halos over light, dark, and
brand-colored surfaces.

Choose delivery formats from the content and destination:

- vector for precise geometry that must scale or theme;
- lossless raster where exact edges, limited-color art, or transparency needs it;
- efficient photographic formats and responsive variants for continuous-tone imagery;
- the destination's required print, native, motion, or archival format when web defaults do not fit.

Do not put ordinary readable copy into a background image. Keep text selectable and adaptable unless
the visual treatment is essential to a logo or the artifact itself.

## Package the handoff

Deliver the editable master separately from optimized exports. Include naming, dimensions, aspect
ratios, color profile or palette, theme/background variants, usage constraints, accessibility intent,
and a rights record. Open every exported file and inspect it in the real renderer before reporting
completion.
