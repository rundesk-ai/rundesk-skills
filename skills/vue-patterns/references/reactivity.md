# Reactivity

Read this when state does not update, updates too often, or updates at the wrong time. Almost every
"my component isn't re-rendering" bug is on this page.

## `ref` is the default

Vue's own recommendation, stated after listing the limitations: "we recommend using `ref()` as the
primary API for declaring reactive state." The community converged on the same rule — VueUse's
guidelines say "use `ref` instead of `reactive` whenever possible."

`reactive()` has three documented limitations, and each produces a silent failure:

```js
// 1. Object types only — no primitives
const n = reactive(0)                    // useless

// 2. Cannot be replaced
let state = reactive({ count: 0 })
state = reactive({ count: 1 })           // the original reference is no longer tracked

// 3. Destructuring and passing lose the connection
const { count } = state                  // a plain number from here on
someFn(state.count)                      // receives a number, tracks nothing
```

Vue on the third: "when we destructure a reactive object's primitive type property into local
variables, or when we pass that property into a function, we will lose the reactivity connection."

Use `reactive()` deliberately for a `Map` or `Set`, or a coherent object you will never reassign.
Everywhere else, `ref`.

**The escalation, in order:** `ref` → a few refs grouped in a composable → a Pinia store. Reach for
`shallowRef` only when profiling says so.

## Where reactivity gets lost

The four common ways, and the fix for each:

| Symptom | Cause | Fix |
|---|---|---|
| Store values never update | `const { a } = useStore()` | `storeToRefs(useStore())` |
| Composable return never updates | Composable returned a `reactive()` object | Return a plain object of refs |
| Prop-derived value is stale | `const x = props.value` at setup | `computed(() => props.value)` |
| Function argument is not tracked | Passed `state.count` | Pass the ref, or a getter `() => state.count` |

Vue's rule for composables: "the recommended convention is for composables to always return a plain,
non-reactive object containing multiple refs. This allows it to be destructured in components while
retaining reactivity."

## `computed` must be pure

A computed is a derived value. It must not fetch, mutate, assign to other state, push to a router, or
read a clock. `eslint-plugin-vue` ships `no-side-effects-in-computed-properties` in its **essential**
preset and calls side effects there "a very bad practice."

```js
// ❌ non-deterministic and untraceable — runs on access, caches, re-runs on invalidation
const total = computed(() => {
  analytics.track('total-viewed')        // side effect
  cart.lastSeen = Date.now()             // mutation
  return items.value.reduce(sum, 0)
})

// ✅ pure
const total = computed(() => items.value.reduce(sum, 0))
```

The failure is not theoretical: a computed runs lazily, caches, and re-runs when a dependency changes.
Anything with an effect in it therefore fires an unpredictable number of times, at times nothing in the
code suggests. Side effects belong in a watcher or an event handler.

Writable computeds exist (`get`/`set`) and are the right tool for a `v-model` bridge — that `set` is
the one legitimate write.

## `watch` vs `watchEffect`

```js
watch(source, (next, prev) => {})        // explicit source, gives you the old value
watchEffect(() => { /* deps inferred */ })
```

- **`watch` tracks only the declared source.** Vue: it "won't track anything accessed inside the
  callback." Prefer it — explicit dependencies are reviewable, and you get the previous value.
- **`watchEffect` tracks everything read during its synchronous run.** Terser, and its dependency set
  is invisible; a later edit can silently add a dependency.
- **A `reactive` property is not a valid source.** `watch(obj.count, ...)` does nothing; use a getter:
  `watch(() => obj.count, ...)`.
- **`deep: true` is expensive.** Vue: it "requires traversing all nested properties in the watched
  object, and can be expensive when used on large data structures." Watching a `reactive` object
  directly is implicitly deep. In 3.5+, `deep` accepts a number to bound the traversal.

Prefer a `computed` over a watcher whenever the goal is a derived value. Reach for a watcher only for
genuine effects: fetching, persisting, imperative DOM work, syncing to something outside Vue.

## Flush timing

| Timing | When | Use for |
|---|---|---|
| `pre` (default) | Before the component's DOM update | Almost everything |
| `post` | After the DOM update | Reading measurements or focusing an element |
| `sync` | Immediately on mutation, unbatched | Almost nothing |

Vue's caution on `sync`: it does "not have batching and triggers every time a reactive mutation is
detected. It's ok to use them to watch simple boolean values, but avoid using them on data sources
that might be synchronously mutated many times, e.g. arrays."

## Cleanup and the memory leak

**A watcher created asynchronously is never stopped.** This is the documented leak:

```js
// ✅ bound to the component, stops on unmount
watchEffect(() => {})

// ❌ not bound — leaks
setTimeout(() => { watchEffect(() => {}) }, 100)
```

Vue: "the watcher must be created **synchronously**: if the watcher is created in an async callback,
it won't be bound to the owner component and must be stopped manually to avoid memory leaks." The fix
is to make the watcher conditional rather than deferred:

```js
watchEffect(() => { if (data.value) { /* ... */ } })
```

Cancel in-flight work when the source changes again, or a slow earlier response overwrites a newer one:

```js
watch(id, (newId) => {
  const controller = new AbortController()
  fetch(`/api/${newId}`, { signal: controller.signal })
  onWatcherCleanup(() => controller.abort())     // 3.5+
})
```

`onWatcherCleanup` "must be called during the synchronous execution" of the callback — not after an
`await`. Use the positional `onCleanup` argument if you need it there.

Everything else you create by hand — `addEventListener`, `setInterval`, `IntersectionObserver`, a
WebSocket, a third-party widget — must be torn down in `onUnmounted`. Community write-ups of real Vue
memory leaks converge on this single cause: "a single un-cleaned interval, event listener, or promise
chain can add up to megabytes of retained memory," accumulating across route navigations.

## Performance-shaped reactivity

- `shallowRef` / `shallowReactive` for large immutable structures — reactive at the root only. Replace
  the value rather than mutating into it.
- `readonly()` for state handed to a subtree that must not write it.
- `toValue(x)` normalizes a ref, a getter, or a plain value — the standard way to accept all three.
- `markRaw()` for a big non-reactive object, such as a chart instance or a map SDK handle, so Vue does
  not proxy it.

## Sources

- [Reactivity fundamentals](https://vuejs.org/guide/essentials/reactivity-fundamentals.html) — the `reactive()` limitations and the `ref()` recommendation
- [Watchers](https://vuejs.org/guide/essentials/watchers.html) — sources, deep cost, flush timing, cleanup, and the async-creation leak warning
- [Computed properties](https://vuejs.org/guide/essentials/computed.html) · [Reactivity in depth](https://vuejs.org/guide/extras/reactivity-in-depth)
- [`vue/no-side-effects-in-computed-properties`](https://eslint.vuejs.org/rules/no-side-effects-in-computed-properties) — essential preset
- [VueUse guidelines](https://vueuse.org/guidelines) — "use `ref` instead of `reactive` whenever possible", `shallowRef` preference
- [Ref vs. reactive — which is best?](https://michaelnthiessen.com/ref-vs-reactive) — Michael Thiessen's escalation rule of thumb
- [The hidden reason your Vue watchers leak memory](https://www.bryceandy.com/posts/the-hidden-reason-your-vue-watchers-leak-memory-and-how-to-avoid-it)
