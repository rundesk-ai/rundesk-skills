# Testing-code source map

Use this map to audit a lesson, not as more testing procedure. Tool documentation establishes
observable runner and environment contracts; practitioner sources establish recurring failures and
field-tested replacements. Links were checked 7 August 2026.

## Contract, boundary, and maintainability

- [Google Engineering Practices: what to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
  asks whether a test would fail when code is broken, warns that tests do not test themselves, and
  requires simple, useful assertions. This supports proving a regression fails and keeping test
  logic small. When the faulty revision cannot safely run, the skill requires disclosing that limit
  rather than substituting an unsourced proof technique.
- [Google Testing Blog: Test Behavior, Not Implementation](https://testing.googleblog.com/2013/08/testing-on-toilet-test-behavior-not.html)
  documents refactor-brittle interaction assertions and the exception for implementation details
  that are actual requirements. It establishes the first good/bad pair and mock boundary.
- Ham Vocke's [Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html),
  published by Martin Fowler, distinguishes unit, integration, contract, and end-to-end scopes;
  recommends observable behavior, real local dependencies, few high-level journeys, and no duplicate
  high-level coverage. The boundary labels in `SKILL.md` are a compact synthesis, not universal
  framework definitions.
- [Pact: writing consumer tests](https://docs.pact.io/consumer) distinguishes contract testing from
  provider functional testing and says each interaction should catch a consumer bug or a real
  misunderstanding. This establishes the narrow contract-test purpose.
- [Microsoft's unit-testing best practices](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices)
  provides worked bad/good cases for minimal inputs, readable Arrange/Act/Assert structure, avoiding
  logic in expected results, and testing private behavior through public behavior. Although its
  syntax is .NET-specific, these cited failure mechanisms are not.
- [Google Testing Blog: Include Only Relevant Details in Tests](https://testing.googleblog.com/2023/10/include-only-relevant-details-in-tests.html)
  demonstrates both traps behind test helpers: noisy fixtures obscure relevance, while over-extracted
  setup hides critical values and their relationship to the assertion.

## Isolation, dependencies, and nondeterminism

- Bazel's normative [Test Encyclopedia](https://bazel.build/reference/test-encyclopedia) defines a
  hermetic test as depending only on declared or runner-guaranteed resources. It explains why
  undeclared services weaken reproducibility and risk cross-test collisions or accidental load, and
  requires unique temporary paths and cleanup when isolation is not supplied.
- John Micco's [Flaky Tests at Google and How We Mitigate Them](https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html)
  reports that retries reduce false positives but encourage teams to ignore flakiness. It supports
  treating retries as mitigation/evidence rather than proof of a pass.
- George Pirocanac's [Test Flakiness remedies](https://testing.googleblog.com/2021/03/test-flakiness-one-of-main-challenges.html)
  maps order dependence, shared state, incomplete cleanup, environment assumptions, and timing races
  to isolation, controlled inputs, and synchronization rather than arbitrary delay.
- [pytest's flaky-test guidance](https://docs.pytest.org/en/stable/explanation/flaky.html) identifies
  uncontrolled system state and failed cleanup as common causes, points to order-randomizing and
  replay tools, and warns that a flaky signal can hide genuine failures.
- [Google Testing Blog: Time is Random](https://testing.googleblog.com/2008/04/tott-time-is-random.html)
  reproduces clock-dependent boundary failures and replaces ambient time with a controlled input.
- [Google Testing Blog: Sleeping Is Not Synchronization](https://testing.googleblog.com/2008/08/tott-sleeping-synchronization.html)
  shows that a fixed sleep is both slow and still racy; synchronization on the completion condition is
  the replacement. Playwright's current [auto-waiting contract](https://playwright.dev/docs/actionability)
  independently demonstrates bounded, condition-based actions and assertions in a maintained runner.

## Execution evidence and coverage

- [pytest exit codes](https://docs.pytest.org/en/stable/reference/exit-codes.html) distinguishes a
  successful collected run from exit code 5, where no tests were collected. This is direct evidence
  for rejecting zero-discovery false greens even when another runner reports them less clearly.
- Python's [`unittest` result and skip contracts](https://docs.python.org/3/library/unittest.html#skipping-tests-and-expected-failures)
  show that skipped and expected-failure cases are not executed as ordinary passing tests and are
  reported separately. The lesson is to inspect counts and reasons, not to prescribe Python syntax.
- [Google Testing Blog: Code Coverage Best Practices](https://testing.googleblog.com/2020/08/code-coverage-best-practices.html)
  says coverage is a lossy, indirect metric: covered code may only be incidental or weakly asserted,
  no ideal percentage applies universally, and uncovered risky behavior is the useful review target.

## Deliberate omissions

- Framework syntax, runner configuration, snapshot mechanics, browser selectors, and language-specific
  fixture APIs belong in the relevant project or ecosystem skill.
- Universal coverage percentages, fixed test-layer ratios, and a rule to mock every dependency were
  omitted because the sources make them context-dependent or identify their failure modes.
- Production test traffic, retries-as-success, fixed sleeps, and “green means proven” were not softened
  into preferences because the cited contracts and field reports document concrete safety or signal
  failures and usable replacements.
