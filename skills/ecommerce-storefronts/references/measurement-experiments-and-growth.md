# Measurement, experiments, and growth

Use this reference to decide what a shop change accomplished. Start with commerce-system truth and
use analytics as an observation layer, not the sole order, refund, or customer-value ledger.

## Build a reconciled event contract

A useful provider-neutral funnel maps to these common event concepts:

```text
view product list or search results
select product
view product and selected variant
add or remove cart line
view cart
begin checkout
choose delivery and payment steps
accepted purchase
cancel, refund, return, replace, or dispute
view and select internal promotion
```

For each event, define:

- business meaning and authoritative owner;
- eligibility and exact firing boundary;
- user, session, cart, order, product-family, variant, list, promotion, and experiment identifiers;
- item quantity, currency, value components, discounts, stock, and fulfillment context;
- client, server, or imported producer;
- deduplication and retry key;
- consent and data-minimization requirements; and
- reconciliation query or report against accepted orders and later reversals.

Google Analytics names such events `view_item_list`, `select_item`, `view_item`, `add_to_cart`,
`begin_checkout`, `purchase`, `refund`, `view_promotion`, and `select_promotion`. Use that taxonomy
when GA4 is present, but do not let a vendor event name redefine application state.

## Keep metrics and denominators explicit

Choose the unit exposed to the decision:

| Scope | Default eligible unit | Primary commercial outcome | Useful diagnostics |
|---|---|---|---|
| Search or listing | Eligible search/list session or assigned user | Retained contribution or purchase value per unit | Result CTR, zero results, reformulation, unavailable clicks |
| Product page | Viewer of a buyable product or assigned user | Retained contribution or accepted purchase per unit | Variant completion, add-to-cart, media/review use |
| Cart | Eligible cart or assigned user | Accepted and retained order per unit | Checkout start, price/stock adjustment, removal |
| Checkout | Checkout starter or assigned user | Accepted and retained order per unit | Step completion, field error, payment failure |
| Promotion | Eligible exposed user | Incremental retained contribution per user | View, click, redemption, discount, stockout |
| Recovery | Eligible abandoned user | Incremental retained contribution per user | Restore, opt-out, complaint, discount cost |
| Retention | First-purchase cohort | Realized repeat purchase and retained contribution | Time to second order, returns, service, reward use |

Do not switch denominator after seeing the result. Report numerator, denominator, absolute rate or
value, delta, uncertainty, exclusions, and observation window.

Separate:

```text
gross order value
accepted purchase value
retained revenue after cancellations, refunds, and returns
contribution after variable costs
realized repeat value by cohort
predicted lifetime value
```

Modeled lifetime value can prioritize hypotheses; it is not a substitute for realized short-horizon
outcomes or a reason to hide model error and cohort assumptions.

## Distinguish diagnostics from objectives

Product clicks, add-to-carts, checkout starts, promotion clicks, coupon use, and email-attributed
orders explain where behavior changed. They rarely represent the business objective.

A useful default overall evaluation criterion for storefront work is retained contribution per
eligible assigned user or session. If margin inputs are unavailable, use retained purchase value
with explicit refund, return, cancellation, fulfillment, and support guardrails; do not relabel it
profit.

Include guardrails appropriate to the change:

- purchase, gross and retained value, discount, and margin proxy;
- cancellations, returns, refunds, replacements, disputes, and fraud loss;
- zero results, dead variants, unavailable attempts, oversell, and stockout;
- late shipment, split shipment, service contacts, and complaints;
- payment failure, application error, latency, accessibility, and mobile completion;
- opt-out, suppression failure, recovery over-send, and dark-pattern complaints; and
- duplicate transaction IDs, missing items, sample-ratio mismatch, and client/server disagreement.

## Write an experiment brief before exposure

Specify:

```text
decision and causal hypothesis
eligible population and exclusions
stable assignment unit and persistence
exposure event and analysis unit
control and complete end-to-end treatment
one primary metric and direction
diagnostics and harm guardrails
baseline, minimum detectable effect, power, and sample estimate
ramp, duration, seasonality, and stopping rule
delayed cancellation, refund, return, and repeat-purchase window
segment plan and multiple-comparison policy
instrumentation, reconciliation, and rollback checks
```

