import json,re,html,statistics as st,os
from mktsec import section as market_section
CSS=open('shared_css.html').read(); HEAD=open('shared_head.html').read()
sheets={r['address']:r for r in json.load(open('sheets.json'))}
cot=json.load(open('cotality.json')); subj=json.load(open('subjects.json'))
act=json.load(open('actives.json')); V={r['addr']:r for r in json.load(open('verdicts.json'))}
zd={}
for it in json.load(open('zdetail_all.json')):
    zd[(it.get('address') or {}).get('streetAddress','').upper()]=it
def e(x): return html.escape(str(x))
def m(x): return f"{x:,.0f}" if x else "&mdash;"
def slug(a): return re.sub(r'[^a-z0-9]+','-',a.lower()).strip('-')

DIRLABEL={'up':('Sheet ARV is low','lo'),'down':('Sheet ARV is high','lo'),'hold':('Sheet ARV holds','hi')}

def report(a):
    sh=sheets[a]; c=cot[a]; s=subj[a]; v=V[a]; z=zd.get(a,{})
    sf=v['sf']; A=act.get(a,{})
    cen,lo,hi=v['central'],v['lo'],v['hi']
    delta=cen-sh['arv']
    avms=[('Ellis CAD 2026',sh['ecad']),('Zillow',sh['zillow']),('Realtor.com',sh['realtor']),
          ('Redfin',sh['redfin']),('Cotality THVX',c['estimate'])]
    avms=[(n,x) for n,x in avms if x]
    sold=[x for x in c['comps'] if x['price'] and x['sqft'] and x['sqft']>500 and x['price']/x['sqft']>60]
    near=[x for x in c['nearby'] if x['est'] and x['sqft'] and x['sqft']>500]
    npsf=[x['est']/x['sqft'] for x in near]
    ph=sorted((z.get('priceHistory') or []),key=lambda h:h.get('date') or '')
    dl,dcls=DIRLABEL[v['dir']]

    P=[]
    P.append(f"<title>{e(a.title())}</title>{HEAD}{CSS}\n<div class=\"wrap\">")
    P.append(f'''<header class="mast">
  <p class="eyebrow">Recast Properties &middot; September auction &middot; sheet #{e(sh['id'])} &middot; 31 Aug 2026</p>
  <h1>{e(a.title())}<span class="sub">{e(sh['cityline'])} &middot; {e(sh['legal'])}</span></h1>
  <div class="mast-meta">
    <span><b>{e(sh['bbgp'])}</b> bd/ba/gar</span>
    <span><b>{sf:,.0f}</b> sf</span>
    <span>Built <b>{e(s['yearBuilt'] or sh['year_built'])}</b></span>
    <span><b>{e(s['acres'])}</b> ac</span>
    <span>Taxes <b>${m(sh['tax_yr'])}</b>/yr</span>
    <span>{e(sh['auction_house'] or 'auction house TBD')}</span>
  </div>
</header>''')

    cbfig=(f'<div class="fig hi"><p class="lab">Credit bid</p><div class="val">${m(sh["credit_bid"])}</div>'
           f'<p class="psf">${sh["credit_bid"]/sf:.0f} / sf{" &middot; cleared" if sh["cleared"] else ""}</p></div>') if sh['credit_bid'] else ''
    P.append(f'''<div class="verdict">
  <h2>{e(dl)} by ${abs(delta):,.0f}</h2>
  <p>{v['why']}</p>
  <div class="figs">
    <div class="fig"><p class="lab">Sheet ARV</p><div class="val">${m(sh['arv'])}</div><p class="psf">${sh['arv']/sf:.0f} / sf</p></div>
    <div class="fig {dcls}"><p class="lab">Comps-derived ARV</p><div class="val">${m(cen)}</div><p class="psf">${cen/sf:.0f} / sf &middot; ${m(lo)}&ndash;${m(hi)}</p></div>
    <div class="fig"><p class="lab">Revised low bid</p><div class="val">${m(v['new_low'])}</div><p class="psf">was ${m(v['old_low'])}</p></div>
    <div class="fig"><p class="lab">Revised high bid</p><div class="val">${m(v['new_high'])}</div><p class="psf">was ${m(v['old_high'])}</p></div>
    {cbfig}
  </div>
</div>''')

    if sh['credit_bid']:
        p0=v['profit_at_credit']
        room=v['new_high']-sh['credit_bid']
        P.append(f'''<div class="callout"><p><strong>At the ${m(sh['credit_bid'])} credit bid, the revised ARV moves profit to ${m(p0)}.</strong>
        The sheet's high bid was ${m(v['old_high'])}; on the comps-derived ARV it becomes ${m(v['new_high'])},
        which leaves {'about $'+m(room)+' of headroom above the credit bid' if room>0 else 'no headroom above the credit bid'}.</p></div>''')

    # ---- AVM stack
    vals=[x for _,x in avms]
    P.append(f'''<section><div class="shead"><h2>What every source says</h2><span class="weight w-primary">Primary evidence</span></div>
<div class="tw"><table><caption><b>Valuation stack</b>Five independent estimates, spread ${m(min(vals))}&ndash;${m(max(vals))}, median ${m(st.median(vals))}.</caption>
<thead><tr><th>Source</th><th>Value</th><th>$/sf</th><th>vs sheet ARV</th></tr></thead><tbody>''')
    for n,x in sorted(avms,key=lambda t:-t[1]):
        d=x-sh['arv']
        P.append(f'<tr><td class="name">{e(n)}</td><td>{m(x)}</td><td>{x/sf:.0f}</td>'
                 f'<td class="{"neg" if d<0 else ""}">{"+" if d>=0 else "&minus;"}{abs(d):,.0f}</td></tr>')
    P.append(f'''</tbody><tfoot><tr><td>Cotality confidence {c['confidence']:.0f} &middot; FSD {c['fsd']:.0f} &middot; range ${m(c['low'])}&ndash;${m(c['high'])}</td>
<td>{m(cen)}</td><td>{cen/sf:.0f}</td><td>comps-derived</td></tr></tfoot></table></div></section>''')

    # ---- Cotality sold comps
    if sold:
        ps=[x['price']/x['sqft'] for x in sold]
        P.append(f'''<section><div class="shead"><h2>Cotality sold comparables</h2><span class="weight w-support">Supporting</span></div>
<div class="col"><p>Cotality is the only source here carrying sale prices at all &mdash; Texas is a non-disclosure state and
every public record returns blank. Read these as <em>imputed</em>, not recorded: several amounts across the set repeat
exactly between different houses and many resolve to a round loan figure divided by 0.8, which is the signature of a
price modelled from the recorded mortgage at 80&#8202;% LTV. Directionally useful, individually unreliable.</p></div>
<div class="tw"><table><caption><b>{len(sold)} sold comps used in the AVM</b>Median ${st.median(ps):.0f}/sf, implying ${st.median(ps)*sf:,.0f} at {sf:,.0f} sf.</caption>
<thead><tr><th>Address</th><th>Date</th><th>Dist</th><th>Sf</th><th>Bd/Ba</th><th>Price</th><th>$/sf</th></tr></thead><tbody>''')
        for x in sorted(sold,key=lambda r:r['date'],reverse=True):
            P.append(f'<tr><td class="name">{e(x["addr"])}</td><td>{e(x["date"])}</td><td>{e(x["dist"])}</td>'
                     f'<td>{x["sqft"]:,.0f}</td><td>{x["beds"]:.0f}/{x["baths"]:.0f}</td><td>{m(x["price"])}</td><td>{x["price"]/x["sqft"]:.0f}</td></tr>')
        P.append('</tbody></table></div></section>')

    # ---- active supply
    if A.get('actives'):
        P.append(f'''<section><div class="shead"><h2>What is actually on the market</h2><span class="weight w-primary">Primary evidence</span></div>
<div class="col"><p>Active asks inside {e(A['sub'].title())} ({A['parcels']} residential parcels on the 2026 roll), matched
address-by-address from the county roll to live listings. $/sf falls as size rises, so compare against the rows nearest
{sf:,.0f}&#8202;sf rather than the column median.</p></div>
<div class="tw"><table><caption><b>Active listings in {e(A['sub'].title())}</b>Asking prices, not sales.</caption>
<thead><tr><th>Address</th><th>Sf</th><th>Ask</th><th>$/sf</th><th>Zestimate</th><th>Status</th></tr></thead><tbody>''')
        for r in A['actives']:
            cls=" class='best'" if abs(r['sqft']-sf)/sf<0.25 else ""
            stt=e(str(r.get("status") or ""))[:18]
            P.append(f'<tr{cls}><td class="name">{e(r["addr"].title())}</td><td>{r["sqft"]:,.0f}</td>'
                     f'<td>{m(r["ask"])}</td><td>{r["psf"]:.0f}</td><td>{m(r.get("zest"))}</td><td class="name">{stt}</td></tr>')
        P.append('</tbody></table></div><div class="col"><p>Rows shaded are within 25&#8202;% of the subject&rsquo;s size &mdash; those are the ones that bear on the ARV.</p></div></section>')

    # ---- own listing history
    if ph:
        P.append(f'''<section><div class="shead"><h2>This house's own market history</h2><span class="weight w-primary">Primary evidence</span></div>
<div class="ladders"><div class="ladder"><h4>{e(a.title())}</h4><p class="lsub">{sf:,.0f} sf &middot; every listing event on record</p>''')
        base=max([h.get('price') or 0 for h in ph]+[1])
        for h in ph:
            p=h.get('price'); ev=str(h.get('event') or '')
            term=ev in ('Listing removed','Sold')
            w=(p/base*100) if p else 100
            P.append(f'<div class="step{" term" if term else ""}"><span class="d">{e(h.get("date"))}</span>'
                     f'<span class="bar"><i style="width:{w:.1f}%"></i></span>'
                     f'<span class="p">{("$"+m(p)) if p else e(ev)}</span></div>')
        P.append(f'<p class="foot">{e(ph[-1].get("event") or "")} on {e(ph[-1].get("date"))}. Current Zillow status: <b>{e(z.get("homeStatus") or "unknown")}</b>, Zestimate <b>${m(z.get("zestimate"))}</b>, rent Zestimate <b>${m(z.get("rentZestimate"))}</b>/mo.</p></div></div></section>')

    # ---- market layer
    P.append(market_section(a, sf, cen, sh['carry_months'], sh['arv']))

    # ---- bid model
    fixed=v['fixed']; rate=v['rate']
    P.append(f'''<section><div class="shead"><h2>The bid model, re-run</h2><span class="weight w-primary">Conclusion</span></div>
<div class="col"><p>The sheet's own formula &mdash; Bid = ARV &minus; (Total Costs + Profit) &mdash; with the sheet's own
cost lines, its {sh['carry_months']:.0f}-month carry and its 9&#8202;% money. Reproduced against the sheet's ${m(sh['arv'])} ARV it
returns the printed bids to within a few hundred dollars, so ARV is the only input changed below.</p></div>
<div class="tw"><table><caption><b>Bid range at each ARV</b>Fixed costs ${m(fixed)} (rehab, tax, utilities, liens, contingency) plus 5&#8202;% of sale for commission and closing.</caption>
<thead><tr><th>ARV</th><th>Hard costs</th><th>Low bid @ {sh['low_profit_pct']:.0f}%</th><th>High bid @ {sh['high_profit_pct']:.0f}%</th>{'<th>Profit at credit bid</th>' if sh['credit_bid'] else ''}</tr></thead><tbody>''')
    def hard(arv): return fixed+0.05*arv
    def bid(arv,p): return (arv*(1-p)-hard(arv))/(1+rate)
    def prof(arv,b): return arv-hard(arv)-rate*b-b
    for arv,lab,cls in ((sh['arv'],"sheet",""),(lo,"low end",""),(cen,"comps central"," class='best'"),(hi,"high end","")):
        cbcell=f"<td>{m(prof(arv,sh['credit_bid']))}</td>" if sh['credit_bid'] else ""
        P.append(f"<tr{cls}><td>{m(arv)} <span class='tag t-res'>{lab}</span></td><td>{m(hard(arv))}</td>"
                 f"<td>{m(bid(arv,(sh['low_profit_pct'] or 0)/100))}</td><td>{m(bid(arv,(sh['high_profit_pct'] or 0)/100))}</td>{cbcell}</tr>")
    P.append('</tbody></table></div></section>')

    # ---- loan + condition
    P.append(f'''<section><div class="shead"><h2>Loan, condition and costs</h2><span class="weight w-context">From the sheet</span></div>
<div class="tw"><table><caption><b>What the sheet carries</b>Reproduced as printed; not independently verified.</caption>
<thead><tr><th>Item</th><th>Value</th><th>Item</th><th>Value</th></tr></thead><tbody>
<tr><td class="name">Loan type</td><td class="name">{e(sh['loan_type'])}</td><td class="name">Rehab budget</td><td>{m(sh['rehab'])}</td></tr>
<tr><td class="name">Mortgagor</td><td class="name">{e(sh['mortgage_holder'])}</td><td class="name">Contingency</td><td>{m(sh['contingency'])}</td></tr>
<tr><td class="name">Loan year</td><td class="name">{e(sh['loan_year'])}</td><td class="name">Carry months</td><td>{sh['carry_months']:.0f}</td></tr>
<tr><td class="name">Original amount</td><td>{m(sh['orig_loan'])}</td><td class="name">Utilities</td><td>{m(sh['utilities'])}</td></tr>
<tr><td class="name">Unpaid balance</td><td>{m(sh['upb'])}</td><td class="name">Additional liens</td><td>{m(sh['addl_liens'])}</td></tr>
<tr><td class="name">Equity vs sheet ARV</td><td>{m(sh['equity'])}</td><td class="name">Taxes owed</td><td>{m(sh['taxes_owed'])}</td></tr>
<tr><td class="name">Equity vs comps ARV</td><td>{m(cen-(sh['upb'] or 0))}</td><td class="name">Trustee</td><td class="name">{e(sh['trustee'])}</td></tr>
</tbody></table></div>
<div class="col"><p><strong>Your note on the sheet:</strong> &ldquo;{e(sh['notes'].replace(' | • Off Market','').replace('• Off Market',''))}&rdquo;</p></div></section>''')

    P.append(f'''<footer>
<p><strong>What this is.</strong> A comparables work-up testing one input to sheet #{e(sh['id'])} &mdash; the ARV &mdash; and a
re-run of the sheet's own bid model on the result. Not an appraisal. Condition is taken from your note on the sheet, not
from an inspection. Rehab, carry and cost lines are the sheet's, carried forward unexamined.</p>
<p><strong>Not covered.</strong> Title is not analysed here; the sheet's own screen and the independent title company's run
are the authority on liens, and neither is reproduced. Nothing here speaks to the quality of the foreclosing lien.</p>
<p><strong>On prices.</strong> Texas is a non-disclosure state. No closed sale price is public; Cotality's sale amounts are
modelled, and every other price on this page is an asking price or an AVM output. Comps-derived ARV figures are estimates,
not observed transactions.</p>
</footer></div>''')
    return "\n".join(P)

os.makedirs('out',exist_ok=True)
made=[]
for a in V:
    h=report(a); fn=f"out/{slug(a)}.html"
    open(fn,'w').write(h); made.append((a,fn,len(h)))
    print(f"{a:<24} -> {fn}  {len(h):,} bytes")
