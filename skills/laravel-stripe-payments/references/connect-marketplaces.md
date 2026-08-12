# Stripe Connect Marketplaces

“Connect their Stripe” can mean either onboarding a participant into a platform's Connect economic model or
authorizing an application to access an existing independent Stripe account. Decide which relationship exists
before choosing Account Links, embedded onboarding, or OAuth.

## Resolve responsibilities first

Create a written matrix for:

| Decision | Required owner |
|---|---|
| Merchant of record and customer statement identity | approved business/legal policy |
| Stripe fees and platform fee | commercial policy |
| KYC requirements collection and account dashboard | Connect account configuration |
| Refund and dispute handling | charge type plus commercial policy |
| Negative balances and fraud losses | controller configuration plus risk policy |
| Tax calculation/reporting | approved tax policy |
| Countries, currencies, service agreements, and settlement delays | live Stripe eligibility plus policy |

For Accounts v1, inspect the `controller.*` properties that assign responsibilities; legacy Standard, Express,
and Custom labels are bundles, not a sufficient architecture. Accounts v2 has different configuration and
feature availability and may be preview-versioned. Inspect the installed SDK/API and required features before
adopting it; do not mix v1 and v2 casually.

## Select the charge flow deliberately

- **Direct charge:** the charge lives on one connected account. It fits a SaaS or single-seller flow where that
  seller normally owns the customer transaction. Retrieve and refund the object in that account's context.
- **Destination charge:** the platform creates the charge and immediately directs funds to one connected account.
  The platform balance bears provider fees, refunds, and disputes; seller recovery is an explicit reversal.
- **Separate charges and transfers:** the platform charge and one or more transfers are independent. Use it for
  multi-party or deferred allocation only when the product accepts the additional liability and reconciliation.

`on_behalf_of` changes settlement-merchant attributes and can carry country constraints. `transfer_group` only
correlates objects; it does not reserve funds, guarantee a transfer, or reverse one on refund.

Bad:

```text
refund charge -> assume application fee and every seller transfer returned
```

Good:

```text
identify charge type -> refund in correct account -> apply approved fee/reversal plan -> reconcile each object
```

Direct-charge application fees are not automatically refunded. Destination charges require deliberate
`reverse_transfer` and application-fee handling. Separate charges leave transfers untouched until the platform
reverses them, and a reversal can fail when the connected account lacks available balance.

## Onboard without collecting partner secrets

For a platform onboarding sellers or service providers, prefer Stripe-hosted or embedded Connect onboarding so
changing verification requirements remain on Stripe's maintained surface. Request only needed capabilities;
extra capabilities can create extra verification duties.

Account Links are short-lived and single-use. Create one for an authenticated owner, redirect immediately, and
do not email, text, or store it as a reusable URL. The `return_url` does not mean onboarding succeeded. Retrieve
the account or consume account events and inspect required capabilities, requirements, `charges_enabled`, and
`payouts_enabled` for the exact next operation.

Use OAuth only when the product truly needs access to an existing independently controlled Stripe account and
the supported account/API model calls for it. Protect the flow with `state`, exact registered redirect URIs,
one-time code exchange, mode and scope checks, and deauthorization handling. Never ask a partner for `sk_live_*`.

## Implement the secure connection flow

For the normal platform/marketplace relationship:

1. An authenticated, authorized partner owner chooses **Connect Stripe**.
2. The server creates or resumes exactly one locally owned connected-account relationship and stores its `acct_`
   ID, mode, controller/responsibility configuration, requested capabilities, and lifecycle state.
3. The server creates a short-lived Account Link or Account Session and returns it only to that owner for an
   immediate redirect or embedded flow. Stripe collects identity and payout-account details; Laravel does not.
4. The return endpoint treats the browser as untrusted progress information. It retrieves the Account, while
   verified Connect webhooks update requirements and capability state.
5. The application enables only the operation whose exact capability and readiness checks pass. It never turns
   a generic `connected=true` flag into charge, transfer, or payout authority.
6. Money moves under the approved charge type. Every charge, application fee, transfer, reversal, refund,
   dispute, and payout keeps its own idempotent local operation and Stripe object link.
7. The application continuously handles new verification requirements, restrictions, deauthorization, failed
   payout accounts, and partner offboarding without deleting financial history.

A partner who already uses Stripe may be able to reuse information through Stripe's hosted/networked experience,
but the platform still needs an authorized Connect relationship. Do not equate “has a Stripe login” with “has
granted this platform permission.”

## Isolate account context in Laravel

Store the authorized relationship between the local partner and Stripe `acct_` ID. Resolve it from local tenant
state for every operation; do not trust an account ID submitted by the browser.

Use per-request SDK options for `stripe_account` and credentials. Mutable global account state can leak one
tenant's context into another request under Octane, queue workers, or concurrent jobs.

Bad:

```text
Stripe::setAccount($request->stripe_account)
```

Good:

```text
authorized local partner -> stored acct_ ID -> per-request stripe_account option
```

Keep platform-account and connected-account webhook destinations/scopes distinct. Store the event's account
scope, verify with that endpoint's secret, and retrieve direct-charge objects within that same connected account.
Cashier does not provide a complete Connect domain model; use a dedicated account-aware service and event path.

## Gate account readiness continuously

Onboarding completion is not permanent authorization. Monitor required capabilities and account fields such as
currently due, past due, pending verification, disabled reason, charges enabled, and payouts enabled. Handle
account and person updates, restrictions, deauthorization, and failed external accounts.

Sandbox environments can relax capability enforcement. Test application gates for every restricted state rather
than relying on a successful test charge.

## Separate transfer and payout lifecycle

A transfer moves money from the platform's Stripe balance to a connected Stripe balance. A payout moves connected
balance to a bank or eligible card. Record, authorize, and reconcile them separately.

For separate charges and transfers, wait for the approved payment success point before transferring.
`source_transaction` can delay availability but does not eliminate asynchronous-payment failure handling. Failed
transfers are not automatically retried merely because balance later becomes available. A failed payout can
disable its external account; surface that operational state.

Account Debits are constrained recovery tools, not generic wallet subtraction. Require explicit platform
eligibility, account configuration, available balance, currency/country support, consent, and legal approval.

## Test the responsibility matrix

Cover incomplete and expired onboarding, Account Link reuse, OAuth state mismatch and deauthorization when used,
all ready/restricted account states, incorrect account scoping, duplicate/out-of-order events, async payment
failure, failed transfer and explicit retry, full/partial refund and fee policy, insufficient transfer reversal,
dispute loss and win, negative balance, failed payout, external-account disablement, and cross-border rejection.
