# Anti-patterns

Read this when reviewing Vue code. Each row names the failure, not just the rule.

Vue's style guide is explicit that only **Priority A** rules are error prevention; B, C, and D are
readability, consistency, and risk. Report them differently.

## Reactivity

| Don't | Do | Because |
|---|---|---|
| `reactive()` by default | `ref()` | Vue's own recommendation. `reactive` cannot hold primitives, cannot be reassigned, and dies on destructure |
| `const { a } = useStore()` | `storeToRefs(useStore())` | Destructuring a reactive object disconnects it; the value freezes at setup |
| Return a `reactive()` object from a composable | Return a plain object of refs | Same reason, one layer out — every consumer that destructures gets dead values |
| `watch(obj.count, cb)` | `watch(() => obj.count, cb)` | A reactive property is not a valid watch source; it silently never fires |
| Side effects in `computed` | A watcher or an event handler | `eslint-plugin-vue` essential rule; computeds run lazily and cache, so effects fire unpredictably |
| `deep: true` on a large object | Watch the specific getter, or bound `deep` with a number | "Can be expensive… beware of the performance implications" |
| `flush: 'sync'` on arrays | Default `pre` | Unbatched — fires on every mutation in a loop |
| Create a watcher in `setTimeout` / a callback | Create it synchronously, make the logic conditional | Not bound to the component, so it never stops — a documented memory leak |
| `toValue()` once at the top of a composable | `toValue()` inside the effect | Read once outside a tracking scope, it tracks nothing |

## Components

| Don't | Do | Because |
|---|---|---|
| Mutate a prop | Emit an event | One-way data flow; `no-mutating-props` is an essential lint rule |
| Mutate an object prop's contents | Emit and let the owner mutate | Vue cannot prevent it — "the child should emit an event to let the parent perform the mutation" |
| `v-for` without `:key` | Key by stable identity | Vue makes "the cheapest DOM mutations": lost component state, lost focus, broken transitions |
| Key by array index on a reorderable list | Key by id | The index is not an identity; rows swap state |
| `v-if` and `v-for` on one element | Filter in a computed | `v-if` evaluates first, so the loop variable does not exist — a runtime error |
| Single-word component names | `TodoItem` | Priority A: collides with current and future HTML elements |
| `this.$parent`, or reading a child's internals via a ref | Props down, events up | Priority D: tightly coupled, unclear state flow |
| Unscoped component styles | `scoped`, CSS Modules, or BEM | Priority A: style leakage in both directions |
| Element selectors inside `scoped` | Class selectors | `button[data-v-x]` is "considerably slower" than `.btn[data-v-x]` |
| A tenth `showX` boolean prop | A slot | The component is asking to be composed, not configured |
| Bare `defineProps(['a','b'])` in real code | Typed or validated definitions | Priority A: no documentation, no dev warnings |

## Structure

| Don't | Do | Because |
|---|---|---|
| Fetch, transform, and validate inside a component | API layer, `utils/`, composable | None of it is testable without mounting, or reusable at all |
| A `use*` function that touches no reactivity | A plain function in `utils/` | It needs a component context it does not use, and is harder to test |
| Module-level `ref` as shared state | Pinia, or app-scoped provide | On the server the module is shared across requests — one user's state leaks to another |
| `provide`/`inject` as a general store | Pinia | Invisible coupling at a distance, no devtools, no clear ownership |
| A store per component | Local state | A store used once is that component's state with extra steps |
| Non-serializable values in store state | Keep them outside, or `markRaw` | Breaks devtools, SSR serialization, and hydration |
| Shared code importing from a feature | Dependencies point inward | The circularity that makes the codebase unsplittable later |

## SSR

| Don't | Do | Because |
|---|---|---|
| `window` / `localStorage` in setup | Access in `onMounted` | They do not exist on the server |
| `Date.now()`, `Math.random()` in render | Client-only, seeded, or `useId()` | Documented hydration-mismatch causes |
| Timezone-dependent formatting in render | Format in `onMounted` | The server's zone is not the user's |
| A side effect in `created` | `onMounted` | Unmount hooks never run on the server, so it is never cleaned up |
| Ignore a hydration warning | Fix the cause | Vue recovers "at a performance loss," on every page load, forever |
| `$fetch` bare in a Nuxt `setup` | `useFetch` / `useAsyncData` | Fetches twice — once on the server, once on hydration |
| A secret outside `runtimeConfig.public` read by a component | Server route | Anything a component reads is in the client bundle |

## Performance

| Don't | Do | Because |
|---|---|---|
| `:config="{ a, b }"` in a template | Hoist to a `computed` | A new object every render, so the child always sees a changed prop |
| Pass `:active-id` to every row | Pass `:active="item.id === activeId"` | Vue's own example: otherwise every row re-renders |
| Render 50,000 rows | Virtualize | No memoization beats not rendering them |
| Deep-proxy a large immutable structure | `shallowRef` / `markRaw` | The proxying is the cost |
| Reach for `v-memo` first | Profile first | A wrong dependency list produces stale UI — worse than slow UI |
| Plan on Vapor Mode | Wait for stable | 3.6 is RC; Vapor does not support the Options API |

## Advice-giving

- **Read the versions first.** Pinia 4 and Vue Router 5 are current; Vue 3.6 is **not** stable. Advice
  naming Pinia 2 or Router 4 is usually still correct but dated, and Vapor Mode advice is premature.
- **Separate bugs from preferences.** Priority A violations are bugs. Naming and ordering are not.
- **Do not recommend a library for what the framework does.** `defineModel`, `useTemplateRef`,
  `useId`, and `onWatcherCleanup` all replaced common userland helpers.
- **Do not report a fix as verified without running it.** A reactivity bug that "should" be fixed
  usually is not.

## Sources

Every quoted line is cited in [`sources.md`](sources.md). The densest sources are the
[Vue style guide](https://vuejs.org/style-guide/),
[reactivity fundamentals](https://vuejs.org/guide/essentials/reactivity-fundamentals.html),
[watchers](https://vuejs.org/guide/essentials/watchers.html),
[SSR](https://vuejs.org/guide/scaling-up/ssr.html), and the
[`eslint-plugin-vue` essential rules](https://eslint.vuejs.org/rules/).
