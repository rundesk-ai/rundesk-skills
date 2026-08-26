---
name: performance-engineering
description: Use when investigating slowness, latency, low throughput, high CPU, memory growth, I/O pressure, saturation, scalability limits, or a performance regression; benchmarking or comparing implementations; load, stress, spike, or soak testing; setting a performance budget; or proving an optimization. It supplies a provider- and language-neutral workflow for defining the workload, collecting trustworthy evidence, locating the limiting boundary, testing one causal change, and proving user-visible improvement without moving cost or hiding errors. Do not use for a functional defect with no performance concern.
---

# Engineer performance

A performance result is incomplete without the operation, workload, environment, statistic, and
correctness boundary it measured. Find the limiting resource or wait before choosing a faster-looking
implementation.

## Route stack-specific mechanics

This skill owns the investigation and proof. Load the stack owner for its profilers and fixes:

- `cpp-patterns` or `python-patterns` for language/runtime work;
- `laravel-patterns`, `vue-patterns`, or `inertia-patterns` for framework work;
- `mysql-patterns`, `postgres-patterns`, or `sqlite-patterns` for query and engine behavior;
- `rundesk-team-marketing/seo` for Core Web Vitals when search or field CWV is the goal; and
- `testing-code` when turning the result into a stable regression check.

Read [profiling-and-observability.md](references/profiling-and-observability.md) when the limiting
boundary is unknown, telemetry disagrees, or a live system is slow. Read
[benchmarking.md](references/benchmarking.md) when comparing code, configurations, builds, or a
before/after change. Read [load-and-capacity.md](references/load-and-capacity.md) when concurrency,
arrival rate, queues, traffic shape, saturation, or sustained operation matters.

## Define the performance contract

Record before measuring:

- the user-visible operation or background outcome;
- latency, throughput, completion time, CPU, memory, allocation, I/O, energy, or cost being judged;
- input sizes, data shape, concurrency or arrival rate, and cold or warm state;
- the measurement boundary and whether failed/cancelled work is included;
- build mode, commit, dependencies, configuration, hardware, topology, and dataset; and
- the target or regression budget and the correctness conditions that must still pass.

- **Bad:** “Average response time improved.”
- **Good:** “Under the same arrival rate and data, compare successful and failed latency separately
  at representative percentiles, throughput, errors, and saturation.”

The good pattern follows Google SRE's latency and percentile guidance. The complete lesson mapping
is in [sources.md](references/sources.md).

Do not invent a universal threshold. Derive it from a product requirement, service objective,
frame/time budget, capacity need, or an explicitly approved baseline.

## Establish a trustworthy baseline

1. Reproduce the reported workload and verify its output is correct. Faster wrong work is failure.
2. Measure end to end first. A microbenchmark cannot identify whether its code matters to the real
   path.
3. Capture raw results and context, not only a dashboard screenshot or one aggregate.
4. Run enough independent repetitions to see noise, warmup, periodic work, and run-to-run drift.
5. Keep one known-good case beside the failing case and change one dimension at a time.

Separate cold-start, warm steady-state, cache-hit, and cache-miss results when each occurs in real
use. Do not warm a benchmark merely because the warm number looks better.

## Locate the limiting boundary

Work from the outcome inward:

1. **Service:** latency distribution, traffic/throughput, errors, and saturation.
2. **Path:** trace or time each major boundary, including dependencies, queues, retries, and
   serialization.
3. **Resource:** for CPU, memory, storage, network, pools, and workers, check utilization,
   saturation/queued work, and errors.
4. **Code:** profile the narrowed path with the stack's supported tool.

High wall time with low CPU is not evidence that the code is efficient; it often means off-CPU wait
for I/O, locks, scheduling, a pool, or a dependency. High utilization is not by itself the cause;
saturation and queued work show that demand is waiting.

## Test one causal improvement

State one hypothesis and its predicted evidence. Prefer removing or bounding work before making the
same work locally faster:

1. eliminate unused work and repeated calls;
2. change an algorithm, data access pattern, or network boundary;
3. batch, stream, or bound work where the contract permits;
4. cache only with a key that preserves correctness and authorization/tenant isolation, plus a
   staleness, invalidation, memory, and stampede plan; then
5. tune implementation details shown by the profile.

Change one causal variable. Keep correctness, workload, and environment comparable. Record tradeoffs:
a latency win that increases errors, tail latency, memory, downstream load, or cost may be a
regression somewhere else.

Do not place personalized or sensitive results in a shared cache unless storage, keying, and reuse
are proven to preserve the authorized audience.

## Prove and preserve the result

Re-run the baseline protocol and report:

- before/after distributions or repeated measurements, not only the best run;
- throughput, failures, timeouts, retries, dropped work, and relevant resource use;
- absolute and relative change with run-to-run variation or an uncertainty interval;
- the exact workload, builds, environment, profiler or harness, and raw-result location; and
- what was not exercised, including scale, duration, platforms, cold state, or production traffic.

Add a regression guard only when its environment and noise support the threshold. Gate on a change
larger than normal variation or on a durable budget; a shared runner that fails on tiny timing
movements creates flaky ceremony, not protection.

Do not declare success because a profiler hotspot shrank, one percentile improved, a restart cleared
the symptom, or the system survived a load test. Success means the named performance contract is met,
correctness holds, and the cost did not reappear at another boundary.
