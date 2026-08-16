# Product lexicon

Use a lexicon when domain terms recur across teams or layers, synonyms are already drifting, or a
rename needs an explicit target. Do not require one for a small codebase with a clear existing owner.

Keep it in a repository location agents and contributors already inspect, such as `docs/lexicon.md`
or beside the schema. Link it from the repository's contributor instructions when it governs changes.

Record one entry per concept, not one per file. Include only forms the product actually uses.

```markdown
# Product lexicon

## Decisions

Interface register: operator
Interface capitalization: sentence case
Missing value: —
Duration unit: seconds

## Terms

### Invoice

- Display: Invoice; plural Invoices
- Schema: `invoice_id`, `invoices`
- API: `invoice`
- Code: `Invoice`, `invoice`
- Definition: A request for payment issued to an account.
- Avoid: bill, charge, payment request
- Intentional mappings: Provider API calls the same object `statement`.

### Payment status

| Stored | Display | Meaning |
|---|---|---|
| `pending` | Pending | Submitted but not settled. |
| `paid` | Paid | Settled successfully. |
| `failed` | Failed | Reached a terminal failure. |
```

## Build or repair it

1. Inventory schema entities, API resources, page titles, states, and recurring operational nouns.
2. Find synonym clusters and overloaded terms. Decide whether they are drift or distinct meanings.
3. Ask practitioners which term identifies the concept; do not let an accidental legacy column
   decide the domain language by itself.
4. Record canonical forms, definition, avoided synonyms, and intentional boundary mappings.
5. Migrate incrementally. A lexicon records the target; it does not authorize breaking contracts.

Update the lexicon with a new recurring concept or approved rename. Periodically search avoided
synonyms, then classify each hit before changing it.

