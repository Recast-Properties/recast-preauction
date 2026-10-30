import sys,json,time
sys.path.insert(0,'/Users/paulbjork/Desktop/Claude/Recast-preauction/src')
from apify import api
def run(actor,inp,label):
    r=api(f"acts/{actor.replace('/','~')}/runs?waitForFinish=60",inp)['data']
    while r['status'] in ('READY','RUNNING'):
        time.sleep(10); r=api(f"actor-runs/{r['id']}?waitForFinish=60")['data']
    items=api(f"datasets/{r['defaultDatasetId']}/items?clean=true&format=json")
    r=api(f"actor-runs/{r['id']}")['data']
    print(f"{label}: {r['status']} {len(items)} items, cost ${r.get('usageTotalUsd',0):.3f}",flush=True)
    return items
