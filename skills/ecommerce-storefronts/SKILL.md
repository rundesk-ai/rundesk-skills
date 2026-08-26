---
name: ecommerce-storefronts
description: Use when planning, designing, building, reviewing, operating, or growing a multi-product online shop, including storefront navigation, category and search discovery, merchandising, product pages, carts, checkout UX, limited sales and promotions, inventory visibility, abandonment recovery, post-purchase service, retention, ecommerce CVR, and shop A/B tests. It supplies an evidence-backed workflow for turning product and operating truth into a usable store, trustworthy offers, measurable browse-to-buy outcomes, and profitable experiments. Do not use it for a dedicated campaign landing page, payment-processor implementation, SEO-only work, or generic UI work without a commerce journey.
---

# Ecommerce storefronts

Build the shop as one commercial and operational system. Help the right shopper find, understand,
buy, receive, and—when appropriate—buy again. Optimize retained contribution, not gross sales,
clicks, add-to-carts, or attributed revenue in isolation.

## Establish the commerce contract

Before choosing a layout or promotion:

1. Define the audience, assortment, acquisition channels, devices, markets, currencies, fulfillment
   methods, service capacity, and new-versus-returning customer mix.
2. Name the authoritative owner and freshness rule for product family, variant or SKU, price,
   promotion, salable inventory, delivery estimate, returns terms, review provenance, compatibility,
   order, cancellation, return, and refund state.
3. Map the shortest successful journey from arrival through discovery, product decision, cart,
   checkout, accepted order, fulfillment, support, and repeat purchase. Include empty, unavailable,
   delayed, partial, failed, cancelled, returned, and refunded paths.
4. Define commercial truth. Reconcile analytics with accepted orders, discounts, cancellations,
   refunds, returns, fraud, cost of goods, payment cost, fulfillment, support, and promotion cost.
5. Record constraints: inventory and fulfillment capacity, truthful claims, accessibility,
   performance, privacy, marketing permission, consumer law, tax, and processor rules. Route current
   jurisdiction-specific conclusions to qualified review rather than freezing them in storefront
   copy or code.

Use a locally defined contribution model, for example:

```text
retained revenue = accepted item revenue - cancellations - refunds - returns
contribution     = retained revenue - discounts - product cost - payment cost
                   - fulfillment cost - variable service and promotion cost
value/session    = contribution attributable to eligible sessions / eligible sessions
```

Change the components to match the business. Do not call gross merchandise value profit or assume
an analytics `purchase` event proves retained value.

## Make the assortment understandable

Let a new visitor infer what the shop sells and reach a useful product scope without knowing the
internal catalog. Use categories for materially different product groups and filters for shared
attributes such as size, color, brand, compatibility, capacity, or material. Build taxonomy and
search from product data, query logs, support language, and representative shopping tasks—not the
organization chart.

Treat these as distinct discovery jobs:

- known-item search by title, model, SKU, or brand;
- category browsing and comparison;
- feature, fit, compatibility, or problem-based search;
- refinement through filters and sorting;
- recovery from misspellings, ambiguity, unavailable products, and zero results; and
- return to a stable list after viewing a product.

Keep active filters and sort visible, preserve state across back navigation, and provide a useful
zero-results recovery path. Never silently substitute unrelated products and imply they match.

Read [discovery-merchandising-and-products.md](references/discovery-merchandising-and-products.md)
when specifying the homepage, navigation, catalog taxonomy, onsite search, autocomplete, product
lists, filters, sorting, product cards, product pages, variants, media, reviews, recommendations, or
availability messages.

## Preserve product and offer truth

Every entry route must resolve to the same product and selected variant the shopper was promised.
Update identity, media, price, currency, stock, delivery, and purchase state together when the
variant changes. Show the current price and material conditions near the buying action; distinguish
a universal sale from a coupon, membership price, quantity break, or conditional offer.

Only show proof the business can substantiate. Ratings need a real count and provenance; product
claims need supporting product data; compatibility must be guaranteed by its owner; scarcity must
come from current salable inventory or a real promotion window. Suppress an unsupported claim
instead of filling the page with fabricated reviews, badges, stock counts, demand messages, or
urgency.

## Design the purchase journey as recoverable state

Treat cart, checkout, payment, order, fulfillment, return, and refund as related but distinct states.
The cart records the shopper's intended product, variant, quantity, and selections; the server
revalidates price, promotion, stock, delivery, and terms before accepting the order. A browser
redirect, payment authorization, or thank-you route is not the authoritative accepted order.

Default to a prominent guest path unless the business genuinely requires an account. Offer optional
account creation after purchase with a concrete benefit and reuse already supplied information.
Collect only the address and contact data required for the selected market and fulfillment method;
support autofill, tolerant input, precise errors, preserved values, and a manual recovery path.

