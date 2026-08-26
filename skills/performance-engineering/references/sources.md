# Performance engineering source basis

This package synthesizes performance investigation methods, maintained tool guidance, empirical
benchmark research, and production-systems practice. It does not copy a profiler or load generator
manual. Verified on **August 7, 2026**.

## Defining and locating the problem

- [Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/) —
  Google SRE's latency, traffic, errors, and saturation signals. It explicitly separates successful
  from failed latency, supporting the core good/bad measurement pair.
- [Service Level Objectives](https://sre.google/sre-book/service-level-objectives/) and
  [Production Services Best Practices](https://sre.google/sre-book/service-best-practices/) — define
  performance from a user-visible operation, use percentiles for distribution shape, separate
  workload classes, and establish capacity by load testing rather than inherited machine ratios.
- [The USE Method](https://www.brendangregg.com/usemethod.html) — Brendan Gregg's practitioner
  checklist: utilization, saturation, and errors for each resource. Its scope is early bottleneck
  discovery, not automatic root cause.
- [CPU Flame Graphs](https://www.brendangregg.com/FlameGraphs/cpuflamegraphs.html) and
  [Off-CPU Flame Graphs](https://www.brendangregg.com/FlameGraphs/offcpuflamegraphs.html) — sampling
  profiles identify accumulated on-CPU paths; blocking, I/O, locks, and scheduling require off-CPU
  evidence. This supports the “low CPU does not clear a slow path” replacement.
- [OpenTelemetry metrics](https://opentelemetry.io/docs/concepts/signals/metrics/) — histograms for
  distributions and the memory cost of one aggregation per attribute combination. It specifically
  names user IDs and raw URL paths as high-cardinality traps.
- [The Tail at Scale](https://research.google/pubs/the-tail-at-scale/) — Jeffrey Dean and Luiz André
  Barroso, *Communications of the ACM*, 2013. Google production-system analysis showing that rare
  component delays dominate end-to-end latency as fan-out and utilization increase; the basis for
  retaining tail distributions rather than optimizing only the average.
- [RFC 9111: HTTP Caching](https://www.rfc-editor.org/rfc/rfc9111.html) — the IETF standard defines
  cache keys, authenticated-response restrictions, `private`, freshness, validation, and
  invalidation. Its shared-cache contract supports the narrower HTTP rule; this catalog generalizes
  the safety gate to any shared cache: prove identity and authorization isolation before counting a
  hit as a performance win.

## Benchmark validity

- [Producing Wrong Data Without Doing Anything Obviously Wrong](https://www2.ccs.neu.edu/racket/Performance/mytkowicz.pdf) —
  Mytkowicz, Diwan, Hauswirth, and Sweeney, ASPLOS 2009. Experiments used 12 SPEC CPU2006 C
  benchmarks across Pentium 4, Core 2, and an m5 simulation, with 5,940 runs per benchmark, plus a
  survey of 133 systems papers. Unused environment size and link order produced material measurement
  bias; the authors propose setup randomization and causal analysis.
- [Rigorous Benchmarking in Reasonable Time](https://kar.kent.ac.uk/33611/) — Tomas Kalibera and
  Richard Jones, ISMM 2013. Models uncertainty at multiple repetition levels—invocations, process/VM
  executions, and builds—and uses confidence intervals to design a defensible experiment without
  blindly maximizing repetitions.
- [Quantifying Performance Changes with Effect Size Confidence Intervals](https://www.cs.kent.ac.uk/pubs/2012/3233/) —
  Kalibera and Jones' method for reporting the magnitude and uncertainty of a performance ratio,
  supporting effect-plus-uncertainty rather than a bare “x times faster.”
- [Google Benchmark user guide](https://github.com/google/benchmark/blob/main/docs/user_guide.md) —
  maintained controls for warmup, independent repetitions, optimizer barriers, result context,
  memory/counters, and random interleaving to reduce state drift.
- [OpenJDK JMH samples](https://github.com/openjdk/jmh/tree/master/jmh-samples/src/main/java/org/openjdk/jmh/samples) —
  maintained worked traps for dead-code elimination, blackholes, constant folding, loops, process
  forks, and run-to-run effects. The project itself warns that a harness does not remove the need to
  reason about benchmark validity.

## Load, latency, and overload

- [Open and closed models](https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/open-vs-closed/) —
  current k6 documentation showing that closed-loop iteration rate falls as responses slow and can
  omit the demand an open system would continue to receive.
- [Dropped iterations](https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/dropped-iterations/) and
  [arrival-rate allocation](https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/arrival-rate-vu-allocation/) —
  unsent work can mean insufficient generator allocation or a system whose latency consumed all
  available virtual users; dynamic allocation can itself overload and skew the generator.
- [API load testing](https://grafana.com/docs/k6/latest/testing-guides/api-load-testing/) — ties smoke,
  average, stress, spike, breakpoint, and soak shapes to different questions rather than treating one
  traffic test as universal proof.
- [HdrHistogram](https://github.com/HdrHistogram/HdrHistogram) — Gil Tene's maintained histogram
  project demonstrates coordinated omission with a system pause: a recorder that waits with the
  system observes too few bad samples, so raw percentiles describe a better experience than
  independent arrivals would encounter.
- [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/) —
  Google SRE's production guidance on queues, resource exhaustion, overload, and retry amplification.
  It supports counting retries and treating load shedding, errors, and recovery as part of capacity.

## Existing owners in this catalog

- `cpp-patterns` and `python-patterns` own runtime-specific profiling and optimization mechanics.
- `laravel-patterns`, `vue-patterns`, and `inertia-patterns` own framework-specific work removal,
  caching, rendering, and delivery traps.
- `mysql-patterns`, `postgres-patterns`, and `sqlite-patterns` own engine plans, indexes, locking,
  pools, and storage behavior.
- `rundesk-team-marketing/seo` owns field-versus-lab Core Web Vitals when search performance is the
  goal.

This package owns the shared contract: choose the right measurement, preserve experimental validity,
locate the limiting boundary, and prove that the system—not merely one isolated operation—improved.
