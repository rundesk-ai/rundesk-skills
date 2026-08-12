# Playtesting games source map

This package independently synthesizes games user research, general user-research ethics, telemetry
guidance, accessibility practice, and player-experience measurement. It does not adapt AAAbench or
another skill package. Links were verified 12 August 2026.

## Study scope, methods, and moderation

- Steve Bromley, Games User Research,
  [Choose the right playtest method](https://gamesuserresearch.com/choose-the-right-playtest-method/)
  (updated 25 September 2023) — practitioner basis for starting with a research objective; choosing
  among observation, interviews, analytics, and surveys; separating understanding from measurement;
  and combining methods because each has different limits. It is professional guidance, not a
  controlled comparison establishing one universally superior method.
- Bromley,
  [How to run a games user research playtest](https://gamesuserresearch.com/how-to-run-a-games-user-research-playtest/)
  — practitioner basis for representative recruitment, study preparation, observation, unbiased
  moderation, analysis, and iterative use throughout development.
- Bromley,
  [Finding usability issues in games](https://gamesuserresearch.com/find-usability-issues-in-games-with-playtests/)
  and [expert playtest moderation](https://gamesuserresearch.com/expert-playtest-moderation-ask-unbiased-questions/)
  — basis for realistic tasks, observing without revealing missing information, neutral probes,
  recording interventions, and describing impact. The good/bad moderator-question pair in `SKILL.md`
  minimizes the documented contrast between bland probes and questions that expose the answer.
- Bromley,
  [How many players do I need for a playtest](https://gamesuserresearch.com/how-many-players-do-i-need-for-a-playtest/)
  — basis for rejecting a universal participant count and choosing sample size from discovery,
  definition, or measurement goals. Its numeric suggestions are explicitly pragmatic practitioner
  starting points, so this package does not repeat them as research constants.
- Nielsen Norman Group,
  [Usability Testing 101](https://www.nngroup.com/articles/usability-testing-101/)
  — independent UX-practice corroboration for realistic participants, realistic tasks, observation,
  and open, neutral questions. Game-specific mechanics can require different protocols.

## Ethics, privacy, and accessibility

- UK Government Service Manual,
  [Getting informed consent](https://www.gov.uk/service-manual/user-research/getting-users-consent-for-research),
  [managing participant privacy](https://www.gov.uk/service-manual/user-research/managing-user-research-data-participant-privacy),
  and [taking notes and recordings](https://www.gov.uk/service-manual/user-research/taking-notes-and-recording-user-research-sessions)
  — operational basis for informed and continuing consent, data minimization, secure handling,
  retention, withdrawal, observers, recordings, and accessible consent. These are UK public-service
  rules and guidance; the applicable law and organizational review still govern each study.
- Microsoft,
  [Gaming Accessibility Testing Service](https://learn.microsoft.com/en-us/xbox/accessibility/mgats)
  and [Making games accessible](https://learn.microsoft.com/en-us/windows/uwp/gaming/accessibility-for-games)
  — official practitioner basis for involving players with relevant disabilities, testing early,
  and combining player feedback with accessibility guidelines. Microsoft explicitly describes its
  guidelines as best practices, not legal-compliance certification.

## Telemetry and measurement

- Shute and Ventura,
  [Guidelines for the Design, Implementation, and Analysis of Game Telemetry](https://cresst.org/publication/guidelines-for-the-design-implementation-and-analysis-of-game-telemetry/)
  (2014 book chapter) — research basis for recording fine-grained descriptions of behavior with
  context rather than interpretations. The telemetry good/bad pair in `SKILL.md` directly applies
  that lesson to a tutorial event.
- Wallner and Kriglstein,
  [Visualization-based analysis of gameplay data: A review of literature](https://doi.org/10.1016/j.entcom.2013.02.002)
  (2013) — review basis for telemetry's scale and behavioral detail, its inability to reliably explain
  why behavior occurs, and combining it with qualitative methods. The review reflects literature
  available through early 2013, so it supports the method boundary rather than current tooling.
- Vanden Abeele et al.,
  [Development and validation of the Player Experience Inventory](https://playerexperienceinventory.org/pub)
  (International Journal of Human-Computer Studies, 2020; DOI
  `10.1016/j.ijhcs.2019.102370`), with the maintainers'
  [PXI user guide](https://playerexperienceinventory.org/docs) — basis
  for multidimensional measurement and preserving validated items, response scales, administration,
  and scoring when using a benchmark.
- Perrig et al.,
  [Independent Validation of the Player Experience Inventory](https://edoc.unibas.ch/entities/publication/5c0c6e43-575c-4248-af2c-889e5db1859c)
  (CHI 2024; DOI `10.1145/3613904.3642270`; preregistered online study, `n=1,518`) — independent
  evidence generally favoring the PXI
  while identifying challenges with immersion and supporting a ten-factor model, or eleven factors
  when enjoyment is measured. Participants rated a recent or memorable game online; this does not
  validate every language, population, or in-session use.

## Workflow examples

- The bounded-question good/bad pair synthesizes Bromley's research-objective and method-selection
  guidance: an observable audience, context, behavior, and decision can be studied; an undefined
  global “fun” question cannot.
- The session-question pair maps to Bromley's moderation examples above.
- The telemetry pair maps to Shute and Ventura's descriptive-not-inferential event guidance.
