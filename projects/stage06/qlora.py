"""Optional GPU answer: actual 4-bit base + trainable LoRA, selected on validation.
Run only with a chosen supported model, immutable revision, and requirements/qlora.txt.
Not executed in CPU-only course validation.
"""
import argparse
import json
import time
from pathlib import Path

def train(model_id,revision,output,epochs=3):
    import torch
    if not torch.cuda.is_available():raise RuntimeError('This reference configuration requires a supported CUDA GPU')
    import pandas as pd
    from transformers import AutoTokenizer,AutoModelForSequenceClassification,BitsAndBytesConfig
    from peft import LoraConfig,TaskType,get_peft_model,prepare_model_for_kbit_training,get_peft_model_state_dict,set_peft_model_state_dict
    from sklearn.metrics import f1_score
    from projects.reference import ROOT
    torch.manual_seed(42);torch.cuda.reset_peak_memory_stats();started=time.perf_counter()
    dtype=torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    quant=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_use_double_quant=True,bnb_4bit_compute_dtype=dtype)
    tokenizer=AutoTokenizer.from_pretrained(model_id,revision=revision,trust_remote_code=False)
    if tokenizer.pad_token is None:
        if tokenizer.eos_token is None:raise ValueError('Select a tokenizer with a pad/eos token')
        tokenizer.pad_token=tokenizer.eos_token
    base=AutoModelForSequenceClassification.from_pretrained(model_id,revision=revision,num_labels=3,quantization_config=quant,device_map={'':0},trust_remote_code=False)
    base.config.pad_token_id=tokenizer.pad_token_id
    if hasattr(base.config,'use_cache'):base.config.use_cache=False
    base=prepare_model_for_kbit_training(base)
    model=get_peft_model(base,LoraConfig(task_type=TaskType.SEQ_CLS,r=8,lora_alpha=16,target_modules='all-linear',lora_dropout=.05))
    data=pd.read_csv(ROOT/'datasets/tickets.csv');labels={label:i for i,label in enumerate(sorted(data.label.unique()))}
    def encoded(frame):
        batch=tokenizer(frame.text.tolist(),padding=True,truncation=True,max_length=128,return_tensors='pt')
        batch['labels']=torch.tensor([labels[label] for label in frame.label])
        return {k:v.to('cuda') for k,v in batch.items()}
    def score(frame):
        model.eval()
        with torch.no_grad():pred=model(**encoded(frame)).logits.argmax(-1).cpu().tolist()
        return float(f1_score([labels[label] for label in frame.label],pred,average='macro'))
    splits={name:data[data.split==name] for name in ['train','validation','test']}
    before=score(splits['validation']);optimizer=torch.optim.AdamW([p for p in model.parameters() if p.requires_grad],lr=5e-4)
    best=-1;best_state=None;history=[]
    for epoch in range(epochs):
        model.train();order=torch.randperm(len(splits['train'])).tolist()
        for start in range(0,len(order),4):
            batch=splits['train'].iloc[order[start:start+4]];optimizer.zero_grad();loss=model(**encoded(batch)).loss;loss.backward();optimizer.step()
        validation=score(splits['validation']);history.append(validation)
        if validation>best:
            best=validation;best_state={k:v.detach().cpu().clone() for k,v in get_peft_model_state_dict(model).items()}
    set_peft_model_state_dict(model,best_state)
    out=Path(output);out.mkdir(parents=True,exist_ok=True);model.save_pretrained(out/'adapter');tokenizer.save_pretrained(out/'tokenizer')
    result={'model':model_id,'revision':revision,'validation_before':before,'validation_history':history,'test_macro_f1':score(splits['test']),
            'seconds':time.perf_counter()-started,'peak_cuda_bytes':torch.cuda.max_memory_allocated(),
            'trainable_parameters':sum(p.numel() for p in model.parameters() if p.requires_grad),
            'limits':'Tiny authored data and initially untrained task head; not real-world accuracy. Verify model license and hardware support before running.'}
    (out/'report.json').write_text(json.dumps(result,indent=2)+'\n');return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--model',required=True);p.add_argument('--revision',required=True);p.add_argument('--epochs',type=int,default=3);p.add_argument('--output',default='work/reference_answers/qlora');a=p.parse_args()
    if a.epochs<1:p.error('Positive epochs required')
    print(json.dumps(train(a.model,a.revision,a.output,a.epochs),indent=2))
