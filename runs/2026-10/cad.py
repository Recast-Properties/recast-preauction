import json,time,urllib.request,sys
API="https://prod-container.trueprodigyapi.com"
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
H={"Origin":"https://www.elliscad.com","Referer":"https://www.elliscad.com/","Accept":"application/json, text/plain, */*","User-Agent":UA}
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
