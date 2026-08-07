# Inertia data loading

Read this when an Inertia page is slow, sends too much, or needs data that should not block the first
render. This is where most Inertia performance work actually lives.

## The prop evaluation matrix

Knowing this table is most of the skill. It decides what the server computes and what it sends.

| Server-side form | Sent on a normal visit | Sent on a partial reload | Evaluated |
|---|---|---|---|
| `'users' => User::all()` | always | only if requested | **always** |
| `'users' => fn () => User::all()` | always | only if requested | only when needed |
| `Inertia::optional(fn () => ...)` | **never** | only if requested | only when needed |
| `Inertia::defer(fn () => ...)` | in a follow-up request | only if requested | only when needed |
| `Inertia::always(...)` | always | **always** | always |
| `Inertia::once(fn () => ...)` | first time, then cached client-side | on request | when not remembered |

The first row is the trap. **A bare value is computed on every request, even when the client asked for
something else.** Wrapping it in a closure costs nothing and means a partial reload of one prop no
longer runs the other five queries.

> Rule of thumb: **make every non-trivial prop a closure.** Then choose `optional`, `defer`, or `once`
> deliberately for the ones that need it.

`Inertia::optional()` was `Inertia::lazy()` in v2.

## Shared data — the default performance leak

Inertia's own warning: **"Shared data should be used sparingly as all shared data is included with
every response."**

`HandleInertiaRequests::share()` runs on every single request. Anything in it — the full user object,
a permissions matrix, notification counts, a menu tree — is computed and shipped on every navigation,
forever, whether the page uses it or not.

Fix it in this order:

1. **Move it to the pages that need it.** Most shared data is shared because it was easy.
2. **Make it a closure**, so it is not computed when a partial reload does not need it.
3. **Make it `Inertia::once()`** if it rarely changes.
4. **Use flash data for flash messages**, not a shared prop.

```php
public function share(Request $request): array
{
    return [
        ...parent::share($request),
        'auth' => [
            'user' => fn () => $request->user()?->only('id', 'name', 'avatar_url'),
        ],
        'plans' => Inertia::once(fn () => Plan::all())->shareOnce(),
    ];
}
```

Note `->only(...)` on the user. Sharing `$request->user()` ships every column of the users table to
the browser on every request — including columns added next year.

## Once props

New and genuinely useful: send data on the first request, remember it client-side, and stop sending
it.

```php
'plans' => Inertia::once(fn () => Plan::all()),
'rates' => Inertia::once(fn () => Rate::current())->until('1 hour'),
'config' => Inertia::once(fn () => $config)->as('app-config'),
```

- Re-sent when explicitly requested via `router.reload({ only: [...] })`, when the expiry passes, when
  you navigate to a page without the prop, and on first load.
- `fresh()` forces re-resolution; `until()` sets expiry; `as()` shares one cache key across
  differently-named props; `shareOnce()` registers it globally in middleware.
- **Conditional props must return `null` rather than being omitted.** A once prop for the authenticated
  user that disappears on logout would otherwise leave the previous user's value remembered on the
  client. Returning `null` overwrites it. This is a real security consideration, not a nicety.

## Deferred props

For data the page can render without.

```php
return Inertia::render('Dashboard', [
    'stats'       => fn () => $this->cheapStats(),
    'permissions' => Inertia::defer(fn () => Permission::all()),
    'revenue'     => Inertia::defer(fn () => $this->slowReport(), 'reports'),
    'churn'       => Inertia::defer(fn () => $this->otherSlowReport(), 'reports'),
]);
```

- Ungrouped deferred props load together in one follow-up request. **Named groups fetch in parallel**,
  so put slow independent things in separate groups and related things in the same one.
- The `<Deferred>` component takes a `data` key (or array), a `fallback` slot, a `reloading` flag, and
  a `rescue` slot for failures.
- `rescue: true` suppresses the exception, reports it through Laravel's handler, and omits the prop —
  right for a non-essential widget, wrong for anything the page needs.

Use it for the expensive panel below the fold. Do not defer the thing the page is about; you have then
added a round trip to the critical path.

## Partial reloads

