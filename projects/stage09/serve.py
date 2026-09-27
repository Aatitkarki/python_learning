"""Opt-in real model benchmark. Never runs automatically during course checks."""
import argparse
import json
import math
import statistics
import time
from urllib.request import Request, urlopen

def chat(base_url,model,prompt,backend='ollama',timeout=30):
    if backend=='ollama':
        url=base_url.rstrip('/')+'/api/chat'
        payload={'model':model,'messages':[{'role':'user','content':prompt}], 'stream':False,'options':{'num_predict':128,'temperature':0}}
    else:
        url=base_url.rstrip('/')+'/v1/chat/completions'
        payload={'model':model,'messages':[{'role':'user','content':prompt}],'max_tokens':128,'temperature':0}
    request=Request(url,data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
    started=time.perf_counter()
    with urlopen(request,timeout=timeout) as response:
        body=response.read(2_000_001)
        if len(body)>2_000_000: raise ValueError('Response too large')
        result=json.loads(body)
    if backend=='ollama': content=result['message']['content']; tokens=result.get('eval_count')
    else: content=result['choices'][0]['message']['content']; tokens=result.get('usage',{}).get('completion_tokens')
    return {'text':content,'seconds':time.perf_counter()-started,'tokens':tokens,'backend':backend,'model':model}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',required=True)
    parser.add_argument('--backend',choices=['ollama','vllm'],default='ollama')
    parser.add_argument('--url',default='http://127.0.0.1:11434')
    parser.add_argument('--runs',type=int,default=3)
    args=parser.parse_args()
    if not 1<=args.runs<=100: parser.error('runs must be 1..100')
    runs=[]
    for _ in range(args.runs): runs.append(chat(args.url,args.model,'Explain a database index in two sentences.',args.backend))
    times=sorted(r['seconds'] for r in runs)
    print(json.dumps({'runs':runs,'p50_seconds':statistics.median(times),'p95_seconds':times[math.ceil(.95*len(times))-1],
                      'note':'Sequential non-streaming timings; first run may include cold loading. Not TTFT or concurrent throughput.'},indent=2))

if __name__=='__main__': main()
