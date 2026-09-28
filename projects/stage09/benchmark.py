"""09a/09b: memory budgets and observed serving distributions, including failures."""
import argparse
import json
import math
import platform
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from projects.stage09.serve import chat

def memory_budget():
    rows=[]
    # Architecture is an explicit scenario, not inferred from parameter count.
    for parameters in [1_000_000_000,7_000_000_000,14_000_000_000]:
        for bits in [4,8,16]:
            for context in [2048,8192,32768]:
                weights=parameters*bits/8/1024**3
                kv=2*32*8*128*context*2/1024**3
                rows.append({'parameters':parameters,'bits':bits,'context':context,'weight_gib':weights,'kv_gib':kv,
                             'assumption':'32 layers, 8 KV heads, dim 128, batch 1, FP16 KV. Excludes activations, quantization metadata and runtime.'})
    return rows

def measure(operation,runs=30,concurrency=1):
    if runs<1 or concurrency<1:raise ValueError('Positive benchmark sizes required')
    def one(index):
        started=time.perf_counter()
        try:
            result=operation()
            return {'index':index,'ok':True,'seconds':time.perf_counter()-started,'tokens':result.get('tokens'),'output_characters':len(result['text'])}
        except Exception as exc:
            return {'index':index,'ok':False,'seconds':time.perf_counter()-started,'error':type(exc).__name__}
    started=time.perf_counter()
    with ThreadPoolExecutor(max_workers=concurrency) as pool:rows=list(pool.map(one,range(runs)))
    elapsed=time.perf_counter()-started;times=sorted(r['seconds'] for r in rows);tokens=[r['tokens'] for r in rows if r['ok']]
    return {'observations':rows,'runs':runs,'concurrency':concurrency,'wall_seconds':elapsed,'failures':sum(not r['ok'] for r in rows),
            'p50_seconds_all_attempts':times[math.ceil(.5*len(times))-1],'p95_seconds_all_attempts':times[math.ceil(.95*len(times))-1],
            'tokens_per_wall_second':sum(tokens)/elapsed if tokens and all(isinstance(n,int) for n in tokens) else None}

def run(output,model=None,url='http://127.0.0.1:11434',backend='ollama',runs=30):
    report={'machine':{'platform':platform.platform(),'processor':platform.processor(),'python':platform.python_version()},'memory_scenarios':memory_budget()}
    if model:
        operation=lambda:chat(url,model,'Explain a database index in two sentences.',backend,timeout=30)
        report['first_request']=measure(operation,1,1)  # Not called cold: model may already be resident.
        report['warm']=[measure(operation,runs,c) for c in [1,2,4]]
        report['model']=model;report['endpoint']=url
    else:report['serving_status']='Not run: provide --model and a running server. No benchmark numbers fabricated.'
    out=Path(output);out.mkdir(parents=True,exist_ok=True);(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--model');p.add_argument('--url',default='http://127.0.0.1:11434');p.add_argument('--backend',choices=['ollama','vllm'],default='ollama');p.add_argument('--runs',type=int,default=30);p.add_argument('--output',default='work/reference_answers/stage09');a=p.parse_args()
    print(json.dumps(run(a.output,a.model,a.url,a.backend,a.runs),indent=2))
