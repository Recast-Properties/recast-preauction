"""Ellis County market layer: zip-level conditions applied to each deal."""
import csv,json
ZIPS={'75165':'Waxahachie','76065':'Midlothian','75154':'Red Oak / Oak Leaf'}
PROP_ZIP={'1751 SHUMARD ST':'75165','408 ABBOTT LN':'75165','469 BRUSHWOOD LN':'75165',
 '495 WASHINGTON AVE':'75165','323 TUMBLEWEED TRL':'75165','5614 LOG CABIN CT':'76065',
 '501 WHITE PLAINS CT':'76065','10407 WALNUT RIDGE DR':'76065','2052 WILLOW BEND DR':'75154'}
def f(r,k):
    v=r.get(k) or ''
    try: return float(v)
    except: return None
zi={}
with open('RDC_Inventory_Core_Metrics_Zip.csv') as fh:
    for r in csv.DictReader(fh):
        z=(r.get('postal_code') or '').strip()
        if z in ZIPS: zi.setdefault(z,[]).append(r)
cty=[]
with open('RDC_Inventory_Core_Metrics_County.csv') as fh:
    for r in csv.DictReader(fh):
        if (r.get('county_name') or '').lower()=='ellis, tx': cty.append(r)
def latest(rs): return sorted(rs,key=lambda r:r['month_date_yyyymm'])[-1]
def pack(r):
    return {'month':r['month_date_yyyymm'],
      'median_list':f(r,'median_listing_price'),'median_list_yy':f(r,'median_listing_price_yy'),
      'active':f(r,'active_listing_count'),'active_mm':f(r,'active_listing_count_mm'),
      'active_yy':f(r,'active_listing_count_yy'),'dom':f(r,'median_days_on_market'),
      'dom_yy':f(r,'median_days_on_market_yy'),'reduced_ct':f(r,'price_reduced_count'),
      'pending':f(r,'pending_listing_count'),'pending_ratio':f(r,'pending_ratio'),
      'psf':f(r,'median_listing_price_per_square_foot'),'psf_yy':f(r,'median_listing_price_per_square_foot_yy'),
      'new_yy':f(r,'new_listing_count_yy')}
M={'county':pack(latest(cty)),'zips':{z:pack(latest(v)) for z,v in zi.items()},
   'zip_names':ZIPS,'prop_zip':PROP_ZIP}
# 13-month history for trend sparkline
hist={}
for z,v in zi.items():
    hist[z]=[{'month':r['month_date_yyyymm'],'psf':f(r,'median_listing_price_per_square_foot'),
              'active':f(r,'active_listing_count'),'dom':f(r,'median_days_on_market')}
             for r in sorted(v,key=lambda r:r['month_date_yyyymm'])[-13:]]
hist['county']=[{'month':r['month_date_yyyymm'],'psf':f(r,'median_listing_price_per_square_foot'),
                 'active':f(r,'active_listing_count'),'dom':f(r,'median_days_on_market')}
                for r in sorted(cty,key=lambda r:r['month_date_yyyymm'])[-13:]]
M['history']=hist
json.dump(M,open('market.json','w'),indent=1)

c=M['county']
print(f"ELLIS COUNTY {c['month']}: median list ${c['median_list']:,.0f} ({c['median_list_yy']:+.1%} yy) | "
      f"{c['active']:,.0f} actives ({c['active_mm']:+.1%} mm, {c['active_yy']:+.1%} yy) | DOM {c['dom']:.0f} ({c['dom_yy']:+.1%} yy) | "
      f"${c['psf']:.0f}/sf ({c['psf_yy']:+.1%} yy) | {c['reduced_ct']:.0f}/{c['active']:.0f} cut = {c['reduced_ct']/c['active']:.0%}")
print()
for z,n in ZIPS.items():
    m=M['zips'][z]
    print(f"{z} {n:<20} list ${m['median_list']:>8,.0f} ({m['median_list_yy']:+.1%}) | act {m['active']:>4.0f} ({m['active_mm']:+.1%}mm {m['active_yy']:+.1%}yy) | "
          f"DOM {m['dom']:>3.0f} ({m['dom_yy']:+.1%}) | ${m['psf']:.0f}/sf ({m['psf_yy']:+.1%}) | cut {m['reduced_ct']/m['active']:.0%} | pend {m['pending_ratio']:.0%}")
print()
print("13-month $/sf trend by zip:")
for z in list(ZIPS)+['county']:
    h=M['history'][z]
    print(f"  {z:<8}", " ".join(f"{x['psf']:.0f}" if x['psf'] else "--" for x in h))
