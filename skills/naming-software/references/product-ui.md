# Product interface text

Read this when naming interface structure, controls, data, feedback, or accessible elements. Follow
the product's design system and content style first.

## Match the slot

Give each string one job:

| Slot | Useful form | Put elsewhere |
|---|---|---|
| Page, section, tab, or column | Short noun phrase naming the content | Instructions and consequences |
| Button or menu action | Verb plus subject, or an established concise action | Feature explanation |
| Field label | The requested value or question in the product's form style | Format examples and constraints |
| Help or hint | Constraint, consequence, or format needed before acting | The field's name |
| Error | Affected subject, problem, and recovery appropriate to the audience | Stack traces and internal codes |
| Empty state | What is absent and the next available action, when one exists | Marketing copy |

Sentence case is a strong default for English product interfaces, but keep the design system's
established capitalization and exceptions. Use parallel grammar for parallel controls.

Do not rely on punctuation bans as a substitute for slot discipline. Fragments, full sentences,
questions, regulated wording, and localized strings legitimately use different punctuation.

## Labels and descriptions

Keep labels concise and familiar to the audience. Move explanation into persistent help when a
choice affects money, permissions, deletion, or downstream behavior. Use a tooltip only when it is
available by keyboard, focus, touch, and assistive technology; hover alone cannot carry required
information.

Placeholder text is an example or affordance, not a replacement for a label. It disappears during
entry and can leave the value without context.

## Accessible names

Give every interactive control a programmatic name that identifies its purpose. Prefer visible,
native labels. When a visible label exists, include that text in the accessible name in the same
order so speech-input users can invoke it. Additional context may distinguish repeated controls;
exact equality is not required.

Name icon-only controls with the action and subject, such as `Delete invoice`, rather than the icon's
appearance. Keep decorative images out of the accessibility tree; describe the information conveyed
by informative images.

## Data display

Use column headers that name the values beneath them. Put definitions or formulas in accessible help,
not in a sentence-length header. Keep a stable display term for each state within one product and
localization context.

Render missing, zero, empty, unavailable, and redacted values distinctly when they mean different
things. Choose those representations in the product vocabulary rather than per table.

If a value is truncated, provide an operable way to reveal or copy the full value. Do not force an
extremely long value into every accessible name.

## Errors and feedback

Write errors for recovery:

1. identify the affected field or action;
2. state what is wrong without blaming the person;
3. state the correction when the system knows it;
4. preserve diagnostic details in logs or stable machine fields rather than exposing internals.

Use the same field term in the label, inline error, and error summary. Confirm completion when the
result is not otherwise evident. Do not claim success before the operation has reached a durable
successful state.

## Review

- Inspect the rendered interface at realistic widths and with localization expansion where relevant.
- Navigate controls by keyboard and verify visible labels against accessible names.
- Read repeated table headers, statuses, and errors as an operator scanning them many times.
- Search for competing display terms and decide whether they represent synonyms or real distinctions.

