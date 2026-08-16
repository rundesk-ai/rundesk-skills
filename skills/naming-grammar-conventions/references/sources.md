# Sources

Verified 16 August 2026. This package is an original Rundesk synthesis of the public guidance below;
rules are narrowed to the audience and ecosystem each source supports.

## Terminology and interface writing

- [Microsoft, Style and tone](https://learn.microsoft.com/en-us/windows/win32/uxguide/text-style-tone)
  explains that consistent terminology reduces the need to decide whether different words mean the
  same action, and recommends parallel syntax for parallel interface elements. This supports one
  canonical product term without requiring identical spelling at every technical boundary.
- [Microsoft Style Guide, Top 10 tips](https://learn.microsoft.com/en-us/style-guide/top-10-tips-style-voice)
  uses sentence-style capitalization as Microsoft's default and omits terminal punctuation from
  headings and UI titles. This package treats those as useful English UI defaults, not universal law.
- [Apple Human Interface Guidelines, Writing](https://developer.apple.com/design/human-interface-guidelines/writing)
  recommends verbs for buttons and links and consistent formatting for each interface element type.
  Its platform-specific examples are why this skill defers to the owning design system.
- [GOV.UK Design System, Error message](https://design-system.service.gov.uk/components/error-message/)
  requires specific, concise recovery text and reuse of field-label language in errors. It also
  separates examples and hints from the error slot.
- [Microsoft Research, language choices](https://www.microsoft.com/en-us/research/?p=689796)
  reports findings from surveys, moderated and unmoderated studies, and practitioner roundtables
  across Microsoft admin products; the authors conclude that consistent terminology and content
  patterns improve predictability and scanning. The evidence concerns those products, not every
  audience.

## Accessibility

- [W3C WAI, Labeling controls](https://www.w3.org/WAI/tutorials/forms/labels/) requires labels that
  describe control purpose and recommends programmatic association, preferably with native HTML.
- [W3C WAI, Providing accessible names and descriptions](https://www.w3.org/WAI/ARIA/apg/practices/names-and-descriptions/)
  explains that interactive elements need short, distinguishing accessible names and that visible,
  native text reduces maintenance and accessibility failures.
- [WCAG technique G211](https://www.w3.org/WAI/WCAG21/Techniques/general/G211) explains why the
  accessible name should match the visible label for speech input. WCAG 2.5.3 requires the visible
  text to be contained in the accessible name; it does not require exact equality.
- [W3C WAI, Form instructions](https://www.w3.org/WAI/tutorials/forms/instructions/) explains that
  placeholders disappear and must not replace labels or required instructions.
- [W3C WAI, User notifications](https://www.w3.org/WAI/tutorials/forms/notifications/) recommends
  concise errors that reference the field and explain correction, plus success feedback when needed.

## Code, data, and contracts

- [PEP 8](https://peps.python.org/pep-0008/) documents Python-specific naming forms and explicitly
  prioritizes internal consistency. It supports deferring casing and prefixes to the language and
  repository instead of presenting one naming convention as a cross-language rule.
- [Google AIP-140, Field names](https://google.aip.dev/140) requires the same name for the same
  concept and different names for different concepts within Google-style protobuf APIs. It also
  makes scalar fields singular, repeated fields plural, field names nouns, and measurable quantities
  carry unit suffixes. This package uses those as scoped examples for values and contracts, not as
  universal rules for every language or protocol.
- [Google AIP-180, Backwards compatibility](https://google.aip.dev/180) treats renaming a public API
  element as removal plus addition and therefore a breaking change in the same major version. This
  supports staged contract renames rather than synchronized copy edits.
- [Simon Holywell, SQL style guide](https://www.sqlstyle.guide/) is a practitioner convention for
  consistent, descriptive SQL identifiers and avoiding cryptic abbreviations. Its table plurality
  and casing choices are examples, not SQL requirements.
- [AlSuhaibani et al., method naming practices](https://arxiv.org/abs/2102.13555) surveys more than
  1,100 professional developers and reports broad agreement that method-naming standards matter and
  are applied. It supports treating naming as a reviewable engineering concern; it does not establish
  one universal naming form across languages or ecosystems.

## Catalog conclusions

The sources do not establish one universal vocabulary workflow. This package therefore labels and
scopes the following synthesis instead of attributing it to a source:

Any retained do/don't pair not mapped directly to a citation above is a catalog conclusion, not a
claim that a source mandates that exact wording. Its adjacent `Why`, failure-prevented column, or
failure prose is the scoped rationale and boundary for applying it; keep the contrast so an agent
can distinguish the rejected form from its replacement, but do not generalize it beyond that named
failure.

- Prefer a precise concept name over placeholders such as `data` or `item`; the stated failure is
  that a reader must reconstruct the value's meaning from assignments and callers.
- Name an operation for its observable outcome; the stated failure is that a generic verb such as
  `process` or `handle` makes the reader reconstruct the outcome from the implementation.
- Put regulated wording, published compatibility, and established ecosystem conventions ahead of a
  catalog default; those are authority constraints, while the default is only a preference.
- Preserve stored data, dashboards, alerts, and other consumers during non-API renames; AIP-180
  directly supports only published API compatibility, while these rows are conservative catalog
  workflow conclusions with the affected consumer named.
- Preserve immutable third-party names at an adapter boundary and document the canonical mapping;
  this is a catalog workflow conclusion, not a claim that AIP-180 governs vendor schemas.
- Prefer positive predicates only when they preserve the same fact. Negative domain facts,
  regulated wording, and fixed contracts are scoped exceptions; silently inverting them can change
  behavior rather than improve a name.
- Recommend an exact name, architecture, interaction, owner, or risk severity only when the supplied
  evidence establishes it. Otherwise state the assumption or decision needed. This is an execution
  guardrail against false precision, not a sourced universal naming rule.
