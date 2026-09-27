"""Small causal character transformer; no model downloads or GPU required."""
import json
from pathlib import Path
import torch
from torch import nn

class TinyLM(nn.Module):
    def __init__(self, vocab, width=32, context=32):
        super().__init__()
        self.context = context
        self.token = nn.Embedding(vocab,width)
        self.position = nn.Embedding(context,width)
        self.attention = nn.MultiheadAttention(width,4,batch_first=True)
        self.norm1, self.norm2 = nn.LayerNorm(width), nn.LayerNorm(width)
        self.ff = nn.Sequential(nn.Linear(width,4*width),nn.GELU(),nn.Linear(4*width,width))
        self.head = nn.Linear(width,vocab)
    def forward(self, ids):
        n = ids.shape[1]
        x = self.token(ids)+self.position(torch.arange(n,device=ids.device))
        mask = torch.triu(torch.ones(n,n,dtype=torch.bool,device=ids.device),1)
        a,_ = self.attention(x,x,x,attn_mask=mask,need_weights=False)
        x = self.norm1(x+a)
        return self.head(self.norm2(x+self.ff(x)))

def run(steps=150):
    torch.manual_seed(42); torch.set_num_threads(1)
    text=(Path(__file__).resolve().parents[2]/'datasets/tiny_corpus.txt').read_text()
    split=int(.8*len(text)); train_text, val_text=text[:split],text[split:]
    chars=sorted(set(train_text)); stoi={c:i for i,c in enumerate(chars)}
    train=torch.tensor([stoi[c] for c in train_text]); val=torch.tensor([stoi[c] for c in val_text])
    model=TinyLM(len(chars)); opt=torch.optim.AdamW(model.parameters(),lr=.003)
    def batch(data):
        starts=torch.randint(0,len(data)-model.context-1,(16,))
        x=torch.stack([data[i:i+model.context] for i in starts])
        y=torch.stack([data[i+1:i+model.context+1] for i in starts])
        return x,y
    losses=[]
    model.train()
    for _ in range(steps):
        x,y=batch(train); opt.zero_grad()
        loss=nn.functional.cross_entropy(model(x).reshape(-1,len(chars)),y.reshape(-1))
        loss.backward(); nn.utils.clip_grad_norm_(model.parameters(),1.); opt.step()
        losses.append(loss.item())
    model.eval()
    with torch.no_grad():
        x,y=batch(val)
        validation=nn.functional.cross_entropy(model(x).reshape(-1,len(chars)),y.reshape(-1)).item()
        ids=torch.tensor([[stoi['A']]])
        for _ in range(100):
            probs=torch.softmax(model(ids[:,-model.context:])[:,-1]/.8,dim=-1)
            ids=torch.cat([ids,torch.multinomial(probs,1)],dim=1)
    return {'initial_loss': losses[0], 'final_train_loss': losses[-1], 'validation_loss': validation,
            'generated': ''.join(chars[i] for i in ids[0].tolist()),
            'limitation': 'The corpus repeats authored sentences. Held-out loss checks mechanics, not linguistic generalization.'}

if __name__ == '__main__': print(json.dumps(run(),indent=2))
