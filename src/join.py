import json,re,statistics as st
sw=json.load(open('sweeps.json')); subs=json.load(open('subs_cad.json'))
subj=json.load(open('subjects.json')); sheets={r['address']:r for r in json.load(open('sheets.json'))}
def norm(a): return re.sub(r'\s+',' ',a.split(',')[0].upper().strip())
Z={}
for k,items in sw.items():
    st_=k.split('|')[1]
    for it in items:
        hi=(it.get('hdpData') or {}).get('homeInfo') or {}
        n=norm(it.get('address',''))
        if not n: continue
        d=Z.setdefault(n,{})
        p=it.get('price') or hi.get('price')
        if isinstance(p,str): p=int(re.sub(r'[^0-9]','',p) or 0)
        sf=it.get('area') or hi.get('livingArea')
        if sf: d['sqft']=sf
        if hi.get('zestimate'): d['zest']=hi['zestimate']
        if hi.get('yearBuilt'): d['yr']=hi['yearBuilt']
        if st_=='for_sale' and p: d['ask']=p; d['status']=it.get('statusText') or hi.get('homeStatus')
        if st_=='sold': d['soldFlag']=True
json.dump(Z,open('zarea.json','w'))
print('area zillow addresses:',len(Z))
MAP={"OAK LEAF FARMS":"2052 WILLOW BEND DR","DOVE CREEK":"5614 LOG CABIN CT",
 "ESTATES OF NORTH GROVE":"469 BRUSHWOOD LN","HAVEN PH":"408 ABBOTT LN",
 "GARDEN VALLEY RANCH":"323 TUMBLEWEED TRL","HAWKINS MEADOWS":"501 WHITE PLAINS CT",
 "GREENWAY TRAILS":"10407 WALNUT RIDGE DR"}
print()
for sub,anchor in MAP.items():
    cad={norm(p['addr']):p for p in subs[sub] if str(p['useCd']).startswith('*')}
    asks=[]
    for a,p in cad.items():
        z=Z.get(a)
        if z and z.get('ask') and z.get('sqft'):
            asks.append((a,z['sqft'],z['ask'],z['ask']/z['sqft'],z.get('status',''),z.get('yr')))
    sf=subj[anchor]['living']
    sh=sheets[anchor]
    print(f"### {sub}  ({len(cad)} parcels)  anchor {anchor} @ {sf:,.0f} sf")
    if asks:
        ps=[x[3] for x in asks]
        for a,s,p,pp,stt,yr in sorted(asks,key=lambda x:x[3]):
            print(f"     {a:<26}{s:>6,} sf  ${p:>9,}  ${pp:>5.0f}/sf  yr {yr}  {str(stt)[:16]}")
        print(f"     -> active ask $/sf median ${st.median(ps):.0f}  | subject implies ${st.median(ps)*sf:,.0f}   (sheet ARV ${sh['arv']:,.0f})")
    else:
        print("     no active listings matched in this subdivision")
    print()

# persist per-subdivision active asks for the report generator
res={}
for sub,anchor in MAP.items():
    cad={norm(p['addr']):p for p in subs[sub] if str(p['useCd']).startswith('*')}
    rows=[]
    for a,p in cad.items():
        z=Z.get(a)
        if z and z.get('ask') and z.get('sqft'):
            rows.append({'addr':a,'sqft':z['sqft'],'ask':z['ask'],'psf':z['ask']/z['sqft'],
                         'status':z.get('status',''),'zest':z.get('zest')})
    res[anchor]={'sub':sub,'parcels':len(cad),'actives':sorted(rows,key=lambda r:r['psf'])}
json.dump(res,open('actives.json','w'),indent=1)
print('saved actives.json')
