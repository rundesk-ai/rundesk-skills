---
name: naming-software
description: Use when choosing, reviewing, or standardizing names and product language across source code, schemas, APIs, logs, and user interfaces, especially when one domain concept crosses several layers. It supplies a lexicon-led workflow for keeping terms precise, consistent, and appropriate to each layer. Do not use for general prose editing, marketing copy, or work where naming is incidental.
---

# Name software

Name the concept or value, then express that meaning in the convention of each layer.

## Establish the vocabulary

1. Read the repository's glossary, schema, public contracts, nearby code, and rendered interface.
2. Identify the thing being named: domain concept, stored value, action, state, event, error, or interface slot.
3. Reuse the established domain term when two layers mean the same thing. Do not create a synonym to
   make one file sound smoother.
4. Preserve a deliberate difference when the meanings, audiences, compatibility promises, privacy
   boundaries, or localization needs differ. Record the mapping instead of pretending the names are
   interchangeable.
5. If no vocabulary owner exists and the term will recur, propose a small lexicon. Do not create or
   rewrite product vocabulary without authority from the owner.

Use [the lexicon reference](references/lexicon.md) when creating or repairing a product vocabulary.

## Put words in the right slot

- Use nouns for values, entities, and collections: `retry_count`, `Invoices`, `Reason`.
- Use verbs for actions and behavior: `archiveInvoice()`, `Retry payment`.
- Use states for state values: `pending_review`, `Archived`.
- Keep a name short enough to scan. Put consequences, constraints, and recovery instructions in the
  description, help text, docstring, or error detail that owns them.
- Avoid placeholders such as `data`, `item`, `helper`, `manager`, and `process` when a more precise
  domain term is known.

Read [code naming](references/code.md) for identifiers, booleans, functions, types, errors, events,
configuration, and tests. Read [data and contracts](references/data-and-contracts.md) for schemas,
API fields, enums, units, logs, and compatibility-sensitive renames. Read [product interface text](references/product-ui.md)
for labels, controls, accessible names, errors, empty states, and feedback.

## Follow the owning convention

Meaning should stay stable; spelling and casing may change by layer. Follow the language, framework,
database, protocol, and design-system conventions already in force. A Python identifier, SQL column,
JSON field, and visible label do not need identical spelling to represent the same concept.

When conventions conflict, prefer in this order:

1. regulated or contractual wording;
2. published compatibility promises;
3. domain language used by practitioners;
4. language, framework, protocol, and accessibility conventions;
5. the repository's established house style;
6. this skill's defaults.

Do not introduce a second convention during an unrelated change. Record drift and plan a migration.

## Review across boundaries

For a new or changed term:

1. Search for the canonical term, known synonyms, abbreviations, and stored values.
2. Trace persistence, code, API clients, events, logs, analytics, documentation, tests, and interface
   text that carry the concept.
3. Distinguish a wording-only change from a contract or data migration.
4. Stage compatibility-sensitive renames with expand, migrate, deprecate, and contract steps. A public
   API rename is not a copy edit.
5. Keep stable machine values separate from localized or audience-specific display text.
6. Test the affected contracts and inspect the rendered or emitted result.

## Verify the result

- The name identifies one meaning at its point of use.
- Distinct meanings do not share one vague term.
- Repeated concepts use the repository's canonical vocabulary or document an intentional mapping.
- Explanations are not compressed into labels or identifiers.
- Accessible names contain the visible control label and still distinguish the control.
- Errors identify the affected subject and give the intended audience a useful recovery path.
- Renames preserve stored data and published consumers for the promised compatibility window.

