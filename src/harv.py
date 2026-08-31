import json,time,urllib.request
API="https://prod-container.trueprodigyapi.com"
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
H={"Origin":"https://www.elliscad.com","Referer":"https://www.elliscad.com/",
   "Accept":"application/json, text/plain, */*","User-Agent":UA}
def req(url,data=None,tok=None,tries=4):
    hdr=dict(H)
    if tok: hdr["Authorization"]=tok
    body=json.dumps(data).encode() if data is not None else None
    if body: hdr["Content-Type"]="application/json"
    r=urllib.request.Request(url,data=body,headers=hdr,method="POST" if body else "GET")
    for a in range(tries):
        try:
            with urllib.request.urlopen(r,timeout=35) as x:
                t=x.read().decode(); return json.loads(t) if t.strip() else {}
        except Exception:
            if a==tries-1: return {}
            time.sleep(4)
def token(): return req(f"{API}/trueprodigy/cadpublic/auth/token",{"office":"Ellis"})["user"]["token"]

SUBS={"OAK LEAF FARMS":"2052 WILLOW BEND DR","DOVE CREEK":"5614 LOG CABIN CT",
 "ESTATES OF NORTH GROVE":"469 BRUSHWOOD LN","HAVEN PH":"408 ABBOTT LN",
 "GARDEN VALLEY RANCH":"323 TUMBLEWEED TRL","HAWKINS MEADOWS":"501 WHITE PLAINS CT",
 "GREENWAY TRAILS":"10407 WALNUT RIDGE DR"}
tok=token(); out={}
for sub in SUBS:
    rows=[]
    for page in range(1,6):
        d=req(f"{API}/public/property/search?page={page}&pageSize=100",
              {"pYear":{"operator":"=","value":"2026"},
               "legalDescription":{"operator":"mlike","value":sub}},tok)
        res=d.get("results",[])
        if not res: break
        rows+=res
        time.sleep(1.0)
    out[sub]=[{"pid":r["pid"],"acct":r["pAccountID"],"addr":r["streetPrimary"],
      "legal":r["legalDescription"],"acres":float(r.get("legalAcreage") or 0),
      "land":r.get("landValue"),"appraised":r.get("appraisedValue"),"useCd":r.get("useCd"),
      "owner":r.get("name"),"mailCity":r.get("addrCity"),"deedDt":(r.get("deedDt") or "")[:10],
      "lat":float(r.get("latitude") or 0),"lng":float(r.get("longitude") or 0),
      "asCode":r.get("asCode")} for r in rows]
    print(f"{sub:26} {len(rows):>4} parcels",flush=True)
    time.sleep(1.5)
json.dump(out,open('subs_cad.json','w'),indent=1)
print("done")