Reveal known mandatory costs early and show how uncertain shipping or tax estimates will be
resolved. Never auto-add a warranty, donation, subscription, insurance, or accessory. Keep promo
entry available without making an empty coupon box the visual focus; explain ineligible, expired,
non-stackable, or replaced promotions rather than failing silently.

When Laravel and Stripe are in use, use `laravel-stripe-payments` for processor choice, PCI scope,
PaymentIntents or Checkout, subscriptions, wallets, webhooks, idempotency, refunds, disputes,
Connect, payouts, and ledger implementation. Otherwise use the active payment-integration owner and
current processor and PCI documentation. Use `frontend-design` alongside this skill for form
behavior, accessibility, responsive interaction states, and rendered verification.

Read [cart-checkout-and-operations.md](references/cart-checkout-and-operations.md) when specifying
cart persistence, guest checkout, address and delivery choices, inventory reservations, limited
sales, order states, cancellations, returns, recovery messages, loyalty, support, fraud, or dispute
handoffs.

## Run promotions as controlled commercial events

Write a promotion contract before publishing the creative:

```text
objective and eligible audience
eligible products and variants
reference price and discount rule
start, end, timezone, and channels
inventory allocation and reservation policy
stacking, exclusions, quantity limits, and refund allocation
fulfillment and support capacity
primary metric, contribution guardrail, holdout, and rollback
```

Start and end the offer consistently across storefront, product data, feeds, cart, checkout, and
support tooling. A countdown uses a server-authoritative end time and stays expired. A low-stock
claim reflects current salable inventory. Do not reset timers, invent viewers or purchases, compare
against a price that was not genuinely offered, or keep an expired price visible to manufacture
urgency.

Judge a sale on incremental retained contribution and longer-term behavior. Measure discount cost,
order padding, cannibalization, stockouts, returns, cancellations, fulfillment delays, complaints,
and repeat purchase. Higher sale-day revenue or average order value alone can hide an unprofitable
promotion.

## Recover abandonment without manufacturing it

Separate browse abandonment, cart abandonment, checkout abandonment, payment failure, and an order
that is merely pending. Some shoppers are researching or not ready; abandonment is not automatically
a checkout defect or recoverable sale.

For each stage:

1. observe the last valid state, error, cost change, stock change, and fulfillment choice;
2. restore the current cart without trusting stale client totals;
3. explain and recover from the actual barrier before offering a discount;
4. check channel-specific permission, suppression, frequency, and current cart eligibility;
5. cancel queued recovery after purchase, cart removal, opt-out, product unavailability, or material
   price or terms change; and
6. use a holdout to measure incremental contribution, not attributed recovered revenue.

Never infer marketing SMS permission from a shipping phone number or label promotional outreach
`transactional` to bypass consent. Use `rundesk-team-marketing/lead-compliance-gates` for U.S. call
and text consent, suppression, revocation, and evidence; route other jurisdictions and commercial-
email rules to current compliance review.

## Measure the complete store

Instrument discovery, product decision, cart, checkout, order, and post-purchase outcomes before
optimizing them. Use stable product-family, variant, list, promotion, cart, order, and experiment
identifiers; deduplicate purchase and refund events; keep sensitive payment data and unnecessary PII
out of analytics.

Use funnel metrics diagnostically:

```text
list CTR             = product selections / eligible product-list impressions
add-to-cart rate     = valid adds / eligible buyable product views
checkout-start rate  = checkout starts / eligible carts
purchase rate        = accepted orders / eligible sessions or assigned users
retained order rate  = non-cancelled, non-returned orders / eligible sessions or assigned users
value/session        = retained contribution / eligible sessions or assigned users
repeat purchase rate = customers with another accepted order / eligible first-purchase cohort
```

Define identity, eligibility, denominator, attribution, observation window, reversals, and truth
source for every metric. A rising intermediate rate is not a win when purchase, contribution,
delivery reliability, customer harm, or retention worsens.

Read [measurement-experiments-and-growth.md](references/measurement-experiments-and-growth.md) when
creating the event contract, dashboards, ecommerce CVR, A/B tests, promotion or recovery holdouts,
cohorts, repeat purchase, attribution, customer value, or a measurable growth program.

## Grow qualified demand, not traffic alone

Map each acquisition route—organic search and shopping feeds, paid search or social, marketplaces,
affiliates and creators, partnerships, referrals, email or SMS, direct and returning visits—to the
intent, product scope, economics, permission, and destination it actually serves. Send a specific
product promise to the matching selected product, a category need to a useful collection or search
state, and a campaign-specific offer to a dedicated page when that makes the promise clearer.

