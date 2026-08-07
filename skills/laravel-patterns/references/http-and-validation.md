# HTTP layer: routing, validation, authorization

Read this for controllers, middleware, form requests, policies, and API responses.

## Routing

```php
Route::middleware('auth')->group(function () {
    Route::apiResource('projects', ProjectController::class);
});

// Scoped bindings: {project} must belong to {account}
Route::scopeBindings()->group(function () {
    Route::get('/accounts/{account}/projects/{project}', [ProjectController::class, 'show']);
});
```

- **Scoped bindings are not authorization.** They constrain the parent-child lookup; they do not
  check the current user may see the parent. Authorize as well, always.
- Bind by a non-id column with `{post:slug}`, or `getRouteKeyName()` on the model.
- Name routes and reference them by name. A literal URL in a redirect is a URL nobody can rename.
- **Route caching requires no closures in route files.** `route:cache` fails on a closure route; use
  controllers.
- Rate-limit anything a stranger can reach: `throttle:60,1`, or a named limiter in a provider.

## Controllers

Keep them thin: authorize, validate, delegate, respond. Business logic in a controller is logic no
console command or job can reach.

Laravel 13 added first-party attributes, which colocate middleware and authorization with the
action:

```php
use Illuminate\Routing\Attributes\Controllers\Authorize;
use Illuminate\Routing\Attributes\Controllers\Middleware;

#[Middleware('auth')]
class CommentController
{
    #[Middleware('subscribed')]
    #[Authorize('create', [Comment::class, 'post'])]
    public function store(Post $post) { /* ... */ }
}
```

Use one style consistently. Attributes on some actions and middleware in `bootstrap/app.php` for
others means the answer to "what protects this route?" is in two places.

### Services and actions

Use them when there is coordination to hold, not by reflex.

```php
final class CreateOrder
{
    public function __construct(private Inventory $inventory) {}

    public function handle(CreateOrderData $data): Order
    {
        return DB::transaction(function () use ($data) { /* ... */ });
    }
}
```

A single-purpose action class per use case is a reasonable default. A `Repository` wrapping Eloquent
usually is not — Eloquent is already the abstraction, and the wrapper's own interface leaks it.

## Validation

Form requests keep validation out of the controller and give you `authorize()` for free.

```php
class StoreOrderRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('create', Order::class);
    }

    public function rules(): array
    {
        return [
            'title' => ['required', 'string', 'max:255'],
            'items' => ['required', 'array', 'min:1'],
            'items.*.sku' => ['required', 'string', Rule::exists('products', 'sku')],
        ];
    }
}
```

- **`authorize()` returning `false` produces a 403 and the controller never runs.** The default in a
  generated request is `false` in some templates — check it, because a request that always 403s
  looks like a routing bug.
- **Use array rule syntax, not pipes.** Spatie's guideline and the practical one: a custom rule
  object or a rule containing a `|` cannot go in a pipe string.
- **Persist `validated()`, never `all()`.** `validated()` returns only what passed.
- **Nested and array input** uses dot notation: `users.*.email`. `Rule::forEach()` gives you the
  value when the rule depends on it.
- `array:name,username` restricts which keys are permitted — otherwise unexpected keys pass through.

Documented security rules worth quoting:

> You should never pass any user controlled request input into the `ignore` method. Instead, you
> should only pass a system generated unique ID such as an auto-incrementing ID or UUID from an
> Eloquent model instance. Otherwise, your application will be vulnerable to an SQL injection attack.

> By default, the `image` rule does not allow SVG files due to the possibility of XSS
> vulnerabilities.

> You should never rely on validating a file by its user-assigned extension alone. This rule should
> typically always be used in combination with the `mimes` or `mimetypes` rules.

## Authorization

Gates for actions with no model; policies for anything about a resource. Laravel's own warning:

> Gates are a great way to learn the basics of Laravel's authorization features; however, when
> building robust Laravel applications you should consider using policies.

```php
class PostPolicy
{
    public function before(User $user, string $ability): bool|null
    {
        return $user->isAdministrator() ? true : null;   // null falls through
    }

    public function update(User $user, Post $post): Response
    {
        return $user->id === $post->user_id
            ? Response::allow()
            : Response::denyAsNotFound();   // 404 rather than confirming the row exists
    }
}
```

- **Policy discovery is convention-based:** `App\Models\Post` → `App\Policies\PostPolicy`. Break the
  convention and register with `Gate::policy()` or the `#[UsePolicy]` attribute on the model.
- **The `before` filter has a documented hole:** "the `before` method of a policy class will not be
  called if the class doesn't contain a method with a name matching the name of the ability being
  checked." An admin bypass silently fails for an ability you forgot to define.
- **Guests return `false` by default.** Type-hint `?User $user` to let a policy decide for guests.
- `Response::deny('message')`, `denyWithStatus(404)`, `denyAsNotFound()` control what the user learns.
  Prefer 404 where the existence of the record is itself privileged.
- Authorize in exactly one place per action — the form request, the attribute, the middleware, or the
  controller. Two places means one of them will drift.

## API responses

Use API resources rather than hand-built arrays; they keep the shape in one file.

```php
class OrderResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'total' => $this->total,
            'items' => ItemResource::collection($this->whenLoaded('items')),
        ];
    }
}
```

- **`whenLoaded()` is the N+1 guard.** Referencing `$this->items` directly makes the resource lazy
  load once per record in the collection.
- Laravel 13 ships **JSON:API resources** for spec-compliant output, handling relationship inclusion,
  sparse fieldsets, and links.
- Pick one envelope and keep it. A payload shaped differently per endpoint is a client's problem for
  years.
- Let exceptions render themselves. `abort(403)`, `abort(404)`, `ValidationException` and
  `AuthorizationException` already produce correct responses in both HTML and JSON contexts.

## Middleware

Registered in `bootstrap/app.php` — there is no `Http/Kernel.php`:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->web(append: [EnsureUserIsSubscribed::class]);
    $middleware->alias(['subscribed' => EnsureUserIsSubscribed::class]);
    $middleware->priority([/* ... */]);
})
```

In Laravel 13 the `web` group's forgery protection is `PreventRequestForgery`, which adds
origin-aware verification alongside token-based CSRF. Do not disable it globally to make an endpoint
work; exclude that route deliberately.

## Sources

- [Routing](https://laravel.com/docs/13.x/routing) · [Controllers](https://laravel.com/docs/13.x/controllers) · [Middleware](https://laravel.com/docs/13.x/middleware)
- [Validation](https://laravel.com/docs/13.x/validation) — the SQL injection, SVG, and file-extension warnings
- [Authorization](https://laravel.com/docs/13.x/authorization) — gates vs policies, the `before` warning, deny responses
- [Eloquent: API Resources](https://laravel.com/docs/13.x/eloquent-resources) — including JSON:API resources
- [CSRF Protection](https://laravel.com/docs/13.x/csrf) — `PreventRequestForgery`
- [Spatie: Laravel & PHP guidelines](https://github.com/spatie/guidelines.spatie.be/blob/master/content/code-style/laravel-php.md) — array rule syntax, conventions, the "follow the documented way" rule
