# Testing

Read this when testing components, composables, or Pinia stores.

## Assert the public behavior

Vue's rule is “test what a component does, not how it does it.” Assert rendered DOM from props and
slots, then rendered changes or emitted events after user input.

```ts
// Bad: coupled to an internal ref and its name.
expect(wrapper.vm.count).toBe(1)

// Good: observes the user's interaction and output.
await wrapper.get('[aria-label="Increment"]').trigger('click')
expect(wrapper.get('[data-testid="value"]').text()).toBe('1')
```

Do not call private methods directly or rely exclusively on snapshots. Extract a pure method when it
needs focused testing; otherwise cover it through component or end-to-end behavior. Avoid stubbing
every child in a component test—Vue recommends user-shaped interaction with as little mocking as
practical.

## Wait for Vue and exercise teardown

Vue batches DOM updates. Await `trigger`, `setProps`, and `nextTick` before reading the result.

A composable with lifecycle hooks needs an active component scope. Mount a minimal host, exercise the
behavior, and unmount it so listener, timer, subscription, and watcher cleanup actually runs. A pure
function or lifecycle-free composable can be called directly.

## Use the matching layer

- Vitest for pure logic and headless composables in Vite-based projects.
- Vitest plus Vue Test Utils for component rendering and interaction.
- The project's existing browser runner for behavior that depends on layout, native browser APIs, or
  multi-page flows.
- Pinia's testing helpers when a component consumes a store; test store actions and getters directly
  when the store itself is the subject.

Run `eslint-plugin-vue`'s essential preset and `vue-tsc` in CI. The linter catches prop mutation,
computed side effects, and missing list keys before a behavioral test has to reproduce them.

Evidence: [testing lessons in sources.md](sources.md#testing).
