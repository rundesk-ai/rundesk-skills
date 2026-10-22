# Examples

## Rough notes to a ticket

**Before**, as handed over:

> customers keep saying the quote form wipes their answers?? I tried on my iphone and yeah hitting
> back clears everything. desktop chrome seems fine. probably the history API thing we changed last
> sprint. can we also save their progress so they can come back tomorrow

**After:**

```markdown
**Title:** Quote form loses answers on Back in mobile Safari

**Problem**
On iPhone Safari, pressing Back on the quote form clears every answer the shopper has entered. Shoppers have to start again, and support is hearing complaints about it.

**Steps to reproduce**
1. On an iPhone, open the quote form in Safari.
2. Answer the first three questions, moving forward after each.
3. Press Back.

**Expected:** The previous question shows with its answer kept.
**Actual:** The form returns to the first question with every answer empty.

**Tested**
- Fails on iPhone Safari [iOS version?], every time.
- Works on Chrome desktop.
- Not yet tried on Android or iPad.

**Done when**
- The steps above keep every answer on iPhone Safari.
- Back still keeps answers on Chrome desktop.
```

**Notes, as handed back:**
- Suspected: last sprint's change to page history handling; not confirmed.
- Saving progress to return another day is a new request, not part of this fix; it needs its own task.
- How many complaints support has logged would give the Problem its cost.

## One report, two failures

**Before:** "Checkout is broken on mobile — the promo code field rejects valid codes, and the pay
button overlaps the footer so you can't tap it."

These are two failures a reader can tell apart, on different parts of the page, likely with
different fixes. The rewrite leads with "Split in two: different symptoms that will be fixed and
checked separately", then writes each ticket in full — one for valid promo codes rejected, one for
the pay button that cannot be tapped — each with its own steps, Tested and Done when.
