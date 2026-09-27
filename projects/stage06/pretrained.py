"""Real pretrained sequence-classification + LoRA path; downloads are explicit.
Example: python -m projects.stage06.pretrained --model distilbert/distilbert-base-uncased --revision <commit>
Use --offline-smoke to test adapters on a random tiny model without a download.
"""
import argparse
import json
import torch
from torch.utils.data import DataLoader
from transformers import AutoTokenizer, AutoModelForSequenceClassification, BertConfig, BertForSequenceClassification
from peft import LoraConfig, TaskType, get_peft_model

def offline_smoke():
    torch.manual_seed(42); torch.set_num_threads(1)
    base=BertForSequenceClassification(BertConfig(vocab_size=64,hidden_size=16,num_hidden_layers=1,num_attention_heads=2,intermediate_size=32,num_labels=3))
    model=get_peft_model(base,LoraConfig(task_type=TaskType.SEQ_CLS,r=4,lora_alpha=8,target_modules=['query','value']))
    optimizer=torch.optim.AdamW((p for p in model.parameters() if p.requires_grad),lr=.01)
    result=model(input_ids=torch.randint(0,64,(4,12)),attention_mask=torch.ones(4,12,dtype=torch.long),labels=torch.tensor([0,1,2,0]))
    result.loss.backward(); optimizer.step()
    return {'loss':result.loss.item(),'trainable_parameters':sum(p.numel() for p in model.parameters() if p.requires_grad),'mode':'random model adapter smoke test; not pretrained accuracy'}

def train(model_id,revision,epochs):
    import pandas as pd
    from pathlib import Path
    from sklearn.metrics import f1_score
    torch.manual_seed(42); torch.set_num_threads(1)
    data=pd.read_csv(Path(__file__).resolve().parents[2]/'datasets/tickets.csv')
    labels={label:i for i,label in enumerate(sorted(data.label.unique()))}
    tokenizer=AutoTokenizer.from_pretrained(model_id,revision=revision,trust_remote_code=False)
    base=AutoModelForSequenceClassification.from_pretrained(model_id,revision=revision,num_labels=3,trust_remote_code=False)
    # DistilBERT uses q_lin/v_lin; BERT uses query/value. Inspect a new architecture before adapting it.
    names={name.split('.')[-1] for name,_ in base.named_modules()}
    targets=['q_lin','v_lin'] if 'q_lin' in names else ['query','value']
    model=get_peft_model(base,LoraConfig(task_type=TaskType.SEQ_CLS,r=8,lora_alpha=16,target_modules=targets,lora_dropout=.05))
    optimizer=torch.optim.AdamW((p for p in model.parameters() if p.requires_grad),lr=5e-4)
    splits={name:data[data.split==name] for name in ('train','validation','test')}
    def encode(frame):
        batch=tokenizer(frame.text.tolist(),padding=True,truncation=True,max_length=128,return_tensors='pt')
        batch['labels']=torch.tensor([labels[label] for label in frame.label])
        return batch
    train_batch=encode(splits['train'])
    def score(frame):
        model.eval()
        with torch.no_grad(): pred=model(**encode(frame)).logits.argmax(-1).tolist()
        return f1_score([labels[label] for label in frame.label],pred,average='macro')
    baseline=score(splits['validation']); best=-1; best_state=None; history=[]
    import copy
    for epoch in range(epochs):
        model.train()
        order=torch.randperm(len(splits['train']))
        for ids in order.split(8):
            optimizer.zero_grad()
            loss=model(**{k:v[ids] for k,v in train_batch.items()}).loss
            loss.backward(); optimizer.step()
        val=score(splits['validation']); history.append(val)
        if val>best: best,best_state=val,copy.deepcopy(model.state_dict())
    model.load_state_dict(best_state)
    return {'model':model_id,'revision':revision,'validation_before':baseline,'validation_history':history,'test_macro_f1':score(splits['test']),
            'limitation':'The task classification head starts untrained; this small authored dataset is a mechanics exercise.'}

def main():
    p=argparse.ArgumentParser(); p.add_argument('--model'); p.add_argument('--revision'); p.add_argument('--epochs',type=int,default=3); p.add_argument('--offline-smoke',action='store_true'); a=p.parse_args()
    if a.offline_smoke: result=offline_smoke()
    else:
        if not a.model or not a.revision or a.epochs<1: p.error('Provide --model, immutable --revision, and positive --epochs, or use --offline-smoke')
        result=train(a.model,a.revision,a.epochs)
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
