# Discovery, merchandising, and products

Use this reference to turn a catalog into storefront behavior. Treat every recommendation as a
starting default to validate against representative products, shoppers, devices, and commercial
outcomes.

## Define catalog identities first

Give each concept one owner:

| Concept | Required contract |
|---|---|
| Product family | The underlying item shoppers compare and review |
| Variant or SKU | The purchasable combination of options with its own price, stock, media, and fulfillment state |
| Category | A materially distinct product scope a shopper can browse |
| Attribute or facet | A shared comparison dimension such as size, material, compatibility, or capacity |
| Offer | Price, eligibility, conditions, effective window, quantity rule, and stacking behavior |
| Availability | Operational meaning of in stock, low stock, preorder, backorder, unavailable, and discontinued |
| Compatibility | The source that guarantees an item works with another product, model, or use |

Do not let the presentation layer infer these concepts from titles or URLs. That creates duplicate
variants, stale prices, false compatibility, broken filtering, and inconsistent analytics.

## Make the homepage and navigation expose the real shop

- Show representative routes into the assortment instead of letting one seasonal campaign imply
  the shop sells only that collection.
- Keep product taxonomy distinct from account, help, editorial, and company navigation.
- Give broad parent categories an explicit destination when shoppers need the whole scope. On
  mobile, label it `View all [category]`; do not hide the behavior in a clickable heading.
- Prefer stable, user-controlled promotion modules. Never make an auto-rotating carousel the only
  path to an important category or offer.
- Preserve the same product vocabulary across navigation, headings, search, filters, cards, product
  pages, support, and order history.

There is no universal category depth, menu size, grid count, or homepage module count. Test whether
representative shoppers can infer the assortment and complete known-item, browse, compare, and
problem-based tasks.

## Specify search as a retrieval contract

Build a fixed query corpus from catalog terminology, site-search logs, support contacts, model and
part numbers, misspellings, synonyms, compatibility expressions, and non-product help queries. Cover
the query types the assortment actually receives:

```text
exact product or model
product type
feature or specification
compatibility or relation
use case, theme, or symptom
brand or collection
misspelling or synonym
policy or support question
```

For each query, record relevant product families, acceptable alternates, forbidden mismatches, and
the intended recovery when no suitable product exists. Evaluate result relevance and downstream
purchase or retained value; a result click alone can reward misleading matches.

Autocomplete must remain short enough to scan, distinguish query suggestions from category paths,
and work with arrows, Enter, Escape, touch, and assistive technology. Zero results should explain
the state and offer corrected queries, adjacent categories, useful alternatives, or support. Never
silently relabel unrelated results as matches.

## Design product lists for comparison

Create a card schema per product class. A useful default includes:

- stable product identity and representative image;
- current price and material conditions;
- genuine rating average and count when available;
- visible variation cues without repeating every cosmetic variant as a separate product; and
- the one to three category-specific facts needed to compare that product class.

Keep comparable fields in consistent positions and use consistent labels and units. Do not make
shoppers open every product page to discover fit, capacity, material, compatibility, pack size, or
another primary decision attribute. Show standardized unit price alongside total price where pack
size, weight, volume, or quantity varies and the comparison is valid.

## Make filters and sort state explicit

Derive facets from real decision attributes per category. A global filter set copied everywhere
creates irrelevant controls and hides the dimensions that matter. Define:

- label, value, unit, missing-data behavior, and compatible categories;
- result count and zero-result combination behavior;
- whether unavailable values remain visible and why;
- URL and back-navigation restoration;
- mobile drawer, applied-filter summary, individual removal, and clear-all behavior;
- keyboard, focus, announcement, and loading behavior; and
- analytics identity independent of translated display copy.

Always label the active sort and document what `Recommended`, `Featured`, `Best selling`, or similar
means. Sort order changes what shoppers notice; it is merchandising policy, not a neutral technical
default.

## Preserve the promised variant on the product page

An inbound product or variant link must select the promised configuration and show matching media,
price, currency, availability, and buying state in the first rendered and hydrated views. When a
selection changes, update those fields together and keep the state addressable so back, share, and
reload do not silently revert it.

Expose important small option sets directly, including unavailable states. Use a select, listbox, or
searchable control when the set is too large for buttons. Never leave an old price, image, stock
message, delivery estimate, or URL after a variant change.

## Give the product decision enough evidence

Keep the following discoverable in the main product-page flow:

- identity and decision-relevant description;
- current price and offer conditions;
- variants, quantity, availability, and buying action;
- delivery estimate or estimator and returns summary;
- images with useful detail, alternate angles, scale or context where relevant, and user-controlled
  zoom;
- specifications, materials, fit, dimensions, compatibility, warranty, or care information the
  product requires;
- genuine reviews, rating count and distribution, negative feedback, incentives, and merchant
  responses; and
- clearly separated substitutes and complementary or compatible items.

Use headings and accessible disclosures for long mobile content. Do not hide essential information
in desktop-only tabs or separate mobile subpages that lose orientation. Media supplements product
truth; it does not replace textual dimensions, materials, compatibility, captions, or accessible
alternatives.

## Treat recommendations as hypotheses

Label why an item appears: `Similar alternatives`, `Works with`, `Frequently bought for`, or another
truthful rationale. Guarantee compatibility before claiming it. Measure total store purchase and
contribution, not clicks or revenue credited to the module; a recommender can move purchases among
items without increasing total value.

Test cue density, placement, and rationale locally. Preserve current price, availability, identity,
and other material terms even when a test suggests less information produces more exploration.

## Handle unavailable products without deception

- Temporarily unavailable: preserve product context, show the current state, and offer a truthful
  restock signal, backorder date, or close alternatives only when operations support them.
- Preorder or backorder: show the expected availability basis and what can change.
- Permanently discontinued: state that clearly and offer a genuine successor or category path.
- Not orderable: disable the buying action. Do not accept money and discover availability later.

Do not redirect a product invisibly to another SKU or invent low-stock counts. Keep search, product
page, cart, feed, support, and order acceptance consistent with the authoritative salable state.

## Verify discovery and product decisions

Test with representative catalog tasks and realistic data:

1. first-time assortment inference from home and mobile navigation;
2. known-item, misspelled, compatibility, feature, thematic, and support search queries;
3. no-results recovery and irrelevant-result protection;
4. category-specific filters, combined filters, sort, pagination or loading, back, and deep links;
5. long names, missing optional fields, translated labels, uncommon units, and zero reviews;
6. every variant price, stock, media, URL, and delivery combination;
7. keyboard, screen reader, zoom, 320 CSS-pixel reflow, touch, and focus restoration; and
8. list-to-product-to-cart identity reconciliation in analytics and commerce state.

Report observed failures and their affected products or tasks. Do not issue a generic
`merchandising optimized` verdict.
