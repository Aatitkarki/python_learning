"""Small evaluation harness with real retrieval calls and explicit release gate."""
import argparse
import json
import tempfile
import time
from pathlib import Path
from projects.reference import Store, ROOT

def run(split='dev'):
    cases=[json.loads(line) for line in (ROOT/'datasets/evals.jsonl').read_text().splitlines() if line.strip()]
    cases=[case for case in cases if case['split']==split]
    results=[]
    with tempfile.TemporaryDirectory() as folder:
        store=Store(Path(folder)/'eval.db'); store.seed()
        for case in cases:
            start=time.perf_counter(); hits=store.search(case['tenant'],case['query'],3)
            ids=[hit['id'] for hit in hits]; relevant=set(case['relevant_ids'])
            recall=len(set(ids)&relevant)/len(relevant) if relevant else None
            correct=bool(recall==1) if relevant else not hits
            unauthorized=any(not (hit['public'] or hit['tenant']==case['tenant']) for hit in hits)
            results.append({'id':case['id'],'category':case['category'],'recall':recall,'correct':correct,'unauthorized':unauthorized,'milliseconds':(time.perf_counter()-start)*1000,'retrieved':ids})
    recall_values=[row['recall'] for row in results if row['recall'] is not None]
    mean_recall=sum(recall_values)/len(recall_values) if recall_values else None
    passed=bool(results) and all(row['correct'] and not row['unauthorized'] for row in results)
    return {'split':split,'cases':results,'mean_recall':mean_recall,'passed':passed,
            'limitation':'Nine authored smoke cases are not a production evaluation set; no generation-groundedness score is inferred.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--split',choices=['dev','holdout'],default='dev'); p.add_argument('--output'); a=p.parse_args()
    report=run(a.split); text=json.dumps(report,indent=2)
    if a.output: Path(a.output).write_text(text+'\n')
    print(text)
    raise SystemExit(0 if report['passed'] else 1)
