# Composables

Read this when extracting reusable logic, or reviewing a `use*` function.

A composable is a function that uses Vue's reactivity to encapsulate stateful logic. It is the unit of
reuse that replaced mixins, and the place most component logic should end up.

## The conventions

```ts
export function useUserSearch(query: MaybeRefOrGetter<string>) {
  const results = shallowRef<User[]>([])
  const loading = ref(false)
  const error = ref<Error | null>(null)

  watch(() => toValue(query), async (q) => {
    if (!q) { results.value = []; return }
    const controller = new AbortController()
    onWatcherCleanup(() => controller.abort())

    loading.value = true
    try {
      results.value = await searchUsers(q, controller.signal)
      error.value = null
    } catch (e) {
      if (e.name !== 'AbortError') error.value = e as Error
    } finally {
      loading.value = false
    }
  }, { immediate: true })

  return { results, loading, error }
}
```

Every rule below is visible in that example.

## Naming

`camelCase`, starting with `use`. Vue: "it is a convention to name composable functions with camelCase
names that start with `use`." Anthony Fu's community convention extends it: `useXxx` for composables,
`createXxx` for factories, `onXxx` for event-shaped helpers.

## Accept refs, getters, or values

Take `MaybeRefOrGetter<T>` and normalize with `toValue()`. Vue: "if you are writing a composable that
may be used by other developers, it's a good idea to handle the case of input arguments being refs or
getters instead of raw values."

Then make sure it is *tracked*: "if your composable creates reactive effects when the input is a ref
or a getter, make sure to either explicitly watch the ref / getter with `watch()`, or call `toValue()`
inside a `watchEffect()`." Calling `toValue()` once at the top of the function reads it exactly once
and tracks nothing — a common mistake.

## Return a plain object of refs

Vue: "the recommended convention is for composables to always return a plain, non-reactive object
containing multiple refs. This allows it to be destructured in components while retaining reactivity."

Return a `reactive()` object and every consumer that destructures gets dead values.

Where a composable produces one primary value, VueUse's convention is to return the value directly and
offer a `controls: true` option for the fuller shape — one obvious return for the common case, an
escape hatch for the rest.

## Own your side effects, and clean them up

Vue permits side effects in composables with two conditions:

1. **SSR safety** — "perform DOM-specific side effects in post-mount lifecycle hooks, e.g.
   `onMounted()`. These hooks are only called in the browser."
2. **Cleanup** — "remember to clean up side effects in `onUnmounted()`."

A composable that adds a listener removes it. A composable that opens a socket closes it. The caller
should never have to know an effect exists, and a composable that leaks is worse than inline code
because it leaks everywhere it is used.

## Call them synchronously, in `setup`

Vue: "composables should only be called in `<script setup>` or the `setup()` hook. They should also be
called **synchronously** in these contexts."

The reason is mechanical: Vue must know the active component instance so lifecycle hooks and watchers
can be registered to it "and disposed when the instance is unmounted to prevent memory leaks."

So:

```ts
// ❌ conditional, in a handler, in a callback, after a non-setup await
if (cond) { const { x } = useThing() }
onClick(() => useThing())

// ✅ top level, unconditional
const { x } = useThing()
```

The one exception: `<script setup>` is "the only place where you can call composables **after** using
`await`" — the compiler restores the instance context for you.

## Keep the scope one concern

- One composable, one concern. `useUser` that also handles routing and toasts is three composables.
- Composables compose — call one from another rather than growing a large one.
- If a function needs no reactivity, make it a plain function in `utils/`, not a `use*`. A composable
  that never touches a ref is a utility wearing a costume, and it cannot be tested without a component
  context that it does not need.
- Design for composition. Anthony Fu's framing: "think your functions like LEGO, there should have
  many different ways of composing them."

## Shared state: the SSR trap

```ts
// ❌ module-level state — one instance shared by every request on the server
export const useCart = () => { /* closes over a module-scope ref */ }
```

A module is initialized once per server process, so module-level reactive state is shared across every
user's request. This is the same cross-request pollution Vue documents for SSR generally, and it is the
single most dangerous composable mistake.

Either scope the state per app with a `create*` + `provide`/`inject` plugin pattern, or use Pinia,
which scopes state to the request by design. See [`state-and-routing.md`](state-and-routing.md).

## Why not mixins

Mixins have three problems composables fix: the source of a property is invisible at the use site,
namespaces collide silently, and there is no way to pass arguments or take multiple instances. A
composable is a function call with an explicit return — every one of those disappears.

## Sources

- [Composables](https://vuejs.org/guide/reusability/composables.html) — naming, `toValue`, return shape, side effects, and the synchronous call-site rule
- [Reactivity utilities](https://vuejs.org/api/reactivity-utilities) — `toValue`, `toRefs`, `unref`
- [Composable Vue](https://antfu.me/posts/composable-vue-vueday-2021) — Anthony Fu: `MaybeRef`, flexible arguments, self-cleaning effects, SSR-friendly shared state
- [VueUse guidelines](https://vueuse.org/guidelines) — options objects, `controls`, `isSupported`, configurable `flush`/`immediate`, `tryOnScopeDispose`
- [Good practices and design patterns for Vue composables](https://dev.to/jacobandrewsky/good-practices-and-design-patterns-for-vue-composables-24lk)
- [SSR: cross-request state pollution](https://vuejs.org/guide/scaling-up/ssr.html)
