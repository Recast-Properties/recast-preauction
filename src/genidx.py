import json,html,statistics as st
CSS=open('shared_css.html').read(); HEAD=open('shared_head.html').read()
U=json.load(open('urls.json')); V={r['addr']:r for r in json.load(open('verdicts.json'))}
sheets={r['address']:r for r in json.load(open('sheets.json'))}
cot=json.load(open('cotality.json')); subj=json.load(open('subjects.json'))
def e(x): return html.escape(str(x))
def m(x): return f"{x:,.0f}" if x else "&mdash;"

SYN={
 "2052 WILLOW BEND DR":"Still the largest gap in the batch, but trimmed by the market layer. Every source lands between $725,436 and $776,931 against a $650,000 ARV. Revised to $735,000 rather than $760,000: 75154 has the weakest absorption of the three zips (37% pending), its per-foot pricing has gone nowhere in 25 months, and a 12-month carry spans two slow seasons with no appreciation to offset it. The $150,000 rehab is still the real variable.",
 "10407 WALNUT RIDGE DR":"The sheet says 1,702 sf. Ellis CAD says 3,184 and Zillow says 3,529. Everything downstream of that number is built on the wrong house &mdash; most importantly the $25,530 rehab budget. Cotality reads $548,762 at 98 confidence against a $500,000 ARV, so value points up while cost risk points the other way. Verify the footprint before bidding.",
 "501 WHITE PLAINS CT":"CAD, Redfin and Cotality all sit $30,000&ndash;$55,000 above the $500,000 ARV, and Hawkins Meadows actives at 4,000&#8202;sf+ ask $139&ndash;158/sf, which puts a 3,250&#8202;sf house comfortably higher. Your own note already says max bid $350k &mdash; above the sheet's own high bid of $341,736. The comps back your instinct, not the sheet.",
 "5614 LOG CABIN CT":"The ARV is Cotality's low bound used verbatim as the number. Five independent sources cluster tightly at $432,700&ndash;$439,593. Credit bid is cleared at $261,020 against a revised high bid of $292,255 &mdash; roughly $31,000 of headroom the sheet does not show, and profit at the credit bid moves from $75,413 to $97,798.",
 "408 ABBOTT LN":"All five sources exceed the $400,000 ARV, and Haven actives imply $405,000&ndash;$429,000 at this size. The brake is its own history: it asked $535,000 in March 2024, ground down to $485,000, and came off unsold. Occupied and well kept per your note, so no rehab surprise expected.",
 "323 TUMBLEWEED TRL":"The one where the sheet and the comps agree. Garden Valley Ranch actives are all smaller houses, so their $172/sf median flatters a 2,460&#8202;sf subject; size-matched it implies $357,000&ndash;$381,000 against a $375,000 ARV. Cotality's $398,084 looks high against what is actually listed. Roof and upkeep already checked.",
 "469 BRUSHWOOD LN":"Estates of North Grove asks imply $355,000&ndash;$375,000 at 2,029&#8202;sf, so the $360,000 ARV holds. Cotality's $398,914 runs above the live asks, which is the same pattern that broke the Shumard number. Credit bid cleared at $228,160 against a revised high bid of $242,977.",
 "495 WASHINGTON AVE":"The only ARV to revise downward, and the thinnest equity in the batch at $15,876. It sold on 19 May 2025 at $389,900 after cutting 8.3% from $425,000 &mdash; an actual arm's-length trade 15 months ago. 499 Washington next door asks $410,000 at 2,411&#8202;sf, implying about $385,000 here. PRISTINE, so the $2,000 rehab holds.",
 "1751 SHUMARD ST":"The outlier, and the only one where the ARV is too high. No Cotality report exists for it, so the sheet leaned on CAD and Realtor.com, both anchored to builder sales. Resale evidence says otherwise: the house itself failed at $529,900 and the nearest comparable resale has cut six times to $495,000 and still has not sold. Credit bid $362,100 is already past the sheet's own 10% floor on a $470,000 ARV.",
}
ORDER=["2052 WILLOW BEND DR","10407 WALNUT RIDGE DR","501 WHITE PLAINS CT","5614 LOG CABIN CT",
       "408 ABBOTT LN","323 TUMBLEWEED TRL","469 BRUSHWOOD LN","495 WASHINGTON AVE","1751 SHUMARD ST"]
SHU={'sheet_arv':500000,'central':470000,'dir':'down','new_low':339998,'new_high':360185,
     'old_low':363033,'old_high':384564,'credit':362100,'sf':3534}

