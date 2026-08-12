# Cart, checkout, and operations

Use this reference when purchase completion depends on stored state, inventory, fulfillment,
promotion, support, or recovery behavior. Keep processor mechanics in the payment skill and database
implementation in the database skills.

## Separate the state owners

Do not collapse these concepts into one `paid` flag:

| State | Owns |
|---|---|
| Cart | Intended products, variants, quantities, selections, and shopper context |
| Price quote | Current item prices, discounts, shipping, tax basis, currency, and expiry |
| Inventory | Salable, reserved, committed, released, and reconciled quantity |
| Payment | Processor authorization, capture, failure, cancellation, refund, and dispute lifecycle |
| Order | Accepted commercial commitment and its line-level state |
| Fulfillment | Allocation, pick, pack, ship, delivery, exception, and return receipt |
| Service | Cancellation, return authorization, replacement, credit, communication, and resolution |

The application accepts an order only after its own business invariants hold. A payment success
page, redirect, authorization, or webhook is evidence for a payment transition, not the complete
order or fulfillment truth.

## Preserve the cart without trusting it

Persist stable product-family and variant identifiers, quantity, selected options, and an opaque
cart identity. Define guest-to-account merge, multi-device conflicts, ownership checks, expiration,
and privacy behavior. Never trust client prices, discounts, stock, or totals.

Before checkout and again before order acceptance:

1. authorize cart ownership;
2. reload current product and selected variant;
3. re-evaluate price, promotion, tax basis, shipping methods, and stock;
4. show material changes and require a clear decision when necessary; and
5. compute the accepted order from server-authoritative state.

A cart does not imply an inventory hold unless the store explicitly creates one. If it does, name
the reservation point, expiry, renewal, release, and compensation behavior so idle carts cannot lock
stock forever.

## Keep checkout short and truthful

Default to a prominent guest path and let an existing-email shopper continue without a password.
Offer account creation after confirmation using already entered details and a concrete benefit.

Collect only data required for the selected market, delivery, payment, fraud, and support path.
Support international address shapes, browser autofill, copy and paste, tolerant formatting,
country-aware validation, and a manual path when lookup fails. Preserve all non-sensitive values
through recoverable errors and keep processor-owned card fields within the approved PCI integration.

Show:

- the exact product, variant, quantity, price, discounts, and removals;
- estimated or known shipping, tax, and other mandatory costs with their basis;
- delivery or pickup choices and credible estimates;
- promotion outcome and why a code did not apply;
- returns, cancellation, subscription, or renewal terms material to the commitment; and
- the truthful final action, pending state, accepted state, and next step.

Do not precheck an add-on or hide a fee until the final action. Do not clear unrelated address,
delivery, or cart state after a payment-field or promo error.

## Make inventory and limited sales operable

Use one authoritative, reconcilable reservation lifecycle. The exact transaction and locking design
depends on the project; use `database-design` and the active engine skill rather than copying a
generic schema or raw SQL.

Specify:

- salable versus physical quantity and any safety stock;
- reservation creation, expiry, conversion, release, and idempotent compensation;
- line-level behavior for partial stock and split fulfillment;
- checkout concurrency and duplicate-order protection;
- backorder, preorder, substitution, and waitlist rules;
- oversell and undersell detection plus reconciliation; and
- stuck reservation and failed compensation recovery.

For a limited sale, add inventory allocation, per-customer quantity rules, queue or overload policy,
clock and timezone ownership, price/promotion consistency, capacity limits, monitoring, and rollback.
Never reserve indefinitely at add-to-cart or promise that an item is secured before the stated
reservation boundary.

## Design post-purchase state for customers

Expose customer-understandable states without hiding operational detail that changes expectations:

```text
order received -> accepted or needs review -> allocated -> shipped or ready -> delivered
                 cancelled | delayed | partially fulfilled | replacement pending
return requested -> authorized -> received -> inspected -> refund pending -> refunded
```

Adapt the vocabulary to the business. Distinguish `request saved`, `return authorized`, `item
received`, and `refund completed`; a generic `returned` label creates false expectations.

Publish current cancellation and return terms before purchase. Provide status, tracking, next step,
deadline, costs, and support handoff without forcing the customer to repeat order history. Confirm
the stored result of an action, not merely receipt of a click.

When Laravel and Stripe are in use, route actual refund, reversal, dispute, negative-balance, and
reconciliation behavior to `laravel-stripe-payments`. Otherwise use the active payment-integration
owner and current processor documentation. Prevent double compensation when a refund, return, store
credit, replacement, dispute, or goodwill adjustment overlaps.

## Recover the correct abandonment stage

Classify eligibility from authoritative state:

| Stage | Useful recovery |
|---|---|
| Browse | Restore discovery context or answer a product question when permission exists |
| Cart | Restore current items and disclose price, stock, and delivery changes |
| Checkout | Return to the last valid step and preserve non-sensitive input |
| Payment failure | Explain the recoverable failure and offer valid methods without exposing fraud rules |
| Pending order | Show status and avoid duplicate purchase prompts |

Do not automatically discount every abandoned cart. Diagnose the barrier, segment by likely intent,
cap frequency, deduplicate, and suppress after purchase, opt-out, empty cart, unavailable product,
or material offer change. Treat recovery email as commercial unless current qualified review
establishes otherwise. Never infer SMS permission from shipping or account data.

Measure recovery with an eligible holdout and retained contribution after discounts, cancellations,
returns, support, and channel cost. Attributed orders include shoppers who would have returned
without a message.

## Earn retention after fulfillment

Prioritize accurate confirmation, delivery, self-service, and support before adding points, tiers,
referrals, memberships, or personalized campaigns. Define loyalty value, qualification, cost,
expiration, exclusion, reversal, and refund behavior as an explicit commercial contract.

Good retention state follows paid and retained order truth. Bad retention state grants irrevocable
rewards before payment, fulfillment, cancellation, or return resolution. Never make marketing
permission or loyalty enrollment a prechecked purchase requirement.

Evaluate repeat purchase, cohort contribution, service contacts, returns, reward liability,
redemption, complaints, and breakage. Do not declare success from enrollment, points issued, or
email-attributed revenue alone.

## Treat fraud controls as a tradeoff

Keep fraud decision, payment status, order status, and fulfillment status separate. Allow explicit
review or pending states and preserve the evidence and deadline needed for disputes. Tune decisions
against fraud loss, false-positive declines, review age, customer friction, dispute rate, and missed
fulfillment—not the processor score alone.

Do not expose exploitable rule detail, ship while a required review is unresolved, or refund and
contest the same amount without reconciliation. When Laravel and Stripe are in use, use
`laravel-stripe-payments` for provider-specific fraud, 3DS, dispute, evidence, and webhook
implementation; otherwise use the active payment-integration owner.

## Verify the operational journey

Exercise at least:

- guest, account, guest-to-account merge, expired cart, multi-device conflict, and unauthorized
  cart access;
- price, promotion, shipping, tax, stock, and terms changing between cart and order acceptance;
- two shoppers competing for the last unit, reservation expiry, duplicate activation, retry, and
  stuck compensation;
- out-of-stock, preorder, backorder, partial fulfillment, delay, cancellation, replacement, return,
  refund, and dispute overlap;
- incomplete address, lookup error, unavailable shipping method, processor-field error, slow or
  interrupted network, back navigation, and restored checkout;
- queued abandonment message after purchase, opt-out, cart removal, price change, or stockout; and
- customer-visible status, notifications, support context, analytics, and operational reconciliation.

Record the actual state transitions and invariant checks. A happy-path browser purchase cannot prove
inventory, payment, order, fulfillment, or recovery correctness.
