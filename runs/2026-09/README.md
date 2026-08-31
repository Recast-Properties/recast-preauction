# September 2026 — first run

Nine properties. Data as captured 2026-08-31, the day before the 1 September sale.

| File | What it holds |
|---|---|
| `sheets.json` | Every field parsed off the nine property-tab PDFs — ARV, cost lines, bid model, loan, condition notes |
| `subjects.json` | Ellis CAD identity per subject, incl. the verified living area that caught the Walnut Ridge error |
| `subs_cad.json` | Whole-subdivision 2026 rolls, seven subdivisions, 1,919 parcels |
| `cotality.json` | Eight AVM reports — estimate, range, confidence, FSD, sold comps, nearby THVX estimates |
| `actives.json` | County roll matched to live listings, per subdivision |
| `verdicts.json` | The ARV calls, their rationale, and the revised bids |
| `urls.json` | Published report URLs (private Artifacts) |

Not committed: the source sheet PDFs and the Cotality PDFs. Those live in Drive at
`1_Auctions/2026/09_September/`.

## Result

Seven ARVs conservative, two high. Aggregate ARV gap across the five that moved
meaningfully: about +$194,000.

Both cleared credit bids gained headroom at the revised ARV — Log Cabin ~$31,000,
Brushwood ~$4,000. Shumard went the other way: its $362,100 credit bid already sits past
the sheet's own 10% profit floor.

## Caveats carried into these numbers

- Three subdivisions (Dove Creek, Greenway Trails, Oak Leaf Farms) returned 0–1 live comps,
  so Log Cabin, Walnut Ridge and Willow Bend rest largely on AVMs.
- Cotality sale amounts are modelled, not recorded — used directionally only.
- Rehab, carry and cost lines are the sheets', carried forward unexamined.
