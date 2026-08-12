# Payment Lifecycle

## Keep one purchase identity

Create a local order and payment operation before the provider call. One customer purchase should normally
reuse one PaymentIntent while it is still the same payable order. A new checkout attempt is not automatically
a new economic intent.

Bad:

```text
timeout -> generate another idempotency key -> create another PaymentIntent
```

Good:

```text
timeout -> load durable operation -> retry the same key or retrieve its PaymentIntent -> reconcile
```

The replacement prevents an uncertain response from becoming a duplicate charge. Stripe's idempotency result
is time-bounded; the local operation and provider ID preserve the longer business invariant.

## Separate client progress from fulfillment

The browser can abandon a Checkout success page, and asynchronous methods can still be processing after a
session completes. Treat redirects and client callbacks as display and polling aids only.

Bad:

```text
GET /checkout/success -> order.paid = true -> ship
```

Good:

```text
verified event/current provider state -> idempotent FulfillOrder operation -> render confirmation
```

For Checkout, cover synchronous and asynchronous payment success and failure. For PaymentIntents, reduce the
provider state into guarded local states such as `requires_action`, `processing`, `succeeded`, `canceled`, and
reconciliation-required.

## Build a durable webhook inbox

The ingress transaction should verify the raw body, insert the event if absent, and acknowledge promptly.
Processing can then be retried without asking Stripe to redeliver.

Suggested identity:

```text
(livemode, stripe_account_scope, event_id)
```

Also make the business transition unique, for example `(payment_operation_id, effect_type)`. Stripe can send
two distinct Event objects that describe the same underlying effect.

Do not apply deltas merely in arrival order. If `updated` arrives before `created`, or an old snapshot arrives
after a new one, retrieve the current provider object when necessary and allow only a legal local transition.

## Prepare future payments deliberately

Use a SetupIntent when collecting a payment method without an immediate charge. If a PaymentIntent also
prepares future use, set `setup_future_usage` for the real on-session or off-session scenario. Capture the
required customer agreement and build a return-to-customer path for later `requires_action` responses.

Do not store PAN or CVC. Store only provider identifiers and safe display attributes returned by Stripe.

## Separate authorization, capture, cancellation, and refund

Set manual capture only for payment methods and fulfillment flows that support it. A successful authorization
puts the PaymentIntent in `requires_capture`; it is not settled revenue and must not fund a wallet or partner
transfer. Record `amount_capturable` and the provider's capture deadline rather than assuming every online card
hold lasts the same number of days.

Cancel the PaymentIntent to release an uncaptured authorization. Once funds are captured, use a Refund. A partial
capture usually releases the remaining authorization, and most payments do not permit a later second capture.
Keep capture and cancellation under stable idempotent domain operations and reconcile ambiguous responses.

Bad:

```text
authorized -> mark paid -> pay seller; later “void” by deleting the local transaction
```

Good:

```text
requires_capture -> capture or cancel before deadline -> webhook/retrieve terminal state -> post ledger effect
```

## Refund through an explicit state machine

Recommended states include `requested`, `submitted`, `pending`, `succeeded`, `failed`, and `canceled`. Preserve
the original requested amount and the provider's actual result. Bound all partial refunds against the remaining
eligible amount under a row lock or equivalent invariant.

Bad:

```text
Stripe returned a Refund object -> mark the order and wallet fully refunded
```

Good:

```text
record Refund ID/status -> reduce later provider state -> append exact order/ledger compensation once
```

Insufficient provider balance or payment-method behavior can delay or fail refunds. A dispute can also arrive
while a refund is unresolved. Detect that collision before adding a second customer benefit.

## Treat disputes as their own event stream

Record the provider dispute, disputed amount, currency, status, reason, evidence deadline, fee effects, and
terminal outcome. Preserve transaction-time evidence before a dispute exists. Keep refund, dispute, and internal
credit entries independently traceable so reconciliation can identify double reimbursement.

## Reconcile cash, not just charges

Use Stripe Balance Transactions and their reporting categories for the provider-side cash view. Charges alone
do not represent fees, refund failures, disputes, adjustments, or payout timing. Reconciliation should compare:

- each durable local operation with its Stripe object;
- each terminal provider object with the corresponding domain transition;
- each local money entry with its processor cash effect or a documented non-cash classification;
- aggregates by account scope, currency, and livemode;
- stuck, missing, duplicated, or contradictory states.

Repair by replaying an idempotent reducer or appending a correction. Do not overwrite the historical entry that
made the discrepancy visible.
