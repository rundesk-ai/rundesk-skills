# Inertia

Read this for the Inertia mental model, responses, forms, validation, security, SSR, versioning, and
testing. Data-loading strategy is in [`inertia-data-loading.md`](inertia-data-loading.md).

**Check the version first.** Inertia v3 shipped 26 March 2026; v2 gets bug fixes until 26 September
2026 and security patches until 26 March 2027. `grep '@inertiajs' package.json` before advising —
several APIs were renamed.

## The mental model

Inertia is not an API and not a SPA framework. It is a protocol that lets a server-rendered
application return a **page component name plus props** instead of HTML, and lets the client swap the
component without a full page load.

The consequences that decide everything else:

- **The controller is still the controller.** Routing, validation, authorization, redirects, and flash
  messages stay in Laravel. There is no client-side router to keep in sync and no API to version.
- **Props are the wire format.** Everything in them is serialized to the browser.
- **A redirect is the success response.** After a `POST`, redirect; Inertia follows it and renders the
  next page. Returning JSON breaks the model.

## Responses and props

```php
return Inertia::render('Event/Show', [
    'event' => $event->only('id', 'title', 'start_date'),
]);
```

Props accept primitives, models and collections (via `toArray()`), API resources (via
`toResponse()`), and closures (evaluated server-side).

**The security rule, quoted:**

> Be aware that all data returned from the controllers will be visible client-side, so be sure to
> omit sensitive information.

So:

- **Never pass a whole model** when the page needs four fields. `$user` includes every column —
  including the ones added later by somebody who did not know this page existed. Use `->only(...)`,
  an API resource, or a DTO.
- Use API resources for anything non-trivial; they put the shape in one reviewable file.
- For data the root Blade template needs but the client must not get, use `->withViewData([...])`.
- Watch payload size. Browser history state has limits — Firefox errors above 16 MiB — and a page
  that ships a thousand rows is slow before it is anything else.

## Authorization

Inertia's own position: "authorization is best handled server-side in your application's authorization
policies." Props carrying permissions exist **to render the UI**, never to control access.

```php
return Inertia::render('Posts/Show', [
    'post' => PostResource::make($post),
    'can' => [
        'update' => $request->user()->can('update', $post),
        'delete' => $request->user()->can('delete', $post),
    ],
]);
```

Hiding a button is presentation. The `update` route must still authorize, because the request can be
made without the button. Every `can` prop implies a matching server-side check, and a page that has
one without the other is the bug this pattern invites.

Laravel's own docs show this shape in `HandleInertiaRequests::share()` — convenient for global
permissions, but see the shared-data warnings in
[`inertia-data-loading.md`](inertia-data-loading.md).

## Forms

Two supported approaches. Both go through Inertia; neither uses `fetch` or `axios`.

```vue
<!-- Declarative: the <Form> component -->
<Form action="/users" method="post" #default="{ errors, processing }">
  <input name="name" />
  <div v-if="errors.name">{{ errors.name }}</div>
  <button :disabled="processing">Save</button>
</Form>
```

```js
// Programmatic: useForm
const form = useForm({ name: '' })
form.post('/users', { preserveScroll: true, onSuccess: () => form.reset() })
```

**Do not submit with `fetch` or `axios`.** It is the most common Inertia mistake. The response is not
an Inertia response, so the page does not update, `errors` is never populated, files are not converted
to `FormData`, and progress and optimistic updates are lost.

Gotchas worth knowing before they cost an afternoon:

- **Checkboxes without a `value` submit `"on"`**, not a boolean, and server validation rejects it.
- **File uploads are automatic** — "Inertia will automatically convert the request data into a
  `FormData` object" when files are present. Do not build `FormData` by hand.
- Laravel does not accept `PUT`/`PATCH` with multipart; send `POST` with `_method: 'put'`.
- **Password fields in history state** can trigger the browser's save-password prompt without a
  submit. Use `dontRemember('password')`.
- Precognition validation is debounced (1500ms default) and **skips files** unless you enable
  `validateFiles`.
- `preserveScroll`, `preserveState`, `preserveUrl`, and `replace` control what survives the visit.
  `preserveScroll` on a long form is almost always right.

## Validation

Standard Laravel validation works unchanged. A `ValidationException` produces a 422, Inertia populates
`errors`, and the component re-renders — no client-side error plumbing.

One documented trap: errors are shared with `Inertia::always()`, so **"an empty error bag from the
server will overwrite any existing client-side validation errors."** Pass `preserveErrors: true` on
visits that must not clear them.

Error bags (`$errors->getBag('name')`) keep multiple forms on one page separate.

## Flash messages

Use flash data rather than a shared prop. Inertia's guidance: "flash data is not persisted in the
browser's history state, so it won't reappear when navigating through history" — which is exactly what
you want from a toast, and exactly what a shared `flash` prop gets wrong.

## Asset versioning

Set the version so clients pick up new builds. Laravel's Vite integration handles it automatically;
otherwise set it in `HandleInertiaRequests::version()`.

