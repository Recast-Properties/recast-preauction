import re,glob,json,os,statistics as st
def num(s):
    s=re.sub(r'[^0-9.]','',str(s))
    try: return float(s) if s else None
    except: return None
DROP=re.compile(r'^(©|Page \d+ of|APN:|CLIP:|Land Use:|Subject$|Comparable$|Nearby THVX Estimates$|'
    r'#$|Comp Address$|Distance$|Sale Amount$|Date of Sale$|Age$|Beds$|Baths$|Living Area$|Lot Area$|'
    r'Property Address$|THVX Estimated Value$|Comparables Used|Nearby THVX Estimated|'
    r'Total Home Value|ESTIMATED$|VALUATION ON|Low Range:|High Range:|Report Run Date:|Last Sale Date:|'
    r'Confidence Score:|Forecast Standard|Deviation:|Owners as of|Disclaimer of Use)')
def clean(T):
    out=[]
    for l in T:
        l=l.strip()
        if not l or DROP.match(l): continue
        if re.match(r'^\d+ [A-Z0-9].* (TX|Tx) \d{5}',l): continue   # address header
        out.append(l)
    return out
def parse(path):
    raw=[l.strip() for l in open(path).read().split('\n')]
    d={'file':os.path.basename(path).replace('.txt','')}
    def val(lbl,off=1):
        for i,l in enumerate(raw):
            if l==lbl:
                for j in range(i+off,min(i+off+4,len(raw))):
                    if raw[j]: return raw[j]
        return None
    d['estimate']=num(val('ESTIMATED')); d['low']=num(val('Low Range:'))
    d['high']=num(val('High Range:')); d['confidence']=num(val('Confidence Score:'))
    d['fsd']=num(val('Forecast Standard',2)); d['runDate']=val('Report Run Date:')
    for l in raw:
        m=re.match(r'^CLIP:\s*(\d+)',l)
        if m: d['clip']=m.group(1)
    # split the doc at the nearby-estimates header
    txt='\n'.join(raw)
    isplit=txt.find('Nearby THVX Estimated Values')
    sold_raw=raw[:len(txt[:isplit].split('\n'))] if isplit>0 else raw
    near_raw=raw[len(txt[:isplit].split('\n')):] if isplit>0 else []
    # SOLD COMPS: anchor on "<dist> mi" then $amount then date
    S=clean(sold_raw); comps=[]
    for i,l in enumerate(S):
        if re.match(r'^\d+(\.\d+)?\s*mi$',l) and i>=1 and i+7<len(S):
            addr=S[i-1]
            if re.match(r'^\d+$',addr): continue
            amt,date=S[i+1],S[i+2]
            if not amt.startswith('$') or not re.match(r'\d{2}/\d{2}/\d{4}',date): continue
            comps.append({'addr':addr,'dist':l,'price':num(amt),'date':date,
              'age':num(S[i+3]),'beds':num(S[i+4]),'baths':num(S[i+5]),
              'sqft':num(S[i+6]),'lot':num(S[i+7])})
    d['comps']=comps
    N=clean(near_raw); nb=[]
    for i,l in enumerate(N):
        if re.match(r'^\d+(\.\d+)?\s*mi$',l) and i>=1 and i+6<len(N):
            addr=N[i-1]
            if re.match(r'^\d+$',addr): continue
            est=N[i+1]
            if not est.startswith('$'): continue
            nb.append({'addr':addr,'dist':l,'est':num(est),'age':num(N[i+2]),
              'beds':num(N[i+3]),'baths':num(N[i+4]),'sqft':num(N[i+5]),'lot':num(N[i+6])})
    d['nearby']=nb
    return d
out={}
for f in sorted(glob.glob('cot/*.txt')):
    d=parse(f); out[d['file']]=d
    ps=[c['price']/c['sqft'] for c in d['comps'] if c['price'] and c['sqft'] and c['sqft']>500]
    dates=[c['date'] for c in d['comps']]
    print(f"{d['file']:<24} est ${d['estimate']:>9,.0f} conf {d['confidence']:.0f} | sold {len(d['comps'])}"
          +(f" med ${st.median(ps):>6.0f}/sf" if ps else " —")+f" | nearby {len(d['nearby'])}")
json.dump(out,open('cotality.json','w'),indent=1)
