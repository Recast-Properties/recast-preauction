"""October 2026: central ARV calls for the 13 live candidates, and the sheet's own bid model re-run on them.
Judgment, not computation - same contract as src/verdict.py. Evidence: sold_comps.json (last ask before contract),
the live-listing sweep, each subject's own listing history, cotality.json. Texas is non-disclosure: no figure here is a closed price."""
import json
sheets={r['address']:r for r in json.load(open('sheets.json'))}
def fixed(r): return sum(r[k] or 0 for k in ('rehab','tax_yr','taxes_owed','utilities','hoa_yr','addl_liens','contingency'))
def c(r): return (r['low_interest']/(r['low_bid']+fixed(r))+r['high_interest']/(r['high_bid']+fixed(r)))/2   # sheet: interest = c*(bid+fixed)
def bid(r,arv,p,k=None): k=c(r) if k is None else k; return (arv*(0.95-p)-fixed(r)*(1+k))/(1+k)
def profit(r,arv,b,k=None): k=c(r) if k is None else k; return arv*0.95-fixed(r)-k*(b+fixed(r))-b
# address: (central, low, high, direction, debt the lender is likely to bid (None = sheet's), why)
V={
'248 BAKERS BRANCH RD':(800000,740000,840000,'hold',None,"Acreage homes this size nearby last asked $640k-$750k before contract (729 Bearden 2,916 sf/9.8 ac $720k Sep; 240 Grande Casa 3,397 sf/9.2 ac $750k Aug; 153 S Oak Branch 3,419 sf/5 ac $740k Jan). Subject adds 2-6 acres, a pool and a 2,500 sf barn. Live: 505 Boz 3,176 sf/6 ac $815k (cut 9/30); 521 Bakers Branch 3,550 sf/7 ac $765k, cut and unsold since before August. $800k needs the full renovation to show; no room above it."),
'3606 REGENT ST':(340000,325000,355000,'up',None,"Kensington Park, last ask before contract: 913 Abbey 1,846 sf $359,900 (2 days, Sep); 3433 Charing Cross 1,756 sf $340,000 (May); 910 Westminster 2,186 sf $379,000 (3 days, Sep). 3429 Newgate 1,818 sf pending at $320,000. $300k is 12% under the subdivision."),
'241 POINSETTA DR':(310000,295000,325000,'hold',None,"250 Poinsetta (1,710 sf, 2023) last asked $340,000 in May and 150 Palmer South $355,000 in April, but today 103 Palomino 1,519 sf sits at $330,000 and 107 Meadowlark 1,673 sf at $297,500, both cut, and the zip has 21 listings with 1 pending. $309k fits today's asks, not spring's."),
'541 TRUMAN ST':(430000,410000,445000,'down',None,"508 Bush Ave, same size (3,269 sf) and 4 years newer, started at $489,999 and went under contract at $445,000 (Aug). 1504 Reagan 2,785 sf $440,000; 1616 Granite 2,866 sf $430,000. Nine listings in the subdivision, none pending. $440k is the ceiling, not the middle."),
'905 ROYSE RIDGE RD':(410000,380000,440000,'up',243973,"Its own listing ran a year: $475,000 Sep 2025, cut to $459,878, removed unsold Sep 2026 - as-is, 'ugly'. 803 Williamsburg 2,776 sf (1992) $399,999 after 172 days; 1109 Oak Creek 2,946 sf $475,000. After $80k of work $410k is supportable; $375k is conservative."),
'102 MYRTLE AVE':(250000,235000,265000,'hold',None,"Gingerbread Village last asks: 210 Myrtle 1,568 sf $280,000 (Mar); 300 Morene 1,447 sf $269,500 (Apr); 210 Morene 1,148 sf $265,000 (Feb). Live: 107 Modene 1,498 sf $260,000 (cut 10/2); 202 Modene 1,441 sf $236,000 (cut)."),
'2329 SLATE DR':(560000,540000,590000,'down',None,"The builder's near-twins on the same street went under contract at $569,000 (2325 Slate, 2,795 sf, 162 days) and $554,000 (2245 Slate, 2,822 sf, 167 days) this summer. Highland still has 2,851-2,887 sf homes at $614k-$634k with cuts; DRB sells 3,000 sf for $488,990. It sold new for $551,250 a year ago. $650k leans on the $699,900 asking price and on AVMs that follow builder list prices."),
'3509 BURDOCK LN':(460000,440000,480000,'down',None,"It failed as a resale: $569,500 Apr 2025, five cuts to $529,000, removed Nov 2025. Brand-new 2,757 sf and 2,513 sf homes 0.07 mi away are pending at $459,990 and $439,990; 3734 Thimbleberry (2,868 sf new) is $479,990 after a $19,810 cut. 49 listings in the subdivision, 24 of them builder."),
'1610 CIMARRON TRL':(725000,680000,770000,'up',None,"Cotton Creek Ranch last asks: 1880 Chuckwagon 3,667 sf $650,000 (6 days, Feb); 1810 Rugged 3,775 sf $599,000; 1850 Cotton Creek 3,428 sf $597,000. Live: 1450 Branding Iron 4,445 sf $765,000 (cut, unsold). Subject is newer, 4,319 sf, on 2 acres. The AVMs at $850k+ follow a 2023 related-party transfer."),
'1618 FM 85':(525000,490000,580000,'hold',None,"Thin evidence: every nearby acreage sale is a 2020-2024 build at $220-$270/sf on 2,500-3,000 sf. Nothing of 1979 vintage and 4,000 sf sold. The 2022 purchase carried a $285,122 VA loan, which usually means a price near that."),
'4602 SADDLEHORN DR':(650000,625000,675000,'up',None,"Listed 7/3/2026 at $680,000, contingent 8/20, listing removed 9/25. 445 Rusty Run 2,902 sf (2021) went under contract at $650,000 in 30 days (Aug). 801 Brandi Ridge 3,210 sf on 1.09 ac is $659,000 after a $30,000 cut on 10/2."),
'3808 KINGS':(225000,215000,240000,'down',None,"The builder is the market here: 15 new homes for sale in the subdivision, one sale since July 1. 1600 Romans (1,355 sf, new) was cut $20,000 on 10/2 to $224,990; 1707 Romans (1,245 sf, new) $239,990. A three-year-old resale has to sit under those."),
'2010 MOBILE DR':(210000,195000,225000,'up',None,"2005 Mobile 1,069 sf $199,500 (Feb, after cuts); 900 Savannah 1,280 sf $235,000 (20 days, Jan); 1110 Edgewood 1,056 sf (1964) $170,000 (Sep). Live: 1106 Lady Bird 1,306 sf $230,000."),
}
if __name__=='__main__':
    out=[]
    print(f"{'PROPERTY':<22}{'SHEET ARV':>10}{'CENTRAL':>9}{'Δ':>9} {'OLD LOW':>8}{'OLD HIGH':>9} {'NEW LOW':>8}{'NEW HIGH':>9}{'TO BEAT':>9}  profit at price-to-beat: sheet ARV / central / central-5% & 9mo")
    for a,(cen,lo,hi,d,debt,why) in V.items():
        r=sheets[a]; pl,ph=r['low_profit_pct']/100,r['high_profit_pct']/100
        nl,nh=bid(r,cen,pl),bid(r,cen,ph)
        cb=r['credit_bid'] or debt or r['upb']
        k9=c(r)*1.5 if abs(c(r)-0.045)<1e-3 else c(r)*11/8      # 6->9 months (8->11 on Bakers)
        fx=dict(r); fx['utilities']=r['utilities']*(1.5 if abs(c(r)-0.045)<1e-3 else 11/8)
        p0,p1,p2=profit(r,r['arv'],cb),profit(r,cen,cb),profit(fx,cen*0.95,cb,k9)
        out.append(dict(addr=a,status=r['status'],sheet_arv=r['arv'],central=cen,lo=lo,hi=hi,dir=d,why=why,old_low=r['low_bid'],old_high=r['high_bid'],new_low=round(nl),new_high=round(nh),
            price_to_beat=cb,price_to_beat_source='posted credit bid' if r['credit_bid'] else ('recorded modification' if debt else "sheet's unpaid balance"),
            profit_at_beat_sheet=round(p0),profit_at_beat_central=round(p1),profit_at_beat_stress=round(p2),stress_low=round(bid(fx,cen*0.95,pl,k9)),stress_high=round(bid(fx,cen*0.95,ph,k9))))
        print(f"{a:<22}{r['arv']:>10,.0f}{cen:>9,.0f}{cen-r['arv']:>+9,.0f} {r['low_bid']:>8,.0f}{r['high_bid']:>9,.0f} {nl:>8,.0f}{nh:>9,.0f}{cb:>9,.0f}{'*' if not r['credit_bid'] else ' '} {p0:>8,.0f} ({p0/r['arv']:.0%}) / {p1:>8,.0f} ({p1/cen:.0%}) / {p2:>8,.0f} ({p2/(cen*.95):.0%}) | stress bids {bid(fx,cen*0.95,pl,k9):,.0f}-{bid(fx,cen*0.95,ph,k9):,.0f}")
    json.dump(out,open('verdicts.json','w'),indent=1)
