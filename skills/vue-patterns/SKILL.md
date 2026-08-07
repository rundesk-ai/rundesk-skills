---
name: vue-patterns
description: Use this skill when the user asks to build, review, debug, refactor, or advise on a Vue 3 or Nuxt application — components and their props, events and slots, reactivity, composables, Pinia stores, Vue Router, separation of concerns, rendering performance, SSR and hydration, or component testing. It supplies version-accurate rules, the failure each convention prevents, and the patterns that keep rendering predictable. Do not use it for Vue 2 maintenance, or for a non-Vue project merely because it uses Vite.
---

# Vue and Nuxt patterns

Write components whose output is a function of their inputs. Most Vue bugs that survive review are a
lost reactivity connection, a hidden side effect, or a component reaching outside itself.

## Establish the versions before advising

```sh
npm ls vue pinia vue-router nuxt 2>/dev/null
cat package.json | grep -E '"(vue|pinia|vue-router|nuxt|vite)"'
```

Current as of **August 2026**:

| Package | Current | Note |
|---|---|---|
| `vue` | **3.5.41** | 3.6 is in **RC**, not stable — Vapor Mode and the alien-signals reactivity refactor land there |
| `pinia` | **4.0.2** | v4 is ESM-only and needs `@vue/devtools-api` installed alongside it |
| `vue-router` | **5.2.0** | v5 is a "boring" release — **no breaking API changes from v4**; typed routes are now first-party |
| `nuxt` | **4.5.2** | |
| `vite` | **8.2.1** | |

Two corrections worth making unprompted: advice written for **Pinia 2** or **Vue Router 4** is mostly
still correct but names an old major, and **Vapor Mode is not stable** — do not recommend building on
it, and note that it does not support the Options API at all.

## Work in this order

1. **Read the component before changing it**, including its template. Vue behaviour is decided by the
   template and the script together.
2. **Fix reactivity before structure.** A lost `ref` connection is a bug; a component that could be
   split is a preference.
3. **Keep the render a pure function of state.** Everything below follows from this.
4. **Put logic where it can be tested without mounting** — a composable or a plain function.
5. **Test what the component does, not how.** Vue's own guidance: "Test what a component does, not how
   it does it."

## Rules that always hold

- **`ref()` is the default.** Vue's own recommendation, "due to these limitations" — `reactive()`
  cannot hold primitives, cannot be reassigned, and loses reactivity on destructure.
- **Never mutate a prop.** Props are a one-way-down binding. Emit an event and let the owner change
  its own state.
- **`computed` must be pure.** No fetching, no mutation, no `Date.now()`. A computed with a side
  effect runs at times nobody predicts and is the hardest class of Vue bug to trace.
- **Always key a `v-for`**, with a stable identity — never the array index for a list that reorders,
  filters, or has stateful children.
- **Never put `v-if` and `v-for` on the same element.** `v-if` evaluates first, so the loop variable
  does not exist yet. Filter in a computed.
- **Composables are called synchronously in `setup()` or `<script setup>`.** Anywhere else and the
  watcher is not bound to the component, so it never stops — a documented memory leak.
- **Clean up every effect you create.** Listeners, timers, observers, and subscriptions in
  `onUnmounted`; in-flight requests with `onWatcherCleanup`.
- **Browser globals only after mount.** `window` and `document` do not exist during SSR, and
  `onMounted` never runs there.

## Read the reference the task needs

| Area | Read for |
|---|---|
| [Components](references/components.md) | SFC shape, props and emits, `v-model`, slots, provide/inject, naming |
| [Reactivity](references/reactivity.md) | `ref` vs `reactive`, computed, `watch` vs `watchEffect`, flush timing, cleanup |
| [Composables](references/composables.md) | Conventions, `toValue`, return shape, side effects, call-site rules |
| [Separation of concerns](references/separation-of-concerns.md) | Where logic belongs, and the patterns that keep rendering deterministic |
| [State and routing](references/state-and-routing.md) | Pinia 4, Vue Router 5, and choosing between local state, a composable, and a store |
| [Performance](references/performance.md) | Prop stability, `v-once`, `v-memo`, `shallowRef`, virtualization, code splitting |
| [SSR and Nuxt](references/ssr-and-nuxt.md) | Hydration mismatches, cross-request state pollution, Nuxt data fetching |
| [Testing](references/testing.md) | What to assert, what never to assert, and the tooling |
| [Anti-patterns](references/anti-patterns.md) | The consolidated do / don't list, with the failure each prevents |
| [Sources](references/sources.md) | The citation basis, to audit or update any claim above |

## Review output shape

```text
[HIGH] Reactivity lost by destructuring a reactive() store
Location: src/components/CartSummary.vue:14
Evidence: const { items, total } = useCartStore() — plain properties, not refs.
Why: destructuring a reactive object disconnects the properties; the template renders the values
     captured at setup and never updates again.
Fix: const { items, total } = storeToRefs(useCartStore())
Check: mount, mutate the store, assert the rendered total changes.
```

Say which findings are bugs and which are preferences. Vue's style guide is explicit that only
Priority A rules are error prevention; the rest are readability and consistency.
