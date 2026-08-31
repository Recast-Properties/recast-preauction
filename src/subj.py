import json,time,urllib.request
API="https://prod-container.trueprodigyapi.com"
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
H={"Origin":"https://www.elliscad.com","Referer":"https://www.elliscad.com/",
   "Accept":"application/json, text/plain, */*","User-Agent":UA}
def req(url,data=None,tok=None,tries=3):
    hdr=dict(H)
    if tok: hdr["Authorization"]=tok
    body=json.dumps(data).encode() if data is not None else None
    if body: hdr["Content-Type"]="application/json"
    r=urllib.request.Request(url,data=body,headers=hdr,method="POST" if body else "GET")
    for a in range(tries):
        try:
            with urllib.request.urlopen(r,timeout=30) as x:
                t=x.read().decode(); return json.loads(t) if t.strip() else {}
        except Exception as e:
            if a==tries-1: return {"__err":str(e)}
            time.sleep(3)
def token(): return req(f"{API}/trueprodigy/cadpublic/auth/token",{"office":"Ellis"})["user"]["token"]
tok=token()
cad=json.load(open('subjects_cad.json'))
sheets={r['address']:r for r in json.load(open('sheets.json'))}
key={'2052 WILLOW BEND':'2052 WILLOW BEND DR','5614 LOG CABIN':'5614 LOG CABIN CT',
 '469 BRUSHWOOD':'469 BRUSHWOOD LN','408 ABBOTT':'408 ABBOTT LN','323 TUMBLEWEED':'323 TUMBLEWEED TRL',
 '501 WHITE PLAINS':'501 WHITE PLAINS CT','495 WASHINGTON':'495 WASHINGTON AVE',
 '10407 WALNUT RIDGE':'10407 WALNUT RIDGE DR'}
out={}
print(f"{'PROPERTY':<24}{'SHEET SF':>9}{'CAD SF':>8}{'DELTA':>8}   {'YR':<6}{'CAD APPR':>10}{'$/SF':>6}")
for k,res in cad.items():
    if not res: continue
    r=res[0]; acct=r['pAccountID']
    imp=req(f"{API}/public/propertyaccount/{acct}/improvement",None,tok).get("results",[])
    liv=sum(float(x.get("livingArea") or 0) for x in imp)
    yrs=[int(d["actualYearBuilt"]) for x in imp for d in x.get("details",[]) if str(d.get("actualYearBuilt") or "").isdigit()]
    gar=sum(float(d.get("area") or 0) for x in imp for d in x.get("details",[]) if "GARAGE" in (d.get("detailTypeDescription") or ""))
    st=2 if any("2ND STORY" in (d.get("detailTypeDescription") or "") for x in imp for d in x.get("details",[])) else 1
    a=key[k]; sh=sheets[a]
    out[a]={'pid':r['pid'],'acct':acct,'legal':r['legalDescription'],'acres':float(r['legalAcreage']),
            'appraised':r['appraisedValue'],'land':r['landValue'],'living':liv,'yearBuilt':min(yrs) if yrs else None,
            'garage':gar,'stories':st,'lat':float(r['latitude']),'lng':float(r['longitude']),
            'owner':r.get('name'),'deedDt':(r.get('deedDt') or '')[:10],'asCode':r.get('asCode'),
            'mailCity':r.get('addrCity'),'situs':r.get('fullSitus')}
    d=liv-(sh['sqft'] or 0)
    flag='  <-- MISMATCH' if abs(d)>50 else ''
    print(f"{a:<24}{sh['sqft'] or 0:>9,.0f}{liv:>8,.0f}{d:>+8,.0f}   {str(min(yrs) if yrs else '?'):<6}{r['appraisedValue']:>10,}{r['appraisedValue']/liv if liv else 0:>6.0f}{flag}")
    time.sleep(1.2)
json.dump(out,open('subjects.json','w'),indent=1)
