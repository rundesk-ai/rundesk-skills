# Name data and contract fields

Dos and don'ts for anything stored or transmitted: tables, columns, enums, migrations, REST paths, API fields, error codes, webhook events, and structured logs.

These names outlive every screen built on top of them. A column name survives three interface redesigns and four engineers. Name it for the person reading it in 2031 with no context.

## Parity across layers

When compatibility and audience needs permit, use one canonical term for the same concept and express it in each layer's convention:

```
reason          column
reason          API field
reason          form field
Reason          label
Reason          export header
```

**The parity test:** trace each layer back to the same canonical concept. Do not require mechanical spelling parity when a stable public contract, localization, privacy boundary, computed value, or audience-specific label requires a documented mapping.

| Don't | Do |
|---|---|
| Column `why`, label `Reason` | Rename the column to `reason` |
| Column `sell_type`, label `Max buyers` | Rename to `max_buyers` and fix the type |
| Column `cust_flg`, API `customerType`, UI `Client` | Column `customer`, API `customer`, UI `Customer` |
| Mapping names in the view layer to hide a bad column | Fix the column |

Undocumented display-layer aliasing makes drift permanent: the next engineer reads the column, not the view mapping, and may invent a third name. Prefer descriptive names for new work; assess migrations, reports, integrations, and rollback before renaming stable data.

---

## Tables

**Common form:** plural, `snake_case`, and the lexicon noun. Follow the database, ORM, and repository convention when they establish another form.

| Don't | Do |
|---|---|
| `tbl_carrier`, `carrier_tb` | `carriers` |
| `carrier` (singular) | `carriers` |
| `usr`, `prod_ln` | `users`, `product_lines` |
| `data`, `records`, `misc_settings` | The actual concept |

**Join tables:** both entity names, singular, alphabetical unless the domain implies an order. `carrier_product_line`.

**Don't** prefix tables by module unless the database is genuinely shared across products. If you do, apply it uniformly, never to half the schema.

---

## Columns

**Common form:** `snake_case`, singular, naming the value. Follow the schema's convention; avoid redundant types, table prefixes, and non-domain abbreviations.

| Don't | Do | Why |
|---|---|---|
| `reason_text`, `name_str`, `count_int` | `reason`, `name`, `count` | The type is in the schema and it changes |
| `carrier_carrier_name` | `name` | The table already says carrier |
| `col1`, `field_2`, `misc` | The meaning | Unnameable means undesigned |
| `qty_rcv`, `dt_crt` | `quantity_received`, `created_at` | Save the keystrokes elsewhere |
| `why`, `who_asked` | `reason`, `requester_id` | Question words are not names |
| `sell_type_flag` | `max_buyers` | Names the mechanism, not the value |
| `notes2`, `extra_field` | Name the second meaning, or don't add it | A numeric suffix is a missing concept |

**Don't create a column you cannot define in one sentence.** If the definition needs "sometimes it holds X, but if Y then Z," you have two columns.

---

## Booleans in the database

**Recommended form:** use the schema's predicate convention. `is_` / `has_` / `can_` stated positively is a useful default.

| Don't | Do |
|---|---|
| `active` | `is_active` |
| `is_not_active`, `disabled`, `no_email` | `is_active`, `email_enabled` |
| `deleted` (when "when" matters) | `deleted_at` timestamp, null when live |
| `flag`, `status` holding true/false | Name the condition, or make it an enum |
| `is_active` + `is_archived` + `is_draft` | One `status` enum |

**Don't let booleans multiply into a state machine.** Three booleans express eight states, of which perhaps three are legal. Every query then carries a comment explaining which combinations are impossible. Use an enum from the moment a second mutually-exclusive flag appears.

**Never negate.** `WHERE NOT is_not_active` is a bug waiting for a tired reader.

---

## Timestamps and dates

**Form:** `{event}_at` for timestamps, `{event}_on` for dates. Name the event, not the tense or the type.

| Don't | Do |
|---|---|
| `date_created`, `when_archived`, `crt_dt` | `created_at`, `archived_at` |
| `timestamp`, `date`, `time` | The event it records |
| `effective_date_date` | `effective_on` |
| Undocumented local time in a timestamp | A documented timezone-aware strategy, commonly UTC; preserve domain-local dates or civil times when that is the business fact |

