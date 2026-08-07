---
name: debugging-code
description: Use this skill when asked to diagnose or fix software that crashes, hangs, regresses, behaves inconsistently, returns wrong results, or fails a test, build, or runtime check without a proven cause. It supplies a language-agnostic workflow to reproduce the failure, preserve evidence, isolate the responsible boundary, test causal hypotheses, find root cause, and prove the smallest safe correction. Do not use it to review a completed change or explain a known cause.
---

# Debug code

Find the cause before choosing the correction. Keep observations, inferences, and hypotheses
separate throughout the investigation.

## Establish the failure

1. Read the applicable repository rules and the system's intended contract.
2. Record the expected behavior, actual behavior, impact, affected scope, last known success, and
   earliest known failure.
3. Preserve the exact error, stack, logs, command, inputs, versions, environment, and timestamps.
   Summaries can erase the clue that distinguishes one failure from another.
4. Reproduce with the smallest safe case that still fails. Run the exact case more than once when
   intermittency is possible.
5. Confirm the signal is valid: the command exercised the intended code, instrumentation is current,
   and the observed failure is not a stale artifact or an unrelated setup error.

If the failure cannot be reproduced, state what was attempted and what evidence is missing. Do not
turn a plausible explanation into a proven cause.

For a live or production failure, stabilize user impact before extended diagnosis when authorized.
Do not experiment on production data, permissions, availability, or irreversible state without
explicit authority and a recovery path.

## Model the failing path

- Trace the request, event, or input from its entry point to the first incorrect state, not merely
  the final error.
- Mark component boundaries, state transitions, external dependencies, retries, and asynchronous
  handoffs where evidence can be compared.
- Compare a working and failing case across one dimension at a time: input, version, configuration,
  data, environment, timing, or dependency response.
- Inspect recent code, dependency, configuration, schema, and infrastructure changes, but do not
  assume correlation proves cause.
- Distinguish the visible symptom, the immediate mechanism, and the root condition that made the
  mechanism possible.

## Run a hypothesis loop

1. State one falsifiable cause and the evidence it predicts.
2. Choose the cheapest safe observation or experiment that distinguishes it from the alternatives.
3. Change one variable. Capture the command, input, and result.
4. Reject, refine, or confirm the hypothesis from that result.
5. Repeat until the evidence explains the complete failing path.

Rank hypotheses by fit with the evidence, likelihood, and cost to test. Use boundary probes, binary
search through the call path or change history, targeted logging, a debugger, or a minimal fixture
to shrink the search space.

Avoid shotgun edits, broad dependency upgrades, blind restarts, and several speculative fixes at
once. They destroy causal evidence. A restart that clears a symptom may reveal state involvement,
but it does not establish root cause.

## Handle intermittent failures

Hold code and inputs constant while controlling sources of nondeterminism:

- time, timezone, locale, randomness, and generated identifiers;
- execution order, shared mutable state, cleanup, and parallel workers;
- scheduling, races, timeouts, retries, and eventual consistency;
- network, filesystem, resource pressure, and external-service behavior.

Capture the seed, order, timing, environment, and artifacts for every failure. Do not treat retries,
longer sleeps, or wider timeouts as fixes unless the contract itself requires that behavior.

## Correct the proven cause

If the request is diagnosis-only, stop after establishing the cause and correction direction. When
a fix is authorized:

1. Add or identify the smallest proof that fails for the defect and expresses the intended contract.
2. Change the narrowest responsible code or configuration. Do not bundle unrelated cleanup.
3. Re-run the original reproduction, the focused proof, and the relevant surrounding checks.
4. Exercise nearby boundary and failure cases that share the corrected path.
5. Remove temporary instrumentation and confirm the fix did not conceal the signal.

Use the applicable language or testing skill for framework-specific mechanics.

## Report what is known

Report the original failure, reproduction, evidence trail, root cause, correction, and verification.
Name residual risk and anything not exercised. If causality remains incomplete, label the result as
a leading hypothesis and state the next discriminating check; never report a symptom disappearing
as proof that the defect is resolved.
