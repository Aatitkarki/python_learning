"""06a/06c: decoding, attention plots, real local BPE, and evidence-bound extraction."""
import argparse
import json
import re
from decimal import Decimal
from pathlib import Path
import numpy as np

def probabilities(logits,temperature=1.,top_k=None,top_p=1.):
    values=np.asarray(logits,dtype=float)
    if values.ndim!=1 or not len(values) or not np.isfinite(values).all() or temperature<=0 or not 0<top_p<=1:
        raise ValueError('Invalid distribution inputs')
    values=values/temperature
    if top_k is not None:
        if not 1<=top_k<=len(values):raise ValueError('Invalid k')
        keep=np.argsort(-values,kind='stable')[:top_k];masked=np.full_like(values,-np.inf);masked[keep]=values[keep];values=masked
    weights=np.exp(values-np.max(values));weights/=weights.sum()
    order=np.argsort(-weights,kind='stable');sorted_weights=weights[order]
    remove=np.cumsum(sorted_weights)-sorted_weights>=top_p
    weights[order[remove]]=0
    return weights/weights.sum()

def entropy(p):
    p=np.asarray(p);p=p[p>0]
    return float(-np.sum(p*np.log(p)))

def causal_attention(q,k,v):
    scores=q@k.T/np.sqrt(q.shape[-1]);scores[np.triu_indices(len(q),1)]=-np.inf
    weights=np.exp(scores-np.max(scores,axis=1,keepdims=True));weights/=weights.sum(axis=1,keepdims=True)
    return weights@v,weights

def extract_revenue(text):
    """Narrow grammar: COMPANY revenue was $NUMBER million/billion. Unknown outside it."""
    pattern=r'(?P<company>[A-Z][A-Za-z ]*?) revenue was \$(?P<number>\d+(?:\.\d+)?) (?P<scale>million|billion)\b'
    matches=list(re.finditer(pattern,text))
    if len(matches)!=1:return {'status':'unknown','reason':'Need exactly one supported revenue statement'}
    match=matches[0];amount=Decimal(match['number'])*{'million':Decimal('1e6'),'billion':Decimal('1e9')}[match['scale']]
    return {'status':'supported','company':match['company'],'revenue':str(amount.quantize(Decimal('1'))),'currency':'USD',
            'quote':match.group(),'start':match.start(),'end':match.end(),
            'convention':'Dollar sign interpreted as USD only for this fictional USD corpus.'}

def run(output):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from tokenizers import Tokenizer,models,pre_tokenizers,trainers
    from projects.reference import ROOT
    out=Path(output);out.mkdir(parents=True,exist_ok=True)
    q=np.eye(4);v=np.arange(12,dtype=float).reshape(4,3)
    result,weights=causal_attention(q,q,v);changed=v.copy();changed[-1]+=100
    assert np.allclose(result[:-1],causal_attention(q,q,changed)[0][:-1])
    fig,ax=plt.subplots();fig.colorbar(ax.imshow(weights,vmin=0,vmax=1),ax=ax);ax.set(xlabel='Key position',ylabel='Query position',title='Causal attention');fig.savefig(out/'attention.png');plt.close(fig)
    tokenizer=Tokenizer(models.BPE(unk_token='[UNK]'));tokenizer.pre_tokenizer=pre_tokenizers.Whitespace()
    tokenizer.train_from_iterator([(ROOT/'datasets/tiny_corpus.txt').read_text()],trainers.BpeTrainer(vocab_size=80,special_tokens=['[UNK]','[PAD]','[BOS]','[EOS]']))
    tokenizer.save(str(out/'tokenizer.json'));encoded=tokenizer.encode('A careful engineer checks evidence')
    w=np.array([-.7,.1,1.]);scale=np.max(np.abs(w))/127;codes=np.round(w/scale).astype(np.int8)
    report={'decoding':{name:{'probabilities':p.tolist(),'entropy':entropy(p)} for name,p in [
        ('temperature_1',probabilities([1,2,3,4])),('temperature_point2',probabilities([1,2,3,4],.2)),
        ('top_k_2',probabilities([1,2,3,4],top_k=2)),('top_p_point7',probabilities([1,2,3,4],top_p=.7))]},
        'bpe':{'ids':encoded.ids,'tokens':encoded.tokens,'vocabulary':tokenizer.get_vocab(),'special_tokens':'UNK handles unknowns; PAD batches sequences; BOS/EOS mark boundaries when explicitly added.'},
        'extraction':extract_revenue('Aurora revenue was $1.2 billion.'),'quantization_max_error':float(np.max(np.abs(codes.astype(float)*scale-w))),
        'lora':{'dense_parameters':1000*1000,'rank8_parameters':8*(1000+1000)}}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='work/reference_answers/stage06-attention');a=p.parse_args();print(json.dumps(run(a.output),indent=2))
