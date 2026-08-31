# Recast-preauction — pre-auction ARV evaluation

**Read `docs/PRE-AUCTION-EVALUATION.md` before doing anything here.** It is the method, and
every rule in it was paid for with a measured failure.

## What this is

Given the monthly auction sheet, test the **ARV** on each property and re-run the sheet's
own bid model on the result. One question: *is the number the bid is built on defensible?*

## What this is not

- **Not a title search.** That is `Auction Sheets/title-cli`, and it stays there. Reports
  produced here must say plainly that they do not speak to liens.
- **Not an appraisal**, and nothing here inspects a property. Condition comes from Paul's
  note on the sheet.
- **Not a re-litigation of Paul's cost policy.** Profit %, carry months, rehab and the 9%
  money are his choices. Change the ARV; leave the rest.

## Relationship to the other workstreams

| Repo | Relationship |
|---|---|
| `Auction Sheets/` | Upstream. Produces the sheet, the Cotality folder and the title runs. This repo **reads** its `ECADscraper.js` API contract and its `PropertyValueScraper.js` Apify actors, and uses `Secrets.js` for tokens. It writes nothing back. |
| `Recast-analyst/` | Adjacent, not the same. That one evaluates *listings* for the public `/reports/` pages. This one evaluates *auction candidates* for a bid, and its output is private. Do not merge them; the rigor contract there (fail closed to NOT VERIFIED) is a good model to borrow from. |

## Current state — 2026-08-31

**First run complete.** Nine September properties evaluated; `runs/2026-09/` holds the data.
Method and code are real and validated. Nothing is automated.

Headline finding: **seven ARVs conservative, two high.** 1751 Shumard was the only property
with no Cotality report *and* the only one where the ARV ran materially high — see §3 of the
method doc for why that correlation is the whole argument for ranking comps above AVMs.

Reports were published as private Artifacts, not to any site. URLs in `runs/2026-09/urls.json`.

### Open items, in priority order

1. **Three subdivisions came back with 0–1 live comps** — Dove Creek (5614 Log Cabin),
   Greenway Trails (10407 Walnut Ridge), Oak Leaf Farms (2052 Willow Bend). Cause is the
   Apify `MAP_MARKERS` ~400-per-box cap; three regional boxes truncated before reaching
   them. Those three reports lean on AVMs alone, and two of them carry the batch's biggest
   decisions (a cleared credit bid, and the +$110,000 ARV gap). **Fix: one tight bounding
   box per subdivision.** This is the highest-value next step.
2. **10407 Walnut Ridge sqft is wrong on the sheet** — 1,702 printed, 3,184 per CAD, 3,529
   per Zillow. Flagged in the report but *not fixed upstream*. The rehab budget ($25,530)
   was sized against the wrong house.
3. **Redfin and Realtor site data unused.** Only their AVM point values are read off the
   sheet. Deliberate — §3 ranks AVM point values low — but their price histories and DOM
   would rank high, and are reachable through the same actors already in
   `PropertyValueScraper.js`. Paul raised this 2026-08-31; the reasoning for deferring is
   in §3 and §9.
4. **No absorption modelling.** Time-to-sell drives the carry. Shumard's subdivision ran a
   230-day median to contract against a 6-month carry assumption.
5. **No checkpointing.** Unlike `title-cli`, a failed run restarts from the top.

## Cost

Ellis CAD is free. Cotality reports are already paid for and sit in Drive. The only spend is
Apify — roughly a dozen actor runs for nine properties on the September run. Not free, not
expensive. Do not fan out sweeps casually.

## Ground rules

- The ARV calls live in `src/verdict.py`, with written rationale per property. **That file
  is judgment, not computation.** A human decides there; the rest of the pipeline is
  plumbing. Do not replace it with a scoring formula — the two architecture panels that
  reviewed `Auction Sheets/` killed computed confidence scores for good reasons, and the
  same reasoning applies here.
- **Run the validation gate (`src/model.py`) before revising any ARV.** If the sheet's own
  printed bids do not reproduce within ~$600, the sheet was misread and everything
  downstream is noise.
- Texas is a non-disclosure state. No closed sale price is public. Every report must say so
  on its face and must never present a derived clearing price as an observed transaction.
