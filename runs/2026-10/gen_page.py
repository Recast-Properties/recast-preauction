"""Build bid-sheet.html for the 6 October 2026 sale from this folder's data. The calls (CALL below) are judgment."""
import json, html, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from verdicts import V, sheets, bid, profit, c
from comps import rows, SALE, subj
sold = json.load(open('sold_comps.json'))

# address: (verdict, max bid, one-line call, watch-outs)
CALL = {
 '248 BAKERS BRANCH RD': ('bid', 402000, "Bid. Stop at $402,000.",
    "The posted credit bid is $386,768, so you have about $15,000 of room and other bidders will likely use it. This zip has the weakest demand in the county: 25 pendings against 95 listings. Town Square found only a water-system filing; our screen also saw a 2000-era lien whose release it could not match."),
 '3606 REGENT ST': ('bid', 180000, "Bid. Stop at $180,000.",
    "No opening bid is posted. There is a $16,257 IRS lien: the sale wipes it, but the IRS gets 120 days to take the house back at your bid price. There is a solar filing on the equipment; take any payoff off your max. The loan was modified in 2018, so the lender's bid may be above the sheet's $99,338."),
 '241 POINSETTA DR': ('bid', 199000, "Bid. Stop at $199,000.",
    "Cleared for auction at $192,150. Nothing found on title. Palmer has 21 listings and 1 pending right now, so do not chase this to your high bid."),
 '541 TRUMAN ST': ('open', 280600, "Opening bid only: $280,600.",
    "At my ARV your 20% line is $277,512, about $3,000 under the opening bid. Taking it at the opening is a 19% deal if it sells at $430,000. Nine listings in the subdivision and none pending. A Vincent Smith filed and lost two Chapter 13 cases in 2024 (name match only), so the sale may be stopped again."),
 '102 MYRTLE AVE': ('open', 115000, "Opening bid only: about $115,000.",
    "The opening bid is $114,624, which is your 20% line. Above it you are paying for the risk you already wrote down: old, and could be hiding something. One small 2025 judgment sits behind the mortgage."),
 '2010 MOBILE DR': ('bid', 76500, "Bid if you want this house. Stop at $76,500.",
    "Only about $19,000 is owed, so the opening bid will be low and other bidders will set the price. Your note says this kind of house makes you nervous; the number does not change that. The posted notice contradicts itself on who the lender is."),
 '1618 FM 85': ('cond', 280000, "Drive by first. If it passes, stop at $280,000.",
    "The value evidence is thin: nothing this old and this large has sold nearby. A 2022 lien from the prior owner has a release that does not say what it releases. The loan was modified in 2024, so the lender's bid may be above the sheet's $270,991."),
 '3509 BURDOCK LN': ('pass', None, "Pass.",
    "The opening bid is $339,500. At my ARV your high bid is $328,542. It only works at $293,000 or less."),
 '2329 SLATE DR': ('pass', None, "Pass.",
    "About $475,000 is owed and no opening bid is posted. At my ARV it only works at $382,000 or less. The tax line on your tab is last year's bill on the bare lot."),
 '905 ROYSE RIDGE RD': ('pass', None, "Pass.",
    "A 2023 modification put the debt near $244,000. Even at my higher ARV it only works at $194,000 or less. A 2005 developer lien also shows no release."),
 '1610 CIMARRON TRL': ('pass', None, "Pass.",
    "About $638,000 is owed. It only works at $425,000 or less."),
 '4602 SADDLEHORN DR': ('pass', None, "Pass.",
    "About $554,000 is owed. It only works at $439,000 or less. The owner had a contract in August and the listing came down 9/25, so it may not reach the steps."),
 '3808 KINGS': ('pass', None, "Pass.",
    "About $265,000 is owed. It only works at $139,000 or less."),
}
ORDER = {'bid': 0, 'open': 1, 'cond': 2, 'pass': 3}
LABEL = {'bid': 'Bid', 'open': 'Opening bid only', 'cond': 'Drive by first', 'pass': 'Pass'}
e = html.escape
def m(x): return '&ndash;' if x is None else f"${x:,.0f}"

def nm(a): return a.title().replace(' Fm ', ' FM ')

def near(x, key): return '' if x['insub'] else f' <i>({x[key]:.1f} mi)</i>'

def stress(r):
    six = abs(c(r) - 0.045) < 1e-3
    k = c(r) * (1.5 if six else 11 / 8); fx = dict(r); fx['utilities'] = r['utilities'] * (1.5 if six else 11 / 8)
    return fx, k

def live(a):
    s = subj[a]; sf = s['living']
    A = [r for r in rows(a, SALE.get(a, [])) if r['price'] and r['sf'] and not r['auc'] and r['d'] > 0.01]
    if a == '248 BAKERS BRANCH RD': M = [r for r in A if r['ac'] and 5 <= r['ac'] <= 40 and 0.6 * sf <= r['sf'] <= 1.5 * sf]
    elif a == '1618 FM 85': M = [r for r in A if r['ac'] and 1 <= r['ac'] <= 6 and 0.6 * sf <= r['sf'] <= 1.5 * sf]
    else: M = [r for r in A if 0.75 * sf <= r['sf'] <= 1.25 * sf]
    return sorted(M, key=lambda r: (not r['insub'], r['d']))[:6]

