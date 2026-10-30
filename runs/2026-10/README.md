# October 2026 - the Yes and maybe pile

Thirteen properties off the October sheet (4 Yes, 9 maybes), captured 2026-10-02 for the 6 October sale.
Data came off the sheet's tabs by gviz (no PDFs), so `sheets.json` was written by hand, not by `src/parse.py`.

| File | What it holds |
|---|---|
| `sheets.json` | Each tab's model inputs and printed bids |
| `subjects.json`, `subs_cad.json` | Ellis CAD identity (all 13 square footages match) and 11 subdivision rolls |
| `cotality.json` | 11 AVM reports (none for 248 Bakers Branch or 1618 FM 85) |
| `subject_history.json` | Zillow price history per subject |
| `sweep_sale.json`, `sweep_sold.json` | The raw Zillow sweeps (649 live, 1,083 sold in 12 months) |
| `actives.json` | Priced live listings around each subject, flagged in-subdivision / builder / cut |
| `sold_comps.json` | 74 recent sold comps: first ask, **last ask before contract**, days to contract |
| `rdc_*_hist.csv`, `market-brief.md` | Realtor.com inventory history (county + 7 zips, through Sep 2026) and the sourced market brief |
| `verdicts.py` -> `verdicts.json` | The ARV calls, rationale, and the sheet's model re-run on them |
| `gen_page.py` + `page_shell.html` -> `bid-sheet.html` | The published bid sheet (private Artifact, link in `urls.json`): bid/pass, max bid, comps per house |
| `cad.py`, `ap.py`, `comps.py`, `boxes.json` | The helpers used (CAD requests, Apify runner, comp matching, search boxes) |

## Result

Five ARVs conservative (Regent +40k, Royse Ridge +35k, Cimarron +25k, Saddlehorn +25k, Mobile +15k), four held
(Bakers Branch, Poinsetta, Myrtle, FM 85), four high (Slate -90k, Burdock -15k, Truman -10k, Kings -10k).
The validation gate reproduced all 13 printed bid pairs to the dollar using the exact form
`interest = c x (bid + fixed costs)`, `c = 0.045` for 6 months, `0.06` for 8.

## What was new this run

- **Last ask before contract** on recent in-subdivision solds (detail scrape of sold comps) is the strongest
  evidence short of a closed price. $0.21 for 74 pages.
- The sweep actor's items now carry `sourceSearchUrl`, `listingPrice.formatted`, `listingStatus`,
  `listingType.isNewHome`, `priceChange` - `src/join.py` still reads the old names.
- Apify spend: about $2.10 (two sweeps $1.88, comp details $0.21).

Not a title search. Nothing here is a closed sale price - Texas does not disclose them.
