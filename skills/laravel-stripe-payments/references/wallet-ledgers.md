# Wallet Ledgers

## Name the economic object

Before writing a `balance` column, decide whether the feature is:

- promotional store credit that cannot be purchased or redeemed for cash;
- customer-funded prepaid value;
- a refund credit;
- an account receivable or invoice adjustment;
- partner earnings awaiting an approved transfer;
- Stripe Customer invoice balance or Stripe Billing Credits;
- Stripe platform or connected-account cash balance.

These objects have different redemption, expiration, refund, tax, accounting, unclaimed-property, and financial-
regulatory consequences. Do not merge them because the UI calls each “credit.” Route customer-funded value,
cash redemption, transferable credit, holding funds for others, or cross-border value to qualified legal and
accounting review before implementation.

## Use an append-only, balanced, currency-scoped ledger

Represent each economic change as an immutable journal transaction with balanced debit and credit entries. At
minimum preserve:

```text
accounts and wallet/account owner
currency
integer amount and debit/credit direction
entry type and business operation
effective and recorded timestamps
external object/event references when applicable
reversal/correction relationship
idempotency key
policy version and actor
```

Balance each journal transaction independently per currency and enforce one application of each business
operation. Derive balances from entries or maintain transactional projections that are always recoverable from
them. Keep separate accounts for customer-credit liability, promotional credit/expense, seller payable, platform
fees or revenue, Stripe clearing, refund/dispute exposure, and reserves as the approved accounting model requires.
Never update a balance without its journal transaction.

Bad:

```text
webhook received -> wallet.balance += payment.amount
```

Good:

```text
verified payment effect + unique operation -> post balanced journal once -> update projections atomically
```

The replacement makes duplicate webhook delivery, replay, refunds, disputes, and operator corrections visible
and reversible. Do not mix customer spendable value with seller withdrawable earnings merely because both have
a positive UI balance.

## Fund only from authoritative success

Create a funding operation before Checkout or PaymentIntent creation. Credit the wallet only after the approved
provider success state is verified. A redirect, client callback, or PaymentIntent creation response is not a
credit event.

Record the source payment and currency. Never silently exchange currencies in a wallet. If exchange is a product
requirement, model the rate, fees, rounding, two currency legs, and responsible party explicitly.

## Spend atomically

Authorize the owner and lock the wallet or otherwise serialize the balance invariant. In one database transaction:

1. insert or find the unique spend operation;
2. compute available funds under the current policy;
3. reject or partially apply according to an approved rule;
4. append the debit and update the recoverable balance projection;
5. commit before dispatching external work.

Test concurrent spends at the database boundary. An application-level `if balance >= amount` without locking or
an equivalent constraint can overspend.

If a purchase combines wallet and Stripe payment, model two tender legs. Define which tender is refunded first,
how partial refunds allocate, and what happens if the external leg fails after reserving wallet value.

## Reverse; do not rewrite

A refund, chargeback, expired promotional grant, operator correction, or canceled purchase appends a related
entry. Preserve the original event. Define whether a dispute can make a wallet unavailable or negative and how
later dispute wins restore it.

Do not treat a local refund credit and a Stripe refund as the same benefit. An approved policy must say whether
the customer receives processor cash, local credit, or both, and reconciliation must prevent accidental double
compensation.

## Do not misuse Stripe balances

Stripe Customer invoice balance is an immutable transaction ledger that automatically applies to future invoices;
it cannot target or skip arbitrary invoices. Stripe Billing Credits apply to specified subscription and usage-
billing scenarios. Neither is a general checkout wallet.

Stripe platform and connected-account balances describe processor funds. Transfers and payouts change those
balances under Connect rules; they do not replace the application's liability ledger or prove a partner has been
paid into a bank.

## Reconcile the complete chain

For wallet funding and spending, reconcile:

```text
local funding operation
  -> Stripe payment and Balance Transaction
  -> wallet credit entry
  -> wallet spend/reservation
  -> order tender allocation
  -> refund/dispute/correction entries
```

Flag a provider success without one wallet credit, a wallet credit without a provider success or approved grant,
duplicate effects, stale reservations, negative balances outside policy, cross-currency entries, and projection
drift. Repair by replaying the unique effect or appending a correction.
