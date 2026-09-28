"""05a/05b: gradient checks, SGD/momentum, and controlled MLP/CNN experiments."""
import argparse
import copy
import json
import time
from pathlib import Path
import numpy as np

def xor_comparison(output,steps=3000):
    from projects.stage05.numpy_xor import loss_grad
    rng=np.random.default_rng(42);x=np.array([[0.,0.],[0.,1.],[1.,0.],[1.,1.]]);y=np.array([[0.],[1.],[1.],[0.]])
    initial=[rng.normal(0,.5,(2,8)),np.zeros(8),rng.normal(0,.5,(8,1)),np.zeros(1)]
    _,analytic=loss_grad(x,y,initial);coordinates=[(i,idx) for i,param in enumerate(initial) for idx in np.ndindex(param.shape)]
    chosen=rng.choice(len(coordinates),10,replace=False);errors=[]
    for choice in chosen:
        pi,idx=coordinates[choice];original=initial[pi][idx];h=1e-5
        initial[pi][idx]=original+h;plus=loss_grad(x,y,initial)[0]
        initial[pi][idx]=original-h;minus=loss_grad(x,y,initial)[0]
        initial[pi][idx]=original
        errors.append(abs((plus-minus)/(2*h)-analytic[pi][idx]))
    histories={}
    for name,momentum in [('sgd',0.),('momentum',.9)]:
        params=copy.deepcopy(initial);velocity=[np.zeros_like(p) for p in params];history=[]
        for _ in range(steps):
            loss,grad=loss_grad(x,y,params);history.append(loss)
            for p,v,g in zip(params,velocity,grad): v*=momentum;v+=g;p-=.05*v
        histories[name]=history
    plot_curves(histories,Path(output)/'xor.png','MSE')
    return {'gradient_entries_checked':10,'maximum_gradient_error':max(errors),'final_losses':{k:v[-1] for k,v in histories.items()}}

def plot_curves(histories,path,ylabel):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots()
    for name,values in histories.items():ax.plot(values,label=name)
    ax.set(xlabel='Update/epoch',ylabel=ylabel);ax.legend();fig.tight_layout();fig.savefig(path);plt.close(fig)

def digits_comparison(output,epochs=8):
    import torch
    from torch import nn
    from torch.utils.data import DataLoader,TensorDataset
    from sklearn.datasets import load_digits
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report
    torch.set_num_threads(1);data=load_digits();x=torch.tensor(data.images[:,None]/16.,dtype=torch.float32);y=torch.tensor(data.target)
    train,test=train_test_split(np.arange(len(y)),test_size=.2,stratify=data.target,random_state=42)
    train,val=train_test_split(train,test_size=.2,stratify=data.target[train],random_state=42)
    specs=[('mlp',.01,0.,False),('cnn',.01,0.,False),('cnn',.001,0.,False),('cnn',.01,.2,False),('cnn',.01,0.,True)]
    reports=[];states={}
    for architecture,lr,dropout,normalize in specs:
        torch.manual_seed(42)
        if architecture=='mlp':model=nn.Sequential(nn.Flatten(),nn.Linear(64,64),nn.ReLU(),nn.Dropout(dropout),nn.Linear(64,10))
        else:model=nn.Sequential(nn.Conv2d(1,8,3,padding=1),nn.BatchNorm2d(8) if normalize else nn.Identity(),nn.ReLU(),nn.MaxPool2d(2),nn.Flatten(),nn.Dropout(dropout),nn.Linear(128,10))
        opt=torch.optim.AdamW(model.parameters(),lr=lr);loader=DataLoader(TensorDataset(x[train],y[train]),batch_size=64,shuffle=True,generator=torch.Generator().manual_seed(42))
        best=float('inf');saved=None;history=[];started=time.perf_counter()
        for epoch in range(epochs):
            model.train();total=0.
            for xb,yb in loader:
                opt.zero_grad();loss=nn.functional.cross_entropy(model(xb),yb);loss.backward();opt.step();total+=loss.item()*len(yb)
            model.eval()
            with torch.no_grad():validation=nn.functional.cross_entropy(model(x[val]),y[val]).item()
            history.append({'training':total/len(train),'validation':validation})
            if validation<best:best=validation;saved=copy.deepcopy(model.state_dict())
        key=f'{architecture}-lr{lr}-drop{dropout}-norm{normalize}';model.load_state_dict(saved)
        states[key]=model
        reports.append(dict(name=key,architecture=architecture,best_validation_loss=best,epochs=epochs,parameters=sum(p.numel() for p in model.parameters()),seconds=time.perf_counter()-started,history=history))
    # Only the validation-selected configuration reaches test; alternatives remain development experiments.
    selected=min(reports,key=lambda r:r['best_validation_loss']);model=states[selected['name']].eval()
    with torch.no_grad():pred=model(x[test]).argmax(1).numpy()
    torch.save(model.state_dict(),Path(output)/'best_weights.pt')
    plot_curves({r['name']:[h['validation'] for h in r['history']] for r in reports},Path(output)/'validation.png','Cross entropy')
    return {'experiments':reports,'selected':selected['name'],'test_report':classification_report(y[test].numpy(),pred,output_dict=True,zero_division=0),
            'errors':[{'dataset_index':int(i),'expected':int(actual),'predicted':int(p)} for i,actual,p in zip(test,y[test],pred) if actual!=p],
            'split_seed':42,'model_card':'8x8 handwritten digits only. CPU training. Scaling fixed to /16. No claim about other images. Selected on validation cross entropy, not test accuracy.'}

def run(output,epochs=8):
    out=Path(output);out.mkdir(parents=True,exist_ok=True)
    result={'xor':xor_comparison(out),'digits':digits_comparison(out,epochs)}
    (out/'report.json').write_text(json.dumps(result,indent=2)+'\n');return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='work/reference_answers/stage05');p.add_argument('--epochs',type=int,default=8);a=p.parse_args()
    if a.epochs<1:p.error('positive epochs required')
    print(json.dumps(run(a.output,a.epochs),indent=2))
