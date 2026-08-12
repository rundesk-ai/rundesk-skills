---
name: laravel-stripe-payments
description: Use when designing, implementing, reviewing, debugging, or testing Stripe in Laravel, including PCI scope, Checkout, PaymentIntents, authorization, capture, voids, saved methods, Products and Prices, Cashier subscriptions, metered billing, invoices, credit notes, refunds, disputes, wallet credits, Stripe Connect onboarding, platform fees, transfers, or partner payouts. It supplies a version-gated workflow for secure collection, durable money state, idempotent webhooks, Connect isolation, and reconciliation. Do not use it to decide unapproved pricing, tax, accounting, stored-value, merchant-of-record, or marketplace policy.
---

# Laravel Stripe Payments

Treat Stripe as an asynchronous payment processor, not the application's order, entitlement, wallet,
or accounting database. Make product policy explicit, record every intended money movement locally, and
reconcile provider events into guarded domain transitions.

This skill supplies engineering guidance, not tax, accounting, PCI, financial-regulatory, or legal
advice. Obtain the required approvals for merchant of record, fees, taxes, refunds, disputes, stored
value, holding periods, negative balances, cross-border funds, and partner payouts before production.

## Route the work

Read only the references needed for the task:

- Read [security-and-pci.md](references/security-and-pci.md) whenever card data, PCI scope, Checkout or
  Elements, API keys, client secrets, 3DS/SCA, fraud controls, or card testing is in scope.
- Read [payment-lifecycle.md](references/payment-lifecycle.md) for one-time payments, authorization and
  capture, cancellation or voids, saved methods, webhooks, refunds, disputes, fulfillment,
  reconciliation, or failure recovery.
- Read [cashier-subscriptions.md](references/cashier-subscriptions.md) for Laravel Cashier, customers,
  subscriptions, invoices, trials, prorations, the Billing Portal, and Cashier webhook compatibility.
- Read [billing-and-invoicing.md](references/billing-and-invoicing.md) for Products, Prices, local plan
  models, recurring or usage pricing, discounts, invoice collection, credit notes, dunning, or tax
  configuration.
- Read [connect-marketplaces.md](references/connect-marketplaces.md) whenever a partner connects a
  Stripe account, receives funds, pays a platform fee, or owns a charge, refund, dispute, or payout.
- Read [wallet-ledgers.md](references/wallet-ledgers.md) for wallet credits, promotional credits,
  prepaid balances, refunds to credit, or any local balance.
- Read [sources.md](references/sources.md) before updating a version claim or relying on a provider
  behavior that can change.

Use `laravel-patterns` with this skill for framework conventions, `database-design` for durable money
models and concurrency, and `testing-code` for the required failure and replay coverage.

This skill owns payment acceptance, customer billing, application credits, and Connect money movement.
When work enters Stripe Tax, Radar, Terminal, Identity, Financial Connections, Treasury, Issuing, Climate,
or another separately governed product, recheck its live documentation and load the domain, legal, and
security guidance that product requires. Apply this skill's authorization, idempotency, webhook, ledger,
tenant-isolation, and reconciliation invariants, but do not infer that a payment implementation authorizes
or fully covers every Stripe product.

## Inspect the installed boundary

Before designing or changing an integration, inspect the actual application:

```sh
php artisan --version
composer show laravel/framework laravel/cashier stripe/stripe-php
```

Read `composer.lock`, Cashier configuration and migrations, the billable model, webhook routes and
middleware, provider service classes, queues, ledger tables, reconciliation jobs, and tests. Inspect the
installed Cashier and Stripe PHP source for the API version they actually send. Do not trust a prose
document's version label over the locked package: Cashier's API version has changed across compatible
minor releases, and mismatched webhook versions have broken handlers.

Never upgrade Cashier, Stripe PHP, the Stripe API version, or webhook destinations as an incidental
step. Treat each as a behavior change: read upgrade notes, compare event/object shapes, create or update
the endpoint deliberately, replay fixtures, and verify sandbox behavior before enabling it.

## Establish the commercial contract before code

Resolve these questions in writing:

1. Who is the customer, seller or service provider, platform, and legal merchant of record?
2. Is the payment for a platform subscription, a purchase from one partner, a multi-party marketplace
   order, wallet funding, or a later partner payout?
3. Who sets price, pays Stripe and platform fees, handles tax, refunds, disputes, fraud, and negative
   balances, and provides customer support?
4. Which currencies, countries, payment methods, settlement delays, refund windows, and payout rules are
   approved?
5. Which system is authoritative for order state, entitlement, internal balance, processor cash,
   accounting ledger, and bank payout?

Stop at a policy seam rather than inventing an answer. The charge type, Connect account configuration,
refund compensation, and wallet liability are business architecture, not SDK details.

## Choose the narrowest Stripe surface

- Prefer Stripe Checkout for hosted one-time purchase or subscription flows when its UX fits. It keeps
  card data away from Laravel and reduces custom state handling.
