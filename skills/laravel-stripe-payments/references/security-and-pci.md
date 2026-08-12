# Security and PCI

PCI compliance is shared responsibility. Stripe's certification and hosted components can reduce the
application's card-data scope; they do not remove the merchant's duty to validate its own compliance. Have the
merchant's acquirer, PCI assessor, or qualified compliance owner determine the applicable questionnaire and
evidence from the deployed data flow. Never promise “PCI compliant” from framework choice alone.

## Minimize the card-data boundary

Prefer a Stripe-hosted Checkout redirect when the product can accept its UX. Use current Stripe-hosted Elements
when checkout must be embedded or customized. In either design, payment details should travel directly from the
customer's browser to Stripe and never through Laravel.

Inventory the real flow before assigning scope:

```text
browser and merchant page
  -> scripts, frames, analytics, tag managers, support widgets
  -> Stripe-hosted collection
  -> Stripe token/PaymentMethod/PaymentIntent identifiers
  -> Laravel, logs, queues, storage, monitoring, support, exports, backups
```

Check every browser script and operational channel, not only the controller. An embedded payment form and a
full-page redirect can have different SAQ eligibility conditions. Keep third-party scripts off payment pages
unless their value justifies the supply-chain exposure, maintain a restrictive tested Content Security Policy,
and follow Stripe's current required origins rather than copying a stale allowlist.

Never collect, proxy, log, persist, email, export, or place in metadata:

- PAN or magnetic-stripe/track data;
- CVC/CVV/CID or PIN data;
- raw bank credentials collected outside an approved hosted flow;
- secret keys, webhook secrets, OAuth codes/tokens, or reusable Account Link URLs.

Store only the provider identifiers and non-sensitive display attributes the UI needs, such as brand, last four,
and expiry returned by Stripe. Do not build a “temporary” raw-card fallback.

## Protect pages, transport, and secrets

- Require HTTPS for every live page and webhook, use currently supported TLS, serve all page resources securely,
  and remove mixed content.
- Keep Stripe.js and hosted components on their documented origins. Do not self-host or modify provider scripts.
- Keep secret keys and webhook secrets in server-side configuration or a secrets manager. Separate test and live
  mode, restrict access and permissions, rotate under an owned procedure, and restart long-running workers after
  rotation when configuration is cached.
- Treat a PaymentIntent client secret as a bearer capability for its intended browser flow. Return it only to an
  authorized participant over TLS, never put it in logs or ordinary URLs, and never use it as application auth.
- Use separate endpoint signing secrets for platform and Connect webhook destinations. Verify the exact raw body
  before parsing and reject mode or account scope mismatches.
- Inventory who can view Dashboard data, issue refunds, change payout details, rotate keys, or replay events.
  Require least privilege, strong authentication, and audit trails for these operator actions.

Do not expose Stripe object existence across tenants. Resolve Customer, PaymentMethod, Subscription, Invoice,
PaymentIntent, Refund, connected account, and payout objects through an authorized local relationship before
retrieval or mutation.

## Support authentication and mandates

Use Checkout, PaymentIntents, and SetupIntents so 3DS and Strong Customer Authentication can transition through
`requires_action` rather than appearing as unexplained failure. Provide a secure return path, then verify the
current PaymentIntent or SetupIntent server-side; a 3DS redirect is not payment confirmation.

For later off-session use, record the customer's agreement and configure the SetupIntent or PaymentIntent for the
actual future-use scenario. Payment-method rules and mandate text vary by method and country. Do not generalize a
card-on-file flow to ACH, SEPA, or another debit method without reading that method's live requirements.

## Defend payment endpoints from abuse

Checkout and current Payment Element integrations include Stripe defenses, but the application still owns its
attack surface. Protect Customer creation, payment-method attachment, SetupIntent, Checkout Session, coupon,
wallet-funding, and low-value payment endpoints with layered controls:

- authentication or a validated server session where the product permits it;
- CSRF protection for browser commands;
- per-account, per-session, per-IP, and behavioral rate limits chosen from measured normal traffic;
- limits on Customers, payment methods, attempts, coupons, and repeated low-value purchases;
- CAPTCHA or another challenge when risk signals justify the friction;
- Radar rules/reviews and 3DS policy aligned with the business's risk appetite;
- anomaly alerts for attempt velocity, declines, blocked payments, new Customers, and credential misuse.

Do not retry hard declines or compromised test traffic indefinitely. Subscription dunning and queue retries can
amplify a card-testing attack; suspend the affected cohort, require a new payment method where appropriate, and
coordinate Radar/provider response.

## Keep PCI operations real

Maintain the deployed card-data-flow diagram, asset and script inventory, provider Attestation of Compliance,
annual merchant attestation, vulnerability and scan evidence required by the chosen validation path, access
reviews, incident response, key-rotation evidence, patching, and change review. Re-evaluate scope when payment UI,
scripts, hosting, Connect account configuration, payment methods, support tooling, or data exports change.

Test at least:

- raw card/CVC fields rejected from Laravel requests and redacted from logs, queues, errors, and analytics;
- Checkout/Elements CSP and HTTPS behavior in the rendered production-like page;
- wrong-mode keys and client secrets, unauthorized object IDs, and expired browser sessions;
- missing or wrong webhook secrets, raw-body mutation, replay, and timestamp rejection;
- 3DS required, abandoned, failed, and completed flows;
- payment-method-specific mandate and delayed-settlement paths;
- card-testing bursts against Customer, SetupIntent, payment-method, and wallet-funding endpoints;
- secret rotation while queues and long-running workers are active.
