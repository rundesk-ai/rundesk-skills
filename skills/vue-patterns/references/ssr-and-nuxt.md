# SSR and Nuxt

Read this when working on a server-rendered Vue or Nuxt app, or when debugging a hydration warning.

## The two SSR failure modes

Everything else on this page is a special case of one of these.

### 1. Hydration mismatch

The server rendered one thing and the client rendered another. Vue 3 "automatically attempts to recover
and adjust mismatched DOM," but that costs performance and the recovery is not always what you wanted.
Fix the cause; do not learn to ignore the warning.

Vue names three causes:

| Cause | Fix |
|---|---|
| **Invalid HTML nesting** — a `<div>` inside a `<p>`, a `<p>` inside a `<p>` | Fix the markup. The browser's parser "corrects" it, so the client tree differs from the server's |
| **Randomly generated values** | Render client-only behind `v-if` + `onMounted`, use a seeded generator, or `useId()` for ids |
| **Timezone / locale differences** | Format dates client-side in `onMounted`; the server's timezone is not the user's |

Two more that come up constantly in practice: reading `window`/`localStorage` during setup, and
branching on `navigator.userAgent`. Both belong after mount.

`<ClientOnly>` in Nuxt (and equivalent elsewhere) is the escape hatch for a genuinely client-only
widget. It is not a fix for a mismatch you have not diagnosed.

### 2. Cross-request state pollution

**The dangerous one, because it is silent and it leaks between users.**

Vue: application modules "are initialized once on server startup and reused across requests," so a
module-scope singleton "can be mutated by one user's request and leaked to another."

```ts
// ❌ one instance for every user on the server
export const currentUser = ref(null)
```

The fix is a fresh instance per request:

```ts
export function createApp() {
  const app = createSSRApp(/* ... */)
  const store = createStore()          // new per request
  app.provide('store', store)
  return { app, store }
}
```

Pinia does this correctly by design — its state is scoped to the request. This is the strongest single
argument for using it over a hand-rolled shared composable in any SSR app.

## Code that must not run on the server

- **`onMounted` and `onUpdated` never run on the server.** Only `beforeCreate` and `created` do.
- Consequently, **a side effect started in `created` is never cleaned up on the server**, because
  unmount hooks never run. A `setInterval` there leaks for the life of the process. Move it to
  `onMounted`.
- **No browser globals in universal code** — `window`, `document`, `localStorage`, `navigator`. Access
  them lazily inside `onMounted`, or use a library that abstracts the platform.

Vue's composable guidance says the same from the other side: "perform DOM-specific side effects in
post-mount lifecycle hooks… these hooks are only called in the browser."

## Nuxt data fetching

Current is **Nuxt 4.5.2**. The rule that catches everyone:

> "If the `$fetch` function is used to perform data fetching in the setup function of a Vue component,
> this may cause data to be fetched twice, once on the server… and once again on the client."

So:

| Use | For |
|---|---|
| `useFetch(url)` | The normal case — fetching for the initial render of a component |
| `useAsyncData(key, fn)` | Wrapping custom async logic: a CMS client, a query layer, several calls |
| `$fetch(url)` | Event handlers and client-side interactions only — never bare in `setup` |

Nuxt: "using only `$fetch` will not provide network calls de-duplication and navigation prevention."

### Keys and shared state

- `useFetch` derives its key from the URL, options, and call site — so **two `useFetch` calls to the
  same URL in different components are independent** unless you pass the same explicit key.
- `useAsyncData`'s first argument is the key; calls sharing a key share `data`, `error`, and `status`.
- Options that **must match** across calls sharing a key: the handler, `deep`, `transform`, `pick`,
  `getCachedData`, and defaults. Options that may differ: `server`, `lazy`, `immediate`, `dedupe`,
  `watch`.

### Options worth knowing

- **`transform` and `pick` shrink the payload** that is serialized into the HTML. On a large API
  response this is the cheapest page-weight win available.
- **`lazy: true`** does not block navigation; you handle `status` yourself.
- **`server: false`** makes it client-only — the data is absent on first render.
- **`watch`** refetches on a reactive change, but note: "watching a reactive value won't change the URL
  fetched." For a dynamic URL, pass a computed or a getter as the URL.
- `await` changes client behaviour, not the server-rendered HTML: with it, navigation waits; without
  it, the page renders and you manage loading state.

### Nuxt 4 specifics

- **`~` points at `app/` by default.** `~/components` resolves to `app/components`. Migration is
  optional — Nuxt auto-detects an existing v3 layout — and `npx codemod@latest nuxt/4/file-structure`
  automates it.
- **Data is freed when the last component using it unmounts**, which fixes the unbounded-memory
  behaviour of long-lived sessions.
- Keys may now be computed refs, plain refs, or getters, which enables automatic refetching.
- `getCachedData` now runs on every fetch, including watcher-triggered ones, and receives the cause.

### Other Nuxt rules

- **`useRuntimeConfig()` for anything environment-dependent.** Only keys under `public` reach the
  browser; everything else is server-only. A secret outside `public` that a component reads is a secret
  in the bundle.
- Server routes in `server/api/` run only on the server — the right place for anything holding a
  credential.
- Auto-imports are convenient and make provenance invisible. When a reviewer cannot tell where a symbol
  came from, import it explicitly.

## Testing SSR

Render on the server in CI and assert no hydration warnings. A mismatch is a warning, not an error, so
it will not fail a test that is not looking for it — and the cost is paid by every user on every page
load until somebody notices.

## Sources

- [Server-side rendering](https://vuejs.org/guide/scaling-up/ssr.html) — hydration mismatch causes, cross-request state pollution, server-hook behaviour
- [Composables: SSR side effects](https://vuejs.org/guide/reusability/composables.html)
- [`useId()`](https://vuejs.org/api/composition-api-helpers.html#useid) — SSR-stable ids
- [Nuxt: data fetching](https://nuxt.com/docs/4.x/getting-started/data-fetching) — `$fetch` vs `useFetch` vs `useAsyncData`, keys, options
- [Nuxt 4 upgrade guide](https://nuxt.com/docs/4.x/getting-started/upgrade) · [Announcing Nuxt 4.0](https://nuxt.com/blog/v4)
- [Nuxt: runtime config](https://nuxt.com/docs/4.x/guide/going-further/runtime-config)