- Use Payment Element plus one PaymentIntent per purchase when the application needs a custom payment
  experience. Reuse that PaymentIntent if the customer resumes the same purchase.
- Use a SetupIntent, or an appropriately configured PaymentIntent, to prepare a method for future or
  off-session use. Saving an identifier alone does not establish the required mandate or future-use setup.
- Use Cashier for the platform's supported Stripe Customer, subscription, invoice, payment-method, and
  Billing Portal workflows.
- Use a dedicated service around the Stripe PHP client for Connect, Stripe resources Cashier does not own,
  and retryable money commands whose Cashier wrapper does not expose request options such as a persistent
  `idempotency_key` or `stripe_account`. Inspect the installed wrapper before choosing it. Keep the SDK behind
  domain operations; do not scatter calls across controllers and models.
- Use Stripe-hosted or embedded Connect onboarding for marketplace partners by default. OAuth is a
  separate existing-account access model, not a generic “connect my Stripe” shortcut.

Prefer hosted Stripe components so PAN and CVC never cross the application. This can reduce PCI scope,
but it does not make the application or business automatically PCI compliant.

## Model money and lifecycle state

Store money as an integer amount plus an ISO currency. Apply that currency's minor-unit rules; never
assume every currency has two decimal places and never use binary floating point for persisted money.
Resolve products, prices, recipients, discounts, and totals from server-authoritative state after
authorization. A browser-supplied amount, currency, Price ID, Customer ID, or connected-account ID is an
untrusted reference, not permission.

Use explicit records and states for orders, payment operations, refunds, disputes, transfers, payouts,
and ledger entries. Persist provider identifiers with livemode and account scope; the same object ID is
not sufficient context across platform and connected accounts. Use uniqueness constraints for both the
provider event and the domain effect it may cause.

Avoid a single `paid` Boolean or mutable `balance` as the record of truth. Provider and business states
can be pending, require customer action, succeed later, fail after an intermediate success, be partially
refunded, disputed, reversed, or reconciled.

Model Stripe Products and Prices separately from the application's stable offering or plan identity. A
price change creates a new economic version; it must not silently rewrite what an existing subscription
or historical invoice meant. Keep environment- and currency-specific Price IDs behind an authorized
server-side mapping.

## Execute one durable operation

For every money-changing command:

1. Authorize the actor and resolve the order, tenant, connected account, amount, currency, and policy on
   the server.
2. Create one durable local operation with a unique business key before calling Stripe.
3. Derive a stable Stripe idempotency key from that operation and mutation. Retry the same key with the
   same parameters; do not generate a new key for each HTTP attempt.
4. Do not hold a database lock or transaction open across the network call. Record the intent, call
   Stripe, then persist the provider ID and returned state through a guarded transition.
5. If the response is ambiguous, mark the operation for reconciliation and retrieve the known provider
   object. Do not create a second payment because the first request timed out.
6. Put only opaque internal references in Stripe metadata. Never store card data, secrets, health data,
   or unnecessary personal data there.

Stripe may prune idempotency results, and provider idempotency does not enforce the application's
business invariant forever. Keep the durable local key and provider ID.

## Make webhooks the authoritative transition path

Verify the signature against the exact raw request body with the endpoint-specific secret before parsing.
Keep the webhook route's CSRF exception as narrow as the exact endpoint and require the signing secret in
every deployed environment. Cashier conditionally installs signature middleware only when its webhook secret
is configured; validate configuration at startup or deployment so a missing value cannot silently create an
unsigned endpoint.

Use a durable inbox keyed by mode, connected-account scope, and event ID. Capture the verified event,
return `2xx` quickly, and queue domain processing. Assume delivery is duplicated, delayed, retried, and
out of order; a separate event can also describe the same business effect. Make each reducer idempotent,
enforce guarded transitions, and retrieve current provider state when order matters.

Never fulfill, credit a wallet, or grant durable entitlement from a success URL or client callback.
Those pages confirm UX only. Fulfill from a verified provider state through an idempotent domain operation.

When Cashier owns the resource, preserve its webhook controller and add application behavior through its
documented events unless a reviewed replacement covers every built-in transition. Connect events need
their own account-aware path; do not force them through a platform-Customer assumption.

## Handle subscriptions as policy-driven state

Define which combination of invoice evidence and subscription status grants, continues, limits, or
revokes access. `active` does not prove every invoice was paid. Cover at least trials, first-invoice
authentication, `incomplete`, `past_due`, `unpaid`, `paused`, grace periods, cancellation, and resumed
service.

Use pending updates when an upgrade must take effect only after its invoice succeeds. Define proration,
dunning, cancellation timing, refunds, and entitlements before exposing controls. Cashier subscription
types are unique active slots; do not create two active subscriptions under the same type and expect both
to be represented correctly.

## Treat refunds and disputes as independent workflows

