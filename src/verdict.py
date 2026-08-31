import json,statistics as st
sheets={r['address']:r for r in json.load(open('sheets.json'))}
cot=json.load(open('cotality.json')); subj=json.load(open('subjects.json'))
def fixed(r): return sum(x or 0 for x in (r['rehab'],r['tax_yr'],r['taxes_owed'],r['utilities'],r['hoa_yr'],r['addl_liens'],r['contingency']))
def rate(r):
    rs=[i/b for b,i in ((r['low_bid'],r['low_interest']),(r['high_bid'],r['high_interest'])) if b and i]
    return st.mean(rs) if rs else .0477
def hard(r,arv): return fixed(r)+0.05*arv
def bid(r,arv,p): return (arv*(1-p)-hard(r,arv))/(1+rate(r))
def profit(r,arv,b): return arv-hard(r,arv)-rate(r)*b-b

# central ARV + rationale, from the size-matched resale asks cross-checked against Cotality
V={
 "2052 WILLOW BEND DR":  (760000,700000,820000,"up","Every AVM $725k-$777k and Cotality $758,465 sit far above the $650,000 ARV. 2056 Willow Bend next door asks $999,999 at 5,908 sf ($169/sf). The $150k rehab is the variable, not the value."),
 "10407 WALNUT RIDGE DR":(535000,505000,565000,"up","Sheet sqft is wrong (1,702 vs 3,184 CAD / 3,529 Zillow). Cotality $548,762 at 98 confidence and nearby THVX $172/sf both land near $549k. Rehab budgeted against the wrong house."),
 "501 WHITE PLAINS CT":  (530000,505000,555000,"up","CAD $530,869, Redfin $542,254, Cotality $555,231. Hawkins Meadows actives run $139-158/sf on larger homes; 3,250 sf sits above that band. Your own note says max bid $350k."),
 "5614 LOG CABIN CT":    (433000,415000,450000,"up","The ARV is Cotality's LOW bound ($409,436) used as the number. Five independent AVMs cluster tightly at $432,700-$439,593."),
 "408 ABBOTT LN":        (415000,398000,435000,"up","All five AVMs exceed $400,000. Haven actives at 2,630-2,641 sf ask $162-184/sf; 2,453 sf implies $405-429k. Tempered by its own failed 2024 resale at $485k."),
 "323 TUMBLEWEED TRL":   (378000,360000,398000,"hold","Garden Valley Ranch actives are all smaller homes, so their $172/sf median overstates for 2,460 sf. Size-matched implies $357-381k. Sheet ARV sits in range; Cotality $398,084 looks high."),
 "469 BRUSHWOOD LN":     (365000,345000,385000,"hold","Estates of North Grove size-matched actives imply $355-375k at 2,029 sf. Cotality $398,914 runs above the asks. Sheet ARV is defensible."),
 "495 WASHINGTON AVE":   (390000,378000,402000,"down","It sold 19 May 2025 at $389,900 after cutting 8.3% from $425,000. 499 Washington next door asks $410,000 at 2,411 sf ($170/sf), implying ~$385k here. PRISTINE, so no rehab drag."),
}
out=[]
print(f"{'PROPERTY':<24}{'SHEET ARV':>11}{'CENTRAL':>11}{'DELTA':>10}  {'NEW LOW':>10}{'NEW HIGH':>10}{'CREDIT':>10}  VERDICT")
for a,(cen,lo,hi,dirn,why) in V.items():
    r=sheets[a]
    nl=bid(r,cen,(r['low_profit_pct'] or 0)/100); nh=bid(r,cen,(r['high_profit_pct'] or 0)/100)
    cb=r['credit_bid']
    rec={'addr':a,'sheet_arv':r['arv'],'central':cen,'lo':lo,'hi':hi,'dir':dirn,'why':why,
         'new_low':nl,'new_high':nh,'old_low':r['low_bid'],'old_high':r['high_bid'],
         'credit':cb,'profit_at_credit':profit(r,cen,cb) if cb else None,
         'sf':subj[a]['living'],'cot':cot[a]['estimate'],'cot_conf':cot[a]['confidence'],
         'rate':rate(r),'fixed':fixed(r)}
    out.append(rec)
    d=cen-r['arv']
    print(f"{a:<24}{r['arv']:>11,.0f}{cen:>11,.0f}{d:>+10,.0f}  {nl:>10,.0f}{nh:>10,.0f}{(cb or 0):>10,.0f}  {dirn.upper()}")
json.dump(out,open('verdicts.json','w'),indent=1)
print()
for r in out:
    if r['credit']:
        p0=profit(sheets[r['addr']],r['sheet_arv'],r['credit'])
        print(f"  {r['addr']:<24} at credit ${r['credit']:,.0f}: profit ${p0:,.0f} (sheet ARV) -> ${r['profit_at_credit']:,.0f} (central ARV)")
