"""07a: versioned chunks, BM25, vector ranking, RRF, and evaluated reranking.
Default vector/reranker are labeled offline baselines. Optional models are explicit.
"""
import argparse
import hashlib
import json
import math
import re
from collections import Counter
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from projects.reference import ROOT

def tokens(text):return re.findall(r'[a-z0-9]+',text.lower())

def chunks(document,size=40,overlap=8):
    if not 0<=overlap<size:raise ValueError('Invalid chunk bounds')
    text=document['text'];words=list(re.finditer(r'\S+',text));digest=hashlib.sha256(text.encode()).hexdigest();out=[]
    for start in range(0,len(words),size-overlap):
        end=min(start+size,len(words));left,right=words[start].start(),words[end-1].end()
        out.append({**document,'id':f"{document['tenant']}:{document['id']}:{digest[:12]}:{left}",'document_id':document['id'],
                    'text':text[left:right],'start':left,'end':right,'sha256':digest,'parser_version':'whitespace-offsets-v1'})
        if end==len(words):break
    return out

def bm25(query,documents,k1=1.5,b=.75):
    counts=[Counter(tokens(d['text'])) for d in documents];lengths=[sum(c.values()) for c in counts];average=sum(lengths)/len(lengths) if lengths else 1
    scores=np.zeros(len(counts))
    for term in set(tokens(query)):
        df=sum(term in c for c in counts);idf=math.log(1+(len(counts)-df+.5)/(df+.5))
        for i,count in enumerate(counts):
            f=count[term];den=f+k1*(1-b+b*lengths[i]/average) if average else 1
            scores[i]+=idf*f*(k1+1)/den
    return scores

def rankings(query,documents,tenant,embedder=None,reranker=None,k=3):
    allowed=[d for d in documents if (d.get('public') or d['tenant']==tenant) and tokens(d['text'])]
    if not allowed:return {mode:[] for mode in ['keyword','vector','hybrid','reranked']}
    lexical=bm25(query,allowed)
    if embedder is None:
        vectorizer=TfidfVectorizer(analyzer=tokens);matrix=vectorizer.fit_transform([d['text'] for d in allowed]);vector=(matrix@vectorizer.transform([query]).T).toarray().ravel()
    else:
        matrix=embedder.encode([d['text'] for d in allowed],normalize_embeddings=True);vector=matrix@embedder.encode(query,normalize_embeddings=True)
    order=lambda scores:[int(i) for i in sorted(range(len(scores)),key=lambda i:(-scores[i],allowed[i]['id'])) if scores[i]>0]
    keyword,semantic=order(lexical),order(vector);fusion={}
    for ranking in [keyword,semantic]:
        for rank,i in enumerate(ranking,1):fusion[i]=fusion.get(i,0)+1/(60+rank)
    hybrid=sorted(fusion,key=lambda i:(-fusion[i],allowed[i]['id']))[:20]
    if reranker is None:
        # Explicit token-coverage baseline, not a claimed neural reranker.
        q=set(tokens(query));scores=[len(q&set(tokens(allowed[i]['text'])))/max(1,len(q)) for i in hybrid]
    else:scores=reranker.predict([(query,allowed[i]['text']) for i in hybrid])
    reranked=[i for score,i in sorted(zip(scores,hybrid),key=lambda pair:(-pair[0],allowed[pair[1]]['id']))]
    return {name:[allowed[i] for i in ids[:k]] for name,ids in [('keyword',keyword),('vector',semantic),('hybrid',hybrid),('reranked',reranked)]}

def run(output,embedder=None,reranker=None):
    docs=json.loads((ROOT/'datasets/documents.json').read_text());index=[c for d in docs for c in chunks(d)]
    cases=[json.loads(line) for line in (ROOT/'datasets/evals.jsonl').read_text().splitlines() if json.loads(line)['split']=='dev']
    result=[]
    for case in cases:
        modes=rankings(case['query'],index,case['tenant'],embedder,reranker)
        for mode,hits in modes.items():
            ids=[d['document_id'] for d in hits];relevant=set(case['relevant_ids'])
            result.append({'id':case['id'],'mode':mode,'recall':len(set(ids)&relevant)/len(relevant) if relevant else None,
                           'mrr':next((1/rank for rank,id in enumerate(ids,1) if id in relevant),0),'retrieved':ids})
    out=Path(output);out.mkdir(parents=True,exist_ok=True)
    report={'vector_model':'selected sentence-transformer' if embedder else 'TF-IDF offline baseline',
            'reranker':'selected cross-encoder' if reranker else 'token coverage offline baseline','results':result}
    (out/'chunks.json').write_text(json.dumps(index,indent=2)+'\n');(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='work/reference_answers/stage07');p.add_argument('--model');p.add_argument('--revision');p.add_argument('--reranker');p.add_argument('--reranker-revision');a=p.parse_args()
    embedder=ranker=None
    if a.model:
        if not a.revision:p.error('Pin --revision for the embedding model')
        from sentence_transformers import SentenceTransformer
        embedder=SentenceTransformer(a.model,revision=a.revision,trust_remote_code=False)
    if a.reranker:
        if not a.reranker_revision:p.error('Pin --reranker-revision')
        from sentence_transformers import CrossEncoder
        ranker=CrossEncoder(a.reranker,revision=a.reranker_revision,trust_remote_code=False)
    print(json.dumps(run(a.output,embedder,ranker),indent=2))
