# Vue and Nuxt source basis

This package is a Rundesk synthesis of the Vue, Pinia, Vue Router and Nuxt documentation, the lint
rules the ecosystem enforces, and a set of practitioner sources. Use this file to audit or update any
claim.

**Read in this order of authority.** Framework documentation states the rules; `eslint-plugin-vue`
encodes which of them the ecosystem actually enforces; practitioner sources carry the conventions and
judgement the docs leave open. Vue's style guide is explicit that only **Priority A** rules are error
prevention — do not present a Priority B or C preference as a defect.

Verified in **August 2026**. Vue 3.6, Pinia 4, Vue Router 5 and Nuxt 4 all moved within the preceding
twelve months, so anything checked against an older copy of these docs is suspect.

## Versions, verified against the npm registry on 7 August 2026

| Package | Latest | Published |
|---|---|---|
| `vue` | 3.5.41 | 2026-08-05 |
| `vue` (rc) | 3.6.0-rc.2 | 2026-07-22 |
| `pinia` | 4.0.2 | 2026-07-15 |
| `vue-router` | 5.2.0 | 2026-07-15 |
| `nuxt` | 4.5.2 | 2026-08-05 |
| `vite` | 8.2.1 | 2026-08-06 |
| `@vue/test-utils` | 2.4.11 | 2026-06-04 |

Re-check with `curl -sS https://registry.npmjs.org/<pkg> | jq '.["dist-tags"]'` rather than trusting
this table. It is a snapshot.

