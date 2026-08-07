# Prompting and iteration

## Write an asset brief, not a spell

Portable prompts describe decisions. Provider syntax, prompt length, negative controls, and
reference strength change between models.

Use this order when it helps the selected model:

```text
Deliverable and use: one 16:9 decorative hero background for a finance dashboard.
Content: layered paper-cut contours suggesting steady growth; no literal currency symbols.
Composition: quiet left 45% for a two-line heading; focal detail in the right third.
System: two brand neutrals and one restrained accent; broad shapes; matte paper texture.
Constraints: low contrast beneath text; safe center crop for 9:16; no words or watermark.
Output: one background without a presentation mockup.
```

Bad:

```text
Epic premium finance background, award-winning, cinematic, masterpiece, 8K, trending.
```

The first prompt makes composition, crop, content pressure, and proof inspectable. The second spends
tokens without defining the asset.

## Give references one job each

Number every input and say what it controls:

```text
Image 1 supplies only the bottle shape and label proportions.
Image 2 supplies only the flat-paper texture and muted palette.
Preserve Image 1's geometry; do not copy Image 2's objects or composition.
```

Bad: `Combine these references and make it match the brand.`

Use only references the project may use. A style or composition reference guides a model; it does
not guarantee exact preservation or grant rights to the source.

## Control iteration

1. Generate divergent concepts against the same brief.
2. Reject candidates that miss a requirement before judging polish.
3. Select one direction and one next question.
4. Change one axis; restate every invariant.
5. Compare at final size and context, not only in the generator.
6. Reconstruct exact geometry, copy, and color in deterministic tools.

```text
Good: Keep the silhouette, palette, stroke, padding, and frontal view unchanged. Change only the
corners from sharp to softly rounded.

Bad: Make it friendlier, more modern, more premium, rearrange it, add detail, simplify it, and try
new colors.
```

## Know the recurring model traps

| Symptom | Likely cause | Replacement |
|---|---|---|
| Objects, attributes, or spatial relations are wrong | compositional binding remains probabilistic | specify placement and count; use a structure reference or construct the layout afterward |
| Exact copy is misspelled or unstable | generated pixels are not controlled typography | use short quoted copy only for exploration; typeset production copy separately |
| A family drifts | repeated adjectives are not a system | reuse an approved anchor and restate its measurable invariants |
| A seed stops matching | seed and settings are mistaken for identity | use seeds only for controlled comparisons; record model/version and use references plus a style contract |
| `no X` produces X | negative behavior differs by model | describe the desired state positively; use a negative field only when current docs support it |
| “transparent” is an opaque checkerboard | appearance was requested instead of alpha output | use documented background controls and an alpha-capable format; inspect the alpha channel |

Turn the brief into pass/fail questions. Overall beauty never compensates for the wrong count,
metaphor, copy, crop, alpha, or family grammar.