P=[f"<title>September Auction Comps</title>{HEAD}{CSS}",'<div class="wrap">']
P.append('''<header class="mast">
  <p class="eyebrow">Recast Properties &middot; September 2026 auction &middot; compiled 31 Aug 2026</p>
  <h1>Nine comps work-ups<span class="sub">Each sheet's ARV tested against county roll, Cotality AVM, live asks and the property's own listing history &mdash; then the sheet's own bid model re-run on the result.</span></h1>
  <div class="mast-meta">
    <span><b>9</b> properties</span><span><b>1,919</b> CAD parcels pulled</span>
    <span><b>8</b> Cotality AVMs</span><span><b>2,118</b> area listings</span>
    <span>Sale <b>Tue 1 Sept</b></span>
  </div>
</header>''')

ups=[a for a in ORDER if a!="1751 SHUMARD ST" and V[a]['dir']=='up']
tot=sum(V[a]['central']-V[a]['sheet_arv'] for a in ups)
P.append(f'''<div class="verdict">
  <h2>Seven ARVs are conservative. Two are not.</h2>
  <p>The Shumard work-up found an ARV set too high. Across the other eight the bias runs the other way &mdash;
  five sit meaningfully below what the evidence supports, adding roughly ${tot:,.0f} of unclaimed value in aggregate.
  The reason is visible in the data: Shumard is the only property with no Cotality report, so its number leaned on
  appraisal-roll and portal AVMs that are anchored to builder sales. Where Cotality exists, the sheet tracks it closely
  &mdash; and on Log Cabin it uses Cotality's floor as the number outright.</p>
  <div class="figs">
    <div class="fig lo"><p class="lab">ARVs set low</p><div class="val">5</div><p class="psf">of 9</p></div>
    <div class="fig"><p class="lab">ARVs holding</p><div class="val">2</div><p class="psf">Tumbleweed, Brushwood</p></div>
    <div class="fig hi"><p class="lab">ARVs set high</p><div class="val">2</div><p class="psf">Washington, Shumard</p></div>
    <div class="fig lo"><p class="lab">Aggregate ARV gap</p><div class="val">+${tot/1000:,.0f}k</div><p class="psf">across the five</p></div>
    <div class="fig"><p class="lab">Data error found</p><div class="val">1</div><p class="psf">Walnut Ridge sqft</p></div>
  </div>
</div>''')

P.append('''<div class="callout"><p><strong>Two properties have live cleared credit bids, and both now show headroom the sheet does not.</strong>
5614 Log Cabin at $261,020 against a revised high bid of $292,255, and 469 Brushwood at $228,160 against $242,977.
1751 Shumard is the reverse: its $362,100 credit bid already sits past the sheet's own 10&#8202;% profit floor.</p></div>''')


