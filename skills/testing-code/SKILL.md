---
name: testing-code
description: Use when designing, adding, repairing, or assessing automated tests in any codebase; reproducing a defect; selecting a test boundary; or diagnosing flaky, brittle, or falsely green results. It supplies a provider- and runner-neutral workflow for deterministic, maintainable cases and auditable evidence. Do not use it only for framework syntax or runner setup.
---

# Testing code

Prove the smallest meaningful contract, then prove the test can detect its violation.

## Define the proof

1. Read repository rules, test commands, nearby tests, and the authoritative requirement.
2. State the observable behavior, required side effects, and risk if it breaks.
3. Search existing tests by behavior; add only missing proof.
4. For a defect, isolate the smallest reproducing input and environment.

```text
Good: assert the public result and required state change.
Bad:  assert a private collaborator was called before another, although users cannot observe it.
```

Assert an interaction only when it is required behavior, such as emitting an event or avoiding an
expensive boundary.

## Choose the boundary that contains the risk

| Boundary | Prove |
|---|---|
| Unit | Decision, transformation, invariant, or error path without infrastructure. |
| Integration | Wiring to a real local boundary such as persistence, filesystem, queue, network, process, or serializer. |
| Contract | Producer and consumer agree on the messages and formats each uses. |
| End to end | A few critical journeys or wiring decisions narrower tests cannot establish. |

Prefer the narrowest boundary containing the risk. Add a wider case only when it answers another
question; do not replay every edge case through the full system. Report what ran and which
dependencies were real because labels vary.

```text
Good: use the real serializer to prove its stored format.
Bad:  mock the serializer and call the result an integration test.
```

## Make one case trustworthy

- Arrange only relevant state, perform one action, and assert the contract.
- Name the condition and behavior; make failures print useful expected and actual values.
- Cover only material partitions such as normal, empty, invalid, maximum, repeated, unauthorized,
  partial, or concurrent behavior.
- Keep causal values visible. Helpers hide noise, not why the case passes.
- Use an independent expected value or oracle. Duplicating production logic can make both wrong.

Never weaken an assertion merely to get green. When behavior changes intentionally, update it from
the requirement—not current output.

## Replace known traps

| Avoid | Do instead | Prove the replacement |
|---|---|---|
| Ambient time, locale, randomness, environment, identifiers, or scheduling | Inject or freeze inputs; record seeds | Re-run the seed and boundaries |
| Shared state or order-dependent cleanup | Use unique state; register cleanup on acquisition | Run alone, reordered, and in parallel |
| Production services or data | Use a real local dependency, hermetic service, contract, or maintained fake | Name the real boundary; test drift separately |
| Mock choreography for computation | Stub inputs; mock only an observable interaction against its real interface | Refactor internals; behavior tests stay green |
| Fixed sleep before an async assertion | Wait for the event or condition with a diagnostic timeout | Delay the operation; completion follows the event |
| Retry that converts intermittent failure to green | Preserve seed, order, timing, logs, and artifacts; fix the cause | Repeat the failing conditions; report retries |

A flaky result is a defect in the test, system, runner, or environment. Quarantine may protect the
main signal temporarily; keep the failure visible and owned.

## Prove the test and the run

1. For a regression, observe failure for the reported reason before the correction. If that is unsafe
   or impractical, state the limitation instead of claiming the defect was reproduced.
2. Run the changed case, containing suite, then required broader checks.
3. Read exit status, discovery/execution counts, skips, expected failures, retries, and warnings.

```text
Good: exit 0; 37 discovered, 37 executed, 0 skipped; new regression passed.
Bad:  "green"; 0 discovered, or the relevant case skipped because its dependency was absent.
```

Coverage locates unexercised code; it does not prove assertions or justify an invented target.

Report the behavior, boundary, command, result, counts, real dependencies, and unresolved paths. Do
not claim more than the evidence covers.

Read [the source map](references/sources.md) when auditing, changing, or extending these rules.
