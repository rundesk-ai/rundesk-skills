---
name: inertia-patterns
description: Use this skill when building, reviewing, debugging, or upgrading an Inertia.js application — page responses and props, shared data, partial reloads, deferred and once props, prefetching, polling, infinite scroll, forms and validation, file uploads, authorization exposure, asset versioning, history encryption, SSR, or migrating between Inertia majors. Applies with any adapter — Laravel, Rails, Phoenix, Django — and any of React, Vue or Svelte. Do not use it for a conventional SPA with its own API, or for Blade-only or Livewire work.
---

# Inertia patterns

Inertia is not an API and not a SPA framework. It is a protocol that lets a server-rendered
application return a **page component name plus props** instead of HTML, and lets the client swap the
component without a full page load.

Three consequences decide everything else:

- **The controller is still the controller.** Routing, validation, authorization, redirects and flash
  messages stay on the server. There is no client-side router to keep in sync and no API to version.
- **Props are the wire format.** Everything in them is serialized to the browser.
- **A redirect is the success response.** After a `POST`, redirect; Inertia follows it and renders the
  next page. Returning JSON breaks the model.

Use the backend's own skill alongside this one — `laravel-patterns` for Laravel — and the client
framework's, such as `vue-patterns`.

## Establish the versions first

**The two halves version independently**, which is the first thing to check and a routine source of
confusion. Checked against the registries on **7 August 2026**:

| Package | Latest | Registry |
|---|---|---|
| `@inertiajs/vue3` (and the React/Svelte siblings) | **3.6.1** (2026-07-07) | npm |
| `inertiajs/inertia-laravel` | **3.3.1** (2026-08-04) | Packagist |
| npm `legacy` tag (the v2 line) | 2.3.27 (2026-06-25) | npm |

Do not infer the client version from the adapter version or vice versa.

```sh
npm ls @inertiajs/vue3 @inertiajs/react @inertiajs/svelte 2>/dev/null
composer show inertiajs/inertia-laravel 2>/dev/null | head -3
curl -sS https://registry.npmjs.org/@inertiajs/vue3 | python3 -c 'import sys,json;print(json.load(sys.stdin)["dist-tags"])'
```

v3 renamed several APIs — most notably `Inertia::lazy()` became `Inertia::optional()`. Advice written
for v2 is usually still structurally right and names things that no longer exist. See
[`migration.md`](references/migration.md).

## Work in this order

1. **Check the two versions.** Half the confusing advice online is v2 advice.
2. **Decide what the page actually needs**, then choose the prop form. This is where Inertia
   performance lives — see [`data-loading.md`](references/data-loading.md).
3. **Keep authorization on the server.** Props that describe permissions are for rendering only.
4. **Let the redirect do the work.** Do not reach for `fetch` to "just get the data".
5. **Check the payload in the network tab** before optimizing anything.

## Rules that always hold

- **Everything in props reaches the browser.** Inertia: "all data returned from the controllers will
  be visible client-side, so be sure to omit sensitive information." Never pass a whole model.
- **Never submit with `fetch` or `axios`.** The response is not an Inertia response: no page update,
  no populated `errors`, no automatic `FormData`, no progress.
- **Authorize on the server, always.** A `can` prop hides a button; it does not protect a route.
- **Shared data is sent with every single response.** Use it sparingly, and prefer closures.
- **Make every non-trivial prop a closure.** A bare value is computed even when a partial reload asked
  for something else.
- **Set an asset version.** Without it clients keep running an old bundle indefinitely, with no signal.
- **Browser-only code must not run during SSR**, and SSR failures fall back silently.

## Read the reference the task needs

| Area | Read for |
|---|---|
| [Core](references/core.md) | The mental model, responses, props, security, authorization, forms, SSR, testing |
| [Data loading](references/data-loading.md) | The prop evaluation matrix, shared data, once, deferred, partial reloads, prefetching, infinite scroll |
| [Migration](references/migration.md) | v2 → v3 renames and breaking changes, and how to plan the upgrade |
| [Anti-patterns](references/anti-patterns.md) | The consolidated do / don't list |
| [Sources](references/sources.md) | The citation basis |

## Review output shape

```text
[HIGH] Whole model passed as a prop
Location: app/Http/Controllers/OrderController.php:41 — 'customer' => $customer
Evidence: the customers table has 23 columns including stripe_id and internal_notes; all 23 are in
     the page payload, visible in the browser.
Why: Inertia serializes props verbatim to the client, and a column added later ships automatically.
Fix: $customer->only('id', 'name') or a CustomerResource.
Check: assertInertia(...)->missing('customer.internal_notes') in the feature test.
```