M=json.load(open('market.json')); HH=json.load(open('market_hist.json'))
c=M['county']; cs=HH['county']
P.append(f'''<section><div class="shead"><h2>The market these nine exit into</h2><span class="weight w-primary">Market layer</span></div>
<div class="col"><p>Two findings from the county's own inventory record shape every deal below, and neither is
visible in any AVM.</p></div>
<div class="figs" style="margin-bottom:24px">
  <div class="fig"><p class="lab">Ellis $/sf, 25 months</p><div class="val">+1.0%</div><p class="psf">${cs[0]['psf']:.0f} &rarr; ${cs[-1]['psf']:.0f}</p></div>
  <div class="fig"><p class="lab">Median DOM, Jul</p><div class="val">{c['dom']:.0f} days</div><p class="psf">{c['dom_yy']:+.1%} YoY</p></div>
  <div class="fig lo"><p class="lab">Median DOM, Dec</p><div class="val">77 days</div><p class="psf">the season this sale feeds</p></div>
  <div class="fig lo"><p class="lab">Actives carrying a cut</p><div class="val">{c['reduced_ct']/c['active']:.0%}</div><p class="psf">{c['reduced_ct']:,.0f} of {c['active']:,.0f}</p></div>
  <div class="fig"><p class="lab">Pending ratio</p><div class="val">{c['pending_ratio']:.0%}</div><p class="psf">county, July 2026</p></div>
</div>
<div class="col">
<p><strong>Per-foot pricing has not moved in two years.</strong> Ellis County went ${cs[0]['psf']:.0f}/sf to
${cs[-1]['psf']:.0f}/sf across 25 months. Waxahachie is flat to the dollar, Oak Leaf is &minus;0.6%, Midlothian
+3.0%. Median <em>list</em> prices rose faster, but that is mix &mdash; bigger, newer houses coming to market, not
the same house being worth more. <strong>There is no appreciation to underwrite on any of these exits.</strong></p>
<p><strong>A 1 September purchase lists into the worst window of the year.</strong> Pooled across the series,
county days-on-market runs 52 in spring and 77 in December. A house taken at this sale and listed in October meets
the rising half of that curve and does not see spring conditions until March. The sheets' 6-month carries run
September to March &mdash; exactly the minimum to reach the spring window, with no slack. The offsetting cushion is
real: every sheet charges a <em>full year</em> of property tax against that 6-month carry, which absorbs much of the
risk. Carry slipping from six months to nine costs $7,000&ndash;$12,700 of bid capacity depending on the property.</p>
</div>
<div class="tw"><table><caption><b>The three zips these nine sit in</b>Realtor.com Research inventory file, July 2026. Per-foot drift is measured across the full 25-month series.</caption>
<thead><tr><th>Zip</th><th>Properties</th><th>Median list</th><th>$/sf</th><th>25-mo drift</th><th>Actives</th><th>YoY</th><th>DOM</th><th>Pending</th></tr></thead><tbody>''')
CNT={'75165':5,'76065':3,'75154':1}
for z,nm in M['zip_names'].items():
    zm=M['zips'][z]; zs=HH['zips'][z]
    dr=(zs[-1]['psf']/zs[0]['psf']-1)
    P.append(f"<tr><td class='name'>{z} {nm}</td><td>{CNT[z]}</td><td>{zm['median_list']:,.0f}</td>"
             f"<td>{zm['psf']:.0f}</td><td class=\"{'neg' if dr<0 else ''}\">{dr:+.1%}</td>"
             f"<td>{zm['active']:,.0f}</td><td class=\"{'neg' if (zm['active_yy'] or 0)>0.08 else ''}\">{zm['active_yy']:+.1%}</td>"
             f"<td>{zm['dom']:.0f}</td><td>{zm['pending_ratio']:.0%}</td></tr>")
P.append('''</tbody></table></div>
<div class="col"><p>Midlothian is the one to watch: inventory is up 14.5% year on year and 15.3% in the last month
alone, and three of these nine sit there. Waxahachie is the opposite &mdash; actives down 12.7% YoY &mdash; which
supports the five properties in that zip. Oak Leaf carries the weakest pending ratio at 37%, which is what pulled
Willow Bend's ARV back from $760,000 to $735,000.</p></div>
</section>''')

# ---- summary table
P.append('''<section><div class="shead"><h2>All nine at a glance</h2><span class="weight w-primary">Summary</span></div>
<div class="tw"><table><caption><b>Sheet ARV against comps-derived ARV</b>Revised bids use each sheet's own formula, cost lines and profit thresholds &mdash; only the ARV changes.</caption>
<thead><tr><th>Property</th><th>Sf</th><th>Sheet ARV</th><th>Comps ARV</th><th>Delta</th><th>Low bid</th><th>High bid</th><th>Credit bid</th></tr></thead><tbody>''')
for a in ORDER:
    v=SHU if a=="1751 SHUMARD ST" else V[a]
    sh=sheets[a]; d=v['central']-v['sheet_arv']
    cls=" class='best'" if v.get('credit') else ""
    P.append(f'''<tr{cls}><td class="name"><a href="{U[a]}">{e(a.title())}</a><br><span style="color:var(--faint);font-size:12px">{e(sh['cityline'].rsplit(' TX',1)[0].title())} &middot; #{e(sh['id'])}</span></td>
<td>{v['sf']:,.0f}</td><td>{m(v['sheet_arv'])}</td><td>{m(v['central'])}</td>
<td class="{'neg' if d<0 else ''}">{'+' if d>=0 else '&minus;'}{abs(d):,.0f}</td>
<td>{m(v['new_low'])}</td><td>{m(v['new_high'])}</td><td>{m(v.get('credit'))}</td></tr>''')
P.append('</tbody></table></div><div class="col"><p>Shaded rows have a cleared credit bid. Low and high bids are the revised figures at the comps-derived ARV; each report shows them beside the sheet\'s originals.</p></div></section>')

