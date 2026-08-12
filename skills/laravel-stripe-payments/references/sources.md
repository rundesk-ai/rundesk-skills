# Sources

Verified August 12, 2026. Stripe features, account eligibility, API versions, SDK versions, and country corridors
change frequently. Inspect the installed application and current live documentation before implementation. Stripe
documentation establishes provider behavior; it does not settle merchant-of-record, tax, accounting, stored-value,
money-transmission, or other legal responsibilities.

## Laravel Cashier and Stripe PHP

- [Laravel 13 Cashier documentation](https://laravel.com/docs/13.x/billing) — supported Customer, subscription,
  Checkout, invoice, payment-method, Billing Portal, incomplete-payment, webhook command, signature middleware,
  and webhook-event workflows. The prose API-version labels have differed from installed package behavior, so use
  source and lockfile evidence below for the exact integration.
- [Laravel Cashier Stripe v16.7.0 release](https://github.com/laravel/cashier-stripe/releases/tag/v16.7.0),
  [package constraints](https://raw.githubusercontent.com/laravel/cashier-stripe/v16.7.0/composer.json), and
  [Cashier source](https://raw.githubusercontent.com/laravel/cashier-stripe/v16.7.0/src/Cashier.php) — release date,
  compatible Stripe PHP range, and derivation of Cashier's API version from the installed Stripe SDK. These are
  current upstream facts, not a requirement to upgrade an application.
- [Stripe PHP v20.3.1 API version](https://raw.githubusercontent.com/stripe/stripe-php/v20.3.1/lib/Util/ApiVersion.php)
  and [per-request configuration](https://github.com/stripe/stripe-php/blob/v20.3.1/README.md#per-request-configuration)
  — the API version used by that Cashier-compatible SDK release and request-scoped `stripe_account` options.
- [Cashier issue #1751](https://github.com/laravel/cashier-stripe/issues/1751) — a reproduced community report where
  manually creating a webhook with a newer API version broke an older Cashier subscription handler. It supports
  the version-inspection good/bad pair in `cashier-subscriptions.md`; it does not establish failure prevalence.
- [Cashier issue #1744, maintainer response](https://github.com/laravel/cashier-stripe/issues/1744#issuecomment-2698917172)
  — Laravel Cashier's maintainer states that Cashier does not support Stripe Connect. Current release/source
  inspection supplies the second check behind the dedicated Connect service boundary.
- Cashier v16.7.0 [WebhookController](https://github.com/laravel/cashier-stripe/blob/v16.7.0/src/Http/Controllers/WebhookController.php),
  [Billable charge concern](https://github.com/laravel/cashier-stripe/blob/v16.7.0/src/Concerns/PerformsCharges.php),
  and [SubscriptionBuilder](https://github.com/laravel/cashier-stripe/blob/v16.7.0/src/SubscriptionBuilder.php) —
  signature middleware depends on a configured secret, event timing, and which high-level operations expose
  Stripe request options. These support configuration validation and the centralized SDK boundary; inspect the
  installed release because method signatures can change.

## Payments, saved methods, and fulfillment

- [PaymentIntents](https://docs.stripe.com/payments/payment-intents) — one PaymentIntent per order/session,
  reuse after interruption, idempotency, metadata, and payment lifecycle guidance.
- [Idempotent requests](https://docs.stripe.com/api/idempotent_requests) — first-response caching, parameter
  comparison, and possible key pruning after at least 24 hours. The catalog conclusion is to pair Stripe keys
  with durable domain uniqueness and stored provider IDs.
- [Checkout fulfillment](https://docs.stripe.com/checkout/fulfillment) and
  [custom success pages](https://docs.stripe.com/payments/checkout/custom-success-page) — customers may not reach
  the success page and delayed methods require webhook-aware fulfillment. These support the redirect good/bad pair
  in `payment-lifecycle.md`.
- [SetupIntents](https://docs.stripe.com/payments/setup-intents) — preparing payment methods for future use and
  the importance of correct usage and customer agreement.
- [Place a hold on a payment method](https://docs.stripe.com/payments/place-a-hold-on-a-payment-method) — manual
  authorization, `requires_capture`, method-specific expiry, partial capture, normally single capture, and
  canceling an uncaptured PaymentIntent. It supports the authorization/capture good/bad pair and the distinction
  between canceling an authorization and refunding captured funds.
- [Dynamically updating payment amounts](https://docs.stripe.com/payments/advanced/dynamically-update-amounts)
  and [currency minor units](https://docs.stripe.com/currencies) — server-authoritative amounts and currency-
  specific units, including zero-decimal currencies.

## Webhooks, subscriptions, and testing

- [Stripe webhooks](https://docs.stripe.com/webhooks) and
  [signature troubleshooting](https://docs.stripe.com/webhooks/signature) — exact raw-body verification,
  endpoint-specific secrets, retries, duplicate and unordered delivery, quick acknowledgment, and asynchronous
  processing.
- [Stripe PHP webhook verification source](https://github.com/stripe/stripe-php/blob/v20.3.1/lib/Webhook.php) —
  SDK implementation for signature construction and timestamp tolerance.
- [Subscription webhooks](https://docs.stripe.com/billing/subscriptions/webhooks) — asynchronous lifecycle,
  invoice events, status meanings, and the fact that an active subscription does not prove every invoice paid.
- [Pending subscription updates](https://docs.stripe.com/billing/subscriptions/pending-updates) — deferring supported
  subscription changes until payment succeeds.
- [Build a subscriptions integration](https://docs.stripe.com/billing/subscriptions/build-subscriptions) and
  [manage Products and Prices](https://docs.stripe.com/products-prices/manage-prices) — Product/Price roles,
  server-side Price use, creating a replacement when amount changes, archiving, and the fact that existing
  subscriptions remain on archived Prices until changed.
- [Change a subscription's Price](https://docs.stripe.com/billing/subscriptions/change-price) — subscription-item
  replacement, proration previews, billing-period consequences, schedules, and pending updates for payment-
  contingent changes.
- [Usage-based billing concepts](https://docs.stripe.com/billing/subscriptions/usage-based/how-it-works) — Meters,
  asynchronous summaries, and unique meter-event identifiers.
- [Smart Retries](https://docs.stripe.com/billing/revenue-recovery/smart-retries) — automatic retry behavior,
  webhook attempts, hard declines, and final recovery action.
- [Stripe Billing testing and Test Clocks](https://docs.stripe.com/billing/testing/test-clocks/api-advanced-usage)
  — supported time simulation and explicit limitations. The skill keeps deterministic domain and non-subscription
  failure tests in addition to Test Clocks.

## Refunds, disputes, security, and reconciliation

- [Refunds](https://docs.stripe.com/refunds) and [Refund API](https://docs.stripe.com/api/refunds/create) — partial
  refund limits, pending or failed behavior, and provider Refund lifecycle. These support the refund good/bad pair
  in `payment-lifecycle.md`.
- [Disputes](https://docs.stripe.com/disputes) and [responding to disputes](https://docs.stripe.com/disputes/responding)
  — separate financial reversal/fee effects, provider evidence deadline, and final evidence submission behavior.
- [Stripe integration security](https://docs.stripe.com/security/guide) and
  [API key practices](https://docs.stripe.com/keys-best-practices) — hosted collection, secret-key handling,
  restricted keys, rotation, TLS, CSP, and storage guidance.
- [3D Secure authentication](https://docs.stripe.com/payments/3d-secure/authentication-flow) — PaymentIntent and
  SetupIntent authentication states and customer action. It supports treating the return flow as incomplete until
  authoritative provider state is checked.
- [Protect against card testing](https://docs.stripe.com/disputes/prevention/card-testing) — recommended payment
  integrations, session/CSRF checks, rate limits, CAPTCHA, behavioral limits, monitoring, Radar, and the risk of
  excessive retries. It supports the layered-abuse controls in `security-and-pci.md`.
- PCI Security Standards Council [FAQ 1438](https://www.pcisecuritystandards.org/faqs/1438/) and
  [FAQ 1604](https://www.pcisecuritystandards.org/faqs/1604/) — SAQ A eligibility depends on the complete payment-
  page implementation and retains merchant responsibilities. These independent sources support the warning that
  Stripe-hosted fields reduce scope rather than guarantee compliance.
- PCI Security Standards Council [FAQ 1588](https://www.pcisecuritystandards.org/faqs/1588/) — the script-security
  SAQ A eligibility condition differs for embedded payment forms and full redirects. It supports deriving the
  actual PCI validation path from the deployed payment page rather than declaring it from the Stripe product name.
- [Stripe balance transaction types](https://docs.stripe.com/reports/balance-transaction-types) and
  [report selection](https://docs.stripe.com/reports/select-a-report) — provider cash effects and reporting
  categories beyond Charges alone.

## Stripe Connect

- [SaaS platforms and marketplaces](https://docs.stripe.com/connect/saas-platforms-and-marketplaces) and
  [Connect charge types](https://docs.stripe.com/connect/charges) — role, merchant-of-record, liability, statement,
  fee, refund, dispute, and object-scope consequences of direct and indirect charges.
- [Controller properties migration](https://docs.stripe.com/connect/migrate-to-controller-properties) — current
  Accounts v1 responsibility properties and legacy type mappings.
- [Accounts v2](https://docs.stripe.com/connect/accounts-v2) and
  [v2 connected-account configuration](https://docs.stripe.com/connect/accounts-v2/connected-account-configuration)
  — configuration model, preview API version shown in current documentation, and feature limitations. These
  support inspecting required features rather than universally selecting v2.
- [Connect onboarding](https://docs.stripe.com/connect/onboarding) and
  [hosted onboarding](https://docs.stripe.com/connect/hosted-onboarding) — hosted/embedded default, changing
  requirements, one-time Account Links, authenticated redirects, and return URL limitations.
- [OAuth for Standard accounts](https://docs.stripe.com/connect/oauth-standard-accounts) — Stripe does not
  recommend OAuth for new Connect platforms; documents `state`, redirect, code, scope, and deauthorization duties
  when OAuth is the actual relationship.
- [Account capabilities](https://docs.stripe.com/connect/account-capabilities),
  [verification handling](https://docs.stripe.com/connect/handling-api-verification), and
  [Connect testing](https://docs.stripe.com/connect/testing) — minimum capability requests, readiness fields,
  lifecycle events, and sandbox capability limitations.
- [Direct charges](https://docs.stripe.com/connect/direct-charges),
  [destination charges](https://docs.stripe.com/connect/destination-charges), and
  [separate charges and transfers](https://docs.stripe.com/connect/separate-charges-and-transfers) — account scope,
  application-fee behavior, refund/transfer reversal options, `transfer_group`, `source_transaction`, and transfer
  failure behavior. These support the Connect refund good/bad pair.
- [Connect disputes](https://docs.stripe.com/connect/disputes) and
  [account balances](https://docs.stripe.com/connect/account-balances) — dispute debit/recovery and negative-balance
  responsibility by charge/account configuration.
- [Connected-account payouts](https://docs.stripe.com/connect/payouts-connected-accounts) — transfer versus payout,
  payout failures, and external-account disablement.
- [Account Debits](https://docs.stripe.com/connect/account-debits) — consent, liability, country, currency, and
  available-balance restrictions. It supports rejecting Account Debits as a generic wallet primitive.
- [Connect webhooks](https://docs.stripe.com/connect/webhooks) — platform and connected-account event scopes and
  account-context retrieval.
- [Cross-border payouts](https://docs.stripe.com/connect/cross-border-payouts) — dynamic country, currency, service-
  agreement, and platform-eligibility constraints. The skill deliberately does not freeze a country matrix.

## Wallet and ledger boundaries

- [Stripe Customer invoice balance](https://docs.stripe.com/billing/customer/balance) — immutable transaction
  ledger automatically applied to later invoices, currency scope, and inability to target or skip arbitrary
  invoices. This supports not treating it as a general checkout wallet.
- [Stripe Billing Credits](https://docs.stripe.com/billing/subscriptions/usage-based/billing-credits) — immutable
  credit-grant ledger for supported subscription/usage-billing scenarios, not a generic stored-value balance.
- Martin Fowler, [Accounting Narrative](https://martinfowler.com/eaaDev/AccountingNarrative.html) — practitioner
  treatment of entries, accounts, transactions, derived balances, and reversal instead of destructive history.
  It supports the append-only ledger and compensating-entry model; it is design guidance, not accounting law.
- Modern Treasury, [Ledger guarantees](https://docs.moderntreasury.com/ledgers/docs/ledgers-guarantees) — practitioner
  implementation guidance for immutable double-entry transactions, per-currency balance, atomic posting, and
  idempotency. It supports the balanced-journal recommendation; it is a vendor's design model, not a universal
  accounting or regulatory authority.

## Invoicing, corrections, and tax configuration

- [Stripe Invoicing overview](https://docs.stripe.com/invoicing/overview) and
  [invoice workflow transitions](https://docs.stripe.com/invoicing/integration/workflow-transitions) — draft,
  open, paid, void, and uncollectible states; finalization; collection; deletion limits; and terminal voiding.
- [Credit notes](https://docs.stripe.com/invoicing/dashboard/credit-notes) — reducing an open or paid invoice and
  allocating a paid-invoice correction among refund, customer credit, or approved out-of-band amount. It supports
  distinguishing an invoice correction from a payment refund.
- [Subscription invoices](https://docs.stripe.com/billing/invoices/subscription) — automatic subscription invoices
  and the subscription-state consequences of voiding particular subscription invoices.
- [Collect tax in Checkout](https://docs.stripe.com/payments/checkout/taxes),
  [Stripe Tax setup](https://docs.stripe.com/tax/set-up), and
  [customer location handling](https://docs.stripe.com/tax/customer-locations) — Product tax code, Price tax
  behavior, customer location, per-object enablement, existing-object migration, and failure/disable behavior.
  These establish processor mechanics, not the business's tax registration or obligation.

## Source map for local examples

- Stable retry versus a new PaymentIntent maps to Stripe's PaymentIntent and idempotency contracts. Durable local
  uniqueness is the catalog's engineering conclusion because provider keys can be pruned.
- Webhook fulfillment versus success-route fulfillment maps to Stripe Checkout fulfillment and custom-success-
  page guidance.
- Compatible versus newest webhook version maps to Cashier source/release evidence and issue #1751.
- Refund state versus immediate completion maps to Stripe refund lifecycle documentation.
- Authorization/capture/cancel versus deleting or refunding maps to Stripe's manual-capture lifecycle.
- Products/Prices and invoice void/credit/refund distinctions map to Stripe's catalog, invoice lifecycle, and
  credit-note documentation.
- Connect refund plus explicit reversals maps to the three charge-type references.
- Request-scoped versus global connected-account context maps to Stripe PHP's per-request configuration and
  Laravel's long-running worker model; the cross-tenant failure is the catalog's concurrency conclusion.
- Balanced immutable wallet journals versus direct balance mutation map to Fowler's accounting patterns, Modern
  Treasury's implementation guarantees, and Stripe's own immutable invoice-balance and Billing Credit ledgers.
  The exact application accounts and schema remain project-specific.

## Coverage limits

- No live Stripe account, Dashboard configuration, regional eligibility response, tax registration, accountant
  determination, QSA assessment, banking contract, or legal opinion was inspected.
- Accounts v2 and cross-border availability are especially volatile. Verify the chosen API namespace and account-
  specific eligibility before implementation.
- Cashier and Stripe release monthly or frequently. The checked releases establish why installed-version
  inspection is necessary; they are not permission for an unrequested dependency upgrade.
