# Pre-auction evaluation

Given a monthly auction sheet, test the **ARV** and re-run the sheet's own bid model on
the result. That is the whole job.

This is **not** a title search — that is `Auction Sheets/title-cli`. It is **not** an
appraisal, and it does not inspect anything. It answers one question: *is the number the
bid is built on defensible?*

---

## 1. Why the ARV is the only target

The bid model is arithmetic. Every input except one is either known or a policy choice:

| Input | Where it comes from |
|---|---|
| Yearly tax, taxes owed, utilities, HOA, liens | County / title run — known |
| Credit bid, unpaid balance, loan terms | Servicer posting / title run — known |
| Profit %, carry months, interest rate | Paul's policy — a choice, not an estimate |
| Rehab, contingency | Walk-through — an observation |
| **ARV** | **An estimate. The only one.** |

So evaluation = attack the ARV, and leave everything else alone. Changing the sheet's cost
policy is a different conversation and should not be smuggled into a comps report.

---

## 2. Validation gate — reproduce before you revise

**Before changing any input, reproduce the sheet's printed Low and High bids from the
sheet's own numbers.** If you cannot land within ~$600, you have misread the sheet and
anything downstream is noise.

```
B    = [ ARV·(1−p) − H ] / (1 + r)
H    = fixed + 0.05·ARV                     # 3% commission + 2% closing
fixed = rehab + yearly tax + taxes owed + utilities + HOA/yr + additional liens + contingency
r    = effective interest as a fraction of the bid,
       back-solved from the sheet's own two rows: mean(interest_low/bid_low, interest_high/bid_high)
```

`r` is *not* simply 9% × carry/12 — the sheet's interest line moves with the bid, so
back-solve it per property rather than assuming. Measured range Sept 2026: 0.047–0.052 on
6-month carries, 0.146 on Willow Bend's 12-month carry.

Sept 2026 result: **8 of 9 sheets reproduced within $600**; Willow Bend within $767. That
residual is the 12-month carry's non-linearity and is acceptable. `src/model.py` runs this
gate.

---

## 3. Evidence hierarchy

Ranked by how much it should move your number. **The top of this list beats the bottom of
it even when the bottom is unanimous.**

1. **The property's own listing history.** What it actually failed or managed to sell for.
   Nothing else is this direct. Shumard listed at $545,000, cut to $529,900, withdrew
   unsold — a completed experiment. Washington sold 19 May 2025 at $389,900 after an 8.3%
   cut — an actual arm's-length trade.
2. **Size-matched live asks in the same subdivision.** Matched address-by-address from the
   county roll to live listings. These are what a buyer can choose instead of your house.
3. **A recent arm's-length sale of the subject itself.**
4. **The AVM band** (Ellis CAD, Zillow, Realtor, Redfin, Cotality). A sanity check on
   whether you are in the right postcode. Not evidence — see §4.
5. **Cotality's sold-comp table.** Imputed, not recorded. Directional only — see §4.

### Why AVMs rank low

They are not independent opinions. Five models trained on largely the same public records,
and in a non-disclosure state leaning on the same imputed sale data. Adding a fifth to four
narrows the apparent spread without adding information — it buys false confidence.

Shumard is the proof: **all five AVMs agreed and all five were wrong in the same
direction**, because every one anchored to builder contract prices. A sixth would not have
helped. One live resale ask did.

---

## 3a. The market layer

The ARV says what the house is worth. The market layer says **whether the exit is realistic**, and
it is the only part of this method that can move a bid without touching a comp.

Source: **Realtor.com Research inventory files** — the same ones the August listings review used.

```
https://econdata.s3-us-west-2.amazonaws.com/Reports/Core/RDC_Inventory_Core_Metrics_County.csv
https://econdata.s3-us-west-2.amazonaws.com/Reports/Core/RDC_Inventory_Core_Metrics_Zip.csv
                                    ...RDC_Inventory_Core_Metrics_County_History.csv
                                    ...RDC_Inventory_Core_Metrics_Zip_History.csv
```

