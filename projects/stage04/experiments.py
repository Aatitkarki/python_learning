"""04a/04b: regression comparison, clustering/PCA, and held-out error records."""
import argparse
import json
from pathlib import Path
import numpy as np
from sklearn.datasets import make_regression, make_blobs, make_moons
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor,GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score,adjusted_rand_score,silhouette_score
from sklearn.cluster import KMeans,DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def regression():
    x,y=make_regression(n_samples=500,n_features=5,n_informative=3,noise=15,random_state=42)
    train,test=train_test_split(np.arange(len(y)),test_size=.2,random_state=42)
    train,val=train_test_split(train,test_size=.25,random_state=42)
    models={'mean':DummyRegressor(),'linear':LinearRegression(),'tree':DecisionTreeRegressor(max_depth=5,random_state=42),
            'forest':RandomForestRegressor(n_estimators=60,max_depth=8,random_state=42),
            'boosting':GradientBoostingRegressor(random_state=42)}
    def metrics(actual,predicted): return dict(mae=float(mean_absolute_error(actual,predicted)),rmse=float(np.sqrt(mean_squared_error(actual,predicted))),r2=float(r2_score(actual,predicted)))
    validation={}
    for name,model in models.items():
        model.fit(x[train],y[train]);validation[name]=metrics(y[val],model.predict(x[val]))
    selected=min(validation,key=lambda name:validation[name]['mae'])
    winner=models[selected].fit(x[np.r_[train,val]],y[np.r_[train,val]])
    return {'validation':validation,'selected':selected,'final_test':metrics(y[test],winner.predict(x[test])),
            'units':'Synthetic demand units; data is a controlled linear relationship plus noise.'}

def clustering(output):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    results=[];fig,axes=plt.subplots(2,2,figsize=(9,7))
    for row,(name,raw) in enumerate([('blobs',make_blobs(n_samples=300,centers=2,random_state=42)),('moons',make_moons(n_samples=300,noise=.06,random_state=42))]):
        x,truth=raw;z=StandardScaler().fit_transform(x)
        for col,(model_name,model) in enumerate([('kmeans',KMeans(n_clusters=2,n_init=10,random_state=42)),('dbscan',DBSCAN(eps=.25,min_samples=5))]):
            labels=model.fit_predict(z);unique=set(labels)
            results.append({'dataset':name,'model':model_name,'ari_external_diagnostic':float(adjusted_rand_score(truth,labels)),
                            'silhouette':float(silhouette_score(z,labels)) if 1<len(unique)<len(z) else None,'noise_count':int(sum(labels==-1))})
            axes[row,col].scatter(z[:,0],z[:,1],c=labels,s=10);axes[row,col].set(title=f'{name}: {model_name}',xlabel='standardized x',ylabel='standardized y')
    fig.tight_layout();fig.savefig(Path(output)/'clusters.png');plt.close(fig)
    pca=PCA(n_components=1).fit(z)
    return {'comparisons':results,'pca_explained_variance':pca.explained_variance_ratio_.tolist(),
            'interpretation':'ARI uses known synthetic labels only for diagnosis. Do not tune repeatedly on labels and claim wholly unsupervised selection.'}

def novel_tickets():
    # New authored cases, not independently human-collected customer evidence.
    examples={
      'access':['My reset link expires before I can use it','Lost access after replacing my authenticator phone','The account is disabled and I cannot sign in','How can I recover a forgotten password','No verification email for my new account','Login keeps saying invalid credentials','I am locked out after too many sign in attempts'],
      'billing':['The renewal receipt shows two identical payments','Please reverse a charge for a cancelled plan','Where can I change the card for billing','The amount on the invoice includes an extra seat','Can I download my payment receipt','A subscription refund has not arrived','The card was declined during payment'],
      'technical':['Exporting a large report makes the page freeze','Image upload fails with a server error','The dashboard graph is empty after refreshing','The app crashes whenever a CSV is opened','A report download finishes with a broken file','Search spins forever without displaying results','The document preview is blank on the dashboard']}
    return [{'id':f'new-{label}-{i}','text':text,'label':label,'provenance':'new authored reference case; human review required'} for label,texts in examples.items() for i,text in enumerate(texts)]

def ticket_errors():
    import pandas as pd
    from sklearn.pipeline import make_pipeline
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from projects.reference import ROOT
    data=pd.read_csv(ROOT/'datasets/tickets.csv');train=data[data.split=='train']
    model=make_pipeline(TfidfVectorizer(),LogisticRegression(max_iter=500,random_state=42)).fit(train.text,train.label)
    rows=novel_tickets();predictions=model.predict([r['text'] for r in rows])
    for row,prediction in zip(rows,predictions):
        row['predicted']=str(prediction);row['correct']=row['label']==prediction
        row['review_category']='correct' if row['correct'] else 'inspect vocabulary, intent overlap, and annotation ambiguity'
    return rows

def run(output):
    out=Path(output);out.mkdir(parents=True,exist_ok=True)
    result={'regression':regression(),'clustering':clustering(out),'new_ticket_review':ticket_errors()}
    (out/'report.json').write_text(json.dumps(result,indent=2)+'\n');return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='work/reference_answers/stage04');a=p.parse_args();print(json.dumps(run(a.output),indent=2))
