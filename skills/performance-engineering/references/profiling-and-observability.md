# Profiling and observability

Read this when the system is slow but the limiting boundary is not yet proven.

## Start with the user-visible path

Measure the operation at the boundary its user experiences. Then correlate the same time window and
request class across service, dependency, resource, and code evidence.

| Observation | First discriminating evidence | Common wrong turn |
|---|---|---|
| Latency rises with traffic | queue depth, pool wait, saturation, errors | resize CPU from utilization alone |
| Wall time rises; CPU stays low | off-CPU wait, dependency spans, lock/I/O timing | CPU micro-optimization |
| CPU rises on the failing path | per-core/worker load, then a sampling profile with symbols | rewrite the function named by one stack sample |
| Memory rises across repeated lifecycles | allocations and retained objects at matched checkpoints | call any high-water mark a leak |
| Periodic spikes | time-correlated GC, compaction, checkpoint, rotation, or batch evidence | average the spike away |
| Only one tenant/input is slow | segment by bounded workload attributes | optimize the global median |

Google SRE's service view is latency, traffic, errors, and saturation. Brendan Gregg's resource view
is utilization, saturation, and errors for each resource. Use both: service signals show the broken
outcome; resource signals narrow why it broke.

## Profile the time that actually elapsed

- Use a sampling CPU profiler for on-CPU cost. Preserve symbols and the optimized build used by the
  failing workload.
- Use wall-time traces, off-CPU profiling, dependency spans, and queue/lock/I/O evidence when threads
  are waiting. CPU samples cannot account for time they did not run.
- Use allocation profiles to find allocation rate; use heap/retention evidence at comparable
  lifecycle points to diagnose growth. A large cache or temporary high-water mark is not necessarily
  retained leakage.
- Correlate a hotspot with the failing operation before changing it. Profile width identifies where
  samples accumulated, not whether deleting that work preserves behavior.

- **Bad:** “CPU is only 20%, so the service is not saturated.”
- **Good:** inspect per-resource utilization, queued work, and errors; then trace wall time to the
  pool, lock, I/O, or dependency where the request waited.

This pair is grounded in the USE method and off-CPU analysis mapped in `sources.md`.
An aggregate can also hide one saturated core, worker, instance, shard, tenant, or operation class;
segment the resource and workload before declaring spare capacity.

## Keep telemetry trustworthy

- Record success and failure latency separately. Fast failures can make combined latency look good.
- Preserve distributions or histograms. An average cannot reveal which fraction of requests missed
  the target.
- Bound metric dimensions. Raw user IDs, request IDs, or unnormalized URLs create one time series per
  value and can exhaust the telemetry system.
- Keep clocks, sampling, aggregation, and retention visible when comparing traces and metrics.
- Measure instrumentation overhead on the target workload. Added logging, tracing, query collection,
  or debug extensions can perturb the result.

Use metrics to find when and where a class of work degrades, traces to follow one path across
boundaries, profiles to attribute resource time, and logs for discrete context. Collecting all four
without a question produces more data, not necessarily an explanation.

## Finish with a causal statement

Distinguish:

- **symptom:** the contract that missed;
- **mechanism:** where time or resources accumulated;
- **root condition:** the input, demand, state, or design that created that mechanism; and
- **proof:** the controlled change and repeated evidence that removed it.

“The database was slow” is not a cause. “At the failing arrival rate, all pool slots were occupied by
one unbounded query shape; requests queued at the pool, and bounding that query removed the queue
while preserving result and error counts” is testable.