> The **Core** files are a single-month snapshot. Only the **_History** files carry the time series,
> and the trend is the whole point — always pull History. County history is ~100 MB, zip history
> ~820 MB.

### The two findings that matter

**Per-foot pricing is flat.** Ellis County went $194/sf to $196/sf over the 25 months to July 2026,
+1.0%. By zip: Waxahachie 75165 exactly flat, Oak Leaf 75154 −0.6%, Midlothian 76065 +3.0%. Median
*list* prices rose 2–10% over the same window, but that is **mix** — bigger and newer houses coming
to market — not the same house appreciating. **Never underwrite appreciation during the carry.**

**Seasonality is severe and it lands on this auction.** Pooled county median days-on-market by
calendar month: 52 in Apr/May, 53 in Jul, then 60 Aug, 66 Sep, 70 Oct, 72 Nov, **77 Dec, 78 Jan**.
A property bought at a 1 September sale and listed in October meets the rising half of that curve
and does not see spring conditions until March.

### Applying it to the bid

The sheets' 6-month carries run September to March — exactly the minimum to reach the spring window,
with no slack. Test the sensitivity rather than asserting it:

| | |
|---|---|
| Carry 6 → 9 months | costs **$7,000–$12,700** of bid capacity, scaling with property size |
| Offsetting cushion | every sheet charges a **full year** of property tax against a 6-month carry |

That over-costing is real and absorbs much of the slow-season risk, which is why the seasonality
finding **tightens** bids rather than breaking them. Scale utilities with the carry; leave the tax
line alone, since it is already annual.

### What it changed on the September run

One ARV. **2052 Willow Bend $760,000 → $735,000** — 75154 has the weakest absorption of the three
zips (37% pending ratio), flat per-foot pricing across the series, and a 12-month carry spanning two
slow seasons with nothing to offset it. The revision moved the central value from the top of the AVM
band to its middle.

Nothing else moved, and that is the correct outcome: the market data contradicts *appreciation
assumptions*, and this method never made any. An upward ARV revision is a statement about today's
level, which flat-but-not-falling pricing supports.

### Denominator discipline

Realtor.com publishes `price_reduced_share`, and it is **not** reproducible from the counts in the
same row: July 2026 Ellis shows 464 reduced against 1,055 active (44%) and 1,513 total (31%), while
the `price_reduced_share` field reads 0.2369. Three different numbers. **Quote the raw counts and
state the denominator**, never the share field alone.

### Submarkets are not one market

Midlothian, Waxahachie and Oak Leaf run different price levels and opposite inventory trends —
in July 2026 Midlothian actives were +14.5% YoY while Waxahachie was −12.7%. Compute county-wide for
context, but drive every per-property verdict off its own zip.

---

## 4. Failure modes

Each of these cost real effort to find. Do not rediscover them.

### Builder anchoring
In a subdivision where the builder is still selling, every AVM anchors to builder contract
prices, which run well above resale. Shumard's Oaks of North Grove: builder contracts
median **$167/sf**, resales asking **$141/sf**. The gap is structural — a resale competes
against new construction with incentives — and no AVM sees it.

**Test:** count active builder listings in the subdivision. If the builder is still there,
discount the AVMs toward the resale asks.

### $/sf falls as size rises
**Never apply a subdivision's raw median $/sf to a subject of a different size.** Garden
Valley Ranch's actives median $172/sf, but every one of them was 1,558–2,103 sf; the
2,460 sf subject belongs nearer $145–155. Compare only against rows within ~25% of subject
size, or regress $/sf on size.

### Cotality sale amounts are modelled, not recorded
Texas discloses nothing, so Cotality imputes. Signatures seen Sept 2026:
- The same amount repeats **exactly** across different houses in different reports
  ($406,598.73 appears for both 309 Western Sky and 330 Windsor; $506,250 twice).
