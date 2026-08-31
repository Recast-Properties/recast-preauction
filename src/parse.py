import re,glob,json,os
def money(s):
    if s is None: return None
    m=re.search(r'-?\$?\s*([\d,]+(?:\.\d+)?)',str(s))
    if not m: return None
    try: return float(m.group(1).replace(',',''))
    except: return None

def parse(path):
    L=[l.rstrip() for l in open(path).read().split('\n')]
    T=[l.strip() for l in L]
    def after(label,n=1,exact=True):
        for i,l in enumerate(T):
            if (l==label) if exact else (label in l):
                for j in range(i+1,min(i+1+n+6,len(T))):
                    if T[j]!='': return T[j]
        return None
    def allafter(label,n):
        for i,l in enumerate(T):
            if l==label:
                out=[]
                for j in range(i+1,len(T)):
                    if T[j]!='': out.append(T[j])
                    if len(out)>=n: break
                return out
        return []
    d={}
    d['id']=next((l for l in T[:4] if l.isdigit()),None)
    ai=next(i for i,l in enumerate(T) if l=='< Back')
    d['address']=T[ai+1]; d['cityline']=T[ai+2]; d['legal']=T[ai+3]
    auc=next((l for l in T if l.startswith('Auction Time')),'')
    d['auction_raw']=auc
    d['auction_house']=('Auction.com' if 'Auction.com' in auc else 'Xome' if 'Xome' in auc else
                        'Hubzu' if 'Hubzu' in auc else None)
    cb=re.search(r'Credit Bid:\s*\$([\d,]+)',auc); d['credit_bid']=money(cb.group(1)) if cb else None
    d['cleared']='**CLEARED**' in auc or 'CLEARED' in auc
    si=next(i for i,l in enumerate(T) if l.startswith('Auction Time'))
    notes=[T[j] for j in range(si+1,si+5) if T[j] and not T[j].startswith('Property Details')]
    d['notes']=' | '.join(notes)
    d['prop_type']=after('Property Type:'); d['year_built']=after('Year Built:')
    d['bbgp']=after('B/B/G/P'); d['sqft']=money(after('Sqft:'))
    d['acres']=after('Lot (Acres):')
    cm=next((l for l in T if l.startswith('Carry Months')),''); d['carry_months']=money(cm)
    d['rehab']=money(after('Rehab Cost:')); d['tax_yr']=money(after('Yearly Property Tax:'))
    d['taxes_owed']=money(after('Property Taxes Owed:'))
    d['utilities']=money(after('Utilities (x Carry Months)'))
    d['hoa_yr']=money(after('HOA/Year')); d['addl_liens']=money(after('Additional Liens'))
    cg=next((l for l in T if l.startswith('Contingency/Roof')),''); d['contingency']=money(cg)
    d['commission']=money(after('3% Commissions:')); d['closing']=money(after('2% Closing Costs:'))
    d['hard_total']=money(after('Total:'))
    ec=next((l for l in T if l.startswith('ECAD #')),''); d['ecad_id']=re.sub(r'\D','',ec) or None
    d['ecad']=money(after(ec)) if ec else None
    d['zillow']=money(after('Zillow:')); d['realtor']=money(after('Realtor.com:'))
    d['redfin']=money(after('Redfin:'))
    ct=after('Cotality:'); d['cotality']=money(ct) if ct and '$' in str(ct) else None
    cr=next((l for l in T if 'Cotality Range' in l),'')
    rng=re.findall(r'\$([\d,]+)', (T[T.index(cr)+1] if cr in T and T.index(cr)+1<len(T) else '')+' '+cr)
    d['cotality_range']=[money(x) for x in rng] if len(rng)>=2 else None
    cs=next((l for l in T if 'Confidence Score' in l),'')
    m=re.search(r'(\d+)%',cs+' '+(T[T.index(cs)+1] if cs in T and T.index(cs)+1<len(T) else ''))
    d['cotality_conf']=int(m.group(1)) if m else None
    d['arv']=money(after('ARV:'))
    bids=[i for i,l in enumerate(T) if l in ('Low Bid:','High Bid:')]
    for i in bids:
        key='low' if T[i]=='Low Bid:' else 'high'
        d[key+'_bid']=money(T[i+1])
    pcts=[money(T[i+1]) for i,l in enumerate(T) if l=='Profit %']
    ints=[money(T[i+1]) for i,l in enumerate(T) if l.startswith('Loan Interest')]
    tcs=[money(l) for l in T if l.startswith('Total Costs (Hard Costs')]
    prs=[money(T[i+1]) for i,l in enumerate(T) if l.startswith('Profit (ARV')]
    d['low_profit_pct'],d['high_profit_pct']=(pcts+[None,None])[:2]
    d['low_interest'],d['high_interest']=(ints+[None,None])[:2]
    d['low_totalcost'],d['high_totalcost']=(tcs+[None,None])[:2]
    d['low_profit'],d['high_profit']=(prs+[None,None])[:2]
    d['loan_type']=after('Loan Type'); d['mortgage_holder']=after('Mortgage Holder:')
    d['trustee']=after('Trustee:'); d['loan_year']=after('Loan Year:')
    d['orig_loan']=money(after('Original Loan Amount:'))
    d['upb']=money(after('Unpaid Balance:'))
    ee=[i for i,l in enumerate(T) if l.startswith('Estimated Equity')]
    d['equity']=money(T[ee[0]+2]) if ee else None
    if d['equity'] is None and ee: d['equity']=money(T[ee[0]+1])
    return d

rows=[]
for f in sorted(glob.glob('sheets/*.txt')):
    if 'OVERVIEW' in f: continue
    try: rows.append(parse(f))
    except Exception as e: print('ERR',f,e)
json.dump(rows,open('sheets.json','w'),indent=1)
for r in rows:
    print(f"#{str(r['id']):>3} {r['address']:<22} {str(r['sqft']):>8} sf  yr {r['year_built']:<5} {str(r['bbgp']):<7}"
          f" ARV ${r['arv'] or 0:>9,.0f}  low ${r['low_bid'] or 0:>9,.0f}  high ${r['high_bid'] or 0:>9,.0f}"
          f"  CB ${r['credit_bid'] or 0:>9,.0f} {'CLEARED' if r['cleared'] else ''}")
