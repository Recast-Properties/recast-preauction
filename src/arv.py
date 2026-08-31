import json,statistics as st,re
sheets={r['address']:r for r in json.load(open('sheets.json'))}
cot=json.load(open('cotality.json'))
subj=json.load(open('subjects.json'))
zd={}
for it in json.load(open('zdetail_all.json')):
    a=(it.get('address') or {}).get('streetAddress','').upper()
    zd[a]=it
key={'10407 WALNUT RIDGE DR':'10407 WALNUT RIDGE DR','2052 WILLOW BEND DR':'2052 WILLOW BEND DR',
 '323 TUMBLEWEED TRL':'323 TUMBLEWEED TRL','408 ABBOTT LN':'408 ABBOTT LN',
 '469 BRUSHWOOD LN':'469 BRUSHWOOD LN','495 WASHINGTON AVE':'495 WASHINGTON AVE',
 '501 WHITE PLAINS CT':'501 WHITE PLAINS CT','5614 LOG CABIN CT':'5614 LOG CABIN CT'}
rows=[]
for a in key:
    sh=sheets[a]; c=cot[a]; s=subj[a]
    z=zd.get(a,{})
    sf=s['living'] or sh['sqft']
    sold=[x for x in c['comps'] if x['price'] and x['sqft'] and x['sqft']>500]
    spsf=[x['price']/x['sqft'] for x in sold]
    near=[x for x in c['nearby'] if x['est'] and x['sqft'] and x['sqft']>500]
    npsf=[x['est']/x['sqft'] for x in near]
    avms=[v for v in (sh['ecad'],sh['zillow'],sh['realtor'],sh['redfin'],c['estimate']) if v]
    rows.append({'addr':a,'sheet':sh,'cot':c,'cad':s,'z':z,'sf':sf,
      'sold':sold,'spsf':spsf,'near':near,'npsf':npsf,'avms':avms})
    print('='*104)
    print(f"{a}   {sf:,.0f} sf | built {s['yearBuilt']} | {sh['bbgp']} | {s['acres']} ac | \"{sh['notes'][:60]}\"")
    print(f"   SHEET ARV ${sh['arv']:,.0f} (${sh['arv']/sf:.0f}/sf)   AVMs: CAD ${sh['ecad']:,.0f} | Z ${sh['zillow'] or 0:,.0f} | R ${sh['realtor'] or 0:,.0f} | RF ${sh['redfin'] or 0:,.0f} | COT ${c['estimate']:,.0f} (conf {c['confidence']:.0f}, FSD {c['fsd']:.0f})")
    print(f"   AVM spread: ${min(avms):,.0f} - ${max(avms):,.0f}   median ${st.median(avms):,.0f}   Cotality range ${c['low']:,.0f}-${c['high']:,.0f}")
    if spsf:
        print(f"   COTALITY SOLD COMPS (n={len(sold)}): median ${st.median(spsf):.0f}/sf -> ${st.median(spsf)*sf:,.0f}   range ${min(spsf):.0f}-${max(spsf):.0f}/sf")
        for x in sorted(sold,key=lambda v:v['date'])[-6:]:
            print(f"      {x['date']}  {x['addr'][:30]:<31}{x['sqft']:>7,.0f} sf  ${x['price']:>10,.0f}  ${x['price']/x['sqft']:>5.0f}/sf  {x['dist']}")
    if npsf:
        print(f"   NEARBY THVX (n={len(near)}): median ${st.median(npsf):.0f}/sf -> ${st.median(npsf)*sf:,.0f}")
json.dump([{k:v for k,v in r.items() if k not in ('z',)} for r in rows],open('arv_rows.json','w'),indent=1,default=str)