- Many resolve to a round loan figure ÷ 0.8 — a price imputed from the recorded mortgage
  at 80% LTV.
- Junk rows survive: 395 Haven Rd at $58,500 on 2,438 sf ($24/sf) is not an arm's-length
  sale.

Filter to `$/sf > 60` at minimum, use the median directionally, and never let a single
Cotality comp decide anything.

### The sheet's square footage can be wrong
Sept 2026: **10407 Walnut Ridge** printed 1,702 sf. Ellis CAD says 3,184; Zillow says
3,529. Eight of nine matched CAD exactly, so it is rare — but it is load-bearing, because
the **rehab budget is sized off it** ($25,530 was set against a house half the real size).

**Always verify sqft against the CAD improvement endpoint before using $/sf anywhere.**

### Blank AVM cells track missing URLs
Where a sheet has no Redfin or Realtor URL, that AVM cell is blank — the scraper could not
find the listing. Sept 2026: 4 blanks, all matching a missing URL. **Not worth chasing**
(see §3); spend the effort on comps for thin subdivisions instead.

---

## 5. Data sources and their gotchas

### Ellis CAD — TrueProdigy API
Contract documented in `Auction Sheets/ECADscraper.js`. No auth beyond a minted token.

- `POST /trueprodigy/cadpublic/auth/token` `{"office":"Ellis"}` → `body.user.token`
- `POST /public/property/search?page=N&pageSize=100` — filter on `streetPrimary` (address)
  or `legalDescription` (whole subdivision), `mlike` operator. Robust.
- `GET /public/propertyaccount/<pAccountID>/improvement` — living area, year built,
  class, per-detail areas. **Key on `pAccountID`, not `pid`.**
- `GET /public/propertyaccount/<pAccountID>/land`, `/value` — also available.

> **WAF.** The `propertyaccount/*` endpoints sit behind an AWS WAF. An 8-thread burst got
> the IP 403-blocked for roughly 40 minutes. **Serial, ≥1 s between calls.** The search
> endpoint stayed up throughout — only `propertyaccount/*` was blocked. A full Chrome
> User-Agent is required; a bare `Mozilla/5.0` fails (`ECADscraper.js:33`).

Use codes vary by subdivision — `*RSTND`, `*USTND`, `*UXTRA`, `*UBASIC`, `*SSTND` are all
residential. Filter on `startswith('*')`, not one literal code, or subdivisions silently
return zero.

Search terms need care: `"DOVE CREEK"` matches the rural *Dove Creek Acres*; the subject's
subdivision is `"DOVE CREEK PH"`. Always take the term from the subject's own
`legalDescription`.

### Cotality AVM reports
Drive: `1_Auctions/<year>/<NN_Month>/Cotality/<ADDRESS> - <CLIP>.pdf`, synced locally under
`~/Library/CloudStorage/GoogleDrive-paul@recast-properties.com/My Drive/`.

Four pages, text-layer PDFs — PyMuPDF reads them, no OCR. Each carries the estimate, low
and high range, confidence score, FSD, the sold-comp table, and ~20 nearby THVX estimates.

> The value exists **only in the PDF**. Cotality's CSV export drops the page header, and
> the valuation *is* the page header. Do not switch to CSV.

Parsing: page furniture (`© 2026 Cotality`, `Page N of 4`, the repeated address/APN/CLIP
block) interleaves into the table stream and breaks fixed-stride parsing. Filter it first,
then anchor records on the `N.NN mi` distance token. `src/cotparse2.py`.

Not every property has one — Shumard has no report, which is exactly why its ARV drifted.

### Zillow via Apify
Actors are the pipeline's own (`PropertyValueScraper.js`): `maxcopell/zillow-detail-scraper`,
`maxcopell/zillow-scraper`. Token in `Auction Sheets/Secrets.js`.

- **Detail scraper** on the subject's Zillow URL (already on each sheet) → `priceHistory`,
  status, Zestimate, rent Zestimate, tax history, resoFacts. This is the highest-value
  Apify call in the whole method.
