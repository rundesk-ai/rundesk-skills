# Components

Read this when writing or reviewing a `.vue` file: its shape, its inputs, its outputs, and its name.

## The single-file component

```vue
<script setup lang="ts">
// 1. imports
// 2. props / emits / models — the component's contract, first
// 3. composables
// 4. local state
// 5. computed
// 6. watchers
// 7. lifecycle
// 8. functions
</script>

<template>...</template>

<style scoped>...</style>
```

`<script setup>` is the default for new code: less boilerplate, better inference, and better runtime
performance than `setup()`. Put the contract — props, emits, models, slots — at the top, because that
is what a reader needs first.

## Props

```ts
const props = withDefaults(defineProps<{
  items: Item[]
  variant?: 'primary' | 'ghost'
}>(), { variant: 'primary' })
```

- **Use detailed prop definitions.** A Priority A rule: they document the API and let Vue warn on
  wrong types in development. Types via `defineProps<...>()` in TypeScript, runtime definitions
  otherwise — never the bare array form outside a prototype.
- **Never mutate a prop.** Vue: props "form a one-way-down binding… this prevents child components
  from accidentally mutating the parent's state, which can make your app's data flow harder to
  understand." `eslint-plugin-vue`'s `no-mutating-props` is in the *essential* preset.
- **Objects and arrays are passed by reference**, so a child *can* mutate their contents and Vue will
  not stop it — "it is unreasonably expensive for Vue to prevent such mutations." Vue's instruction is
  explicit: "the child should emit an event to let the parent perform the mutation."
- The two legitimate reasons people reach for mutation, and what to do instead:
  - *A prop as an initial value* → copy it into local state: `const count = ref(props.initialCount)`.
  - *A transformed prop* → a computed: `computed(() => props.size.trim().toLowerCase())`.
- **camelCase in script, kebab-case in the template.** Priority B.
- Prefer many small primitive props over one large config object — they diff better and keep the
  component's contract legible. See prop stability in [`performance.md`](performance.md).

## Events

```ts
const emit = defineEmits<{
  select: [id: string]
  'update:modelValue': [value: string]
}>()
```

Declare every event. A declared emit is documentation, gives type-checked payloads, and stops the
event falling through to the root element as a stray DOM listener. Name events for what happened
(`submitted`, `selected`), not for what the parent should do (`closeModal`) — the child does not know
what the parent wants.

## `v-model` and `defineModel`

```vue
<script setup>
const model = defineModel<string>()
const first = defineModel<string>('firstName')
</script>

<template><input v-model="model" /></template>
```

`defineModel()` (stable since 3.4) replaces the manual `modelValue` prop plus `update:modelValue`
emit, and it is a writable ref, so `v-model` on it inside the child works. Reach for the manual
prop + emit pair only when you need to transform on the way in or out.

## Slots

Slots are the answer to "this component needs to be flexible" far more often than another prop.

```vue
<!-- Scoped slot: the child owns the data, the parent owns the markup -->
<template>
  <li v-for="item in items" :key="item.id">
    <slot name="item" :item="item">{{ item.label }}</slot>
  </li>
</template>
```

- Provide fallback content so the common case needs no slot.
- A component with a growing set of `showX` / `hideX` booleans usually wanted a slot.
- Scoped slots are how a list component stays reusable without knowing what a row looks like.

## provide / inject

For passing something down a subtree without threading props through every level — a theme, a form
context, a design-system configuration.

```ts
// keys.ts
export const FormKey: InjectionKey<FormContext> = Symbol('form')

// parent
provide(FormKey, { register, unregister })
// descendant
const form = inject(FormKey)          // typed, because the key is typed
```

- **Use a typed `InjectionKey`**, not a string. It is the community-standard pattern (Anthony Fu's
  "typed provide/inject") and the only way the injected value is typed at the other end.
- **Provide readonly state** and provide mutators alongside it, so a descendant cannot silently change
  a parent's state.
- Do not use it as a general state manager. It is invisible coupling at a distance; if any component
  might need the value, that is a store. See [`state-and-routing.md`](state-and-routing.md).

## Template refs

```ts
const input = useTemplateRef('input')     // 3.5+; replaces a matching-name ref()
onMounted(() => input.value?.focus())
```

Refs are `null` until mount and `null` again after unmount. Reach for one only for what the DOM alone
can do — focus, measure, play, scroll. Reading child component internals through a ref is the
implicit coupling Vue's Priority D rule warns about.

## Naming

- **Multi-word component names**, always. Priority A, because every HTML element is a single word and
  `<Item>` can collide with a future one.
- **PascalCase** for files and for use in SFC templates; kebab-case in in-DOM templates.
- **Prefix by relationship, most general word first:** `SearchButtonClear`, not `ClearSearchButton`;
  `TodoListItem`, not `TodoItem`, when it is tightly coupled to `TodoList`. This makes the file list
  sort into families.
- **Base components** get a consistent prefix — `Base`, `App`, or `V`.
- **Full words over abbreviations:** `StudentDashboardSettings`, not `SdSettings`.

## Styling

- **Always scope component styles** — Priority A. `scoped`, CSS Modules, or a strict class convention.
- **Do not use element selectors inside `scoped`.** Priority D: `button[data-v-f3f3eg9]` is
  "considerably slower" than `.btn-close[data-v-f3f3eg9]`. Use a class.

## Sources

- [Style guide — Priority A: Essential](https://vuejs.org/style-guide/rules-essential) · [Priority B](https://vuejs.org/style-guide/rules-strongly-recommended) · [Priority D: Use with caution](https://vuejs.org/style-guide/rules-use-with-caution)
- [Props](https://vuejs.org/guide/components/props.html) — one-way data flow and the mutation warning
- [Events](https://vuejs.org/guide/components/events.html) · [v-model](https://vuejs.org/guide/components/v-model.html) · [Slots](https://vuejs.org/guide/components/slots.html) · [provide / inject](https://vuejs.org/guide/components/provide-inject.html)
- [`vue/no-mutating-props`](https://eslint.vuejs.org/rules/no-mutating-props) — in the essential preset
- [Composable Vue](https://antfu.me/posts/composable-vue-vueday-2021) — Anthony Fu on typed provide/inject and `useVModel`
