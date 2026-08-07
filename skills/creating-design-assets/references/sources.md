# Creating design assets source basis

This package is an original Rundesk synthesis. Provider documentation establishes current model and
tool behavior; standards, maintained design systems, studies, and public practitioner guidance
establish the production traps and replacements. Provider-specific controls are evidence, not
portable syntax.

## Prompt structure and controlled iteration

- [OpenAI Cookbook — Image generation prompting guide](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide): field-tested prompt structure, explicit composition, logo framing, invariants, single-change iteration, exact-text handling, and the distinction between concept generation and production refinement.
- [OpenAI API — Image generation](https://developers.openai.com/api/docs/guides/image-generation): multi-image roles, background controls, and current limitations around composition, placement, text, and transparency. Model capabilities must be checked at execution time.
- [Google Cloud — Imagen prompt guide](https://cloud.google.com/vertex-ai/generative-ai/docs/image/img-gen-prompt-guide): subject, context, style, incremental refinement, and examples showing that concrete visual attributes change output.
- [Black Forest Labs — FLUX prompting guide](https://docs.bfl.ai/guides/prompting_guide_flux2): structured subject, action, context, and style instructions plus explicit roles for multiple references.
- [Adobe Firefly — Match composition to a reference](https://helpx.adobe.com/firefly/web/work-with-images/generate-images/match-image-composition-to-reference-image.html) and [use style references](https://helpx.adobe.com/firefly/web/work-with-images/generate-images/reference-images-for-styling.html): composition and style are separate reference roles; a reused style reference helps continuity but does not prove exact fidelity.
- [Midjourney — Style Reference](https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference): content prompts should name the content rather than instruct the model to copy a reference; conflicting style words weaken the reference's role.

The good/bad prompt structures in this package minimize these published examples. The catalog's
portable conclusion is to brief observable decisions rather than preserve any provider's syntax.

## Prompt and model traps

- [Midjourney — Seeds](https://docs.midjourney.com/hc/en-us/articles/32604356340877-Seeds) says seeds have little final influence, are not reliable across sessions or changed settings, and are weaker consistency tools than references.
- [Google Cloud — Deterministic images](https://cloud.google.com/vertex-ai/generative-ai/docs/image/generate-deterministic-images) scopes repeatability to documented same-input conditions. Together with Midjourney's warning, this supports using a seed for controlled comparison—not as a brand style.
- [Black Forest Labs — Negative prompting](https://docs.bfl.ai/guides/prompting_guide_t2i_negative) documents models without negative prompts and recommends positive desired states. [Imagen negative prompts](https://cloud.google.com/vertex-ai/generative-ai/docs/image/omit-content-using-a-negative-prompt) limits the feature to named models. No negative syntax is universal.
- [T2I-CompBench](https://arxiv.org/abs/2307.06350) evaluates 6,000 compositional prompts and documents attribute binding, spatial, and complex-composition failures. [TIFA](https://arxiv.org/abs/2303.11897) uses 4,000 prompts and 25,000 questions to expose counting, spatial, and multi-object failures. These results motivate question-based verification; they do not rank every current model.
- [Character-Aware Models Improve Visual Text Rendering](https://arxiv.org/abs/2212.10562) experimentally connects text-rendering failures with missing character-level information. Current models improve text but still require exact-copy inspection and deterministic production typography.
- [HEIM](https://arxiv.org/abs/2311.04287) evaluates 26 text-to-image models over 62 scenarios and finds no model best across every dimension. This supports checking the brief instead of selecting by one aesthetic score.

Generic magic-token lists, mandatory prompt length or JSON, named-artist imitation, exact prompted
HEX claims, and universal transparency promises were rejected because the sources do not establish
them across providers.

## Logos, recognition, and brand systems

- [OpenAI's logo workflow](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide) supplies the strong-silhouette, balanced-negative-space, isolated-mark, small/large, and controlled-iteration basis used by the logo example.
- [Apple — App icons](https://developer.apple.com/design/human-interface-guidelines/app-icons) supports simplifying small marks and avoiding inaccessible, hard-to-localize text. Its platform template and exact geometry are not universal logo rules.
- [Van Grinsven and Das, 2016](https://www.tandfonline.com/doi/abs/10.1080/13527266.2013.866593) reports two experiments where simple logos gained short-term recognition while complex logos benefited from exposure. [Tang et al., 2025](https://www.sciencedirect.com/science/article/pii/S0167811625000345) reports seven studies in which complexity can signal luxury or craftsmanship. Together they contradict “minimal is always better.”
- [IBM — 8-bar logo usage](https://www.ibm.com/design/language/ibm-logos/8-bar/) demonstrates a production identity system: clear space, positive/reversed versions, scale relationships, and background restrictions. IBM's ratios are evidence for testing and documenting local values, not values to copy.
- [Spectrum design tokens](https://spectrum.adobe.com/page/design-tokens/) and [Spectrum color](https://spectrum.adobe.com/page/using-color/) support role-based, theme-aware color decisions rather than an unexplained palette. [Carbon color usage](https://carbondesignsystem.com/elements/color/usage/) recommends tokenizing SVG illustrations or swapping assets between themes, with one transparent asset as a fallback. The package's neutral-themeable-texture versus separate-art-direction decision is a qualified synthesis of those options.
- [USPTO — Likelihood of confusion](https://www.uspto.gov/trademarks/search/likelihood-confusion) and [comprehensive clearance](https://www.uspto.gov/trademarks/search/comprehensive-clearance-search-similar-trademarks) establish that similarity may be visual, phonetic, semantic, or commercial and that a clearance search extends beyond identical registered marks.
- [Creative Commons license types](https://creativecommons.org/share-your-work/cclicenses/) distinguishes attribution, commercial-use, derivative, and ShareAlike permissions. [U.S. Copyright Office AI report summary](https://www.copyright.gov/newsnet/2025/1060.html) says prompts alone do not provide sufficient human control for authorship while human selection, arrangement, or modification may be protectable. Rights conclusions remain jurisdiction-specific.

## Icon grammar, optical balance, and meaning

- [Apple — Icons](https://developer.apple.com/design/human-interface-guidelines/icons) calls for familiar simplified metaphors and consistent size, detail, weight, and perspective; it explicitly permits dimensional adjustments for optical weight.
- [Material iconography](https://m1.material.io/style/icons.html) uses shared grids, keylines, live areas, and optical correction. The system demonstrates a method; its measurements are not universal.
- [IBM UI icon usage](https://www.ibm.com/design/language/iconography/ui-icons/usage/) states that mechanical centering can fail and directs optical alignment around visual weight.
- [Spectrum iconography](https://spectrum.adobe.com/page/iconography/) shows why arbitrary scaling or fill changes break weight, proportions, radius, and hierarchy; it maintains separately optimized sizes.
- [Fluent iconography](https://fluent2.microsoft.design/iconography) simplifies product icons below 48 px. [Material Symbols](https://developers.google.com/fonts/docs/material_symbols) varies stroke through optical sizing. These establish that SVG scaling alone does not guarantee small-size quality.
- Noun Project's practitioner reviews on [technical icon quality](https://blog.thenounproject.com/technical-guidelines-for-creating-icons/) and [coherent icon sets](https://blog.thenounproject.com/what-makes-a-great-icon-set/) catalog stray artifacts, inconsistent paths, strokes, negative space, corners, scale, and padding. They support the anchor-and-contact-sheet checks.
- [Collaud et al., 2022](https://backend.epfl-ecal-lab.ch/wp-content/uploads/2022/08/EPFLECALLab_2022-08-18_Collaud-et-al.pdf) tests 64 novel icons with 276 participants. Concreteness materially improved function understanding, while some structural deformation impaired precise movement interpretation. This supports recognizable metaphors and intentional asymmetry; it does not impose one grid.
- [USWDS — Icon](https://designsystem.digital.gov/components/icon/) requires consistent meanings and recommends labels where meaning is unclear.
- [IBM pictogram usage](https://www.ibm.com/design/language/iconography/pictograms/usage/), [Fluent iconography](https://fluent2.microsoft.design/iconography), and [Apple SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols) distinguish system icons from brand marks and impose trademark or logo-use restrictions.

The good family-extension example is a compact application of the shared-grid, family-grammar,
anchor-reference, and controlled-iteration sources above.

## SVG construction, optimization, accessibility, and trust

- [SVG 2 — Coordinate systems](https://www.w3.org/TR/SVG/coords.html) defines `viewBox` and `preserveAspectRatio`; removing the root view box can break responsive scaling.
- [SVGO v4 releases](https://github.com/svg/svgo/releases) record disabling `removeViewBox` and `removeTitle` by default after scalability and accessibility failures. [SVGO `cleanupIds`](https://svgo.dev/docs/plugins/cleanupIds/) warns that separately optimized inline SVGs can collide on minimized IDs.
- [Carbon icon contribution](https://v10.carbondesignsystem.com/contributing/contribute-icons/) requires expanded strokes and combined shapes, while [Apple custom symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols) preserves layers and annotations for rendering and animation. Their conflict is the evidence for following the destination contract instead of mandating one path policy.
- [W3C image alternatives](https://www.w3.org/WAI/tutorials/images/) distinguishes informative, functional, and decorative images. [WCAG non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast) applies 3:1 to meaningful graphical objects and UI indicators, while excluding decoration and essential logos.
- [MDN — SVG as an image](https://developer.mozilla.org/en-US/docs/Web/SVG/Guides/SVG_as_an_image) documents the inert restrictions of image contexts. [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html) establishes allowlisting, type/size validation, storage isolation, and active-content risk. Exact sanitization belongs to the consuming stack.

## Patterns, backgrounds, and delivery

- [SVG 2 — Patterns](https://www.w3.org/TR/SVG2/pservers.html) defines fixed-interval tiling and pattern coordinate systems.
- [Adobe Illustrator — Edit patterns](https://helpx.adobe.com/illustrator/desktop/paint-and-fill/create-and-edit-patterns/edit-patterns.html) exposes tile type, size, spacing, overlap, edge, repeat bounds, and multiple-copy previews. [Midjourney — Tile](https://docs.midjourney.com/hc/en-us/articles/32197978340109-Tile) warns that the result is one tile and that upscaling can break seamlessness. The multi-copy preview is the portable proof; tool controls are not.
- [WCAG background-image failure F83](https://www.w3.org/WAI/WCAG22/Techniques/failures/F83.html) requires checking foreground text against the least-contrasting region behind it.
- [web.dev — Choose the right image format](https://web.dev/articles/choose-the-right-image-format) distinguishes scalable geometric assets from continuous-tone raster imagery, recommends responsive raster delivery, and warns that ordinary text in images is not selectable, searchable, or zoomable.

The package's multi-copy check, alpha inspection over several surfaces, contact sheet, and export
reopening are local proof methods derived from these contracts, not claims that a standard mandates
those exact fixtures.
