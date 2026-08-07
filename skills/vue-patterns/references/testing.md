# Testing

Read this when writing or reviewing tests for Vue code.

## The principle

Vue's own line, and the whole discipline follows from it:

> **"Test what a component does, not how it does it."**

And the corresponding prohibition:

> "Don't assert the private state of a component instance or test the private methods of a component.
> Testing implementation details makes the tests brittle, as they are more likely to break and require
> updates when the implementation changes."

A component's job is to render correct DOM from its inputs and emit correct events from user actions.
Those are the two things worth asserting.

## What to assert

| Kind of logic | Assert |
|---|---|
| Visual | The render output, given props and slots |
| Behavioural | The render update or the emitted event, given a user input event |

```ts
const wrapper = mount(Stepper, { props: { max: 1 } })

expect(wrapper.find('[data-testid=value]').text()).toContain('0')
await wrapper.find('[data-testid=increment]').trigger('click')
expect(wrapper.find('[data-testid=value]').text()).toContain('1')
```

Note the `data-testid` selectors. Querying by CSS class couples the test to styling; querying by
component internals couples it to the implementation.

## What not to assert

- `wrapper.vm.someInternalRef` — internal state.
- A private method called directly. Vue's own advice: "if a method needs thorough testing, extract it
  as a standalone utility function" — which is the same pressure toward extraction described in
  [`separation-of-concerns.md`](separation-of-concerns.md).
- Whole-component snapshots as the primary assertion. Vue: "don't rely exclusively on snapshot tests."
  A snapshot fails on every cosmetic change and passes on most real regressions, so it is reviewed by
  approving the diff — which is not review.
- That a child component received a prop, when you could assert what the user sees instead.

## The layers

| Layer | Scope | Tool |
|---|---|---|
| **Unit** | Pure functions, composables | Vitest |
| **Component** | Mounting, rendering, interaction | Vitest + `@vue/test-utils` |
| **End-to-end** | Multi-page flows against a real build | Playwright or Cypress |

Vue recommends Vitest explicitly: it "is a unit testing framework designed specifically for this
purpose, created and maintained by Vue / Vite team members," and it reuses the project's existing Vite
config and transform pipeline.

## Testing composables

A composable with no lifecycle hooks is a plain function — call it and assert.

One that registers hooks or watchers needs a component context, because Vue can only bind them to an
active instance:

```ts
function withSetup<T>(composable: () => T) {
  let result!: T
  const app = createApp({ setup() { result = composable(); return () => {} } })
  app.mount(document.createElement('div'))
  return [result, app] as const
}

const [{ count, increment }, app] = withSetup(() => useCounter())
increment()
await nextTick()
expect(count.value).toBe(1)
app.unmount()          // proves the teardown path runs
```

Unmounting at the end is worth doing deliberately: it is the only place the cleanup path gets
exercised, and an effect that never tears down is the leak described in
[`reactivity.md`](reactivity.md).

## Practicalities

- **`await` anything that changes state** — `trigger`, `setProps`, `nextTick`. Vue's DOM updates are
  batched, so a synchronous assertion reads the previous render. This is the most common false failure
  in a Vue test suite.
- **Stub the boundary, not the component.** Mock the API module; render the real child components. A
  test that stubs everything asserts only that `mount` works.
- **Test a store as a store** — call actions, assert state and getters. `createTestingPinia()` for
  components that consume one.
- **Test the route-independent thing.** A view taking `props: true` from the router is testable without
  a router at all, which is one reason to prefer it.
- **Assert accessible output** where you can — role and label rather than class. It tests the thing the
  user actually gets, and it catches accessibility regressions for free.

## The static layer

Two checks catch more real Vue bugs than most tests, and they run in a second:

- **`eslint-plugin-vue`**, at least the *essential* preset. It encodes the Priority A rules as lint:
  `no-mutating-props`, `no-side-effects-in-computed-properties`, `require-v-for-key`.
- **`vue-tsc`** for type checking `.vue` files in CI. `defineProps<...>()` and `defineEmits<...>()` only
  pay off if something checks them.

## Sources

- [Testing](https://vuejs.org/guide/scaling-up/testing.html) — the principle, what not to test, the tool recommendations
- [Testing composables](https://vuejs.org/guide/scaling-up/testing.html#testing-composables)
- [Vue Test Utils](https://test-utils.vuejs.org/) · [Vitest](https://vitest.dev/)
- [Testing Pinia stores](https://pinia.vuejs.org/cookbook/testing.html)
- [`eslint-plugin-vue` — available rules](https://eslint.vuejs.org/rules/)
