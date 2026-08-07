# Migration

Read this before an Inertia upgrade, or when advice you found online names an API that does not exist.

## Check both halves

The client package and the server adapter version **independently**, so "we're on Inertia 3" is an
incomplete statement. As of **7 August 2026**, registry-checked: `@inertiajs/vue3` is **3.6.1**, while
`inertiajs/inertia-laravel` is **3.3.1**. The npm `legacy` tag still carries the v2 line at 2.3.27.

```sh
npm ls @inertiajs/vue3 @inertiajs/react @inertiajs/svelte
composer show inertiajs/inertia-laravel | head -3
```

Upgrade them together, and read both changelogs — an adapter release can add a server-side prop form
that the client version you are on does not understand.

## v2 → v3

**Floors:** PHP 8.2+, Laravel 11+, React 19+, Svelte 5 with runes. Output is **ESM-only**.

**Renames** — the ones that make older advice fail to compile rather than fail quietly:

| v2 | v3 |
|---|---|
| `Inertia::lazy()` | `Inertia::optional()` |
| `router.on('invalid')` | `router.on('httpException')` |
| `router.on('exception')` | `router.on('networkError')` |
| `router.cancel()` | `router.cancelAll()` |
| `inertia` attribute in the root template | `data-inertia` |
| `hideProgress()` / `revealProgress()` | `progress.hide()` / `progress.reveal()` |

**Dependency removals.** Axios, `qs` and `lodash-es` are gone — Inertia ships its own XHR client,
roughly 15KB gzipped smaller. **If you had Axios interceptors, they must move** to the built-in
interceptor system; this is the item most likely to be missed, because nothing fails at build time
and the interceptor simply stops running.

**Configuration.** The `testing` block in `config/inertia.php` moved under `pages`, and the `future`
namespace is gone with all four of its options permanently enabled.

**React.** Arrow-function layouts must be wrapped in an array: `Dashboard.layout = [Layout]`.

**Initial page data** is now always passed via `<script type="application/json">`; the legacy
`data-page` attribute is unsupported.

## What v3 added that is worth adopting

Not required for the upgrade, but each replaces something people previously hand-rolled:

- **`useHttp`** — requests that should not trigger a page navigation. Previously this is why people
  reached for Axios, which is exactly what v3 removed.
- **Optimistic updates**, first-class, with automatic rollback on a non-2xx response.
- **Layout props** — `useLayoutProps` / `setLayoutProps` — instead of an event bus or provide/inject
  to get data from a page into its layout.
- **Instant visits**, swapping to the target component immediately.
- **SSR during `npm run dev`** without a separate Node process, via `@inertiajs/vite`.

## How to do the upgrade

1. **Read both changelogs**, client and adapter, for every version you are crossing.
2. Upgrade the npm packages and the composer package **together**.
3. Republish and diff `config/inertia.php`, then reapply your customizations — the `testing` block
   moved.
4. `php artisan view:clear`.
5. **Grep for the renamed APIs.** `Inertia::lazy`, `router.cancel`, `router.on('invalid'`,
   `router.on('exception'`, `hideProgress`, `revealProgress`, and the root-template `inertia`
   attribute.
6. **Grep for Axios.** If it appears anywhere in the front end, decide deliberately whether to install
   it or port to the built-in client and interceptors.
7. Convert any `require()` to `import` — ESM only.
8. Run the suite, then click through a page with a form, a file upload, and a partial reload. Those
   three exercise most of what changed.

## When you find v2 advice online

Most of it is structurally correct and names things that moved. Translate rather than discard: the
prop evaluation model, the shared-data warning, the redirect-as-response rule and the form handling
are all unchanged. It is the identifiers that drifted.

## Sources

- [Upgrade guide for v3.0](https://inertiajs.com/docs/v3/getting-started/upgrade-guide) — every rename, floor, dependency removal, and configuration move above
- [Inertia v3 documentation](https://inertiajs.com/docs/v3/) · [full page index](https://inertiajs.com/docs/llms.txt)
- [Inertia.js v3.0.0 is here](https://laravel-news.com/inertia-3-0-0) — Laravel News on `useHttp`, optimistic updates, layout props, and the Axios removal
- Versions checked against [npm](https://registry.npmjs.org/@inertiajs/vue3) and [Packagist](https://repo.packagist.org/p2/inertiajs/inertia-laravel.json) on 7 August 2026
