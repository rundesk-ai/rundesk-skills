# Sources

Accessed 7 August 2026. Standards establish minimum behavior; maintained design systems and
practitioner research show how teams apply those contracts and where users encounter failures.
External cursor conventions disagree. This catalog therefore records `cursor: pointer` for every
enabled activation target as its own universal UI standard, not as a WCAG or CSS requirement.

## Upstream adaptation

- [Anthropic `frontend-design` at commit `2235be7c`](https://github.com/anthropics/skills/tree/2235be7c60b551f5de82ade908fd3816455afcda/skills/frontend-design)
  supplies the Apache-2.0 base for subject-specific visual direction, deliberate composition, and a
  memorable signature element. This adaptation retains those ideas while adding the sourced UI/UX
  workflow, interaction rules, failure patterns, and verification criteria in this package.
  Attribution and the license are recorded in `THIRD_PARTY_NOTICES.md` and `LICENSE.txt`.

## Core UX workflow

- [Jakob Nielsen, “10 Usability Heuristics for User Interface Design”](https://www.nngroup.com/articles/ten-usability-heuristics/)
  was last reviewed in 2024 and traces the heuristics to a factor analysis of 249 usability problems.
  It supports visible system status, user control and undo, internal and external consistency, error
  prevention, recognition over recall, focused visual design, and actionable error recovery.
- [Carbon Design System: Button usage](https://carbondesignsystem.com/components/button/usage/)
  supports one clear action hierarchy, specific action labels, distinct interactive states, keyboard
  activation, and inline loading feedback. It provides the source pattern for the good/bad label and
  state examples.

## Semantics, keyboard, and focus

- [WAI-ARIA Authoring Practices: Button pattern](https://www.w3.org/WAI/ARIA/apg/patterns/button/)
  distinguishes commands from links, requires accessible naming, and defines `Enter`, `Space`, and
  post-action focus behavior. It supports the semantic control and dialog-focus examples.
- [WAI-ARIA Authoring Practices: Link pattern](https://www.w3.org/WAI/ARIA/apg/patterns/link/)
  recommends native links and warns that adding `role="link"` does not create navigation, context
  menu, or keyboard behavior.
- [WAI-ARIA Authoring Practices: Modal dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/)
  defines contained tab order, `Escape`, initial focus, and focus return. It supports the modal
  good/bad pair.
- [MDN: `<button>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/button)
  documents multi-modal activation, the form-submit default, explicit `type="button"`, accessible
  names for icon buttons, and target-size considerations.
- [WAI-ARIA Authoring Practices: Tooltip pattern](https://www.w3.org/WAI/ARIA/apg/patterns/tooltip/)
  defines a tooltip as non-interactive descriptive content shown on hover or keyboard focus and
  directs interactive popups to a non-modal dialog pattern.

## Affordance, cursors, states, and targets

- [MDN: `cursor`](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/cursor)
  maps cursors to operations and describes `pointer` as indicating a link. It supports treating a
  cursor as contextual feedback rather than semantics.
- [Adobe Spectrum: Button](https://spectrum.adobe.com/page/button/) and
  [States](https://spectrum.adobe.com/page/states/) deliberately use the default arrow for command
  buttons, reserve the hand for link buttons, and define default, hover, down, keyboard-focus, and
  disabled states.
- [SAP Fiori: Cursors](https://www.sap.com/design-system/fiori-design-web/v1-136/foundations/interaction/cursors)
  uses the pointer over clickable elements. Spectrum and MDN establish that external conventions
  differ; SAP demonstrates the activation-cursor convention this catalog adopts universally.
- [WCAG 2.2](https://www.w3.org/TR/WCAG22/) establishes keyboard operation, visible and unobscured
  focus, status messages, orientation independence, concurrent input, pointer-gesture and dragging
  alternatives, pointer cancellation, and a 24-by-24 CSS-pixel AA target-size minimum with
  exceptions. Its 44-by-44 enhanced target and
  [Spectrum platform scale](https://spectrum.adobe.com/page/platform-scale/), which targets 48-pixel
  touch areas where possible, support the larger practical default.
- [Carbon Design System: Tile usage](https://carbondesignsystem.com/components/tile/usage/)
  documents whole-tile activation, separate targets when a tile contains independent controls, and
  the ambiguity caused by multiple click targets. It supports the clickable-container pair.
- [W3C: Understanding Content on Hover or Focus](https://www.w3.org/WAI/WCAG22/Understanding/content-on-hover-or-focus.html)
  requires additional content to be dismissible, hoverable, and persistent, and explains why a
  pointer-triggered disclosure must also work through keyboard focus.

## Forms, feedback, and recovery

- [GOV.UK Design System: Button](https://design-system.service.gov.uk/components/button/) supports
  specific action labels, one primary action, avoiding disabled buttons without research, prompt
  feedback on slow operations, and protection against duplicate submission. Its documented Notify
  case found duplicate invitations caused by double-clicking, and it requires server-side protection
  in addition to a JavaScript double-click guard.
- [GOV.UK Design System: Recover from validation errors](https://design-system.service.gov.uk/patterns/validation/)
  supports accepting harmless format variation, preserving entered values, inline errors, a focused
  summary, and submit-time validation unless research establishes a need for earlier feedback.
- [WAI Forms Tutorial: Labeling controls](https://www.w3.org/WAI/tutorials/forms/labels/) and
  [WCAG: Labels or Instructions](https://www.w3.org/WAI/WCAG22/Understanding/labels-or-instructions.html)
  support persistent visible labels, programmatic association, and instructions for required input
  formats. They provide the source for the placeholder-only good/bad pair.
- [WCAG: Error Identification](https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html)
  requires errors to identify the affected item and describe the error in text. It supports the
  specific corrective-message example.
- [GOV.UK Design System: Error summary](https://design-system.service.gov.uk/components/error-summary/)
  requires consistent linked error messages and deliberate focus. It supports the long-form recovery
  pattern.
- [GOV.UK Design System: Confirmation pages](https://design-system.service.gov.uk/patterns/confirmation-pages/)
  supports naming the completed transaction, references, next steps, contact or recovery routes, and
  durable records for consequential work.
- [Carbon Design System: Remove pattern](https://carbondesignsystem.com/community/patterns/remove-pattern/)
  scales confirmation to impact: undo or no modal for low-impact reversible removal, consequences
  and explicit confirmation for irreversible deletion, and stronger identity checks for catastrophic
  loss. It supports the destructive-action pair.
- [Carbon Design System: Empty states](https://carbondesignsystem.com/patterns/empty-states-pattern/)
  distinguishes first-use/no-data, no-results, permission, system, and configuration states and
  routes each to a contextual explanation and next action. It supports the empty-state good/bad pair.

## Mobile and responsive behavior

- [web.dev: Responsive web design basics](https://web.dev/articles/responsive-web-design-basics)
  supports the viewport declaration, preserving zoom, flexible layouts, content-led breakpoints,
  capability media queries, and not hiding content merely because the screen is small.
- [WCAG: Understanding Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html) establishes
  the 320 CSS-pixel AA reflow requirement, its two-dimensional-content exception, and the rule that
  the exception applies only to the content that requires it.
- [web.dev: Accessible responsive design](https://web.dev/articles/accessible-responsive-design)
  connects responsive layout to zoom accessibility and requires testing reading and focus order at
  each breakpoint.
- [MDN: Layout and the containing block](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Display/Containing_block)
  and [CSS `position`](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/position)
  establish how a sticky element's containing block and nearest scrolling ancestor bound its travel.
- [MDN: CSS `env()`](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/env) and the
  [CSS Environment Variables specification](https://www.w3.org/TR/css-env-1/) define safe-area,
  keyboard-inset, and viewport-segment variables. They support the edge-to-edge good/bad pair without
  hard-coded device dimensions.
- Timothy Horton's WebKit article [“Designing Websites for iPhone X”](https://webkit.org/blog/7929/designing-websites-for-iphone-x/)
  demonstrates why `viewport-fit=cover` requires safe-area padding and why `max()` preserves a normal
  minimum inset. It supports this technique, not adding full-bleed rendering to every page.
- [web.dev: The large, small, and dynamic viewport units](https://web.dev/blog/viewport-units)
  distinguishes `lvh`, `svh`, and `dvh`, records their browser-UI tradeoffs, and notes that the
  on-screen keyboard does not generally affect these units.
- [MDN: Visual Viewport](https://developer.mozilla.org/en-US/docs/Web/API/VisualViewport) explains
  that on-screen keyboards and pinch zoom can shrink the visible viewport without changing the
  layout viewport.
- [MDN: VirtualKeyboard API](https://developer.mozilla.org/en-US/docs/Web/API/VirtualKeyboard_API)
  documents browser-default keyboard resizing, keyboard geometry and inset values, and the API's
  limited availability. It supports default browser handling plus progressive enhancement.
- [web.dev: Form attributes in depth](https://web.dev/learn/forms/attributes/) supports semantic
  input types, `inputmode`, `enterkeyhint`, avoiding `type="number"` for identifiers, avoiding
  surprise autofocus, and leaving submit available for validation.
- [MDN: `autocomplete`](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/autocomplete)
  defines field-purpose tokens and explains how they let user agents offer appropriate form-filling
  assistance. It supports the precise-token example.
- Jamie Holst's 2015 [Baymard mobile checkout and form study](https://baymard.com/blog/mobile-ecommerce-checkout-forms)
  reports 5,200 manually assigned usability scores across 50 major mobile commerce sites and observed
  reduced context with keyboards, placeholder-label failures, nearby-instruction needs, redundant
  entry, and keyboard mismatches. Its e-commerce scope supports the mobile form examples but not a
  universal checkout layout.
- Kara Pernice and Raluca Budiu's [NN/g hidden-navigation study](https://www.nngroup.com/articles/hamburger-menus/)
  tested 179 participants on six live sites and found discoverability and task costs from fully
  hidden navigation. Its strongest mobile result favors partially visible or combined navigation;
  it does not prove every destination must remain visible.
- Steven Hoober's [field observations of mobile grip](https://www.uxmatters.com/mt/archives/2013/02/how-do-users-really-hold-mobile-devices.php)
  recorded 1,333 naturalistic observations, including 780 active screen interactions. The varied
  grips support testing action reach and accidental activation, not a universal thumb-zone layout.
- [U.S. Web Design System: Table](https://designsystem.digital.gov/components/table/) recommends
  minimizing columns, horizontally scrolling wide numerical comparisons, and stacking directory-like
  rows with programmatic labels. It supports choosing a mobile data representation by comparison task.
- [Carbon Design System: Data table](https://carbondesignsystem.com/components/data-table/usage/)
  documents keeping overflow actions persistent when hover is unavailable on mobile and touch.
- [web.dev: Adaptive loading](https://web.dev/articles/adaptive-loading-cds-2019) supports a fast
  baseline and optional enhancement for network or hardware constraints; it also records limited
  browser coverage for several capability signals.
- [MDN: Save-Data](https://developer.mozilla.org/docs/Web/HTTP/Reference/Headers/Save-Data) defines an
  explicit reduced-data preference and warns that support remains limited.
- [web.dev: Offline UX design](https://web.dev/articles/offline-ux-design-guidelines) supports making
  connectivity state visible, preserving useful cached work, and designing explicit slow, offline,
  reconnection, and synchronization states.
- [MDN: Page Visibility API](https://developer.mozilla.org/en-US/docs/Web/API/Page_Visibility_API)
  establishes the visible/hidden lifecycle signal, and [web.dev: Back/forward cache](https://web.dev/articles/bfcache)
  documents persisted `pageshow` after a cached page is restored. They support reconciliation after
  browser suspension; they do not imply that every page must refetch everything.
- [Apple Human Interface Guidelines: Layout](https://developer.apple.com/design/human-interface-guidelines/layout)
  provides platform-practitioner evidence for safe areas, orientation, resizing, text changes, and
  locale changes. This native guidance reinforces the test matrix; it does not define web behavior.
- [Chrome DevTools: Device Mode](https://developer.chrome.com/docs/devtools/device-mode) explicitly
  describes device emulation as a first-order approximation and directs teams to real devices when
  in doubt. It supports the final verification boundary.

## Anonymized production field evidence

These reproductions were audited 7 August 2026. Private implementation and owner identifiers are
omitted; the public sources above define the auditable platform and accessibility contracts.

- A touch-only wrapper became a sticky header's shallow containing block, so the header stopped at
  the wrapper edge. Rendered scroll testing proved the repaired ancestry; the MDN sources generalize
  the contract without prescribing the implementation's `display: contents` fix.
- Three iterations on a full-screen mobile dialog separated keyboard-clear inner content, complete
  overlay coverage, and background scroll ownership. Unit tests covered changing visual-viewport
  overlap, close, unmount, scroll restoration, and cleanup.
- A backgrounded realtime view missed invalidations, while a restored page retained incomplete
  deferred state. Visibility return and persisted `pageshow` reconciliation recovered canonical
  state; the skill omits the implementation's unproven watchdog timing.
- A portaled suggestion popup closed its parent modal when trailing mobile pointer/focus events arrived
  after the child unmounted. Explicit nested-overlay ownership fixed the reproduction; the skill does
  not retain the implementation's tuned grace duration.
- Immediate touch drag activation stole scroll flicks, and a separate card reproduction assigned
  competing long-press recognition to context-menu and reorder behavior. A dedicated handle,
  one gesture owner, intent tolerance, and explicit menu controls fixed the paths. Later retuning
  confirmed that exact time and distance thresholds are project/device choices.

## Scope limits

- These sources do not establish `cursor: pointer` on command buttons as a WCAG requirement. It is a
  deliberate catalog standard. Button order, validation timing, and confirmation patterns remain
  context-dependent and should be tested with representative users when consequential.
- Web target sizes use CSS pixels; do not substitute native-platform units. Safe-area handling is
  for intentional edge-to-edge layouts, and viewport units do not solve every keyboard behavior.
- WCAG conformance cannot be inferred from source inspection or automated checks alone. Verify the
  rendered task with keyboard and representative assistive technology, and report the tested scope.
