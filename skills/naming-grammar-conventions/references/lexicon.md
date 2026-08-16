# Maintain the product lexicon

The conventions in this skill are defaults; each product's vocabulary is specific to its domain. Keep a lexicon when terms recur across teams or layers, and look terms up before coining synonyms.

This is the load-bearing artifact. Consistency is unreachable through better writing, because every file and screen written independently invents a fresh synonym for the same idea. Consistency is only reachable through lookup.

## Where it lives

Keep the lexicon in a repository location documented for contributors and agents, such as `docs/lexicon.md` or beside the schema.

## Rules

- When a recurring concept is missing, confirm the term from product evidence or an appropriate owner, then update the lexicon with the naming change.
- One entry per concept, not per layer. The entry carries every layer's form of the term.
- The **avoid list matters alongside the canonical term.** It makes known synonym drift reviewable while allowing contextual uses that carry another meaning.
- Enum display values are lexicon entries.
- When a term is renamed, update the lexicon with the implementation when feasible. For a staged migration, record current, target, and compatibility forms.
- Requirements documents are not the lexicon. PRD prose describes mechanisms; the lexicon names values.

---

## Template

```markdown
# Lexicon

## Product decisions

Register:            operator
Case (UI):           sentence case everywhere
Case (columns):      snake_case
Case (API):          snake_case
Case (code):         camelCase identifiers, PascalCase types
Enum storage:        snake_case
Dates shown as:      Mar 4, 2026, 2:14 PM EST
Currency:            integer minor units, column suffix _cents
Null renders as:     —
Toasts:              suppressed when the result is visible on screen
Persist verb:        save   (not store, not persist)
Read verbs:          get (in-memory) / fetch (I/O) / find (may be empty)

## Terms

### Consumer
display:     Consumer
plural:      Consumers
column:      consumer_id, consumers
api:         consumer
code:        Consumer, consumer
definition:  The person on a lead. The subject of suppression.
avoid:       user, customer, contact, person, lead owner, "who asked", they

### Carrier
display:     Carrier
plural:      Carriers
column:      carrier_id, carriers
api:         carrier
code:        Carrier, carrier
definition:  An insurance carrier that buys leads.
avoid:       provider, company, partner, vendor, "something here"

### Max buyers
display:     Max buyers
column:      max_buyers  (integer, 1–8, default 3)
api:         max_buyers
code:        maxBuyers
definition:  How many buyers a lead can be sold to. 1 sells it exclusively.
avoid:       exclusivity, sharing model, buyer count, "how a lead is sold"

### Reason
display:     Reason
column:      reason  (text)
api:         reason
code:        reason
definition:  Why a consumer was added to the suppression list.
avoid:       why, note, explanation, cause

## Enums

### Carrier status
stored       display        meaning
active       Active         Currently buying leads.
paused       Paused         Temporarily not receiving leads. Configuration retained.
archived     Archived       No longer in use. Retained for historical records.
avoid:       inactive, disabled, off, deleted, "turned off"
```

---

## Building the first lexicon for an existing product

1. **Inventory the nouns.** List every table, every top-level API resource, and every page title. That is most of the domain.
2. **Find the collisions.** Grep for the obvious synonym clusters (`user` / `customer` / `client`, `delete` / `remove` / `archive`). Each cluster is one concept wearing several names, or two concepts sharing one. Both need deciding.
3. **Ask practitioners and check the contracts.** Prefer the term people in the domain use consistently while checking user comprehension, accessibility, legal wording, and published compatibility. A legacy schema name does not decide the vocabulary by itself.
4. **Record discouraged alternatives.** Build the avoid list from the synonym drift found in step 2 and state intentional exceptions.
5. **Decide the product-level settings** at the top of the file once, so they are not re-litigated per screen.
6. **Do not mass-rename without a migration plan.** Record current, target, and compatibility forms; then make bounded, compatibility-safe changes. An undocumented partial rename adds another vocabulary state.

## Maintain the lexicon

- Any pull request introducing a new domain concept updates the lexicon in the same change.
- Any rename updates the lexicon in the same change as the migration.
- Periodically search code and interface strings for entries on the avoid lists. Classify every hit as drift, an intentional distinct meaning, or a lexicon entry to revise.
