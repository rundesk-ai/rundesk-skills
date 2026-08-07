# Separation of concerns, and a deterministic codebase

Read this when a component has grown, when logic is hard to test, or when the UI behaves differently
between runs, between users, or between server and client.

## The rule

**Components render. Composables hold stateful logic. Plain functions hold pure logic. Stores hold
shared state.**

A component's job is to turn state into markup and turn user events into calls. When it also fetches,
transforms, validates, persists, and coordinates, none of that is reachable by anything except a
mounted component — so it can only be tested by mounting, and only reused by copying.

The test:

> Could this logic be tested without mounting a component, and reused by a second component that looks
> nothing like this one?

If not, it is in the wrong place.

## What each layer owns

| Layer | Owns | Never |
|---|---|---|
| **Component** | Template, local UI state, wiring events to calls | Business rules, data fetching logic, cross-component state |
| **Composable** | Stateful reusable logic, effects and their cleanup | Markup, knowledge of one specific component |
| **Plain function** (`utils/`) | Pure transformation, formatting, validation | Reactivity, lifecycle, anything needing a component instance |
| **Store (Pinia)** | Shared cross-component state and the actions that change it | Component-local concerns, DOM access |
| **API layer** (`api/`) | HTTP calls, request/response shape | Vue reactivity, deciding what the UI does with errors |

Two things fall out of that table:

- **A composable that never touches a ref should be a plain function.** It is easier to test and does
  not need a component context.
- **An API call belongs behind a function, not inline in a component.** `fetch('/api/users')` in a
  component makes the endpoint untestable and unmockable everywhere it appears.

## The refactor

```vue
<!-- ❌ One component doing five jobs -->
<script setup>
const users = ref([])
const loading = ref(false)
const query = ref('')

watch(query, async (q) => {
  loading.value = true
  const res = await fetch(`/api/users?q=${q}`)      // API layer
  const json = await res.json()
  users.value = json.data                            // no error handling, no cancellation
    .filter(u => u.active)                           // business rule
    .map(u => ({ ...u, label: `${u.first} ${u.last}`.trim() }))   // formatting
  loading.value = false
})
</script>
```

```vue
<!-- ✅ The component wires things together -->
<script setup>
const query = ref('')
const { results, loading, error } = useUserSearch(query)   // stateful logic
</script>
```

```ts
// api/users.ts — the transport
export const searchUsers = (q: string, signal?: AbortSignal) =>
  http.get<User[]>('/api/users', { params: { q }, signal })

// utils/users.ts — pure, testable with no Vue at all
export const activeOnly = (users: User[]) => users.filter(u => u.active)
export const displayName = (u: User) => `${u.first} ${u.last}`.trim()

// composables/useUserSearch.ts — reactivity, effects, cleanup
```

Each piece is now independently testable, and `displayName` is a two-line unit test rather than a
mounted component.

## What makes rendering deterministic

Deterministic means: **the same state produces the same output, every time, on the server and in the
browser.** These are the practices that hold that property, and each has a failure attached.

### 1. The render is a pure function of state

No side effects in `computed` — `eslint-plugin-vue` treats this as *essential*, and calls it "a very
bad practice." No mutation inside a template expression. No writing to state during render.

A computed runs lazily, caches, and re-runs on invalidation. Anything with an effect inside therefore
fires an unpredictable number of times at times nothing in the code suggests.

### 2. No non-deterministic values in render output

`Date.now()`, `new Date()`, `Math.random()`, and `crypto.randomUUID()` in a render path produce
different output on the server and the client. Vue documents both cases as hydration-mismatch causes,
along with the fix: render them client-only in `onMounted`, or use a seeded generator, or `useId()` for
stable ids.

Timezone formatting is the same bug wearing a different hat — the server's zone is not the user's.

### 3. Stable identity in lists

Always key `v-for`, and key it with something stable. Without a key Vue makes "the cheapest DOM
mutations," which destroys component state, breaks focus, and breaks transitions. The array index is
not a stable identity for anything that reorders, filters, or holds state.

### 4. One-way data flow

Props down, events up. Never mutate a prop; never mutate the contents of an object prop. When data can
be changed from two directions, no single place explains the current value.

### 5. No reaching outside the component

Vue's Priority D rule names `this.$parent` and prop mutation as producing components that are "tightly
coupled" and whose state flow is unclear. The same applies to reading a child's internals through a
template ref, and to mutating DOM that Vue owns — Vue will overwrite it on the next patch, at a moment
you cannot predict.

### 6. No ambient mutable state

Module-level `ref`s are global singletons. In the browser they survive route changes and tests; on the
server they are **shared between users**, which is Vue's documented cross-request state pollution. Put
shared state in a store or an app-scoped provide.

### 7. Explicit dependencies

Prefer `watch(source, cb)` over `watchEffect`. Vue notes `watch` "only tracks the explicitly watched
source," which means the trigger set is visible in review and cannot silently grow when somebody adds a
read inside the callback.

### 8. Effects are declared and cleaned up

Every listener, timer, observer, subscription, and in-flight request has a matching teardown. An effect
that outlives its component changes state that no longer has anything to render — and the symptom
appears in a different component, later.

### 9. Async results are ordered

Two requests can return out of order, so the slower earlier one overwrites the newer. Cancel with
`onWatcherCleanup` and an `AbortController`, or discard responses that are no longer current.

## Project structure

Structure by feature once the app has more than a handful of screens; group by type only inside a
feature.

```text
src/
├── components/            shared, presentational, no feature knowledge
├── composables/           shared stateful logic
├── utils/                 pure functions
├── api/                   transport
├── stores/                Pinia
└── features/
    └── checkout/
        ├── components/
        ├── composables/
        └── api.ts
```

The rule that matters is not the shape but the direction: **shared code must not import from a
feature.** A `components/` file importing `features/checkout` is the circularity that makes a codebase
impossible to split later.

Presentational components take props and emit events and know nothing about stores or routes; container
components own the data and pass it down. This is what makes a component reusable and testable — a
component that reads a store directly can only be tested with that store.

## The honest caveat

None of this is enforced by Vue, and a small app does not need an `api/` layer or a store. The rules
earn their keep when **a piece of logic has more than one caller, more than one step, or an effect that
can fail**. Apply them there, and say plainly when a component is small enough not to need it.

Vue's own style guide is explicit about the split: only Priority A rules are error prevention. Report
Priority A violations as bugs and the rest as preferences.

## Sources

- [Style guide — Priority A](https://vuejs.org/style-guide/rules-essential) — keyed `v-for`, no `v-if` with `v-for`, scoped styles, detailed props
- [Style guide — Priority D](https://vuejs.org/style-guide/rules-use-with-caution) — implicit parent-child communication
- [Props: one-way data flow](https://vuejs.org/guide/components/props.html)
- [`vue/no-side-effects-in-computed-properties`](https://eslint.vuejs.org/rules/no-side-effects-in-computed-properties) · [`vue/no-mutating-props`](https://eslint.vuejs.org/rules/no-mutating-props)
- [SSR: hydration mismatches and cross-request state pollution](https://vuejs.org/guide/scaling-up/ssr.html)
- [Watchers](https://vuejs.org/guide/essentials/watchers.html) — explicit sources, cleanup
- [Composables](https://vuejs.org/guide/reusability/composables.html)
- [Composable Vue](https://antfu.me/posts/composable-vue-vueday-2021) — Anthony Fu on composition and SSR-safe shared state
- [Composables vs. provide/inject vs. Pinia — when to use what](https://vueschool.io/articles/vuejs-tutorials/composables-vs-provide-inject-vs-pinia-when-to-use-what/) — Vue School