Run an A/A test or equivalent preflight when assignment or commerce telemetry is new. Inspect sample
ratio and exposure loss before outcomes. Ramp safely, but use an allocation that can answer the
question once risk checks pass. Fixed-horizon tests must not be repeatedly stopped when the p-value
looks favorable; use a supported sequential method if continuous monitoring is required.

Report absolute outcomes and uncertainty. `Significant` does not mean commercially material,
practically important, or safe. A test that raises purchase rate but worsens contribution, returns,
delivery, accessibility, or complaints is not a clean win.

## Measure promotions and limited sales incrementally

Track eligibility, exposure, interaction, purchase, discount, inventory, cancellation, return,
fulfillment, and repeat behavior. Preserve a randomized holdout when possible; otherwise state the
weaker design and threats such as seasonality, product mix, acquisition changes, and pull-forward.

Ask:

- Did more eligible customers purchase because of the offer?
- Did the offer shift full-price or later purchases into the discount window?
- Did shoppers pad orders to cross a threshold and then return items?
- Did one product, channel, store, or time period cannibalize another?
- Did stockouts, delays, support, fraud, or returns erase gross lift?
- Did acquired customers return without another deep discount?

Do not credit every redeemed order to the promotion. Redemption and attribution are not causal
incrementality.

## Measure abandonment recovery with a holdout

Define the abandoned stage and eligible moment before assignment. Keep treatment and holdout subject
to the same cart, stock, price, channel permission, suppression, and purchase checks. Measure:

- incremental accepted and retained orders;
- incremental contribution after discount and message cost;
- time to purchase and cross-device purchase;
- opt-outs, complaints, duplicate or post-purchase sends; and
- return, cancellation, fraud, and repeat behavior.

Do not compare messaged buyers with all non-buyers or count last-touch revenue as recovered lift.
Those groups differ by intent and exposure.

## Interpret retention by cohort

Anchor cohorts to first accepted purchase or another explicit starting event. Compare cohorts at the
same age rather than mixing a mature cohort with customers who have not had time to repurchase.
Report 30-, 60-, or 90-day windows only when they match the category's purchase cycle; do not treat
them as universal.

Track time to second order, repeat purchase, retained revenue, contribution, return and service
burden, promotion dependence, and churn or inactivity definition. Segment only as prespecified or
clearly exploratory; small post-hoc segments manufacture stories.

## Separate attribution from causality

Attribution decides how reporting credit is distributed across known touchpoints and depends on
identity, eligible channels, lookback window, consent, and model. Changing it can change reported
channel results without changing customer behavior.

Random assignment estimates the causal effect of an intervention under its assumptions. Use it for
questions such as whether a new filter, recommendation, free-shipping threshold, abandoned-cart
message, or promotion produced incremental value. Use attribution for descriptive channel reporting;
do not present it as proof of lift.

For omnichannel stores, reconcile store, pickup, marketplace, call-center, and online outcomes when
the intervention can shift purchases between them. A channel can appear to lose while the total
business gains, or the reverse.

## Build a growth loop

1. Reconcile local funnel and commercial baselines by relevant device, market, source, customer,
   product, and fulfillment segment.
2. Map each acquisition channel to its intended audience, destination, attributed cost, new-customer
   rate, retained contribution, payback window, and operational load. Mark causal evidence separately
   from attribution.
3. Rank verified failures and evidence-backed hypotheses by expected customer and contribution
   impact, confidence, effort, and operational risk.
4. Repair defects before testing persuasion or adding paid traffic.
5. Run the smallest trustworthy qualitative study, instrumentation check, or controlled experiment
   that can resolve the decision.
6. Ship only with explicit guardrails and rollback; continue through the delayed outcome window.
7. Record the result, limits, segment heterogeneity, and what belief changed.
8. Scale acquisition or promotion only while fulfillment, service, returns, and contribution remain
   healthy.

Never copy a vendor benchmark into a target. A strong program improves a reconciled local baseline
and records why a tactic worked or failed in this store.
