"""04-P5: persist a fitted text pipeline and serve the identical trusted artifact."""
import argparse
import hashlib
import json
from pathlib import Path
import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from projects.reference import ROOT
from projects.stage04.api import Ticket

def save_pipeline(path):
    data=pd.read_csv(ROOT/'datasets/tickets.csv');train=data[data.split=='train']
    pipeline=make_pipeline(TfidfVectorizer(ngram_range=(1,2)),LogisticRegression(max_iter=500,random_state=42))
    pipeline.fit(train.text,train.label)
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    joblib.dump(pipeline,path)
    return pipeline

def create_app(trusted_artifact):
    # Pickle/joblib loading can execute code. This path is operator-controlled and trusted.
    path=Path(trusted_artifact);pipeline=joblib.load(path)
    version=hashlib.sha256(path.read_bytes()).hexdigest()
    app=FastAPI(title='Saved ticket pipeline answer')
    @app.post('/predict')
    def predict(ticket:Ticket):
        scores=pipeline.predict_proba([ticket.text])[0]
        return {'label':str(pipeline.classes_[scores.argmax()]),
                'scores':dict(zip(map(str,pipeline.classes_),map(float,scores))),
                'artifact_sha256':version,'scores_calibrated':False}
    return app

def run(output):
    out=Path(output);out.mkdir(parents=True,exist_ok=True);path=out/'ticket_pipeline.joblib'
    pipeline=save_pipeline(path);texts=['I cannot sign in to my account','Please refund the duplicate charge']
    expected=pipeline.predict(texts).tolist()
    with TestClient(create_app(path)) as client:
        observed=[client.post('/predict',json={'text':text}).json()['label'] for text in texts]
        invalid=client.post('/predict',json={'text':''}).status_code
    assert expected==observed and invalid==422
    report={'before_save':expected,'after_reload_via_http':observed,'invalid_status':invalid,
            'artifact_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'limitations':'Fixed logistic model for artifact mechanics; scores uncalibrated. Never load untrusted joblib files.'}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='work/reference_answers/stage04-artifact');a=p.parse_args()
    print(json.dumps(run(a.output),indent=2))
