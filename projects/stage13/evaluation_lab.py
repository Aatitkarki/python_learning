"""13a/13b: reference labels, paired uncertainty, slices, and regression gates."""
import argparse
import csv
import json
import random
import tempfile
from collections import defaultdict
from decimal import Decimal
from pathlib import Path
from projects.reference import ROOT,Store
from projects.stage07.retrieval_lab import chunks,rankings

def reference_cases():
    with (ROOT/'datasets/financials.csv').open() as handle:rows=list(csv.DictReader(handle))
    cases=[]
    templates={
        'revenue':['What was {c} revenue in {y}?','Report {c} sales for {y}.','How much annual revenue did {c} report for {y}?','Give the revenue figure in {c} fiscal {y} statement.'],
        'operating_margin':['Calculate {c} operating margin for {y}.','What share of {c} revenue was operating income in {y}?','Divide {c} operating income by revenue for {y}.'],
        'free_cash_flow':['What was {c} free cash flow in {y}?','Subtract {c} capital expenditures from operating cash flow for {y}.','How much cash remained after {c} capex in {y}?']}
    for row in rows:
        values={'revenue':row['revenue'],'operating_margin':str(Decimal(row['operating_income'])/Decimal(row['revenue'])),
                'free_cash_flow':str(Decimal(row['operating_cash_flow'])-Decimal(row['capex']))}
        # Ten questions per source family: 40 development and 20 holdout, no source overlap.
        for i,field in enumerate(['revenue']*4+['operating_margin']*3+['free_cash_flow']*3):
            cases.append({'id':f"{row['source_id']}-{i}",'question':templates[field][i if i<4 else i-4 if i<7 else i-7].format(c=row['company'],y=row['year']),
                          'company':row['company'],'year':int(row['year']),'field':field,'expected':values[field],
                          'source_id':row['source_id'],'group':row['source_id'],'tenant':'A','category':field,
                          'split':'holdout' if int(row['year'])==2025 else 'dev','label_status':'deterministic fictional reference; learner human review pending'})
    return cases

def paired_interval(baseline,candidate,groups=None,repeats=2000,seed=42):
    if not baseline or len(baseline)!=len(candidate):raise ValueError('Paired nonempty observations required')
    if repeats<1:raise ValueError('Positive repeats required')
    groups=list(range(len(baseline))) if groups is None else groups
    if len(groups)!=len(baseline):raise ValueError('Group mismatch')
    grouped=defaultdict(list)
    for a,b,g in zip(baseline,candidate,groups):grouped[g].append(b-a)
    keys=list(grouped);rng=random.Random(seed);samples=[]
    for _ in range(repeats):
        values=[v for key in rng.choices(keys,k=len(keys)) for v in grouped[key]]
        samples.append(sum(values)/len(values))
    samples.sort()
    return {'delta':sum(b-a for a,b in zip(baseline,candidate))/len(baseline),'ci95':[samples[int(.025*repeats)],samples[min(repeats-1,int(.975*repeats))]],'resampling_unit':'source group' if len(keys)<len(baseline) else 'case','groups':len(keys)}

def release_gate(report):
    return bool(report['cases']) and all(c['correct'] and c['citation_correct'] and c['authorized'] for c in report['cases'])

def evaluate_numeric(cases,store):
    results=[]
    for case in cases:
        result=store.compare(case['tenant'],[case['company']],[case['year']])[0]
        results.append({'id':case['id'],'category':case['category'],'correct':Decimal(result[case['field']])==Decimal(case['expected']),
                        'citation_correct':result['source_id']==case['source_id'],'authorized':case['tenant']=='A'})
    slices={category:{'n':sum(c['category']==category for c in results),'accuracy':sum(c['correct'] for c in results if c['category']==category)/sum(c['category']==category for c in results)} for category in {c['category'] for c in results}}
    return {'cases':results,'slices':slices,'mode':'Structured numerical tool evaluation, not natural-language parsing or generative groundedness.'}

def compare_chunking():
    docs=json.loads((ROOT/'datasets/documents.json').read_text())
    cases=[json.loads(line) for line in (ROOT/'datasets/evals.jsonl').read_text().splitlines() if json.loads(line)['split']=='dev']
    scores={}
    for size in [8,40]:
        index=[c for d in docs for c in chunks(d,size,min(3,size-1))];values=[]
        for case in cases:
            hits=rankings(case['query'],index,case['tenant'])['keyword'];ids={h['document_id'] for h in hits};relevant=set(case['relevant_ids'])
            values.append(len(ids&relevant)/len(relevant) if relevant else float(not hits))
        scores[str(size)]=values
    return {'per_case_recall':scores,'comparison':paired_interval(scores['8'],scores['40'],[c['id'] for c in cases]),'labels_unchanged':True}

def run(output,split='dev'):
    out=Path(output);out.mkdir(parents=True,exist_ok=True);cases=reference_cases()
    (out/'reference-cases.jsonl').write_text(''.join(json.dumps(c)+'\n' for c in cases))
    selected=[c for c in cases if c['split']==split]
    with tempfile.TemporaryDirectory() as folder:
        store=Store(Path(folder)/'eval.db');store.seed();report=evaluate_numeric(selected,store)
    report.update(split=split,passed=release_gate(report),retrieval_experiment=compare_chunking(),
                  caveat='60 template-based cases have only six source families. They are a complete worked labeling example, not 60 independent human-reviewed questions or a completed 100–500-case capstone corpus.')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='work/reference_answers/stage13');p.add_argument('--split',choices=['dev','holdout'],default='dev');a=p.parse_args();report=run(a.output,a.split);print(json.dumps(report,indent=2));raise SystemExit(not report['passed'])