Use `rundesk-team-marketing/seo` for crawling, indexing, product structured data, feeds, category and
product search visibility, and AI shopping surfaces. Use
`rundesk-team-development/designing-landing-pages` to design a dedicated single-offer campaign
destination and its source-to-page message match. The storefront remains responsible for the
complete catalog, product, cart, checkout, fulfillment, and retained-value journey after arrival.

For each channel, separate attributed orders from incremental acquisition. Compare new retained
customers, retained contribution, acquisition and offer cost, payback window, repeat behavior,
returns, fraud, and support burden. Do not scale a channel because it produces cheap clicks,
last-touch revenue, first orders bought by unprofitable discounts, or customers the store cannot
fulfill and retain.

## Improve in dependency order

1. Repair incorrect product, price, stock, delivery, terms, order, and measurement state.
2. Remove broken navigation, search dead ends, inaccessible controls, mobile failures, hidden costs,
   duplicate effects, and unrecoverable errors.
3. Improve decision information, comparison, fulfillment clarity, and service recovery.
4. Test merchandising, recommendation, offer, promotion, and retention hypotheses.
5. Scale acquisition only after the store converts qualified demand into retained value without
   unacceptable operational or customer harm.

For each experiment, prespecify the hypothesis, eligible population, stable assignment unit,
exposure event, one primary commercial outcome, diagnostics, harm guardrails, baseline, minimum
detectable effect, power and duration, stopping method, and delayed return/refund window. Run an A/A
or equivalent instrumentation check, inspect sample-ratio mismatch, and use sequential inference if
the team will continuously monitor. Attribution assigns credit; randomized experiments estimate
causal lift.

Use `performance-engineering` when diagnosing speed, setting a performance budget, or proving an
optimization. Use `database-design` plus the active database-engine skill for cart, order, inventory,
promotion, or ledger schemas, transactions, constraints, locking, and queries. Do not paste generic
SQL into a project before inspecting its engine, data model, tenancy, concurrency, and query plan.

## Produce an implementation-ready shop package

For a build, redesign, or growth program, deliver:

1. a commerce brief covering audience, assortment, markets, acquisition, unit economics,
   fulfillment, service, constraints, and source-of-truth owners;
2. a storefront journey and information architecture with representative shopping tasks, query
   corpus, category/facet rules, mobile navigation, and recovery states;
3. page specifications for home, category/search, product, cart, checkout, confirmation, order
   status, cancellation, return, and support, including responsive and accessibility behavior;
4. a product and offer contract for variants, pricing, promotions, stock, delivery, returns,
   reviews, compatibility, and claims;
5. cart, inventory, order, and post-purchase state contracts with idempotency, reservation,
   compensation, timeout, and reconciliation owners—without inventing project-independent schemas;
6. a promotion or limited-sale runbook with capacity, truth, measurement, holdout, and rollback;
7. an analytics and experiment contract with denominators, event owners, deduplication,
   reconciliation, contribution components, guardrails, and delayed outcomes; and
8. a verification report covering representative mobile and desktop journeys, keyboard and screen
   reader behavior, product/price/stock consistency, cost disclosure, failure recovery, oversell,
   duplicate action protection, order truth, analytics reconciliation, and known limits.

## Reject ecommerce folklore

| Folklore | Better decision |
|---|---|
| More products and promotions on the homepage create more sales | Make the assortment legible and give high-intent paths priority; measure discovery and downstream value. |
| More add-to-carts means the shop is winning | Treat adds as a diagnostic; require accepted orders, retained contribution, and no unacceptable harm. |
| Cart abandonment is mainly a checkout defect | Segment intent and stage; some shoppers are browsing, and recovery can annoy or subsidize buyers who would return anyway. |
| Forced accounts build loyalty | Let shoppers complete as guests; earn optional enrollment with a clear post-purchase benefit. |
| Scarcity and countdowns always convert | Use only verified inventory or real deadlines; measure net effects and never manufacture urgency. |
| A free-shipping threshold or free returns always pays | Include order padding, fulfillment, returns, repeat purchase, and contribution in a controlled decision. |
| Recommendations create incremental sales | Measure total store value and cannibalization, not revenue credited to recommended items. |
| Discounts grow customer value | Test acquisition quality, repeat behavior, margin, and post-promotion pull-forward; deep discounts can train strategic waiting. |
| Attributed recovered revenue proves recovery worked | Keep an eligible holdout and compare incremental retained contribution. |
| One benchmark CVR defines a good shop | Compare like-for-like traffic, market, device, product, price, and fulfillment; improve against a reconciled local baseline. |

The research methods, evidence limits, and good/bad lesson mapping for this package are in
[sources.md](references/sources.md).
