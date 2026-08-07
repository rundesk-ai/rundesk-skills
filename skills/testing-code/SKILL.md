---
name: testing-code
description: Use this skill when asked to design, add, repair, organize, or assess automated tests in any language; reproduce a defect; choose unit, integration, contract, or end-to-end coverage; or diagnose flaky, slow, brittle, or misleading tests. It supplies a language-neutral workflow to choose the smallest meaningful boundary, assert observable behavior, control nondeterminism and dependencies, and produce actionable failures. Pair it with a language- or framework-specific testing skill for syntax and tooling.
---

# Test code

Write the smallest test that would detect a meaningful violation of the intended contract. Treat test
code as maintained production code: readable, deterministic, and valuable when it fails.

## Establish what must be proven

1. Read the repository's rules, existing test layout, runner commands, and nearby conventions.
2. Translate the requirement or defect into observable behavior before choosing a framework or
   assertion.
3. Identify the risk: wrong result, invalid state, broken boundary, lost data, unsafe access,
   concurrency error, or failed user journey.
4. Inspect existing coverage by behavior. Add a test only when it proves something not already
   established at an appropriate level.

For a defect, first create a focused regression case that fails for the reported reason. A case that
passes before the correction, or fails during unrelated setup, does not prove the defect.

## Choose the smallest useful boundary

| Boundary | Use it to prove |
|---|---|
| Unit | Pure decisions, transformations, invariants, and error handling inside one small boundary. |
| Integration | Serialization, persistence, filesystem, process, queue, network, or component contracts with a real local dependency where practical. |
| Contract | A producer and consumer agree on requests, responses, events, or stored formats without requiring the complete system. |
| End to end | A small number of critical user journeys and wiring decisions that lower levels cannot prove. |

Prefer the lowest boundary that includes the risk. Add a wider test only when it answers a different
question; repeating every edge case through the full stack increases cost without adding confidence.
Testing terminology varies, so describe what runs and which dependencies are real instead of relying
on the label alone.

## Design an actionable case

- Arrange only the state required, perform one meaningful action, then assert the resulting contract.
- Name the behavior and condition so the failure is understandable without opening the test body.
- Cover the normal case plus material boundaries and failures: empty, invalid, repeated, maximum,
  partial, unauthorized, or concurrent behavior when the contract makes them relevant.
- Assert public results and meaningful side effects. Avoid private fields, incidental call order,
  generated formatting, or other implementation details unless they are the contract.
- Use the narrowest assertion that prints useful expected and actual values. A failure should expose
  enough evidence to begin diagnosis without adding instrumentation and rerunning.
- Keep control flow and helper logic small. A reader should not need to simulate the test to learn
  which behavior failed.

Do not weaken an assertion merely to make a suite green. When intended behavior changes, update the
test from the authoritative requirement, not by copying the current implementation.

## Control the environment

- Give every case its own mutable state and make execution order irrelevant.
- Control clocks, timezones, locale, randomness, identifiers, environment variables, and scheduling
  when they affect the result. Record seeds for generated cases.
- Create resources in setup and register cleanup immediately. Use unique temporary files, records,
  ports, accounts, and namespaces when cases may run concurrently.
- Never call production services or modify production data. Prefer a real local dependency, a
  hermetic test service, or a maintained fake.
- Use stubs to supply inputs and mocks only when an interaction is itself observable behavior.
  Constrain doubles to the real interface; extensive mock choreography usually tests implementation.
- Wait for an observable condition or event in asynchronous tests. Fixed sleeps trade one race for a
  slower race.

Treat a flaky result as a defect in the test, system, runner, or environment. Preserve the failing
seed, order, timing, and artifacts, then find the source of nondeterminism. Retries may gather
evidence; they must not redefine an unreliable test as passing.

## Run proof in widening circles

1. Run the new or changed case and confirm it exercises at least one test.
2. For a regression, observe the expected failure before the correction when practical.
3. Run the containing file, class, or package to expose isolation and shared-state problems.
4. Run the repository's required broader checks in its prescribed environment.

Read exit status, discovered-test count, skips, retries, warnings, and failure output. A green command
that selected nothing or silently skipped the relevant environment proves nothing.

Use coverage to locate unexercised risk, not as a substitute for assertions or as an invented target.
A covered line may be incidental; an uncovered line may be unreachable or irrelevant.

## Report the evidence

State the behavior proved, boundary chosen, test command, result, and discovered count. Name any real
dependency, skipped environment, unresolved flake, or important path not exercised. Do not claim the
whole system works when the evidence covers only one boundary.