On a version mismatch Inertia performs a full page visit instead of an XHR, forcing new assets.
Background requests — polling, `router.reload()` — deliberately do **not** force a reload, so unsaved
state survives; the next user-initiated visit picks the new assets up.

**Without versioning configured, clients keep running the old bundle indefinitely** with no signal.
This is the failure that presents as "only some users have the bug."

## History encryption

For applications showing privileged data, encrypt the history state so the back button after logout
cannot reveal it.

```php
Inertia::encryptHistory();            // per request
Inertia::clearHistory();              // on logout — rotates the key
```

Enable globally with `inertia.history.encrypt`, or apply the `EncryptHistory` middleware to a group.
It uses `window.crypto.subtle`, **available only in secure contexts** — it does not work without
HTTPS, so it silently does nothing in a plain-HTTP staging environment.

## SSR

v3 made this much easier: the `@inertiajs/vite` plugin auto-detects the entry point, and SSR works
during `npm run dev` **without a separate Node process**. In production, build both bundles
(`vite build && vite build --ssr`) and run `php artisan inertia:start-ssr` under a process supervisor,
restarting it on deploy.

Caveats:

- **Node.js 22 or higher** is required.
- **Browser-only code breaks SSR.** `window` and `document` must move into client lifecycle hooks.
- **SSR failures fall back to client rendering silently.** Convenient in production, dangerous in
  testing — enable `throw_on_error` in test environments or a broken SSR build passes unnoticed and
  no user ever gets server-rendered HTML.
- Single-threaded by default; enable `cluster: true` for production.
- Exclude routes with `Inertia::withoutSsr()` or the middleware's `$withoutSsr`.

Adopt SSR when you need SEO or first-paint on public pages. For an authenticated dashboard it is
usually deployment complexity with no benefit.

## Testing

```php
$this->get('/podcasts/41')
    ->assertInertia(fn (Assert $page) => $page
        ->component('Podcasts/Show')
        ->has('podcast', fn (Assert $p) => $p->where('id', 41)->etc())
        ->missing('secretToken')
    );
```

- `has`, `where`, `missing`, `etc()` for props; `component()` for the page.
- `reloadOnly()` / `reloadExcept()` test partial reloads; `loadDeferredProps()` tests deferred ones.
- `hasFlash()` / `assertInertiaFlash()` for flash data.
- **`missing()` is the security test.** Assert that pages do not ship fields they should not — that is
  the check that catches somebody passing a whole model later.

## v2 → v3 breaking changes

Requires PHP 8.2+, Laravel 11+, React 19+, Svelte 5 with runes. ESM-only output.

| v2 | v3 |
|---|---|
| `Inertia::lazy()` | `Inertia::optional()` |
| `router.on('invalid')` | `router.on('httpException')` |
| `router.on('exception')` | `router.on('networkError')` |
| `router.cancel()` | `router.cancelAll()` |
| `inertia` attribute in Blade | `data-inertia` |
| `hideProgress()` / `revealProgress()` | `progress.hide()` / `progress.reveal()` |

Axios, `qs`, and `lodash-es` are no longer dependencies — Inertia ships its own XHR client, which is
about 15KB gzipped smaller. Axios interceptors must migrate to the built-in interceptor system. The
`config/inertia.php` `testing` block moved under `pages`, and the `future` namespace is gone with all
four options permanently on. React arrow-function layouts must be wrapped: `Dashboard.layout = [Layout]`.

New in v3 and worth reaching for: `useHttp` for requests that should not navigate, first-class
optimistic updates with automatic rollback, layout props (`useLayoutProps` / `setLayoutProps`) instead
of an event bus, and instant visits.

## Sources

- [Inertia v3 documentation](https://inertiajs.com/docs/v3/) · [full index](https://inertiajs.com/docs/llms.txt)
- [Upgrade guide for v3.0](https://inertiajs.com/docs/v3/getting-started/upgrade-guide) — every rename and breaking change
- [Responses](https://inertiajs.com/docs/v3/the-basics/responses) — the client-visibility warning
- [Forms](https://inertiajs.com/docs/v3/the-basics/forms) · [Validation](https://inertiajs.com/docs/v3/the-basics/validation) · [File uploads](https://inertiajs.com/docs/v3/the-basics/file-uploads)
- [Authorization](https://inertiajs.com/docs/v3/security/authorization) · [History encryption](https://inertiajs.com/docs/v3/security/history-encryption)
- [Asset versioning](https://inertiajs.com/docs/v3/advanced/asset-versioning) · [SSR](https://inertiajs.com/docs/v3/advanced/server-side-rendering) · [Testing](https://inertiajs.com/docs/v3/advanced/testing)
- [Laravel: Authorization & Inertia](https://laravel.com/docs/13.x/authorization#authorization-and-inertia)
- [Inertia.js v3.0.0 is here](https://laravel-news.com/inertia-3-0-0) — Laravel News on the release
