# Cashier Subscriptions

## Verify the installed version contract

Laravel Cashier wraps selected Stripe Billing workflows; its supported API surface and exact Stripe API version
depend on the installed Cashier and `stripe/stripe-php` releases. Inspect `composer.lock`, `Cashier::STRIPE_VERSION`,
and the Stripe SDK API-version constant. Do not copy the version printed in current prose documentation into a
webhook configuration without checking the package.

Prefer Cashier's webhook command when it creates the endpoint compatible with the installed package. If endpoint
creation is managed elsewhere, set the same version deliberately, initially disable traffic, replay saved event
fixtures, and enable only after subscription state converges.

Bad:

```text
create webhook with Stripe's newest API version -> send it directly to Cashier
```

Good:

```text
inspect locked Cashier/SDK version -> create matching endpoint -> replay fixtures -> enable
```

A documented Cashier issue reproduces the failure: a newer manually selected webhook version omitted a field an
older Cashier handler expected.

## Choose the billable owner explicitly

Cashier defaults to the application User, but account-oriented SaaS often bills a tenant, organization, or other
model. Decide before creating Customers or subscriptions. Enforce authorization between the acting user and the
billable owner for Checkout, payment methods, invoices, refunds, and Billing Portal sessions.

Use Cashier for platform-owned Stripe Customers and subscriptions. Do not stretch Cashier's Customer assumptions
into Stripe Connect account onboarding or connected-account charge handling.

Inspect whether the installed Cashier method exposes Stripe request options before using it for a retryable
money command. Some high-level charge, payment, refund, subscription-create, and subscription-mutation methods
do not accept a persistent `idempotency_key` or connected-account scope even though Stripe PHP does. In that
case, use one centralized Stripe PHP adapter with request options and preserve the Cashier boundary for the
Customer/subscription state it supports. Automatic SDK retries do not protect a later Laravel job retry.

## Define subscription and entitlement policy

Keep provider subscription status, invoice payment state, and application entitlement separate. Resolve policy
for:

- trial access and trial payment-method requirements;
- first invoice requiring authentication or remaining `incomplete`;
- renewal `past_due`, `unpaid`, or `paused` behavior;
- grace periods and dunning;
- immediate versus period-end cancellation;
- resume eligibility;
- prorations, credits, downgrades, and refunds;
- upgrades that must not take effect until payment succeeds.

Use pending updates for the last case. Without them, Stripe can apply certain subscription changes even when the
invoice for that change is not successfully paid.

Bad:

```text
subscription.status == active -> every invoice is paid -> grant every entitlement
```

Good:

```text
provider status + paid-invoice evidence + explicit grace/dunning policy -> entitlement transition
```

Cashier models one active subscription per application-defined type. Give genuinely concurrent subscriptions
different types or adopt a separately reviewed model; creating duplicate `default` subscriptions does not make
both reliably addressable through Cashier's normal helpers.

## Preserve Cashier's webhook behavior

Configure and validate the signing secret so Cashier's signature middleware is active. In current Cashier,
that middleware is conditionally attached only when the secret is truthy; an omitted secret does not fail closed
by itself. Exempt only the exact webhook route from CSRF. Keep Cashier's controller for the resources it owns,
and attach domain behavior through `WebhookReceived` or `WebhookHandled` listeners when appropriate. Queue
expensive work only after durable capture and database commit.

Do not assume event order or synchronous completion. Cover subscription, invoice, payment failure, customer
deletion, and payment-method changes used by the installed Cashier version.

Cashier emits `WebhookReceived` before its recognized handler changes local models and `WebhookHandled` after a
recognized handler succeeds. Unsupported events can be acknowledged without a `WebhookHandled` event. Choose
the listener boundary deliberately and list every Stripe event the application itself must reduce.

## Test time and authentication

Use deterministic tests around entitlement policy and webhook replay. Use Stripe Test Clocks for supported
subscription time transitions such as trials, renewals, schedules, and prorations, while respecting their object
and rate constraints. Test ordinary payments, refunds, disputes, and arbitrary event reordering separately.

Before an upgrade, run the old fixture corpus through the new code, create new sandbox objects under the target
API version, and verify local Customer, subscription, item, invoice, and entitlement state.
