import json,re,math,urllib.parse,statistics as st
RUN=__import__('os').path.dirname(__import__('os').path.abspath(__file__))+'/'
subj=json.load(open(RUN+'subjects.json')); subs=json.load(open(RUN+'subs_cad.json'))
sheets={r['address']:r for r in json.load(open(RUN+'sheets.json'))}
boxes=json.load(open('boxes.json'))
SUBS={"KENSINGTON PARK":"3606 REGENT ST","MEADOWS OF PALMER":"241 POINSETTA DR","ESTATES OF NORTH GROVE":"541 TRUMAN ST","WALKERS RUN":"905 ROYSE RIDGE RD","GINGERBREAD VILLAGE":"102 MYRTLE AVE","RIDGE CROSSING":"2329 SLATE DR","PRAIRIE RIDGE PH":"3509 BURDOCK LN","COTTON CREEK RANCH":"1610 CIMARRON TRL","BRANDI RIDGE":"4602 SADDLEHORN DR","CHRISTIAN MEADOWS":"3808 KINGS","SOUTHGATE":"2010 MOBILE DR"}
inv={v:k for k,v in SUBS.items()}
SUF=r'\b(DR|ST|LN|RD|TRL|AVE|CT|BLVD|WAY|CIR|PL|PKWY|TER|DRIVE|STREET|LANE|ROAD|TRAIL|AVENUE|COURT)\b\.?'
def norm(a): return re.sub(r'\s+',' ',re.sub(SUF,'',a.split(',')[0].upper())).strip()
def money(p):
    if not p: return None
    if p.get('amount'): return float(p['amount'])
    m=re.sub(r'[^0-9]','',p.get('formatted') or ''); return float(m) if m else None
def acres(l):
    if not l or not l.get('value'): return None
    return l['value'] if l.get('unit')=='acres' else l['value']/43560
def dist(a,b,c,d): return math.hypot((a-c)*69.0,(b-d)*58.3)
def boxof(it):
    u=urllib.parse.unquote(it.get('sourceSearchUrl') or ''); m=re.search(r'"south":([\d.-]+)',u)
    if not m: return None
    s=float(m.group(1))
    for a,b in boxes.items():
        if abs(b['south']-s)<1e-6: return a
def load(f):
    out={}
    for it in json.load(open(f)):
        a=boxof(it)
        if a: out.setdefault(a,[]).append(it)
    return out
SALE=load('sweep_sale.json'); SOLD=load('sweep_sold.json')
def rows(a,items):
    s=subj[a]; roll={norm(p['addr']) for p in subs[inv[a]]} if a in inv else set()
    R=[]
    for it in items:
        ad=(it.get('listingAddress') or {}).get('full','')
        c=it.get('coordinates') or {}; lt=it.get('listingType') or {}
        R.append(dict(addr=ad.split(',')[0],price=money(it.get('listingPrice')),sf=it.get('livingArea'),status=it.get('listingStatus'),
          new=lt.get('isNewHome'),auc=lt.get('isForAuction') or lt.get('isForeclosure') or lt.get('isBankOwned'),cut=it.get('priceChange'),cutAt=(it.get('priceChangedAt') or '')[:10],
          ac=acres(it.get('lotArea')),insub=norm(ad) in roll,d=dist(s['lat'],s['lng'],c.get('latitude',0),c.get('longitude',0)),
          zest=it.get('zestimate'),type=it.get('homeType'),sold=(it.get('dateSold') or it.get('marketingTagline') or ''),beds=it.get('bedrooms'),baths=it.get('bathrooms'),tag=it.get('marketingTagline')))
    return R