# ---- per property cards
P.append('<section><div class="shead"><h2>Property by property</h2><span class="weight w-context">Reports</span></div><div class="ladders">')
for a in ORDER:
    v=SHU if a=="1751 SHUMARD ST" else V[a]
    sh=sheets[a]; d=v['central']-v['sheet_arv']
    c=cot.get(a)
    tag=('<span class="tag t-new">ARV low</span>' if v['dir']=='up' else
         '<span class="tag t-res">ARV high</span>' if v['dir']=='down' else
         '<span class="tag t-res">ARV holds</span>')
    cb=f" &middot; credit bid ${m(v.get('credit'))}" if v.get('credit') else ""
    cotline=(f"Cotality ${m(c['estimate'])} at {c['confidence']:.0f} confidence" if c else "No Cotality report exists for this property")
    P.append(f'''<div class="ladder">
  <h4><a href="{U[a]}">{e(a.title())}</a> {tag}</h4>
  <p class="lsub">#{e(sh['id'])} &middot; {v['sf']:,.0f} sf &middot; {e(sh['bbgp'])} &middot; built {e(subj[a]['yearBuilt'] if a in subj else sh['year_built'])}{cb}</p>
  <div class="step"><span class="d">Sheet ARV</span><span class="bar"><i style="width:{min(100,v['sheet_arv']/max(v['sheet_arv'],v['central'])*100):.0f}%"></i></span><span class="p">${m(v['sheet_arv'])}</span></div>
  <div class="step{' term' if d<0 else ''}"><span class="d">Comps ARV</span><span class="bar"><i style="width:{min(100,v['central']/max(v['sheet_arv'],v['central'])*100):.0f}%"></i></span><span class="p">${m(v['central'])}</span></div>
  <p class="foot">{SYN[a]}</p>
  <p class="foot" style="border:0;padding-top:6px"><b>{cotline}.</b> <a href="{U[a]}">Read the full work-up &rarr;</a></p>
</div>''')
P.append('</div></section>')

# ---- method
P.append('''<section><div class="shead"><h2>How these were built</h2><span class="weight w-context">Provenance</span></div>
<div class="srcgrid">
  <div class="src"><h5>September auction sheets</h5><p>Nine property tabs, exported 31 Aug. Source for ARV, cost lines, loan file, condition notes and the bid model. Each sheet's model was reproduced to within a few hundred dollars before any input was changed.</p></div>
  <div class="src"><h5>Ellis CAD 2026 roll</h5><p><b>1,919 parcels</b> across seven subdivisions, via the same TrueProdigy API the pipeline's ECAD scraper uses. Appraised value, legal, acreage, owner, deed date &mdash; and the living areas that caught the Walnut Ridge error.</p></div>
  <div class="src"><h5>Cotality AVM reports</h5><p><b>Eight reports</b> from the September Drive folder, 90&ndash;98 confidence. Estimate, range, FSD, plus the sold comps and ~20 nearby THVX estimates each. Shumard has no report, which is why its number drifted.</p></div>
  <div class="src"><h5>Zillow, via Apify</h5><p>Nine subject detail scrapes for price history, plus three area sweeps returning <b>2,118 listings</b>, matched address-by-address against the county roll to isolate genuine in-subdivision asks.</p></div>
</div>
<div class="col">
<p><strong>On sale prices.</strong> Texas is a non-disclosure state. Cotality is the only source here carrying sale amounts at all, and those are modelled rather than recorded &mdash; several repeat exactly between different houses and many resolve to a round loan figure divided by 0.8, the signature of a price imputed from the recorded mortgage at 80&#8202;% LTV. They are used directionally and never as the deciding evidence. Everything else on these pages is an asking price or an AVM output.</p>
<p><strong>What is not here.</strong> No title analysis &mdash; the sheets' own screen and the independent title company's run remain the authority on liens. No inspections; condition is taken from your notes. Rehab, carry and cost assumptions are the sheets', carried forward unexamined, which matters most on Willow Bend at $150,000 and Walnut Ridge where the budget was set against the wrong square footage.</p>
</div></section>''')

P.append('''<footer>
<p>Nine comparables work-ups supporting one input to each sheet &mdash; the ARV. Not appraisals. Comps-derived ARVs are
estimates, and in a non-disclosure state there is no observed transaction price to check them against.</p>
<p>Sale is Tuesday 1 September. Auction windows differ by property and are printed on each sheet, not repeated here.</p>
</footer></div>''')
open('out/index-september.html','w').write("\n".join(P))
print('wrote index-september.html', len("\n".join(P)), 'bytes')
