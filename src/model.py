"""Reproduce each sheet's own bid model, then re-solve it on a comps-derived ARV."""
import json,statistics as st
sheets={r['address']:r for r in json.load(open('sheets.json'))}
def fixed(r):
    """Hard costs that do NOT scale with ARV."""
    return sum(x or 0 for x in (r['rehab'],r['tax_yr'],r['taxes_owed'],r['utilities'],
                                r['hoa_yr'],r['addl_liens'],r['contingency']))
def rate(r):
    """Effective interest as a fraction of the bid, back-solved from the sheet's own rows."""
    rs=[]
    for b,i in ((r['low_bid'],r['low_interest']),(r['high_bid'],r['high_interest'])):
        if b and i: rs.append(i/b)
    return st.mean(rs) if rs else 0.0477
def hard(r,arv): return fixed(r)+0.05*arv
def bid(r,arv,p): return (arv*(1-p)-hard(r,arv))/(1+rate(r))
def profit(r,arv,b): return arv-hard(r,arv)-rate(r)*b-b

print(f"{'PROPERTY':<24}{'SHEET LOW':>11}{'MODEL':>11}{'Δ':>7}   {'SHEET HIGH':>11}{'MODEL':>11}{'Δ':>7}   {'r':>7}")
ok=0
for a,r in sheets.items():
    if not r['arv']: continue
    lo=bid(r,r['arv'],(r['low_profit_pct'] or 0)/100)
    hi=bid(r,r['arv'],(r['high_profit_pct'] or 0)/100)
    dl=lo-(r['low_bid'] or 0); dh=hi-(r['high_bid'] or 0)
    if abs(dl)<600 and abs(dh)<600: ok+=1
    print(f"{a:<24}{r['low_bid'] or 0:>11,.0f}{lo:>11,.0f}{dl:>+7,.0f}   "
          f"{r['high_bid'] or 0:>11,.0f}{hi:>11,.0f}{dh:>+7,.0f}   {rate(r):>7.4f}")
print(f"\nreproduced within $600 on {ok}/{len(sheets)} sheets")