**Do** name for the business event, not the row operation. `received_at` (when the lead arrived) and `created_at` (when we inserted the row) are different facts, and conflating them destroys reconciliation.

**Do** document the temporal model. UTC timestamps are a strong default for instants; domain-local dates and civil times remain local when that locality is the fact being stored.

---

## Foreign keys and relations

**Form:** `{singular_entity}_id`.

| Don't | Do |
|---|---|
| `carrier`, `carrierid`, `fk_carrier` | `carrier_id` |
| `parent_id` with no indication of parent type | `parent_carrier_id` |
| `user_id` used for two different roles | `created_by_id`, `assigned_to_id` |

**Do** name role-bearing references by role, not by the target table. A table with two references to `users` needs `created_by_id` and `approved_by_id`, not `user_id` and `user_id_2`.

---

## Enums and stored states

**Form:** stored values are `snake_case` (or `SCREAMING_SNAKE`, chosen once per codebase). Values are **states**, expressed as adjectives or past participles.

| Don't | Do |
|---|---|
| `archive`, `suspend` | `archived`, `suspended` |
| `1`, `2`, `3` in the column | Named values |
| `Active`, `PENDING_REVIEW`, `paused` mixed | One case convention |
| `status` holding `'Archived (see notes)'` | The enum value only |

**Never store display strings.** Storing `Pending review` means a copy change becomes a data migration, and the same state renders three ways across the product.

**Do not render machine values directly.** Keep an authoritative stored-to-display mapping in each client or shared presentation layer. Localization and consumer-specific presentation may require separate mappings. A view that merely replaces underscores can turn `awaiting_carrier_confirm` into poor interface text.

**Do** keep the enum's legal values and their display terms together in the lexicon.

---

## Nullability semantics

Decide and document what each absent-value case means. Ambiguity here produces bugs that no amount of good naming fixes.

| State | Meaning | Renders as |
|---|---|---|
| `NULL` | One documented absence meaning for this field | `—` or the product's documented absence marker |
| Explicit state | Unknown and not applicable are different domain meanings | Distinct, localized labels |
| `0` | Known to be zero | `0` |
| `''` | Known to be empty | `—` or blank, chosen once |
| Sentinel (`-1`, `9999`) | Don't | Never use one |

| Don't | Do |
|---|---|
| `-1` meaning "unlimited" | A nullable column, or a separate `is_unlimited` boolean |
| `''` and `NULL` both used in one column | Pick one, add a constraint |
| Rendering `0` as `—` | They are different facts |

---

## Money, units, and precision

| Don't | Do |
|---|---|
| `price` as a float | `price_cents` as an integer |
| `amount` with no currency | `amount_cents` plus `currency_code` |
| `timeout`, `distance`, `size` | `timeout_seconds`, `distance_meters`, `size_bytes` |
| Percentages stored inconsistently (0.15 in one column, 15 in another) | One convention, named: `rate_bps` or `rate_percent` |

**Include the unit when it could be misread.** A number whose unit lives only in a doc comment can be misread, especially when it represents money.

---

## JSON columns

| Don't | Do |
|---|---|
| A `meta` or `data` blob absorbing new fields indefinitely | Promote recurring keys to real columns |
| Mixed key cases inside the document | The same convention as columns |
| Storing display strings or computed values | Store facts |

JSON columns are where naming discipline goes to die, because nothing enforces a schema. Anything queried, filtered, or shown in a table belongs in a column.

---

## Indexes and constraints

**Form:** `{table}_{columns}_{type}`. Predictable, so the name can be derived rather than looked up.

```
carriers_name_unique
leads_carrier_id_received_at_index
product_lines_carrier_id_foreign
```

Constraint names appear in raw database errors. A meaningful one lets you map a violation to a domain error and a user-facing message; `idx_4` does not.

---

## Migrations

**Form:** `{timestamp}_{verb}_{object}`. The verb states the schema change.

| Don't | Do |
|---|---|
| `update_table`, `fix_stuff`, `migration_12` | `rename_why_to_reason_on_suppressions` |
| `add_column` | `add_max_buyers_to_product_lines` |

**Do** enumerate the full fanout of a rename: column, index, constraint, API field, validation rule, form field, label, export header, saved filters or reports, and lexicon entry. Change private names atomically; stage stored and published contracts through expand, migrate, deprecate, and contract steps.

