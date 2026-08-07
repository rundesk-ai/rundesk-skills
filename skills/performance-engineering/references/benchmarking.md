# Trustworthy benchmarking

Read this when comparing implementations, builds, configurations, dependencies, or a performance
regression.

## Benchmark the claim at the right boundary

Start with the complete operation. Isolate a smaller benchmark only after a profile shows that the
unit materially contributes to the outcome. A microbenchmark proves that unit under its harness; it
does not prove the application is faster.

Write the benchmark contract before code:

```text
operation | inputs and distribution | timed boundary | cold/warm state | environment
correct output | metric/unit | repetitions | comparison | decision threshold
```

Keep setup outside the timed region unless setup is part of the real operation. Include parsing,
allocation, network setup, or teardown when the user must pay it.

## Prevent the harness from measuring fiction

- Use the ecosystem's established benchmark harness. Its controls for warmup, process forks,
  optimizer barriers, timers, and repetitions exist because hand-rolled loops routinely lie.
- Consume or verify the result so compilers and runtimes cannot remove the work. Avoid constant
  inputs that let the result be folded before timing.
- Distinguish wall time from CPU time. Choose the clock that matches the contract.
- Keep realistic input sizes, shapes, hit rates, and branch distributions. Include adversarial or
  worst-relevant cases when the contract requires them.
- Separate cold and steady-state measurements. Managed runtimes, caches, allocators, filesystems,
  and hardware change behavior during warmup.

- **Bad:** time a loop once, ignore its result, and call the elapsed difference a speedup.
- **Good:** use the stack's harness, verify equivalent output, prevent elimination, separate setup,
  warm deliberately, repeat independent runs, and retain raw results.

OpenJDK JMH's maintained samples demonstrate dead-code elimination, constant folding, loop,
forking, and run-to-run traps; Google Benchmark exposes matching warmup, repetition, optimizer,
context, and random-interleaving controls.

## Compare against noise, not hope

Run the baseline and candidate under comparable conditions. When possible, randomize or interleave
their order so thermal drift, background work, and machine state do not always favor one side.

Report every independent run or retain it in the artifact. Summarize central tendency only with
variation or an uncertainty interval. Prefer an effect size with units and a relative change:
“12 ms lower, 8%, across these runs” is more useful than “1.08x faster.”

Do not discard outliers merely because they weaken the claim. Investigate whether they represent
measurement failure, periodic system behavior, or a real tail the workload encounters. State any
exclusion rule before seeing the result.

Mytkowicz et al. showed that seemingly irrelevant setup changes can reverse performance conclusions;
Kalibera and Jones model multiple sources of benchmark variation. The replacement is controlled
context, independent repetitions, order randomization, and explicit uncertainty—not one clean run.

## Guard regressions at the right level

- Keep a small benchmark when it protects a proven hotspot or capacity contract.
- Store the workload, raw baseline, environment metadata, and correctness check with the guard.
- Use dedicated or characterized runners for tight thresholds. On noisy shared CI, prefer larger
  budgets, repeated confirmation, trend detection, or a non-blocking signal.
- Rebaseline only for an explained environment or contract change. Never move the threshold solely
  to make a regression green.

Before concluding, re-run the end-to-end operation. A microbenchmark improvement that vanishes in the
real path is a valid local observation and an unsuccessful product optimization.
