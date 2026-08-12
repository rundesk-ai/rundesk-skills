# Sources

Accessed 12 August 2026. This package independently synthesizes camera research, named practitioner
analysis, official accessibility guidance, and input-platform contracts. It does not adapt AAAbench
or another skill package. Camera findings are genre-, task-, display-, and implementation-dependent;
none establishes one universally best view, smoothing value, FOV, or control scheme.

## Cameras, framing, and spatial information

- Denisova and Cairns,
  [“First Person vs. Third Person Perspective in Digital Games: Do Player Preferences Affect Immersion?”](https://openaccess.city.ac.uk/id/eprint/21350/)
  (CHI 2015), experimentally examined perspective and reported immersion in one role-playing game.
  It supports treating perspective as part of the experience rather than a cosmetic choice; its
  self-reported outcome and game context do not prescribe a view for other genres.
- Burelli,
  [“Virtual Cinematography in Games: Investigating the Impact on Player Experience”](https://pure.itu.dk/da/publications/virtual-cinematography-in-games-investigating-the-impact-on-playe/)
  (FDG 2013), investigates how camera behavior affects player experience. Its bounded experimental
  context supports testing camera decisions rather than assuming cinematographic rules transfer
  unchanged to interactive play.
- Itay Keren,
  [“Scroll Back: The Theory and Practice of Cameras in Side-Scrollers”](https://www.gdcvault.com/play/1022243/Scroll-Back-The-Theory-and)
  and [slides](https://media.gdcvault.com/gdc2015/presentations/Keren_Itay_ScrollBack.pdf)
  (GDC 2015), compares position locks, camera windows, movement cues, look-ahead, and framing across
  shipped side-scrollers. It supports task-specific camera layers and the deadzone/look-ahead rules;
  it is practitioner analysis, primarily for side views.
- John Nesky,
  [“50 Camera Mistakes”](https://www.gdcvault.com/play/1021262/50-Camera)
  (GDC 2014), documents practitioner failures involving direction, distance judgment, line of sight,
  usefulness, and simulation sickness. It supports the edge-state and player-needs validation
  workflow, not fixed implementation constants.
- Mark Haigh-Hutchinson,
  [“Fundamentals of Real-Time Camera Design”](https://media.gdcvault.com/gdc05/slides/GD_Haigh-Hutchinson_FundamentalsReal-TimeCameraDesign2.pdf)
  (GDC 2005), provides a named-practitioner treatment of transform, targeting, smoothing, and
  constraint concerns. APIs and hardware assumptions are dated; this package retains only portable
  decision boundaries.

## Input and accessibility

- Microsoft,
  [Xbox Accessibility Guideline 107: Input](https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/107),
  supports alternate input, configurable controls, simplified interactions, and avoiding assumptions
  about physical ability. XAGs are best practices developed with disability-community input, not a
  compliance certificate.
- Microsoft,
  [Xbox Accessibility Guideline 117: Visual distractions and motion settings](https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/117),
  supports options for FOV, sensitivity, auto-centering, shake, bob, blur, sway, and other motion that
  can create barriers. It maps to the comfort rule and optional-shake portion of the first pair.
- Microsoft,
  [GameInput overview](https://learn.microsoft.com/en-us/gaming/gdk/docs/features/common/input/overviews/input-overview),
  documents timestamped readings, polling/callback modes, and multiple device families. It supports
  treating physical input as an adapter contract; the package does not prescribe this API.
- SDL,
  [Gamepad API overview](https://wiki.libsdl.org/SDL3/CategoryGamepad) and
  [adding a mapping](https://wiki.libsdl.org/SDL3/SDL_AddGamepadMapping),
  documents the difference between raw joystick controls and standardized gamepad positions, plus
  mappings for unknown devices. It supports testing device variation and recoverable mappings rather
  than assuming one physical layout covers every controller; the package does not prescribe SDL.

## Good/bad mapping

- The layered-follow pair applies Keren's composition patterns, Nesky's failure cases, Haigh-
  Hutchinson's camera decomposition, and XAG 117's motion-control guidance. Time-based damping is the
  catalog's portable conclusion; exact equations remain implementation-specific.
- The semantic-binding pair applies XAG 107 and the GameInput/device-variation contracts. Keeping
  prompts synchronized is a conservative usability requirement; no source claims one storage schema.
