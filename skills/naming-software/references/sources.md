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
  headings and UI titles. This catalog treats those as useful English UI defaults, not universal law.
- [Apple Human Interface Guidelines, Writing](https://developer.apple.com/design/human-interface-guidelines/writing)
  recommends verbs for buttons and links and consistent formatting for each interface element type.
  Its platform-specific examples are why this skill defers to the owning design system.
- [GOV.UK Design System, Error message](https://design-system.service.gov.uk/components/error-message/)
  requires specific, concise recovery text and reuse of field-label language in errors. It also
  separates examples and hints from the error slot.
- [Microsoft Research, language choices](https://www.microsoft.com/en-us/research/?p=689796)
  reports surveys, moderated and unmoderated studies, and practitioner roundtables across Microsoft
  admin products; the authors conclude that consistent terminology and content patterns improve
  predictability and scanning. The evidence concerns those products, not every audience.

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
  repository instead of presenting one grammar as cross-language law.
- [Google AIP-140, Field names](https://google.aip.dev/140) requires the same name for the same
  concept and different names for different concepts within Google-style protobuf APIs. Its casing
  and cardinality rules are ecosystem-specific; this skill adopts only the semantic distinction.
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
