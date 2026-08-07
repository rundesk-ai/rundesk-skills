---
name: creating-design-assets
description: Use when creating, prompting, refining, or reviewing visual design assets such as logos, brand marks, icon families, SVGs, illustrations, backgrounds, textures, patterns, or custom shapes. It supplies a provider-neutral workflow for choosing the medium, defining a coherent visual grammar, prompting image models, constructing production assets, and verifying consistency, scale, accessibility, rights, and export quality. Do not use it for page layout or interaction design.
---

# Creating design assets

Treat a generated image as a candidate, not a deliverable. A production asset must express a known
purpose, belong to a coherent visual system, survive its real contexts, and be editable enough for
the team that owns it.

Use `frontend-design` for the page, flow, responsive placement, or interaction that consumes an
asset. This skill owns the asset brief, concept, construction, family consistency, export, and
asset-level proof.

## Ground the asset before making it

1. Inspect the product, existing brand, approved assets, tokens, nearby files, and target surfaces.
   Reuse established visual language; do not infer a new brand from one screenshot.
2. Write the asset contract: audience, purpose, meaning, contexts, target sizes and aspect ratios,
   required variants, format, editable source, background or alpha behavior, and acceptance checks.
3. Define one visual grammar: shape language, fill or stroke, corner treatment, perspective, detail
   ceiling, optical weight, palette roles, texture, lighting, padding, and theme behavior.
4. Separate requirements from preferences. Preserve requirements through every iteration; make
   preferences easy to change.

If meaning, required variants, target sizes or crops, the existing visual system, or the destination
contract is missing, do not invent it. Name the missing decision; continue only with a clearly
labeled, reversible art-direction proposal that does not depend on it.

```text
Good: 24 px navigation icon; familiar archive-box metaphor; rounded outline family; readable at
16 px; light and dark themes; SVG master; visible label remains in the interface.

Bad: Make an amazing premium archive icon, modern, beautiful, trending, ultra-detailed, 8K.
```

The good structure follows published prompting and icon-system guidance; see
[sources.md](references/sources.md).

## Choose the medium before the tool

- Use raster generation for concept exploration, illustration, texture, photographic material, and
  other organic imagery.
- Use deliberate vector geometry or the destination's icon tooling for logos, interface icons,
  custom shapes, exact typography, and assets that require stable paths, colors, or small-size
  behavior.
- Use a hybrid when generation helps explore a direction: select the concept, then reconstruct and
  normalize the production asset. Auto-tracing a bitmap does not prove clean geometry.
- Follow the destination contract. Do not universalize one artboard, stroke width, path-flattening
  rule, color profile, or export format across web, native, print, and motion work.

## Prompt for decisions, not magic

State the deliverable and use, subject, composition, visual grammar, constraints, and output framing.
Assign each reference one role. Generate one asset or one art-direction question at a time. After a
useful draft, change one axis and restate what must remain invariant.

Do not rely on adjective piles, named-artist imitation, seeds as saved styles, undocumented negative
syntax, or claims that a model will reproduce exact text, geometry, color, or transparency. Use
provider controls only after checking the selected model's current contract.

Read [prompting-and-iteration.md](references/prompting-and-iteration.md) before prompting an image
model, using references, extending a family, preserving a direction, or diagnosing drift.

## Build systems, not isolated samples

- Approve an anchor asset and its written grammar before extending a family. Review the family
  together; a locally attractive icon can still be globally inconsistent.
- Use grids, key shapes, and shared metrics as scaffolding, then correct for optical balance.
  Mathematical centering and perfect symmetry can look uneven or erase directional meaning.
- Keep concepts recognizable at their target size. Simplify or create size-specific masters when
  detail, spacing, or weight collapses; SVG preserves geometry, not legibility.
- Keep brand marks separate from interface metaphors and third-party icon libraries.
- Construct wordmarks and required copy with controlled typography. Never ship generated lettering
  merely because it looks correct at a glance.

Read [logos-and-brand-systems.md](references/logos-and-brand-systems.md) for identity exploration,
logo variants, wordmarks, themes, clearance, and brand handoff. Read
[icons-and-svg.md](references/icons-and-svg.md) for icon families, custom shapes, SVG construction,
accessibility, optimization, and untrusted SVG.

## Validate the actual deliverable

Inspect the master and every required export, not only a presentation mockup:

1. Compare the result with the brief: meaning, objects, counts, placement, exact copy, palette,
   silhouette, and exclusions.
2. Test every target size, crop, background, theme, and one-color or reversed variant. Inspect alpha
   edges on light and dark surfaces.
3. Compare related assets in one contact sheet for stroke, corner, perspective, padding, detail, and
   optical weight drift.
4. Test meaningful graphics and functional icons for contrast, text alternatives, and recognition.
   Decoration gets an empty alternative; the consuming control owns the accessible name.
5. Render SVGs in the destination. Verify the `viewBox`, aspect behavior, geometry, theming, IDs,
   and absence of unwanted raster content or active external behavior.
6. Preview a repeating tile across multiple copies and backgrounds. Test backgrounds behind real
   content at required crops, not as empty artwork.
7. Record source, prompt or construction decisions, references and their rights, model and version
   when relevant, human edits, editable master, exports, and usage constraints.

Read [patterns-and-backgrounds.md](references/patterns-and-backgrounds.md) for repeat tiles,
responsive backgrounds, transparency, formats, and delivery checks.

Before consequential brand adoption, search similar names and designs in the relevant markets and
get accountable human or legal clearance. “Original” in a prompt is not evidence of ownership,
copyrightability, or trademark availability.
