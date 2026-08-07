# Performance

Read this when a Vue app is slow. Profile first — Vue's guidance names the tools, and the common
guesses are usually wrong.

## Measure before changing

- **Load:** PageSpeed Insights, WebPageTest.
- **Runtime:** Chrome DevTools performance panel with `app.config.performance = true`, and the Vue
  DevTools profiler, which attributes time to components.

Vue's own caution on abstraction-removal work: "reducing only a few instances won't have noticeable
effect." Component overhead matters in large lists and nowhere else.

## Page load

- **Choose the right architecture.** "Avoid pure client-side SPAs for load-sensitive applications" —
  use SSR or SSG. For marketing pages inside an SPA, "ship them separately as static HTML with minimal
  JS."
- **Keep the build step.** Pre-compiled templates save "14kb min+gzipped" versus runtime compilation,
  and a build enables tree-shaking of unused Vue APIs.
- **Split by route.** A dynamic import per route is the single highest-value change:
  `component: () => import('@/views/Foo.vue')`.
- **Split heavy components** with `defineAsyncComponent`, and pair it with `<Suspense>` or a loading
  component. Editors, chart libraries, and date pickers are the usual candidates.
- **Prefer tree-shakeable dependencies** — `lodash-es` over `lodash`. Check the bundle rather than
  assuming; `rollup-plugin-visualizer` will show what is actually in it.

## Update performance

### Prop stability

Vue's own example. Give the child the answer, not the inputs:

```vue
<!-- ❌ every ListItem re-renders when activeId changes -->
<ListItem v-for="item in items" :id="item.id" :active-id="activeId" />

<!-- ✅ only the two items whose `active` actually changed re-render -->
<ListItem v-for="item in items" :id="item.id" :active="item.id === activeId" />
```

The same logic applies to object and array literals in templates: `:config="{ a, b }"` creates a new
object every render, so the child always sees a changed prop. Hoist it to a `computed`.

### `v-once` and `v-memo`

- **`v-once`** — "render content that relies on runtime data but never needs to update. The entire
  sub-tree will be skipped for all future updates."
- **`v-memo`** — "conditionally skip the update of large sub-trees or `v-for` lists." Give it the exact
  dependency list; a wrong list produces stale UI, which is worse than a slow one. Reach for it only
  after profiling.

### Computed stability

Since 3.4, a computed only triggers effects when its value actually changes. For computeds returning
new objects each run, return the previous value when nothing meaningful changed:

```js
const state = computed((old) => {
  const next = { isEven: count.value % 2 === 0 }
  return old && old.isEven === next.isEven ? old : next
})
```

### Reactivity overhead

For large immutable structures, make them reactive at the root only:

```js
const rows = shallowRef([/* 50,000 rows */])

rows.value.push(row)                    // does NOT trigger
rows.value = [...rows.value, row]       // triggers
```

`shallowRef` / `shallowReactive` skip deep proxying, which is where the cost is. `markRaw()` for
objects that should never be proxied at all — chart instances, map SDK handles, class instances.

VueUse's internal guideline goes further: "prefer `shallowRef` over `ref` whenever possible."

### Large lists

Virtualize past a few hundred rows — `vue-virtual-scroller` or equivalent. No amount of memoization
beats not rendering 50,000 DOM nodes.

Also avoid deep watchers over large structures: Vue warns deep watching "requires traversing all nested
properties… and can be expensive." In 3.5+, bound it with a numeric `deep`.

## The usual real causes

In rough order of how often each turns out to be the answer:

1. **An unkeyed or index-keyed `v-for`** forcing re-creation of subtrees.
2. **An unstable prop** — a fresh object or array literal every render.
3. **A deep watcher** over a large object.
4. **A computed doing real work** that runs more often than expected, often because something in it is
   not actually reactive.
5. **A giant non-virtualized list.**
6. **A dependency that should have been lazy-loaded** — an editor or chart library in the entry chunk.
7. **Everything reactive** when `shallowRef` would do.

## Vapor Mode: not yet

Vue 3.6 ships Vapor Mode — rendering without the virtual DOM, benchmarked alongside Solid and Svelte 5,
with a reactivity core refactored onto alien-signals. **3.6 is in RC, not stable.** It is 100% opt-in,
supports template-only SFCs and `<script setup>` only, and **does not support the Options API**.

The team's own framing is partial adoption: a performance-sensitive page in Vapor Mode, or a small new
app. Do not recommend it as a general answer to a performance problem, and do not plan a migration
around an RC.

## Sources

- [Performance](https://vuejs.org/guide/best-practices/performance.html) — every quoted recommendation above
- [`v-memo`](https://vuejs.org/api/built-in-directives.html#v-memo) · [`v-once`](https://vuejs.org/api/built-in-directives.html#v-once)
- [Reactivity API: advanced](https://vuejs.org/api/reactivity-advanced) — `shallowRef`, `shallowReactive`, `markRaw`
- [Watchers](https://vuejs.org/guide/essentials/watchers.html) — deep-watch cost
- [Async components](https://vuejs.org/guide/components/async.html) · [Lazy loading routes](https://router.vuejs.org/guide/advanced/lazy-loading.html)
- [VueUse guidelines](https://vueuse.org/guidelines) — `shallowRef` preference
- [vuejs/core releases](https://github.com/vuejs/core/releases) — 3.6 RC, Vapor Mode, alien-signals