- [vuejs/core releases](https://github.com/vuejs/core/releases) — 3.6 RC status, Vapor Mode feature
  completeness, the alien-signals reactivity refactor, and that Vapor supports template-only SFCs and
  `<script setup>` but **not** the Options API.
- [Vue releases policy](https://vuejs.org/about/releases) — cadence and pre-release meaning.
- [Pinia v4.0.0](https://github.com/vuejs/pinia/releases/tag/v4.0.0) — ESM-only, `@vue/devtools-api`
  must be installed alongside, Nostics error refactor. "Only technically breaking changes."
- [Vue Router v5.0.0](https://github.com/vuejs/router/releases/tag/v5.0.0) — a "boring" release with no
  breaking core-API changes; merges `unplugin-vue-router` (typed routes) into core; the IIFE build no
  longer bundles `@vue/devtools-api`.
- [Announcing Nuxt 4.0](https://nuxt.com/blog/v4) · [Nuxt 4 upgrade guide](https://nuxt.com/docs/4.x/getting-started/upgrade) —
  `~` pointing at `app/`, data freed on unmount, `getCachedData` changes, ref/getter keys.

## Vue core documentation

- [Reactivity fundamentals](https://vuejs.org/guide/essentials/reactivity-fundamentals.html): the three
  `reactive()` limitations, quoted, and "we recommend using `ref()` as the primary API for declaring
  reactive state."
- [Watchers](https://vuejs.org/guide/essentials/watchers.html): `watch` vs `watchEffect` tracking, valid
  sources, the deep-watch cost warning, flush timing including the `sync` caution, `once`,
  `onWatcherCleanup` and its synchronous-call constraint, and **the async-creation memory leak
  warning**.
- [Computed properties](https://vuejs.org/guide/essentials/computed.html) · [Reactivity in depth](https://vuejs.org/guide/extras/reactivity-in-depth) · [Reactivity API: advanced](https://vuejs.org/api/reactivity-advanced)
- [Props](https://vuejs.org/guide/components/props.html): one-way data flow, the readonly warning, the
  two legitimate reasons to want mutation and their alternatives, and the object/array caveat —
  "unreasonably expensive for Vue to prevent such mutations."
- [Events](https://vuejs.org/guide/components/events.html) · [v-model](https://vuejs.org/guide/components/v-model.html) · [Slots](https://vuejs.org/guide/components/slots.html) · [provide / inject](https://vuejs.org/guide/components/provide-inject.html) · [Async components](https://vuejs.org/guide/components/async.html)
- [Composables](https://vuejs.org/guide/reusability/composables.html): naming, `toValue` for
  ref/getter/value arguments, the plain-object-of-refs return convention, SSR-safe side effects,
  cleanup in `onUnmounted`, and **the synchronous call-site restriction and why it exists**.
- [Performance](https://vuejs.org/guide/best-practices/performance.html): profiling tools, the 14kb
  pre-compiled-template figure, prop stability with Vue's own `ListItem` example, `v-once`, `v-memo`,
  computed stability since 3.4, `shallowRef` for large immutable structures, virtualization, and the
  caution that removing a few component abstractions "won't have noticeable effect."
- [Server-side rendering](https://vuejs.org/guide/scaling-up/ssr.html): the three hydration-mismatch
  causes, **cross-request state pollution** and the per-request app instance fix, which lifecycle hooks
  run on the server, and the uncleaned-`created`-side-effect gotcha.
- [Testing](https://vuejs.org/guide/scaling-up/testing.html): "test what a component does, not how it
  does it," the prohibition on asserting private state and methods, the snapshot caution, the
  extract-to-a-utility advice, and the Vitest recommendation.
- [State management](https://vuejs.org/guide/scaling-up/state-management.html) · [`useId()`](https://vuejs.org/api/composition-api-helpers.html#useid)

## Style guide

- [Priority A: Essential](https://vuejs.org/style-guide/rules-essential) — multi-word component names,
  detailed prop definitions, keyed `v-for`, avoiding `v-if` with `v-for`, component-scoped styling, each
  with the failure it prevents.
- [Priority B: Strongly recommended](https://vuejs.org/style-guide/rules-strongly-recommended) — file
  and name casing, base-component prefixes, tightly-coupled naming, word order, self-closing
  components, prop name casing, simple template expressions, directive shorthand consistency.
- [Priority D: Use with caution](https://vuejs.org/style-guide/rules-use-with-caution) — element
  selectors with `scoped` and their performance cost, and implicit parent-child communication.

## The enforced subset

`eslint-plugin-vue` is where the ecosystem records which rules are worth failing a build over. The
*essential* preset contains the Priority A rules as lint.

- [Available rules](https://eslint.vuejs.org/rules/)
- [`vue/no-mutating-props`](https://eslint.vuejs.org/rules/no-mutating-props)
- [`vue/no-side-effects-in-computed-properties`](https://eslint.vuejs.org/rules/no-side-effects-in-computed-properties) —
  "it is considered a very bad practice to introduce side effects inside computed properties"
- [`vue/require-v-for-key`](https://eslint.vuejs.org/rules/require-v-for-key.html)

## Ecosystem documentation

- [Pinia](https://pinia.vuejs.org/) · [Dealing with composables](https://pinia.vuejs.org/cookbook/composables.html) · [Composing stores](https://pinia.vuejs.org/cookbook/composing-stores.html) · [Testing stores](https://pinia.vuejs.org/cookbook/testing.html)
- [Vue Router](https://router.vuejs.org/) · [Lazy loading routes](https://router.vuejs.org/guide/advanced/lazy-loading.html)
- [Nuxt: data fetching](https://nuxt.com/docs/4.x/getting-started/data-fetching) — the double-fetch
  warning, `$fetch` vs `useFetch` vs `useAsyncData`, key derivation and which options must match across
  shared keys, `transform`/`pick`/`lazy`/`server`/`watch`.
- [Nuxt: runtime config](https://nuxt.com/docs/4.x/guide/going-further/runtime-config)
- [Vue Test Utils](https://test-utils.vuejs.org/) · [Vitest](https://vitest.dev/)

## Practitioner sources

Conventions and judgement, cited where the docs deliberately do not decide.

- [Composable Vue](https://antfu.me/posts/composable-vue-vueday-2021) — **Anthony Fu**, Vue core team.
  The community reference for composable design: `MaybeRef` arguments, "think your functions like
  LEGO," object-of-refs returns, self-cleaning side effects, typed `InjectionKey` provide/inject,
  `useVModel`, and the SSR-safe `createXxx` + provide pattern for shared state.
- [VueUse guidelines](https://vueuse.org/guidelines) — the largest composable library's internal rules:
  "use `ref` instead of `reactive` whenever possible," "prefer `shallowRef` over `ref` whenever
  possible," options objects for extensibility, configurable `immediate`/`flush`, `isSupported` flags,
  `configurableWindow` for SSR and testing, `tryOnScopeDispose` for cleanup.
- [Ref vs. reactive — which is best?](https://michaelnthiessen.com/ref-vs-reactive) — **Michael
  Thiessen**. The escalation rule of thumb, and the `.value` inconsistency argument.
- [Debugging guide: why your Vue component isn't updating](https://michaelnthiessen.com/debugging-guide-why-your-component-isnt-updating)
- [Top 5 mistakes to avoid when using Pinia](https://masteringpinia.com/blog/top-5-mistakes-to-avoid-when-using-pinia) ·
  [My top 5 tips for using Pinia](https://masteringpinia.com/blog/my-top-5-tips-for-using-pinia) —
  **Eduardo San Martin Morote**, author of Pinia and Vue Router.
- [Composables vs. provide/inject vs. Pinia — when to use what](https://vueschool.io/articles/vuejs-tutorials/composables-vs-provide-inject-vs-pinia-when-to-use-what/) —
  Vue School. The scope-escalation guidance, and the SSR argument for Pinia over module-level shared
  state.
- [Good practices and design patterns for Vue composables](https://dev.to/jacobandrewsky/good-practices-and-design-patterns-for-vue-composables-24lk)
- [The hidden reason your Vue watchers leak memory](https://www.bryceandy.com/posts/the-hidden-reason-your-vue-watchers-leak-memory-and-how-to-avoid-it) —
  the async-watcher leak from the field rather than the spec.
- [How to fix memory leaks in Vue](https://coreui.io/answers/how-to-fix-memory-leaks-in-vue/) — the
  practical teardown checklist; community write-ups converge on uncleaned intervals, listeners, and
  promise chains accumulating across route navigations.

## About the code examples

Examples in this package are one of two things, and the text says which:

- **Lifted from the source** — the framework's own documented example, or a worked case from a cited
  article. These are marked inline, because "this is how the maintainers show it" is stronger evidence
  than anything a skill can assert.
- **Synthesised to isolate one failure** — written here to show a specific trap with nothing else in
  the frame. These are the package's own judgement, and the surrounding prose gives the mechanism so a
  reader can evaluate rather than trust.

Every ✅/❌ pair states the failure the ❌ produces. An example that only says "prefer this" is not
worth the space.

**Examples are version-gated where the behaviour is.** Where a pattern only works above a floor, or
behaved differently below it, the text says so — silently correct-looking code that misbehaves on an
older version is worse than no example.

JavaScript examples in this package were syntax-checked with `node --check`, each ✅ and ❌ variant
independently.

## What this package deliberately does not cite

- Vue 2 and Options API material, except where naming a migration.
- Tutorials predating Pinia 4, Vue Router 5, or Nuxt 4 without saying so. Most stale Vue advice online
  is version drift, not error.
- Folder-structure opinions presented as requirements. Vue mandates no structure; where this package
  takes a position it says so and gives the failure it prevents.
- Benchmark posts without a published method, and Vapor Mode performance claims applied to stable Vue.
