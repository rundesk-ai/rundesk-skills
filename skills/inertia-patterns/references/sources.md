# Inertia source basis

This package is a Rundesk synthesis of the Inertia documentation, the reference application the
project itself calls best practice, and community writing. Use this file to audit or update a claim.

**Read in this order of authority.** The documentation states the protocol and the API; Ping CRM shows
the intended shape in working code; community sources carry the judgement and the traps.

## Versions, checked against the registries

Checked on **7 August 2026**, against the registries rather than documentation prose — the two halves
version independently and the docs do not state either number.

| Package | Latest | Source |
|---|---|---|
| `@inertiajs/vue3` (and React/Svelte siblings) | **3.6.1**, 2026-07-07 | [npm](https://registry.npmjs.org/@inertiajs/vue3) |
| `inertiajs/inertia-laravel` | **3.3.1**, 2026-08-04 | [Packagist](https://repo.packagist.org/p2/inertiajs/inertia-laravel.json) |
| npm `legacy` tag (v2 line) | 2.3.27, 2026-06-25 | npm |

```sh
curl -sS https://registry.npmjs.org/@inertiajs/vue3 | python3 -c 'import sys,json;print(json.load(sys.stdin)["dist-tags"])'
curl -sS https://repo.packagist.org/p2/inertiajs/inertia-laravel.json | python3 -c 'import sys,json;print(json.load(sys.stdin)["packages"]["inertiajs/inertia-laravel"][0]["version"])'
```

## Documentation

- [Inertia v3 documentation](https://inertiajs.com/docs/v3/) · [full page index](https://inertiajs.com/docs/llms.txt).
- [Responses](https://inertiajs.com/docs/v3/the-basics/responses) — **"all data returned from the
  controllers will be visible client-side, so be sure to omit sensitive information"**, prop
  serialization, `withViewData`, and the browser history-state size limit.
- [Shared data](https://inertiajs.com/docs/v3/data-props/shared-data) — **"shared data should be used
  sparingly as all shared data is included with every response"**, and flash data as the alternative
  for toasts.
- [Partial reloads](https://inertiajs.com/docs/v3/data-props/partial-reloads) — the prop evaluation
  matrix, and the warning that `errors` is an `always` prop so an empty bag overwrites client-side
  errors.
- [Once props](https://inertiajs.com/docs/v3/data-props/once-props) — the API, re-send rules, and the
  conditional-prop `null` rule that prevents stale cached authentication state.
- [Deferred props](https://inertiajs.com/docs/v3/data-props/deferred-props) · [Load when visible](https://inertiajs.com/docs/v3/data-props/load-when-visible) · [Prefetching](https://inertiajs.com/docs/v3/data-props/prefetching) · [Polling](https://inertiajs.com/docs/v3/data-props/polling) · [Merging props](https://inertiajs.com/docs/v3/data-props/merging-props) · [Infinite scroll](https://inertiajs.com/docs/v3/data-props/infinite-scroll).
- [Forms](https://inertiajs.com/docs/v3/the-basics/forms) — `<Form>` versus `useForm`, the checkbox
  `"on"` trap, automatic `FormData` conversion, the password/history-state prompt, precognition
  debouncing and file exclusion, and what breaks when you submit with fetch or axios.
- [Validation](https://inertiajs.com/docs/v3/the-basics/validation) · [File uploads](https://inertiajs.com/docs/v3/the-basics/file-uploads) · [Flash data](https://inertiajs.com/docs/v3/data-props/flash-data).
- [Authorization](https://inertiajs.com/docs/v3/security/authorization) — "authorization is best
  handled server-side in your application's authorization policies."
- [History encryption](https://inertiajs.com/docs/v3/security/history-encryption) — the back-button
  problem, key rotation, and the `window.crypto.subtle` secure-context requirement.
- [Asset versioning](https://inertiajs.com/docs/v3/advanced/asset-versioning) — mismatch behaviour,
  why background requests do not force a reload, and the failure mode when unset.
- [SSR](https://inertiajs.com/docs/v3/advanced/server-side-rendering) — dev-mode SSR without a Node
  process, the Node 22 floor, browser-API errors, and the **silent fallback to client rendering**.
- [Testing](https://inertiajs.com/docs/v3/advanced/testing) — `assertInertia`, `has`/`where`/`missing`/
  `etc`, `reloadOnly`, `loadDeferredProps`, flash assertions.
- [Upgrade guide for v3.0](https://inertiajs.com/docs/v3/getting-started/upgrade-guide) — every rename,
  floor, dependency removal, and configuration move.
- [The protocol](https://inertiajs.com/docs/v3/core-concepts/the-protocol) — what is actually on the
  wire, which settles most arguments about what Inertia "is".

## The reference application

- [Ping CRM](https://github.com/inertiajs/pingcrm) — the demo the project maintains, and the closest
  thing to a canonical style guide: the community consensus is that **most of the approaches taken in
  Ping CRM are Inertia best practices**. Read it rather than inventing a convention.
  [Discussion #360](https://github.com/inertiajs/inertia/discussions/360) is its introduction.
- Ports demonstrate that Inertia is not Laravel-specific and are useful when the adapter differs:
  [Svelte](https://github.com/inertiajs/pingcrm-svelte) ·
  [React](https://github.com/liorocks/pingcrm-react) ·
  [Rails](https://github.com/ledermann/pingcrm).
- [Demo application](https://inertiajs.com/docs/v3/getting-started/demo-application) — the docs' own
  pointer to it.

## Community

- [Inertia GitHub Discussions](https://github.com/inertiajs/inertia/discussions) and
  [issues](https://github.com/inertiajs/inertia/issues) — where a behaviour that looks like a bug gets
  settled. Search before assuming.
- [Inertia.js v3.0.0 is here](https://laravel-news.com/inertia-3-0-0) — Laravel News on `useHttp`,
  optimistic updates, layout props, and the Axios removal.
- [Inertia.js once props: stop sending the same data over and over](https://jump24.co.uk/journal/inertiajs-once-props-stop-sending-the-same-data-over-and-over-again) —
  Jump24, on the shared-data bloat problem that once props exist to solve. A practitioner framing of
  the single most common Inertia performance fault.
- [Type-safe shared data and page props in Inertia.js](https://laravel-news.com/type-safe-shared-data-and-page-props-in-inertiajs) —
  Laravel News, on typing the prop contract so a shape change fails at build rather than at runtime.

## Related skills

Inertia sits between a backend and a client framework, and this package deliberately covers only the
seam:

- `laravel-patterns` — the server side, when the adapter is Laravel.
- `vue-patterns` — the client side, when the adapter is Vue.
- `debugging-code` → `vue.md` for diagnosing a page that will not update.

## What this package deliberately does not cite

- v2-era tutorials without saying so. Most are structurally right and name renamed APIs.
- Blog posts that reimplement something the protocol already provides — hand-rolled deferred loading,
  Axios interceptors for progress — except as an example of what not to do.
