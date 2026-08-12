# Billing and Invoicing

Keep the application's commercial catalog, Stripe's billing objects, and customer entitlement distinct. Stripe
automates billing mechanics; it does not decide what the product promises or when the application should grant
service.

## Version products, prices, and plans

Use these separate identities:

- **Application offering/plan:** stable product meaning, features, eligibility, and business policy.
- **Stripe Product:** the provider catalog object describing what is sold.
- **Stripe Price:** one economic version: amount, currency, recurring interval or one-time behavior, usage model,
  and tax behavior.
- **Subscription and items:** one customer's recurring relationship to one or more Prices.

Store an authorized mapping from a stable local plan/version to the correct test/live, currency-specific Price
ID. Never accept an arbitrary Price ID from the browser. Keep historical mappings so an invoice or dispute can be
interpreted under the terms that existed when the customer bought.

Stripe Price amounts cannot be edited in place through the API. Create a new Price, move only the intended new or
existing subscriptions under an approved migration, and archive the old Price for new sales. Archiving does not
move existing subscribers. Product and price changes therefore need explicit grandfathering and migration policy.

## Choose one-time payment or invoice deliberately

Use Checkout or a PaymentIntent for an immediate one-time purchase that needs a payment receipt but not a formal
accounts-receivable workflow. Use Stripe Invoicing when the customer needs itemized billing, due dates, hosted
invoice payment, automatic collection from a saved method, or a durable invoice lifecycle.

Do not create both a standalone PaymentIntent and an automatically charging invoice for one obligation. Model one
local receivable/order and link it to the provider object that owns collection.

Invoices progress through `draft`, `open`, `paid`, `void`, or `uncollectible`. Preserve the provider state and the
application's receivable state separately. `open` can include failed or overdue collection; `uncollectible` is a
bad-debt decision, not a refund; and `void` is a terminal zero-value invoice record, not deletion.

Choose collection method explicitly:

- `charge_automatically` attempts a saved payment method and participates in configured retry/dunning behavior.
- `send_invoice` waits for customer payment under the invoice's due terms.

Treat out-of-band payment marking, payment application/unapplication, and reopening as privileged accounting
operations with audit evidence and reconciliation.

## Use the correct correction object

“Void” is not one universal Stripe operation:

| Situation | Preferred Stripe operation | Economic meaning |
|---|---|---|
| Payment authorized but not captured | cancel the PaymentIntent before authorization expiry | release the hold; no captured sale |
| Payment already captured | create and track a Refund | return captured funds |
| Standalone draft invoice created in error | delete only if allowed and policy permits | remove an unfinalized draft |
| Open or uncollectible invoice should never be payable | void the Invoice | terminal zero-value invoice with paper trail |
| Open invoice amount must decrease | issue a Credit Note | reduce amount due without recording payment |
| Paid invoice must be corrected | issue a Credit Note and allocate refund, customer credit, or approved out-of-band amount | preserve original invoice and correction |

Check local invoice law before revising, voiding, or crediting. Subscription invoices can have additional
subscription-status effects when voided. Never expose a generic `void()` button that guesses the object or
economic outcome.

## Handle authorization and capture

Use manual capture only when the business truly separates authorization from fulfillment. Record the
authorization, `amount_capturable`, capture deadline, intended capture amount, fulfillment evidence, and terminal
release/capture state. Capture before the payment-method-specific authorization expires.

Most payments permit one capture; a partial capture can release the remainder. Multicapture, overcapture, and
extended authorization are conditional capabilities, not defaults. Do not simulate a second capture by charging
again without a separately authorized operation.

## Control subscription changes

Before creating or changing a subscription, define:

- subscription items and quantities;
- billing interval and anchor;
- trial and payment-method requirements;
- proration and credit behavior;
- immediate versus period-end changes;
- pending update or Subscription Schedule behavior;
- cancellation, pause, resume, grace, and dunning policy;
- entitlement effects for every invoice/subscription state.

Preview customer-visible prorations before a paid change. Updating to a new Price without the existing
subscription-item ID can add a second item instead of replacing the first. Use pending updates when the commercial
change must take effect only after payment; use schedules for approved future phases. Existing subscribers remain
on old Prices until deliberately migrated.

## Meter usage exactly once

For usage billing, keep the application event as the usage source of truth. Map it to the Stripe Meter and submit
a stable unique identifier, customer, value, timestamp, and dimensions. Provider meter summaries update
asynchronously, so do not grant or revoke product behavior from an immediately read aggregate.

Define late-arriving usage, corrections, resets, pauses, trial usage, backfills, time zones, minimums, tiers, and
invoice-finalization cutoffs. Reconcile source usage totals to Stripe's meter summaries and invoice lines before
and after finalization. Do not silently mix legacy Usage Records with Billing Meters.

## Apply discounts, tax, and recovery as policy

Resolve discounts and promotion codes from server-authorized campaign policy. Define eligibility, duration,
redemption limits, stacking, currency, plan scope, and what happens on upgrade, renewal, cancellation, and refund.
Do not treat knowledge of a coupon code as authorization for an unbounded discount.

Stripe Tax calculation still requires the business to decide where it is registered and obligated. Configure
Product tax codes, Price tax behavior, customer location evidence, and `automatic_tax` on each relevant Checkout,
Subscription, or Invoice path. Enabling a Dashboard setting does not automatically repair existing objects, and
missing customer location can disable or fail tax calculation. Alert and fail according to approved tax policy;
do not quietly collect an untaxed payment because finalization continued.

Use Smart Retries or an explicitly owned schedule for recoverable invoice failures. Hard declines require a new
payment method rather than repeated charges. Keep dunning notifications, next attempt, final action, subscription
status, and application access policy aligned without assuming Stripe's Dashboard setting changed historical
application state.

## Prove the billing matrix

Test at least:

- local plan to test/live Price mapping, unauthorized Price IDs, archived Prices, and grandfathered subscribers;
- monthly/yearly, one-time setup fee, multi-item, quantity, trial, coupon, tax-inclusive/exclusive, and zero-value
  cases used by the product;
- upgrade/downgrade previews, immediate and period-end changes, pending payment failure, schedules, pause/resume,
  and cancellation;
- usage duplicate, late, corrected, out-of-order, trial, paused, and finalization-boundary events;
- automatic-charge versus send-invoice collection, hard decline, Smart Retry, final dunning, and new method;
- invoice draft/finalize/pay/fail/void/uncollectible, credit note, external refund, customer credit, and out-of-band
  payment paths;
- authorization, partial/full capture, expired hold, cancellation, and incorrect second capture;
- tax-location failure, existing objects without automatic tax, and tax-behavior price replacement;
- reconciliation from local order/receivable and ledger through invoice, payment, credit note, refund, dispute,
  Balance Transaction, and payout.
