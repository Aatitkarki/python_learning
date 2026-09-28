"""06b: one/two-block causal models and actual per-layer key/value caching."""
import argparse
import json
import math
from pathlib import Path
import torch
from torch import nn

class Block(nn.Module):
    def __init__(self,width=24,heads=3):
        super().__init__();self.heads=heads;self.dim=width//heads
        if width%heads:raise ValueError('Width must divide into heads')
        self.qkv=nn.Linear(width,3*width);self.out=nn.Linear(width,width)
        self.norm1=nn.LayerNorm(width);self.norm2=nn.LayerNorm(width)
        self.ff=nn.Sequential(nn.Linear(width,4*width),nn.GELU(),nn.Linear(4*width,width))
    def forward(self,x,cache=None):
        batch,length,width=x.shape
        q,k,v=self.qkv(x).chunk(3,dim=-1)
        reshape=lambda z:z.reshape(batch,length,self.heads,self.dim).transpose(1,2)
        q,k,v=map(reshape,(q,k,v));past=0
        if cache is not None:
            past=cache[0].shape[2];k=torch.cat([cache[0],k],2);v=torch.cat([cache[1],v],2)
        scores=q@k.transpose(-2,-1)/math.sqrt(self.dim)
        future=torch.arange(k.shape[2],device=x.device)[None,:] > past+torch.arange(length,device=x.device)[:,None]
        scores=scores.masked_fill(future,-torch.inf)
        attended=(scores.softmax(-1)@v).transpose(1,2).reshape(batch,length,width)
        x=self.norm1(x+self.out(attended));x=self.norm2(x+self.ff(x))
        return x,(k,v)

class CachedLM(nn.Module):
    def __init__(self,vocab,blocks=2,width=24,context=128):
        super().__init__();self.context=context
        self.token=nn.Embedding(vocab,width);self.position=nn.Embedding(context,width)
        self.blocks=nn.ModuleList([Block(width) for _ in range(blocks)]);self.head=nn.Linear(width,vocab)
    def forward(self,ids,cache=None):
        cache=cache or [None]*len(self.blocks)
        if len(cache)!=len(self.blocks):raise ValueError('Cache layer mismatch')
        past=0 if cache[0] is None else cache[0][0].shape[2]
        if past+ids.shape[1]>self.context:raise ValueError('Context exceeded; recompute an explicitly cropped context')
        x=self.token(ids)+self.position(torch.arange(past,past+ids.shape[1],device=ids.device));updated=[]
        for block,old in zip(self.blocks,cache):x,new=block(x,old);updated.append(new)
        return self.head(x),updated

def cache_agreement(model,ids):
    model.eval()
    with torch.no_grad():
        full,_=model(ids);cache=None;steps=[]
        for i in range(ids.shape[1]):
            logits,cache=model(ids[:,i:i+1],cache);steps.append(logits)
    return float((full-torch.cat(steps,dim=1)).abs().max())

def run(output,steps=100):
    from projects.reference import ROOT
    torch.set_num_threads(1);text=(ROOT/'datasets/tiny_corpus.txt').read_text();split=int(.8*len(text))
    chars=sorted(set(text[:split]));mapping={c:i for i,c in enumerate(chars)}
    train=torch.tensor([mapping[c] for c in text[:split]]);val=torch.tensor([mapping[c] for c in text[split:]])
    reports=[]
    for blocks in [1,2]:
        torch.manual_seed(42);model=CachedLM(len(chars),blocks=blocks);optimizer=torch.optim.AdamW(model.parameters(),lr=.003)
        generator=torch.Generator().manual_seed(99);losses=[]
        for _ in range(steps):
            starts=torch.randint(0,len(train)-25,(8,),generator=generator)
            x=torch.stack([train[i:i+24] for i in starts]);y=torch.stack([train[i+1:i+25] for i in starts])
            optimizer.zero_grad();logits,_=model(x);loss=nn.functional.cross_entropy(logits.reshape(-1,len(chars)),y.reshape(-1));loss.backward();optimizer.step();losses.append(loss.item())
        model.eval()
        with torch.no_grad():
            x=val[:240].reshape(10,24);y=val[1:241].reshape(10,24)
            validation=nn.functional.cross_entropy(model(x)[0].reshape(-1,len(chars)),y.reshape(-1)).item()
            ids=torch.tensor([[mapping['A']]]);cache=None;generated=ids.tolist()[0]
            for _ in range(40):
                logits,cache=model(ids,cache);ids=logits[:,-1].argmax(-1,keepdim=True);generated.append(int(ids[0,0]))
        reports.append({'blocks':blocks,'initial_loss':losses[0],'final_train_loss':losses[-1],'validation_loss':validation,
                        'cache_max_error':cache_agreement(model,val[:16].reshape(1,-1)),'generated':''.join(chars[i] for i in generated)})
    out=Path(output);out.mkdir(parents=True,exist_ok=True);(out/'report.json').write_text(json.dumps(reports,indent=2)+'\n');return reports

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='work/reference_answers/stage06-cache');p.add_argument('--steps',type=int,default=100);a=p.parse_args();print(json.dumps(run(a.output,a.steps),indent=2))
