import re, json, urllib.request, os
SEC="/Users/paulbjork/Desktop/Claude/Auction Sheets/Secrets.js"
def tok():
    s=open(SEC).read()
    return re.search(r"APIFY_TOKEN:\s*'([^']+)'", s).group(1)
def api(path, data=None):
    url=f"https://api.apify.com/v2/{path}"
    sep='&' if '?' in url else '?'
    url=f"{url}{sep}token={tok()}"
    body=json.dumps(data).encode() if data is not None else None
    r=urllib.request.Request(url, data=body,
        headers={"Content-Type":"application/json"}, method="POST" if body else "GET")
    with urllib.request.urlopen(r, timeout=300) as resp:
        return json.loads(resp.read().decode())
