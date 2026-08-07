# Inertia anti-patterns

Read this when reviewing an Inertia application. Each row names the failure, not just the rule.

Backend rules live with the backend's skill (`laravel-patterns` and so on); client-framework rules
with the client's (`vue-patterns`). This page is what Inertia itself adds.

## Props and payload

| Don't | Do | Because |
|---|---|---|
| Pass a whole model | `->only(...)`, a resource, or a DTO | Every column reaches the browser — "all data returned from the controllers will be visible client-side" — including ones added next year |
| Bare values for expensive props | Closures | A bare value is computed on **every** request, even when a partial reload asked for something else |
| Pile data into shared data | Page props, or `Inertia::once()` | "Shared data should be used sparingly as all shared data is included with every response" |
| Share `$request->user()` whole | `->only('id','name','avatar_url')` | The users table ships on every navigation, forever |
| A shared `flash` prop | Flash data | Shared props persist in history state, so the toast reappears on back navigation |
| Ship a thousand rows | Paginate, or `Inertia::scroll()` | Browser history state has limits — Firefox errors above 16 MiB |
| A once prop that disappears when null | Return `null` explicitly | The client keeps the previous value — for an auth prop that is the **previous user** |

## Security

| Don't | Do | Because |
|---|---|---|
| Trust a `can` prop for access control | Authorize the route too | The request can be made without the button |
| A `can` prop with no matching server check | Pair every one | The pattern invites exactly this omission |
| Put a secret in `withViewData` reasoning | Know the difference | `withViewData` stays server-side; props do not |
| Skip history encryption on privileged pages | `Inertia::encryptHistory()`, and `clearHistory()` on logout | The back button after logout reveals the previous user's data |
| Rely on history encryption over plain HTTP | HTTPS | It needs `window.crypto.subtle`, which is secure-context only — it silently does nothing otherwise |

## Forms and requests

| Don't | Do | Because |
|---|---|---|
| Submit with `fetch` or `axios` | `<Form>` or `useForm` | The response is not an Inertia response: no page update, no `errors`, no `FormData`, no progress |
| Return JSON from a form action | Redirect | A redirect is the success response; JSON breaks the model |
| Build `FormData` by hand for uploads | Let Inertia convert it | It does so automatically when files are present |
| `PUT`/`PATCH` with multipart | `POST` with `_method` | Laravel does not parse multipart on those verbs |
| Checkboxes without a `value` | Set one | A checked box submits `"on"`, and server validation rejects it |
| Leave a password field in history state | `dontRemember('password')` | Some browsers prompt to save the password without a submit |
| Assume errors persist across a partial reload | `preserveErrors: true` | `errors` is an `always` prop, so an empty bag overwrites client-side errors |

## Loading and performance

| Don't | Do | Because |
|---|---|---|
| Poll or reload without `only` | Scope it | Every interval re-runs the whole controller |
| Defer the thing the page is about | Defer below-the-fold data | You added a round trip to the critical path |
| `prefetch` on mount for everything | Hover, or high-intent links | One page view becomes a dozen server renders |
| Unbounded infinite scroll | `manualAfter`, or paginate | DOM and history state grow until the tab struggles |
| Offset pagination for a large feed | `cursorPaginate()` | It drifts as rows are inserted and slows with depth |
| Forget `reset` when filters change | `reset: ['items']` | New results merge into the old ones |

## Build and deployment

| Don't | Do | Because |
|---|---|---|
| Skip asset versioning | Set `version()` | Clients keep the old bundle indefinitely with no signal — "only some users have the bug" |
| Read `window` or `localStorage` in setup | After mount | They do not exist during SSR |
| Assume SSR works because tests pass | `throw_on_error` in testing | SSR failures fall back to client rendering **silently** |
| Run the SSR server without restarting on deploy | Restart it | It holds the old bundle in memory |
| Mix client and adapter major versions casually | Check both registries | They version independently |

## Advice-giving

- **Read both versions before advising.** Most Inertia advice online is v2 and names APIs that were
  renamed — `Inertia::lazy()`, `router.cancel()`, the `invalid` and `exception` events.
- **Do not recommend Axios.** v3 removed it deliberately; `useHttp` covers the case it was used for.
- **Check the payload before optimizing.** The network tab names the offending prop in seconds, and it
  is usually shared data.
- **Say whether a finding is a defect or a preference.** A whole model in props is a defect; a prop
  that could be a closure is a performance finding.

## Sources

Cited in [`sources.md`](sources.md). The densest are the
[Inertia v3 documentation](https://inertiajs.com/docs/v3/) — responses, shared data, partial reloads,
once props, forms, history encryption, asset versioning — and the
[upgrade guide](https://inertiajs.com/docs/v3/getting-started/upgrade-guide).
