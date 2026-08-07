# State and routing

Read this when choosing where state lives, or when working with Pinia or Vue Router.

## Choosing the scope

Escalate only when the current level stops working. The community consensus is consistent on this:
"when in doubt, start with a ref. You can always promote it later. The real mistake isn't picking the
wrong abstraction on the first try — it's reaching for a complex one before you need it."

| Need | Use |
|---|---|
| State one component owns | `ref` / `reactive` in that component |
| A parent coordinating a few children | Props down, events up |
| Logic reused across unrelated components | A composable |
| Context for a subtree — theme, form, design-system config | `provide` / `inject` with a typed key |
| Shared across routes, needs devtools and SSR safety | A Pinia store |
| Server data — cached, refetched, invalidated | A query library, or Nuxt's `useAsyncData` |

Two boundaries worth stating plainly:

- **A composable is not shared state.** Each call creates its own state unless you deliberately hoist
  it, and hoisting it to module scope is the SSR bug in [`composables.md`](composables.md).
- **Server data is not application state.** URL-keyed, cached, refetchable data belongs in something
  built for it, not in a store you invalidate by hand.

## Pinia 4

Current is **4.0.2**. The v4 breaking changes are technical rather than API-level: the package is
**ESM-only**, and **`@vue/devtools-api` must now be installed alongside Pinia**. Store code written for
Pinia 2 or 3 largely does not change.

Prefer setup stores — same syntax as a composable, better typing, and composables work inside them:

```ts
export const useCartStore = defineStore('cart', () => {
  const items = ref<CartItem[]>([])

  const total = computed(() => items.value.reduce((n, i) => n + i.price * i.qty, 0))
  const isEmpty = computed(() => items.value.length === 0)

  function add(product: Product, qty = 1) {
    const existing = items.value.find(i => i.id === product.id)
    existing ? existing.qty += qty : items.value.push({ ...product, qty })
  }

  function $reset() { items.value = [] }

  return { items, total, isEmpty, add, $reset }
})
```

Rules:

- **`storeToRefs()` when destructuring state.** `const { items } = useCartStore()` gives you dead
  values; `storeToRefs` preserves reactivity. Actions destructure fine — they are plain functions.
- **Call `useStore()` inside `setup`**, not at module top level. At module scope Pinia may not be
  installed yet, and on the server it binds to the wrong request.
- **Setup stores need an explicit `$reset`.** Only option stores get one for free.
- **One store per domain**, not one per component and not one global store. A store that only one
  component uses is that component's local state.
- **Stores may use other stores** — call `useOther()` inside an action or a getter, not at the top of
  the store definition, to avoid circular initialization.
- **Do not put non-serializable things in state.** Class instances, DOM nodes, and socket handles break
  devtools, SSR serialization, and hydration.
- **Keep components out of stores.** A store that imports a component or touches the DOM has become a
  component.

## Vue Router 5

Current is **5.2.0**, and it is deliberately dull: **no breaking API changes from v4**. The two things
that did change — `unplugin-vue-router` was merged into the core package, so **typed routes are now
first-party**, and the IIFE build no longer bundles `@vue/devtools-api`. Code written for Router 4
works; the migration guide exists for people coming from the plugin.

```ts
const routes = [
  { path: '/', name: 'home', component: HomeView },
  {
    path: '/orders/:id',
    name: 'order',
    component: () => import('@/views/OrderView.vue'),   // lazy — one chunk per route
    props: true,                                        // params as props
    meta: { requiresAuth: true },
  },
]
```

- **Lazy-load route components.** A dynamic import per route is the highest-value code split in a Vue
  app, and it is one line.
- **`props: true`** decouples the view from the router: the component takes an `id` prop and can be
  tested and reused without a router at all.
- **Name routes and navigate by name.** A path string spread through the codebase is a path nobody can
  change.
- **Route params are strings.** Always. Coerce and validate at the boundary.

### Reacting to param changes

The trap: navigating from `/orders/1` to `/orders/2` reuses the component, so `onMounted` does not run
again.

```ts
const route = useRoute()
watch(() => route.params.id, fetchOrder, { immediate: true })
```

### Guards

```ts
router.beforeEach((to) => {
  if (to.meta.requiresAuth && !useAuthStore().isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }
})
```

- Return a location or `false`; do not call `next()` in new code.
- Keep guards to authorization and redirection. Data fetching in a global guard blocks every navigation
  behind the slowest route.
- **A guard is not security.** It hides a route in one client. The server authorizes.

## The URL is state

Anything a user should be able to bookmark, share, or reload into — filters, pagination, sort order,
the open tab — belongs in the query string, not in a store. It is free persistence, free
shareability, and it makes the back button behave the way users expect.

## Sources

- [Pinia](https://pinia.vuejs.org/) · [Pinia v4.0.0 release](https://github.com/vuejs/pinia/releases/tag/v4.0.0) — ESM-only, `@vue/devtools-api`
- [Pinia: dealing with composables](https://pinia.vuejs.org/cookbook/composables.html) · [Composing stores](https://pinia.vuejs.org/cookbook/composing-stores.html)
- [Top 5 mistakes to avoid when using Pinia](https://masteringpinia.com/blog/top-5-mistakes-to-avoid-when-using-pinia) · [My top 5 tips for using Pinia](https://masteringpinia.com/blog/my-top-5-tips-for-using-pinia) — Eduardo San Martin Morote, Pinia's author
- [Vue Router](https://router.vuejs.org/) · [Vue Router v5.0.0 release](https://github.com/vuejs/router/releases/tag/v5.0.0)
- [Composables vs. provide/inject vs. Pinia — when to use what](https://vueschool.io/articles/vuejs-tutorials/composables-vs-provide-inject-vs-pinia-when-to-use-what/) — Vue School
- [State management](https://vuejs.org/guide/scaling-up/state-management.html)
