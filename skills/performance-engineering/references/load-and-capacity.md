# Load and capacity testing

Read this when demand, concurrency, queues, saturation, sustained use, or a traffic surge is part of
the question.

## Choose the test from the decision

| Need | Test shape | Proof sought |
|---|---|---|
| Validate the script and environment | minimal smoke | assertions and telemetry are credible |
| Prove expected demand | representative steady load | target holds with acceptable errors/resources |
| Find degradation or capacity limit | gradually increasing stress/breakpoint | first contract or resource limit to fail |
| Model sudden demand | spike and recovery | queueing, shedding, recovery, and retry behavior |
| Find accumulation over time | sustained soak | memory, pools, queues, storage, and latency remain bounded |

Capacity is the demand where the approved contract first stops holding, not merely the point where a
process crashes.

## Model arrivals instead of choosing a convenient user count

Derive the workload from observed or required operations, mixes, payloads, think time, concurrency,
arrival rate, burst shape, and dependency behavior.

Closed-loop clients wait for a response before beginning more work. When the system slows, they also
send work more slowly. That is correct for some fixed-user workflows and misleading when real
arrivals continue independently.

- **Bad:** hold virtual users constant, observe a stable average, and claim the target arrival rate
  passed even though throughput fell as latency rose.
- **Good:** use an open arrival model when arrivals are independent; record requested and achieved
  rate, unfinished/dropped iterations, latency distribution, errors, and generator saturation.

Grafana k6 documents this coordinated-omission trap directly. HdrHistogram's maintainers show why a
long pause can be represented by too few samples when measurement waits with the system.

## Observe the whole experiment

During every run record:

- achieved demand and operation mix;
- success, failure, timeout, cancellation, retry, and dropped-work counts;
- latency percentiles or distributions for important operation classes;
- queue depth, pool wait, worker concurrency, dependency behavior, and resource saturation;
- load-generator CPU, memory, network, open connections, and scheduling limits; and
- warmup, steady-state, ramp, and recovery windows separately.

A generator that cannot issue the planned work invalidates a capacity claim. A fast response that is
an error does not satisfy a latency target. A retry can hide an error while increasing latency and
amplifying load; count original operations and every attempt.

## Keep tests safe and representative

- Use isolated or explicitly approved environments and synthetic accounts/data. Load tests can
  create bills, send messages, trigger rate limits, exhaust quotas, or destroy shared test data.
- Do not run against production or a third-party service without explicit authority, agreed limits,
  stop conditions, monitoring, and recovery ownership.
- Begin with a smoke run, then increase one load dimension. Stop on the agreed error, latency,
  saturation, data-integrity, or generator limit.
- Preserve dependency behavior. Stubbing every dependency can measure application capacity but not
  end-to-end capacity; hitting every real dependency can be unsafe. State the boundary.
- Verify cleanup and correctness after the run. Throughput that duplicates, drops, or corrupts work
  is not capacity.

## Explain the breaking point

Report the first missed contract, its demand level, the saturated or queued boundary, and recovery
behavior. Distinguish a system limit from a generator limit, dependency quota, test-data artifact,
or configured pool cap. If the test never reached the target arrival rate, report that as an
inconclusive run rather than a pass.