- **Area sweep** (`zillow-scraper`) for supply. **`MAP_MARKERS` caps near 400 results per
  search URL.** Three regional boxes truncated before reaching Dove Creek, Greenway Trails
  and Oak Leaf Farms, which is why those three came back with 0–1 comps. **Use one tight
  box per subdivision**, or `PAGINATION_WITH_ZOOM_IN`.

> `daysOnZillow` counts across relist cycles, not time-to-contract. It read a 584-day median
> where the true list-date → contract-date median was **230**. Compute it from
> `priceHistory` instead: first `Listed for sale` → `Pending sale`.

Sold records in Texas return `price: ""` and `priceLabel: "$--"`. Sale **dates** are
available; prices are not. The `Pending sale` price in `priceHistory` is the last list price
before contract — the closest public proxy, and it sits above net because builder incentives
come off outside the list.

---

## 6. Texas non-disclosure — the standing constraint

No closed sale price is public. Zillow returns blank. Cotality's are modelled. Everything
else on any page produced here is an **asking price** or an **AVM output**.

**Never present a derived clearing price as an observed transaction.** Every report must say
so on its face. This is the same fail-closed posture the title screen uses.

---

## 7. Running it

Scripts in `src/` are a manual pipeline, run in order from a scratch directory holding the
exported sheet PDFs. There is no automation and no checkpointing yet.

| Step | Script | Output |
|---|---|---|
| 1 | `parse.py` | `sheets.json` — every field off the property-tab PDFs |
| 2 | `subj.py` | `subjects.json` — CAD identity + **sqft verification** |
| 3 | `harv.py` | `subs_cad.json` — whole-subdivision rolls |
| 4 | `cotparse2.py` | `cotality.json` — AVM values, sold comps, nearby estimates |
| 5 | *(Apify)* | Zillow subject detail + per-subdivision sweeps |
| 6 | `join.py` | `actives.json` — county roll × live listings |
| 6b | `market.py` | `market.json`, `market_hist.json` — zip + county conditions and the 25-month series |
| 7 | `model.py` | **validation gate** — reproduce printed bids |
| 8 | `verdict.py` | `verdicts.json` — central ARV + revised bids |
| 9 | `gen.py` (calls `mktsec.py`), `genidx.py` | per-property reports + index |

`verdict.py` holds the per-property ARV calls and their written rationale. **That file is
judgment, not computation** — it is where a human decides, and it should stay that way.

---

## 8. Worked example — September 2026

`runs/2026-09/` holds the full data set for nine properties. Headline: **seven ARVs
conservative, two high.** Shumard was the only property with no Cotality report and the only
one where the ARV ran materially high — the correlation is the point of §3.

Two properties carried cleared credit bids, and re-running the model at the comps-derived
ARV changed the answer on both: Log Cabin gained ~$31,000 of headroom the sheet did not
show; Brushwood gained ~$4,000.

---

## 9. Known gaps

- **Redfin and Realtor site data unused.** Only their AVM point values are read, off the
  sheet. Their price histories and DOM are reachable through the same Apify actors
  (`solidcode/realtorcom-scraper`, `h4sh/redfin-scraper`) and are not wired in. Deliberate —
  §3 says comps beat AVMs — but the *site data* would rank high on the §3 hierarchy, unlike the point values.
- **Three Sept subdivisions returned 0–1 live comps** (Dove Creek, Greenway Trails, Oak Leaf
  Farms) because of the `MAP_MARKERS` cap. Those three reports lean on AVMs alone. Fix is
  per-subdivision sweeps.
- **No absorption modelling.** Time-to-sell drives the carry, and the carry is a policy
  input the sheet sets by hand. Shumard's subdivision ran a 230-day median to contract
  against a 6-month carry assumption.
- **Nothing is automated or checkpointed.** Unlike `title-cli`, a failed run restarts.