def block(a):
    cen, lo, hi, d, debt, why = V[a]; r = sheets[a]; verdict, mx, call, watch = CALL[a]
    pl, ph = r['low_profit_pct'] / 100, r['high_profit_pct'] / 100
    nl, nh = (r['low_bid'], r['high_bid']) if cen == r['arv'] else (bid(r, cen, pl), bid(r, cen, ph))
    beat = r['credit_bid'] or debt or r['upb']; posted = bool(r['credit_bid'])
    fx, k = stress(r)
    figs = [('Your ARV', m(r['arv'])), ('My ARV', m(cen)), ('Likely range', f"{m(lo)} to {m(hi)}"),
            ('Your bid range', f"{m(r['low_bid'])} to {m(r['high_bid'])}"), ('Range at my ARV', f"{m(round(nl))} to {m(round(nh))}"),
            ('Posted credit bid' if posted else 'Owed (estimate)', m(beat))]
    if mx:
        p0, p1 = profit(r, cen, mx), profit(fx, cen * 0.95, mx, k)
        figs.append(('Profit at the max', f"{m(round(p0, -2))} ({p0 / cen:.0%})"))
        figs.append(('If it sells 5% lower and takes 3 more months', f"{m(round(p1, -2))} ({p1 / (cen * 0.95):.0%})"))
    out = [f'<section class="prop v-{verdict}" id="p{r["id"]}">',
           f'<header><div><h3>{e(nm(a))}</h3><p class="where">{e(r["city"].title())} {r["zip"]} &middot; {subj[a]["living"]:,.0f} sf &middot; built {r["year_built"]}'
           + (f' &middot; {r["acres"]} ac' if r['acres'] and r['acres'] >= 0.5 else '') + f' &middot; status on your sheet: {e(r["status"])}</p></div>',
           f'<div class="call"><span class="pill">{LABEL[verdict]}</span><span class="max">{m(mx) if mx else "No bid"}</span></div></header>',
           f'<p class="verdict">{e(call)} {e(watch)}</p>',
           '<dl class="figs">' + ''.join(f'<div><dt>{e(k_)}</dt><dd>{v}</dd></div>' for k_, v in figs) + '</dl>',
           f'<p class="why"><strong>Why {m(cen)}.</strong> {e(why)}</p>']
    if r['notes']: out.append(f'<p class="note">Your note: &ldquo;{e(r["notes"])}&rdquo;</p>')
    S = sold.get(a, []); L = live(a)
    out.append('<div class="tables">')
    if S:
        out.append('<div class="tw"><table><caption>Sold nearby: last asking price before the contract</caption><thead><tr><th>Address</th><th class="n">Sq ft</th><th class="n">Built</th><th class="n">Last ask</th><th class="n">$/sf</th><th>Sold</th></tr></thead><tbody>'
                   + ''.join(f'<tr><td>{e(x["addr"])}{near(x,"dist")}</td><td class="n">{x["sf"]:,}</td><td class="n">{x["yb"] or ""}</td><td class="n">{m(x["last"])}</td><td class="n">${x["last"] / x["sf"]:.0f}</td><td>{x["sold"][5:7]}/{x["sold"][2:4]}</td></tr>' for x in S)
                   + '</tbody></table></div>')
    if L:
        def tag(x):
            t = []
            if x['status'] != 'forSale': t.append('pending')
            if x['new']: t.append('builder')
            if x['cut'] and x['cut'] < 0: t.append(f"cut {m(-x['cut'])}")
            return ', '.join(t)
        out.append('<div class="tw"><table><caption>For sale now: what a buyer can pick instead</caption><thead><tr><th>Address</th><th class="n">Sq ft</th><th class="n">Asking</th><th class="n">$/sf</th><th>Note</th></tr></thead><tbody>'
                   + ''.join(f'<tr><td>{e(x["addr"])}{near(x,"d")}</td><td class="n">{x["sf"]:,}</td><td class="n">{m(x["price"])}</td><td class="n">${x["price"] / x["sf"]:.0f}</td><td>{e(tag(x))}</td></tr>' for x in L)
                   + '</tbody></table></div>')
    out.append('</div></section>')
    return '\n'.join(out)

addrs = sorted(V, key=lambda a: (ORDER[CALL[a][0]], -(CALL[a][1] or 0)))
summary = ''.join(
    f'<tr class="v-{CALL[a][0]}"><td><a href="#p{sheets[a]["id"]}">{e(nm(a))}</a></td><td><span class="pill">{LABEL[CALL[a][0]]}</span></td>'
    f'<td class="n strong">{m(CALL[a][1]) if CALL[a][1] else "&ndash;"}</td><td class="n">{m(V[a][0])}</td><td class="n">{m(sheets[a]["arv"])}</td>'
    f'<td class="n">{m(sheets[a]["credit_bid"] or V[a][4] or sheets[a]["upb"])}{"" if sheets[a]["credit_bid"] else "*"}</td></tr>' for a in addrs)

page = open('page_shell.html').read().replace('{{SUMMARY}}', summary).replace('{{BLOCKS}}', '\n'.join(block(a) for a in addrs))
open('bid-sheet.html', 'w').write(page)
print('wrote bid-sheet.html', len(page))
