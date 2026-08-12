---
name: planning-game-production
description: Use when planning a game's development lifecycle, preproduction, prototypes, technical spikes, first playable, vertical slice, production milestones, content pipeline, scope gates, or a transition into full production. It supplies a risk-driven workflow that makes each phase retire a named uncertainty and requires observable evidence before scaling cost. Do not use it for gameplay design alone, detailed implementation plans, sprint administration, or launch operations alone.
---

# Planning game production

Plan the project as a sequence of evidence purchases. Spend the least time and fidelity needed to
answer the most consequential unresolved question, then scale only what the evidence supports.

## Establish the production mandate

Ground the plan in the current game-design contract. Record:

- intended audience, platforms, input, business model, distribution, rating, localization, and
  accessibility constraints;
- experience pillars and the representative slice of play that expresses them;
- team roles, availability, demonstrated capabilities, tools, budget, external dependencies, and
  immovable dates;
- target quality and content breadth, with explicit non-goals; and
- who can approve scope, quality, schedule, spending, platform, and release decisions.

Keep this mandate current and short enough to guide tradeoffs. A large design document is not proof
that the interaction works or that the team can produce it.

## Rank risks before features

Build a risk register around claims that could invalidate the project or materially change its
scope. Include at least:

- **experience risk:** the intended players do not perceive or value the core experience;
- **design risk:** the rules do not create the predicted decisions or dynamics;
- **technical risk:** required performance, simulation, networking, platform, tools, or integration
  cannot meet the target;
- **content risk:** the team cannot produce enough variety at the quality and cost assumed;
- **production risk:** dependencies, staffing, review, build, test, and rework rates cannot support
  the plan;
- **market and business risk:** the audience, price, acquisition, distribution, or ongoing cost
  assumptions are unsupported; and
- **safety and compliance risk:** accessibility, privacy, child safety, ratings, monetization, or
  platform obligations would require redesign.

For each risk, record its assumption, impact if wrong, current evidence, cheapest discriminating
test, owner, decision date, and response if contradicted. Prioritize by consequence and cost of late
discovery, not by which feature is easiest or most exciting to build.

Do not invent team size, dates, phase duration, content counts, or throughput to make an incomplete
brief look scheduled. Keep them as unresolved inputs or ranges tied to a named assumption until
staffing, dependencies, accepted quality, and representative production evidence can support them.

## Choose the smallest evidence vehicle

Match fidelity to the question:

| Vehicle | Use it to answer | Do not demand |
|---|---|---|
| Thought experiment, rules walkthrough, or paper model | Rule completeness, choice structure, obvious exploits | Timing, feel, or technical feasibility |
| Spreadsheet or simulation | Economy flows, probability, trajectories, capacity assumptions | Human understanding or enjoyment |
| Interaction prototype | A mechanic, control, camera, timing, or player loop | Reusable architecture or finished content |
| Technical spike | One feasibility, performance, pipeline, or integration risk | Representative player experience |
| First playable | Whether the core actions and intended response coexist in a playable draft | Final quality or production throughput |
| Vertical slice | Whether one representative segment can meet the intended quality through the real pipeline | Complete content breadth or launch readiness |
| Production sample | Repeatable throughput, review, integration, and cost for a content family | Proof for unrelated content families |

Keep prototypes disposable unless reuse is itself the hypothesis. Polishing exploratory code and
content slows iteration and can make the team defend sunk work instead of testing the claim.

Write a prototype contract before building:

```text
question and decision it unlocks
representative audience, input, state, and scenario
included behavior and deliberately fake or omitted behavior
evidence to collect and confounds to avoid
pass, revise, stop, or escalate criteria
time/cost boundary and owner
what may and may not enter production
```

Use `playtesting-games` for studies with representative players, `testing-code` for automated
correctness evidence, and `performance-engineering` for technical budgets and benchmarks.

Read [prototypes-and-production-gates.md](references/prototypes-and-production-gates.md) when
choosing a prototype, defining first-playable or vertical-slice evidence, evaluating pipeline
readiness, or writing phase gates.

## Build milestones around outcomes

Make each milestone a coherent, observable build or production capability. Define:

- the decision or risk it owns;
- playable or inspectable entry and exit state;
- quality, performance, accessibility, and platform requirements that apply now;
- content and system dependencies;
- named evidence and acceptance owner;
- excluded work and change budget; and
- response to acceptance, partial evidence, contradiction, or missed capacity.

Separate discovery from production commitment. A discovery milestone may end by deleting code,
changing the game, or stopping the project; that is a useful result when it prevents expensive
production based on a false assumption.

Order dependencies so representative work traverses the real path early: authoring, integration,
build, review, test, localization where relevant, and correction. Do not declare a pipeline ready
because one expert hand-built one polished asset outside it.

## Control scope through the experience contract

Maintain a scope ledger with every material feature and content family mapped to a pillar, required
constraint, dependency, estimated production load, and validation state. When capacity or evidence
changes:

1. preserve the smallest coherent player experience;
2. cut unsupported breadth before weakening every feature;
3. remove dependent content and promises with the owning feature;
4. re-estimate integration, test, localization, certification, support, and rework—not only creation;
5. revalidate affected loops and production samples; and
6. update external commitments through their authorized owner.

Do not use overtime as capacity or defer accessibility, performance, save compatibility, build
reliability, and platform requirements until polish. Late discovery turns them into redesigns and
false schedule confidence.

Route the resulting cross-component implementation work to `writing-plans`. This skill owns phase
and evidence decisions, not repository-specific file and symbol instructions.

## Report the decision, not activity

At every review, show:

- what build, artifact, or pipeline path was exercised;
- which claim the evidence supports, contradicts, or leaves unresolved;
- representative observations and measured results, including failures;
- quality or scope debt intentionally accepted;
- current burn, throughput, rework, and remaining uncertainty at the resolution the team can
  actually defend; and
- the explicit continue, change, cut, pause, or stop decision.

Avoid percent-complete claims for uncertain creative work and asset counts without verified
throughput. Activity, code volume, and polished screenshots can rise while project risk remains
unchanged.

## Deliver an executable production plan

Produce:

1. the production mandate, authority map, constraints, and non-goals;
2. a ranked risk register with evidence vehicles and decision dates;
3. prototype contracts and disposal/reuse boundaries;
4. first-playable, vertical-slice, production, and release gates that apply to this project;
5. milestone outcomes, dependencies, owners, acceptance evidence, and change budgets;
6. representative content families and pipeline throughput tests;
7. scope ledger, cut order, contingency, and stop conditions; and
8. a current evidence report with unresolved claims and the next cheapest decisive test.

```text
Good: build a disposable movement-and-camera prototype to decide whether traversal supports the
      exploration pillar; exclude progression, final art, and save architecture.
Bad:  start the production character controller so the prototype work will not be wasted.

Good: enter production after a representative slice proves the experience, target quality, real
      pipeline, correction path, and defensible cost assumptions.
Bad:  call a polished demo a vertical slice and green-light production without testing throughput.

Good: define a milestone by a playable outcome, applicable quality constraints, evidence owner,
      excluded scope, and the decision it unlocks.
Bad:  define a milestone as a feature list and report percent complete from closed tasks.
```

The evidence, pair mapping, and research limits are in [sources.md](references/sources.md).
