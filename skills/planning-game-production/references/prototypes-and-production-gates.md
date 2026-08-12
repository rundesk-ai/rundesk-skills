# Prototype and production gates

Use gates to change the amount of money, people, dependencies, and content exposed to uncertainty.
A gate is a decision based on named evidence, not a ceremonial build label.

## Prototype gate

Approve a prototype when its question could materially change the project and its method can
distinguish useful outcomes. Before accepting its result, verify:

- the tested players, system state, controls, and content represented the claim;
- omitted or fake systems did not determine the result;
- observations answer the declared question rather than demonstrate effort;
- contrary behavior and technical failure remain visible; and
- the decision follows the predeclared criteria or explains why the criteria were invalid.

Stop or redesign a prototype whose fidelity cannot answer the question. Adding unrelated systems
usually adds confounds and iteration cost rather than evidence.

## First-playable gate

Use a first playable to align the team around a draft of the core experience. Require:

- the representative player can perform the central actions without developer intervention;
- the system produces enough real response and feedback to evaluate the intended dynamics;
- the team can identify what is authentic, placeholder, missing, or deliberately simplified;
- the build captures failures, observations, and revision decisions; and
- the remaining unknowns and next prototypes are explicit.

Do not require final presentation. Do not infer content throughput, platform readiness, or launch
quality from this gate.

## Vertical-slice gate

Select a segment representative of the hardest important integration—not merely the easiest scene
to polish. Exercise the intended production path for its relevant systems and content:

```text
specification -> authoring -> review -> integration -> build -> test -> correction -> accepted result
```

Require evidence that:

- representative players experience the intended pillars;
- the integrated systems meet the applicable quality, performance, accessibility, save, and
  platform constraints;
- representative content can be produced, reviewed, integrated, tested, and corrected through the
  real pipeline;
- measured effort, rework, external dependencies, and specialist bottlenecks support a defensible
  forecast; and
- unresolved risks, excluded content families, and scaling assumptions remain explicit.

A vertical slice is not automatically a prototype, MVP, marketing demo, alpha, or production
sample. One artifact may serve more than one purpose only when each purpose has its own audience and
acceptance evidence.

## Production-entry gate

Scale content and staffing only when:

- the creative direction and core systems are stable enough that bulk content is unlikely to be
  invalidated;
- the representative slice has exercised the real pipeline and correction path;
- major technical and platform risks have bounded responses;
- content families have samples, owners, quality bars, dependencies, and throughput evidence;
- build, integration, testing, source control, review, and asset management support the planned
  concurrency;
- scope fits demonstrated capacity with contingency for rework and uncertainty; and
- leadership has explicitly accepted the remaining risk.

If evidence is partial, authorize only the work whose assumptions were proven. A date or sunk cost
does not resolve a risk.

## Production and release gates

During production, inspect playable integration and end-to-end content flow, not departmental
completion in isolation. Track accepted output, blocked work, rework, defects, build health,
performance, playtest findings, and scope change at a resolution appropriate to the project.

Define alpha, beta, content complete, code complete, release candidate, and launch from the actual
publisher and platform contracts. Labels vary across organizations; do not import one studio's
definitions as universal. A late phase should narrow change and harden the complete experience,
not become the first time systems, accessibility, saves, platforms, or full-game progression meet.

```text
Good: select a representative content family, run it through authoring to correction, and forecast
      from accepted output and observed rework.
Bad:  estimate the whole content set from the fastest asset made by the pipeline's expert author.

Good: authorize only the content families and systems whose dependencies and throughput were
      exercised; keep the rest behind their own gate.
Bad:  treat one attractive slice as proof that every mode, level type, platform, and pipeline can
      scale.
```

The source mapping for these pairs is in [sources.md](sources.md).
