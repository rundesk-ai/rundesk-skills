# Choose methods and analyze playtest evidence

Read this when a playtest needs telemetry, a survey, variant comparison, or mixed-method synthesis.

## Match question, data, and claim

| Question | Useful evidence | Claim limit |
|---|---|---|
| What usability problems occur? | Direct observation plus neutral probes | Problems in the tested tasks, build, context, and participant groups |
| Why did a player act this way? | Immediate neutral interview grounded in an observed moment | The participant's account, not an objective cause by itself |
| How often did an event occur? | Versioned telemetry with an explicit denominator | Descriptive behavior in the instrumented population |
| Did one variant change an outcome? | Randomized assignment where practical, predefined outcome and analysis | The tested variants and eligible population; inspect uncertainty and attrition |
| How was an experience rated? | A fit, validated instrument administered as specified | The constructs and population supported by that instrument |

Select the method before looking at outcomes. If the build or recruitment cannot support the intended
claim, narrow the claim rather than decorating weak evidence with more metrics.

## Design behavioral telemetry

Start with the research question and decision. Define every event before implementation:

```text
event name | exact trigger | required properties | denominator | build/content version | exclusions
```

- Record actions and state, not guessed motives or emotions.
- Include enough context to distinguish retries, progression states, difficulty settings, variants,
  accessibility options, and interrupted sessions.
- Define a funnel from eligible opportunities. A completion count without exposure and eligibility
  cannot measure success.
- Version schemas and content. A renamed level, changed tutorial, or altered trigger can make two
  identical-looking events incomparable.
- Validate logging against a known play trace: missing, duplicated, reordered, or retried events can
  produce a convincing false result.
- Minimize identifiers and payloads. Consent and product telemetry policy govern collection,
  retention, access, and deletion; a useful metric is not automatic permission to collect it.

Telemetry answers what the implementation recorded. Pair surprising patterns with observation or
interviews before assigning a cause.

## Use surveys without manufacturing precision

Define the construct before writing a question. Prefer an established instrument whose population,
language, timing, and validation fit the decision. Preserve its wording, response anchors, item set,
ordering rules, and scoring when claiming to use that instrument.

Do not treat one satisfaction item, free-text prompt, or average of unrelated questions as a
validated measure of “fun.” The Player Experience Inventory, for example, treats player experience as
multiple functional and psychosocial constructs. Its maintainers require the validated items and
scale for benchmark comparisons, while an independent 2024 study found generally favorable evidence
but a challenge around its immersion construct. Report constructs separately and retain such limits.

For a custom survey:

- ask one thing per item in neutral, concrete language;
- place questions after the relevant experience while recall is fresh;
- pilot interpretation with people like the intended respondents;
- predefine exclusions, scoring, comparisons, and uncertainty; and
- preserve distributions and missing responses instead of reporting only an average.

## Compare builds or variants

Change one decision-relevant difference when feasible. Keep hardware, instructions, session length,
starting state, and moderator behavior comparable. Randomize assignment or order where learning and
fatigue could bias the result; use a within-player comparison only when carryover is acceptable.

Record assignment, exposure, technical failures, noncompletion, and exclusions. Analyze the outcome
chosen before inspection. An observed difference is not automatically important, causal, or
generalizable; show its size, uncertainty, sample, and practical consequence.

## Synthesize without voting

Build a traceable evidence table:

```text
finding | intended experience | participant/context | timestamps/events | impact | counter-evidence | confidence
```

Triangulate rather than tally unlike evidence. Observation establishes behavior, interviews add the
participant's account, telemetry adds scale, and surveys measure stated constructs. Agreement raises
confidence; disagreement is a result to investigate, not a reason to discard one method.

Separate:

- a usability barrier that prevents intended action;
- a preference that differs across player groups;
- a balance outcome that depends on skill or strategy;
- a technical defect that invalidates a task; and
- a new design idea suggested by a participant.

Present findings with representative evidence and material counterexamples. A player suggestion is a
clue to the experienced problem, not a requirement. Convert the explanation into a prediction, make
the smallest relevant change, and run the next round.