---

## REST paths

**Form:** plural nouns for resources; the HTTP method supplies the verb.

| Don't | Do |
|---|---|
| `POST /createCarrier` | `POST /carriers` |
| `GET /getCarrierById/4` | `GET /carriers/4` |
| `POST /carriers/4/doArchive` | `POST /carriers/4/archive` (a real state transition) |
| `/carrier`, `/Carriers`, `/product-Lines` | `/carriers`, `/product-lines` |

**Do** allow a verb in the path only for genuine actions that are not CRUD on a resource: `/carriers/4/archive`, `/invoices/9/send`. Do not use it as a workaround for a resource you have not modeled.

**Query parameters** are `snake_case` (or the API's single convention) and name the filter field: `?status=active&carrier_id=4`. Pagination parameters are consistent across every endpoint.

---

## API fields and payloads

| Don't | Do |
|---|---|
| Mixing `camelCase` and `snake_case` in one payload | One convention, API-wide |
| Leaking accidental internal names into a public contract | Use the canonical concept term or document an intentional API mapping |
| Returning raw enum plus a display string | Return the enum; the client maps it |
| `id` of ambiguous type across endpoints | Consistent identifier type and format |
| Booleans named negatively | Positive form |

**Do** treat the API contract as a published vocabulary. Renaming a field is a breaking change; preserve existing versions and introduce a replacement through the API's compatibility policy.

---

## Error codes and messages

**Code form:** `SCREAMING_SNAKE_CASE`, `{ENTITY}_{CONDITION}`. Stable forever; clients branch on it.

| Don't | Do |
|---|---|
| `ERR_5`, `BAD_REQUEST` for everything | `CARRIER_NAME_TAKEN`, `RATE_SHEET_EXPIRED` |
| Changing a code's meaning | Add a new code |
| Codes derived from HTTP status alone | The domain condition |

**Message form:** name the entity and condition, then write detail for the audience. UI text needs recovery; logs need safe diagnostics; API clients need a stable code.

| Don't | Do |
|---|---|
| `Something here already goes by that name` | `A carrier with that name already exists.` |
| `Invalid value` | `max_buyers must be between 1 and 8.` |
| `SQLSTATE[23000]: Integrity constraint violation` | Map to a domain error at the boundary |
| `The received_at field must be a valid date.` | Rewrite framework defaults in display language |

**Do** include a reference identifier on unexpected errors so a user's report maps to a log line.

---

## Webhooks and published events

**Common form:** `{entity}.{past-tense verb}`, lowercase and dotted. Follow the published event convention when it differs.

| Don't | Do |
|---|---|
| `carrierUpdate`, `CARRIER_EVENT`, `carrier.change` | `carrier.archived`, `carrier.rates_updated` |
| `carrier.archive` (imperative) | Past tense. If it has not happened, it is a command, not an event. |
| `row_updated` | The business fact |

**Do** name for the business fact rather than the row write. `invoice.paid` survives a schema redesign; `invoices_updated` forces every consumer to diff payloads to find out what happened.

---

## Structured logs and metrics

**Log field keys** use the canonical concept term where contracts permit, with documented mappings for deliberate differences. A support engineer should be able to trace `carrier_id` across storage, payloads, and logs.

| Don't | Do |
|---|---|
| `cid`, `carrierID`, `carrier` used across three services | `carrier_id` everywhere |
| Free-text log lines with values interpolated into prose | Structured fields plus a short factual message |
| `log.info("doing the thing now")` | `log.info("archiving carrier", carrier_id=4)` |

**Metric names:** follow the metrics ecosystem. Prometheus commonly uses `{subsystem}_{measure}_{unit}`, such as `carrier_rate_sync_duration_seconds`; other systems differ. Include the unit whenever ambiguity is possible.

---

## Files, exports, reports

| Don't | Do |
|---|---|
| Export headers that differ from on-screen column headers | Identical strings |
| `export(1).csv`, `report_final.xlsx` | `carriers_2026-03-04.csv` |
| Raw enum values in an export | The display terms the user sees on screen |

A user reconciling a spreadsheet against a screen should never have to translate between two vocabularies for the same data. Export headers are a UI slot that happens to live in a file.
