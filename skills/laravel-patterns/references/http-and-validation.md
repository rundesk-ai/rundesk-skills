# HTTP, validation, and authorization

Read this for route binding, form requests, file validation, policies, or API resources.

## Treat binding and authorization as separate checks

Scoped route binding ensures a child belongs to its parent; it does not prove the current user may
access either model.

```php
// Bad: ownership is scoped, but user access is unchecked.
Route::get(
    '/accounts/{account}/projects/{project}',
    [ProjectController::class, 'show'],
)->scopeBindings();

// Good: keep scoped binding and authorize inside the action or request.
public function show(Account $account, Project $project): ProjectResource
{
    Gate::authorize('view', $project);

    return new ProjectResource($project);
}
```

Name routes so redirects survive URL changes. Rate-limit public write and authentication endpoints
with a named limiter whose policy matches the product; do not paste a universal threshold.

## Validate and authorize before persistence

Use a form request once rules or authorization would distract from the controller. Prefer array rule
syntax: it accepts rule objects and values containing `|`, which pipe strings cannot represent
safely.

```php
final class StoreOrderRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('create', Order::class);
    }

    public function rules(): array
    {
        return [
            'items' => ['required', 'array', 'min:1'],
            'items.*.sku' => ['required', Rule::exists('products', 'sku')],
        ];
    }
}
```

Persist `validated()`, not `$request->all()`. For arrays, constrain permitted keys with
`array:name,username`; otherwise Laravel validates the array but may return unvalidated nested keys
inside it.

Three Laravel warnings deserve explicit review:

```php
// Bad: attacker-controlled SQL fragments can reach the unique rule.
Rule::unique('users')->ignore($request->input('id'));

// Good: use the route-resolved model or its trusted key.
Rule::unique('users')->ignore($user);
```

- Do not validate an upload by its user-assigned extension alone; combine extension checks with
  MIME/content validation.
- The `image` rule rejects SVG by default because SVG can carry XSS. Enable `allow_svg` only with a
  deliberate sanitization and delivery policy.

## Keep policy fall-through explicit

Use policies for resource abilities. A `before()` method should return `true` or `false` for a final
decision and `null` to continue to the named ability method.

Laravel's gotcha: `before()` is not called unless the policy class contains a method matching the
checked ability. Define the ability; do not assume an administrator bypass covers a misspelled or
missing method.

Use `denyAsNotFound()` when even confirming a resource exists would leak privileged information.
Client-visible `can` flags may shape a UI, but the server must still authorize the request.

## Prevent resource-level N+1

```php
// Bad: each resource can lazy-load items.
'items' => ItemResource::collection($this->items),

// Good: serialization includes only relationships the query loaded intentionally.
'items' => ItemResource::collection($this->whenLoaded('items')),
```

Pair `whenLoaded()` with eager loading in the controller; it prevents accidental resource queries but
does not fetch missing data. Keep the response envelope consistent rather than hand-building a new
shape in each controller.

## Match session lifetime to the request flow

State that exists after a POST but disappears after its redirected GET was likely flashed for only
the next request. A direct post-response assertion misses that browser-visible failure.

```php
// Bad: a later workflow step needs this after the redirect target has rendered.
return to_route('review')->with('workflow.result', $result);

// Good: keep multi-request state until the workflow consumes it.
$request->session()->put('workflow.result', $result);
// In the later request:
$result = $request->session()->pull('workflow.result');
```

Exercise the POST, redirect target, and later request in order, then assert the final response props.

## Follow the installed skeleton

On Laravel 11+, middleware registration belongs in `bootstrap/app.php`, not
`app/Http/Kernel.php`. Exclude exceptional routes narrowly from CSRF/request-forgery middleware;
never disable the protection application-wide to fix one endpoint.

The exact source mapping for every pair and warning is in [`sources.md`](sources.md).