A refund request is not completion. Record its authorization, amount, currency, reason, original payment,
provider Refund ID, and lifecycle from requested through terminal state. Serialize or constrain concurrent
partial refunds so their sum cannot exceed the eligible amount. A failed or pending refund must not silently
produce a completed internal credit.

Disputes are separate financial events with evidence deadlines, fees, and possible later wins or losses.
Capture the provider deadline and preserve transaction-time purchase, fulfillment, terms, and communication
evidence. Prevent a pending refund plus a dispute from compensating the customer twice.

For Connect, the charge type determines who is debited and whether a transfer or application fee must be
reversed separately. Never infer “refund” means all marketplace money movements were unwound.

Use “void” precisely. Cancel an uncaptured PaymentIntent to release its authorization; refund a captured
payment; void an eligible unpaid invoice when it should become a terminal zero-value document; and use a
credit note or jurisdiction-approved correction for an open or paid invoice. These actions have different
objects, ledger effects, customer communications, and legal records.

## Keep wallets in an application ledger

A generic wallet, store credit, or partner balance is an application liability. Represent material money
movement with immutable, balanced, currency-scoped journal entries and append compensating entries for refunds,
expirations, disputes, or corrections. Keep buyer spendable value separate from seller earnings or payables.
Credit it only from a verified, idempotent payment transition. Spend it in a database transaction that enforces
sufficient funds and a unique business operation.

Stripe Customer invoice balance, Billing Credits, platform balance, connected balance, transfers, and payouts
have specific Stripe meanings. Do not relabel one as a general wallet. Read the wallet reference before adding
any balance feature and route stored-value, expiration, escheat, money-transmission, and accounting questions
to qualified owners.

## Isolate connected accounts

Resolve the stored `acct_` identifier from an authorized tenant or partner relationship. Never accept an
arbitrary connected-account ID from the request, never request a partner's secret key, and never use mutable
global Stripe account state in queues, Octane, or other long-running workers. Pass account context per SDK
request.

Gate charges, transfers, and payout-facing UX on the exact capabilities and account status required by that
operation. An onboarding return URL proves only that the browser returned. Retrieve current account state or
process `account.updated`; handle missing requirements, restrictions, deauthorization, and disabled external
accounts explicitly.

Remember that a transfer moves Stripe balance to a connected account, while a payout moves connected balance
to an external bank or card. These are different objects, failures, retries, and responsibilities.

## Protect secrets and account boundaries

- Keep secret keys and webhook secrets in server configuration or a secrets manager; use restricted keys
  where supported, separate test/live credentials, rotate them, and never log them.
- Never log PaymentIntent client secrets, Account Link URLs, OAuth codes/tokens, complete webhook payloads,
  or sensitive metadata. Redact before error reporting.
- Account Links are short-lived, single-use credentials. Create them server-side for an authenticated account
  owner, redirect immediately, and never email or persist them as reusable links.
- Reauthorize every refund, transfer, payout setting, billing-portal session, and payment-method action against
  the local owner. Possessing a Stripe ID is not authorization.

## Prove the failure paths

Test at least:

- server-side amount and recipient tampering;
- retry after timeout with the same operation, and reconciliation after an ambiguous response;
- signed, invalid, duplicate, delayed, and reversed-order webhooks;
- PaymentIntent authentication, decline, processing, success, cancellation, and delayed-method failure;
- manual authorization, capture deadline, partial capture, cancellation before capture, and attempted
  cancellation after capture;
- first and renewal invoice failure, trials, grace, cancellation, proration, and pending updates;
- product/price version changes, invoice finalization, void, uncollectible, credit note, discount, usage,
  tax-location failure, and collection-method differences;
- concurrent partial refunds, pending and failed refunds, dispute-before-refund completion, and dispute win/loss;
- PCI data-flow violations, secret/client-secret leakage, 3DS return, card-testing rate controls, and wrong-mode
  credentials or objects;
- wallet double-credit, concurrent spend, reversal, negative-balance policy, and cross-currency rejection;
- incomplete or expired Connect onboarding, restricted capabilities, wrong-account object access, and
  long-running-worker tenant isolation;
- each approved charge type's partial/full refund, fee treatment, transfer reversal, dispute, negative balance,
  transfer failure, and payout failure;
- webhook/API-version upgrade fixtures and sandbox behavior.

Use deterministic Laravel tests for domain policy and replay behavior, Stripe sandboxes and CLI delivery for
provider integration, and Test Clocks for subscription time transitions. Sandbox success does not prove live
capabilities, country eligibility, or production readiness.

## Reconcile and operate

Continuously compare local operations and ledger entries with Stripe objects and Balance Transactions. Detect
events that never reduced, operations stuck without provider IDs, terminal provider states missing locally,
refund or dispute deltas, failed transfers, negative balances, and payout failures. Make event replay safe and
audited; never repair history by editing the original money entry.

For delivery, report the chosen payment and Connect architecture, responsibility matrix, lifecycle states,
idempotency design, webhook scopes, ledger mappings, failure handling, test matrix, reconciliation plan, and
every policy or legal decision still blocking production.