```js
router.reload({ only: ['users'] })
router.reload({ except: ['sidebar'] })
router.visit(url, { only: ['results'], preserveState: true, preserveScroll: true })
```

The point of partial reloads is refreshing one region without re-running the whole controller — which
only works if the other props are closures. With bare values you save bandwidth and nothing else.

Remember `errors` is an `always` prop, so a partial reload returning no errors clears client-side ones
unless you pass `preserveErrors: true`.

## Prefetching

```vue
<Link href="/users" prefetch>Users</Link>
<Link href="/users" :prefetch="['mount', 'hover']" cache-for="1m">Users</Link>
```

- Strategies: `hover` (default, after 75ms), `click` (on mousedown), `mount`.
- `cacheFor` defaults to 30 seconds. A tuple gives stale-while-revalidate: `['30s', '1m']` serves fresh
  for 30s, serves stale while revalidating up to 1m, expires after.
- `cacheTags` plus `router.flushByCacheTags()` — and `invalidateCacheTags` on forms — keep the cache
  honest after a mutation.

Prefetch high-intent navigation: the row a user is hovering, the next step of a wizard. Prefetching
everything on mount turns one page view into a dozen server-side renders; the docs do not warn about
this, so it is on you to bound it.

## Polling

```js
usePoll(5000, { only: ['notifications'] })
```

Always scope polling with `only`, or every interval re-runs the entire controller. Stop polling when
the tab is hidden. For anything busier than a slow counter, use broadcasting instead — polling is a
per-user constant load on the server.

## Merging props and infinite scroll

```php
return Inertia::render('Users/Index', [
    'users' => Inertia::scroll(fn () => User::paginate()),
]);
```

`Inertia::scroll()` works with `paginate()`, `simplePaginate()`, `cursorPaginate()`, and API resources.
The `<InfiniteScroll>` component uses intersection observers and **merges** rather than replaces.

- Use `itemsElement` when items are not direct children of the root, so each item can be tagged with
  its page number for URL sync.
- `manualAfter` switches to a button after N pages — worth doing, because unbounded infinite scroll
  grows the DOM and the history state until the tab struggles.
- `reset: ['users']` on a filter change, or the new results merge into the old ones.
- Multiple scrollers on one page need distinct `pageName` values.
- The URL updates with the visible page. Disable with `preserve-url` for secondary content.
- Prefer `cursorPaginate()` for large or fast-changing sets: offset pagination both drifts as rows are
  inserted and gets slower the deeper it goes.

## A diagnostic order for a slow Inertia page

1. Open the network tab and read the **response size and prop names**. The offender is usually visible
   immediately, and is usually shared data.
2. Count queries with Telescope, Debugbar, or Pulse. An N+1 inside a prop closure is still an N+1.
3. Check which props are bare values that could be closures.
4. Move below-the-fold data to `defer`, rarely-changing data to `once`, and page-specific data out of
   `share()`.
5. Scope every poll and every reload with `only`.
6. Only then consider SSR or prefetching — they change perceived latency, not the amount of work.

## Sources

- [Shared data](https://inertiajs.com/docs/v3/data-props/shared-data) — the "used sparingly" warning
- [Once props](https://inertiajs.com/docs/v3/data-props/once-props) — including the null-overwrite rule
- [Deferred props](https://inertiajs.com/docs/v3/data-props/deferred-props) · [Load when visible](https://inertiajs.com/docs/v3/data-props/load-when-visible)
- [Partial reloads](https://inertiajs.com/docs/v3/data-props/partial-reloads) — the evaluation matrix and the errors warning
- [Prefetching](https://inertiajs.com/docs/v3/data-props/prefetching) · [Polling](https://inertiajs.com/docs/v3/data-props/polling)
- [Merging props](https://inertiajs.com/docs/v3/data-props/merging-props) · [Infinite scroll](https://inertiajs.com/docs/v3/data-props/infinite-scroll)
- [Inertia.js once props](https://jump24.co.uk/journal/inertiajs-once-props-stop-sending-the-same-data-over-and-over-again) — Jump24 on the shared-data problem once props solve
