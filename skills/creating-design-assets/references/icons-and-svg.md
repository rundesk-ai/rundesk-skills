# Icon families and SVG

## Define the family before its members

Inventory the existing system and destination sizes. Reuse its grid and rules. If none exists,
declare a master grid and target sizes for this project; do not import universal numbers from a
different design system.

Specify:

- familiar metaphor and visible-label requirements;
- fill or outline treatment, stroke weight, caps, and joins;
- corner language, perspective, detail ceiling, and modifier position;
- live area, padding, optical weight, and palette or theme roles.

Approve one anchor, then create and review one icon at a time against it.

```text
Good: Use the approved calendar icon only as the style anchor. Create one notification-bell icon.
Preserve its canvas, safe area, monochrome outline, stroke, round caps and joins, corner language,
optical weight, and detail level. Change only the metaphor.

Bad: Make 20 matching cute icons for my app.
```

Review the set as a contact sheet at actual sizes. Correct mechanical centering when visual weight
makes a glyph appear displaced. Preserve meaningful asymmetry. Create a simplified or separately
adjusted size when one master becomes muddy; vector scaling cannot restore lost perception.

## Keep meaning ahead of novelty

Use a recognized metaphor when one exists. Pair unfamiliar or consequential actions with visible
labels, and test recognition without telling participants the intended answer. A cohesive but
unrecognizable set has failed.

Avoid letters in small icons unless the convention is established and localizable. A brand wordmark
is a different artifact and may legitimately contain controlled typography.

## Construct and inspect SVG deliberately

- Set a root `viewBox` and preserve the intended aspect behavior.
- Prefer clear primitives and paths; remove accidental points, stray objects, embedded rasters, and
  editor debris without destroying needed IDs, layers, titles, strokes, or animation hooks.
- Normalize fills and strokes only as the destination requires. Some systems require expanded,
  combined paths; others need live strokes, CSS theming, or layers.
- Preserve an editable master before optimization. Render the optimized copy and compare it with the
  master at every target size.
- Check IDs when multiple SVGs are inlined; optimization can create collisions.

Do not accept “SVG” as proof of a vector asset. A bitmap wrapped in SVG remains a bitmap, and a noisy
auto-trace remains difficult to edit and theme.

## Handle accessibility and trust at the consumer boundary

Decorative assets receive an empty alternative or are hidden from assistive technology. Meaningful
images need an equivalent name or description. A button or link owns the accessible name for its
functional icon; do not make the nested SVG a second control.

Treat uploaded or third-party SVG as active content. Validate file type and size, sanitize or reject
unsupported constructs, and prefer an inert image context when scripting or interaction is not
needed. The consuming stack's security guidance owns the exact sanitizer and content policy.
