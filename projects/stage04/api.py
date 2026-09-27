"""Local classifier API. Run: python -m uvicorn projects.stage04.api:app --host 127.0.0.1 --port 8001.
This early-stage demo has no authentication; bind only to localhost. Later stages add identity.
"""
from pathlib import Path
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field, ConfigDict
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

class Ticket(BaseModel):
    model_config=ConfigDict(extra='forbid')
    text: str=Field(min_length=1,max_length=4000,pattern=r'.*\S.*')

def create_app():
    data=pd.read_csv(Path(__file__).resolve().parents[2]/'datasets/tickets.csv')
    train=data[data.split=='train']
    model=make_pipeline(TfidfVectorizer(ngram_range=(1,2)),LogisticRegression(max_iter=500,random_state=42))
    model.fit(train.text,train.label)
    app=FastAPI(title='Learning ticket classifier')
    @app.post('/predict')
    def predict(ticket:Ticket):
        scores=model.predict_proba([ticket.text])[0]
        return {'label':str(model.classes_[scores.argmax()]),
                'scores':{str(label):float(score) for label,score in zip(model.classes_,scores)},
                'model_version':'authored-fixture-logistic-v1',
                'limitation':'Scores are not calibrated confidence; this tiny authored dataset is instructional.'}
    return app

app=create_app()
