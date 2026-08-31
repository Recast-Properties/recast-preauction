"""Market layer -> per-property HTML section. Ellis County conditions applied to the deal."""
import json,statistics as st
H=json.load(open('market_hist.json')); M=json.load(open('market.json'))
PZ=M['prop_zip']; ZN=M['zip_names']
def m(x): return f"{x:,.0f}" if x else "&mdash;"
MONTH={'01':'Jan','02':'Feb','03':'Mar','04':'Apr','05':'May','06':'Jun',
       '07':'Jul','08':'Aug','09':'Sep','10':'Oct','11':'Nov','12':'Dec'}

def dom_by_month():
    bym={}
    for x in H['county']:
        if x['dom']: bym.setdefault(x['month'][4:],[]).append(x['dom'])
    return {k:st.median(v) for k,v in bym.items()}
DOM=dom_by_month()

def sparkline(series,key,w=560,h=54):
    """Inline SVG line, theme-aware via currentColor."""
    pts=[(i,x[key]) for i,x in enumerate(series) if x[key]]
    if len(pts)<2: return ''
    ys=[p[1] for p in pts]; lo,hi=min(ys),max(ys)
    rng=(hi-lo) or 1
    step=w/(len(series)-1)
    d=" ".join(f"{'M' if i==0 else 'L'}{p[0]*step:.1f},{h-4-((p[1]-lo)/rng)*(h-12):.1f}" for i,p in enumerate(pts))
    last=pts[-1]
    cx=last[0]*step; cy=h-4-((last[1]-lo)/rng)*(h-12)
    return (f'<svg viewBox="0 0 {w} {h}" width="100%" height="{h}" role="img" '
            f'aria-label="trend" style="overflow:visible"><path d="{d}" fill="none" '
            f'stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>'
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3.5" fill="currentColor"/></svg>')

def section(addr, sf, arv, carry_months, sheet_arv):
    z=PZ[addr]; zm=M['zips'][z]; c=M['county']; zs=H['zips'][z]; cs=H['county']
    psf=arv/sf
    z0,z1=zs[0],zs[-1]
    drift=(z1['psf']/z0['psf']-1) if z0['psf'] and z1['psf'] else 0
    cut_share=zm['reduced_ct']/zm['active'] if zm['active'] else 0
    # seasonal path from a 1 Sept purchase
    path=[('Sep',DOM.get('09')),('Oct',DOM.get('10')),('Nov',DOM.get('11')),
          ('Dec',DOM.get('12')),('Jan',DOM.get('01')),('Feb',DOM.get('02')),
          ('Mar',DOM.get('03')),('Apr',DOM.get('04'))]
    worst=max(v for _,v in path if v); best=min(v for _,v in path if v)
    P=[]
    P.append(f'''<section><div class="shead"><h2>The deal against the Ellis County market</h2><span class="weight w-primary">Market layer</span></div>
<div class="col"><p>Two facts from the county's own inventory record decide how much weight the exit deserves:
<strong>per-foot pricing has not moved in two years</strong>, and <strong>a September purchase lists into the
slowest months of the year</strong>. Neither is visible in any AVM.</p></div>

<div class="tw"><table><caption><b>{z} {ZN[z]} against Ellis County</b>Realtor.com Research inventory file, {zm['month'][:4]}-{zm['month'][4:]} &mdash; the same source the August listings review used.</caption>
<thead><tr><th>Metric</th><th>{z} {ZN[z]}</th><th>Ellis County</th><th>Reading</th></tr></thead><tbody>
<tr><td class="name">Median list price</td><td>${m(zm['median_list'])}</td><td>${m(c['median_list'])}</td><td class="name">{zm['median_list_yy']:+.1%} YoY</td></tr>
<tr class="best"><td class="name">Median $/sf</td><td>${zm['psf']:.0f}</td><td>${c['psf']:.0f}</td><td class="name">{zm['psf_yy']:+.1%} YoY &middot; <b>{drift:+.1%} over 25 months</b></td></tr>
<tr><td class="name">Active listings</td><td>{m(zm['active'])}</td><td>{m(c['active'])}</td><td class="name {'neg' if (zm['active_yy'] or 0)>0.08 else ''}">{zm['active_mm']:+.1%} MoM &middot; {zm['active_yy']:+.1%} YoY</td></tr>
<tr><td class="name">Median days on market</td><td>{zm['dom']:.0f}</td><td>{c['dom']:.0f}</td><td class="name">{zm['dom_yy']:+.1%} YoY</td></tr>
<tr><td class="name">Actives carrying a cut</td><td>{m(zm['reduced_ct'])} of {m(zm['active'])}</td><td>{m(c['reduced_ct'])} of {m(c['active'])}</td><td class="name">{cut_share:.0%} of this zip's inventory</td></tr>
<tr><td class="name">Pending ratio</td><td>{zm['pending_ratio']:.0%}</td><td>{c['pending_ratio']:.0%}</td><td class="name">{'below county &mdash; slower absorption' if zm['pending_ratio']<c['pending_ratio'] else 'at or above county'}</td></tr>
<tr><td class="name">This deal's exit</td><td>${m(arv)} &middot; ${psf:.0f}/sf</td><td>&mdash;</td><td class="name">{(psf/zm['psf']-1):+.0%} vs zip median $/sf</td></tr>
</tbody></table></div>

<div class="col">
<h3>Per-foot pricing is flat, so there is no appreciation to underwrite</h3>
<p>{z} {ZN[z]} went <strong>${z0['psf']:.0f}/sf to ${z1['psf']:.0f}/sf</strong> across the 25 months to
{z1['month'][:4]}-{z1['month'][4:]} &mdash; {drift:+.1%}. County-wide the move was +1.0%. Median <em>list</em> prices
rose faster than that, but that is mix: bigger and newer houses coming to market, not the same house being worth more.
Any exit here has to be earned on price today, not on the market lifting it.</p>
</div>
<div class="ladder" style="margin:24px 0"><h4>{ZN[z]} median $/sf &mdash; 25 months</h4>
<p class="lsub">${z0['psf']:.0f} &rarr; ${z1['psf']:.0f} &middot; {drift:+.1%}</p>
<div style="color:var(--accent)">{sparkline(zs,'psf')}</div>
<div class="step" style="grid-template-columns:1fr auto;margin-top:6px"><span class="d">{z0['month'][:4]}-{z0['month'][4:]}</span><span class="d">{z1['month'][:4]}-{z1['month'][4:]}</span></div>
</div>

<div class="col">
<h3>A 1 September purchase lists into the worst window of the year</h3>
<p>Pooled across the series, Ellis County days-on-market runs <strong>{best:.0f} days in spring and {worst:.0f} in
December</strong>. A house taken at this sale and listed in October meets the rising half of that curve and does not
see spring conditions until March &mdash; roughly five months later.</p>
</div>
<div class="tw"><table><caption><b>Where the months after this auction sit</b>Median days on market by calendar month, pooled across the 25-month county series.</caption>
<thead><tr><th>Month after the sale</th><th>Median DOM</th><th></th></tr></thead><tbody>''')
    for nm,v in path:
        if not v: continue
        bar='&#9608;'*int(v/6)
        hot=" class='best'" if v<=55 else ""
        P.append(f"<tr{hot}><td class=\"name\">{nm}</td><td>{v:.0f}</td><td class=\"name\" style=\"color:var(--accent)\">{bar}</td></tr>")
    P.append(f'''</tbody></table></div>
<div class="col"><p>Shaded rows are the spring window. The sheet assumes a <strong>{carry_months:.0f}-month carry</strong>;
from a 1 September purchase that runs to {'March' if carry_months==6 else 'next September'}, which is
{'exactly the minimum needed to reach spring pricing &mdash; there is no slack in it' if carry_months==6 else 'a full year spanning two slow seasons'}.</p>
<p><strong>The offsetting cushion:</strong> the sheet charges a <em>full year</em> of property tax against that
{carry_months:.0f}-month carry. That over-costing is real and it absorbs much of the slow-season risk &mdash; which is why
the carry finding tightens the bid rather than breaking it.</p></div>
</section>''')
    return "\n".join(P)
