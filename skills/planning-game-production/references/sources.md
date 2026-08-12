# Sources

Accessed 12 August 2026. This package synthesizes named studio processes, practitioner postmortems,
official engine education, and empirical analysis of published game-development postmortems. It is
not a universal studio lifecycle. Terms such as first playable, vertical slice, alpha, beta, MVP,
and content complete vary by organization, publisher, platform, team size, and development model;
the package therefore defines gates by purpose and evidence rather than label.

## Prototyping and preproduction

- Remo's report on Eric Todd's GDC session,
  [“Spore: Pre-Production Through Prototyping”](https://www.gamedeveloper.com/design/post-gdc-i-spore-i-pre-production-through-prototyping)
  (2006), documents the *Spore* team's use of focused prototypes to communicate interaction and
  reduce production risk. It records failures from making prototypes too integrated, polished, or
  production-oriented and warns that a prototype's fidelity can produce misleading results. This
  supports the smallest-evidence-vehicle rule and the first good/bad pair in `SKILL.md`. It is a
  conference report about one project, not a universal schedule or architecture rule.
- Todd,
  [“Spore: Preproduction Through Prototyping”](https://gdcvault.com/play/1013443/Spore-Preproduction-Through)
  (GDC 2006), describes prototypes, regular demonstrations, and critique as a preproduction cycle.
  The session overview corroborates the report's scope but does not expose the full talk method.
- Sigman,
  [“Guerilla Prototyping: A Design Post-mortem of the Arcade Strategy Game HOARD”](https://www.gdcvault.com/play/1015523/Guerilla-Prototyping-A-Design-Post)
  (GDC 2012), reports using paper games, low-fidelity 2D prototypes, spreadsheets, and modular
  systems to increase iteration under project constraints. It supports selecting the cheapest
  medium that can answer the question, not its reported project duration as a benchmark.
- Unity,
  [“Ideation and Pre-production”](https://learn.unity.com/course/unity-for-humanity-guide-for-creators/unit/game-development-in-a-nutshell/tutorial/ideation-and-preproduction?version=6.0)
  (verified against the Unity 6.0 course), recommends small, focused prototypes that answer questions
  without needing to enter the final project and notes that paper, spreadsheet, and text prototypes
  can test different claims. This is vendor education, not independent proof of productivity.

## First playable, vertical slice, and production gates

- Donovan,
  [“The Vertical Slice Challenge”](https://gdcvault.com/play/1022328/The-Vertical-Slice)
  (GDC 2015), describes Volition's vertical slice as a preproduction-to-production gate that must
  show both understanding of the intended game and the ability to make it. This supports separating
  experience proof from production-capability proof and maps to the vertical-slice good/bad pair in
  `SKILL.md`. It is one studio's practitioner model; its terminology is not universal.
- Ubisoft,
  [“Creative Process: How We Make Games”](https://www.ubisoft.com/en-us/company/how-we-make-games/creative-process)
  describes an iterative preconception phase, a maintained project mandate, a first playable for a
  draft core experience, preproduction work on tools and process, and later production. It supports
  the mandate and phase-purpose distinction. The public page is a high-level account of one
  publisher's process and does not establish detailed acceptance criteria.
- Unity,
  [“Create Your Production Plan”](https://learn.unity.com/tutorial/create-your-production-plan?version=2022.3)
  (verified against the 2022.3 tutorial), defines milestones as checkpoints with requirements and
  tasks, starts its case study with core interactions, integrates user testing, and reserves its
  final slice milestone for correction and polish rather than new features. It supports outcome-
  based milestones and the third good/bad pair in `SKILL.md`; the case study is illustrative, not a
  required phase count.
- Ruiz,
  [“Quick and Dirty Prototyping: A Success Story”](https://www.gamedeveloper.com/design/quick-and-dirty-prototyping-a-success-story)
  (2010), reports one shipped team's use of an unusually polished one-level slice to evaluate its
  design, art direction, tools, and team capability, followed by lower-fidelity whole-game content
  during production. It supports giving a slice an explicit purpose and using representative work
  to expose team and pipeline capability. It does not establish the reported fidelity or timeline
  as a general target.

## Scope and production risk

- Politowski, Fontoura, Petrillo, and Guéhéneuc,
  [“Game Industry Problems: An Extensive Analysis of the Gray Literature”](https://doi.org/10.1016/j.infsof.2020.106366)
  (Information and Software Technology, 2021), analyzes 200 practitioner postmortems published from
  1997 through 2019, extracting 927 problems in 20 categories. The authors report persistent
  production problems and substantial management, team, planning, scope, prototyping, and feature-
  change concerns, while warning that many remedies are project-specific. This supports keeping
  scope, team, production, and evidence risks visible; the source corpus is self-selected gray
  literature and cannot estimate industry-wide prevalence.
- Politowski et al.,
  [“Video Game Project Management Anti-patterns”](https://arxiv.org/abs/2202.06183)
  (2022 preprint), maps 440 management-related postmortem problems to software project-management
  anti-patterns and identifies feature creep, feature cuts, inadequate tools, and multiple-project
  work as game-specific candidates not covered by its comparison set. It supports explicit scope,
  tooling, and capacity controls. The authors state that the candidate definitions still require
  practitioner-survey validation, so the package does not present their taxonomy as settled.

## Good/bad pair mapping and limits

- The disposable traversal-prototype pair applies the *Spore* report and Unity's focused,
  non-production prototype guidance. Its particular movement-and-camera question is a minimized
  example, not a claim about a real game.
- The vertical-slice pair applies Donovan's production-gate purpose, Ubisoft's separation of first
  playable and preproduction, and Ruiz's team/pipeline evaluation. The package's integrated evidence
  list is a conservative synthesis; no source guarantees forecast accuracy from one slice.
- The outcome-milestone pair applies Unity's milestone requirements and user-testing integration,
  plus the postmortem research's documented planning and scope problems. Closed-task percentage is
  presented as insufficient evidence for uncertain creative work, not as a measured universal
  failure.
- The production-sample pair in the conditional reference applies Ruiz's tool/team-capability
  evaluation and the postmortem research's warning that production remedies are project-specific.
- The attractive-slice pair applies Donovan's distinction between understanding the game and
  knowing how to make it. It deliberately limits inference to the exercised content families and
  pipelines.

GDC and Game Developer sources are named practitioner reports and session descriptions, not
controlled studies. Unity and Ubisoft describe provider or studio practice, not mandatory industry
contracts. No claim depends on AAAbench or its upstream packages; those repositories informed topic
discovery only.
