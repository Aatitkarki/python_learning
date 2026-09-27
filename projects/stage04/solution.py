"""Compare models on validation data, then evaluate only the selected model on test."""
import json
from pathlib import Path
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import FunctionTransformer
from sklearn.metrics import classification_report, f1_score, confusion_matrix

ROOT = Path(__file__).resolve().parents[2]

def dense(x): return x.toarray()

def run():
    data = pd.read_csv(ROOT/'datasets/tickets.csv')
    assert data.groupby('group')['split'].nunique().max() == 1
    train, validation, test = [data[data.split == split] for split in ('train','validation','test')]
    candidates = {
        'majority': make_pipeline(TfidfVectorizer(), DummyClassifier(strategy='most_frequent')),
        'logistic': make_pipeline(TfidfVectorizer(ngram_range=(1,2)), LogisticRegression(max_iter=500, random_state=42)),
        'forest': make_pipeline(TfidfVectorizer(), RandomForestClassifier(n_estimators=100, random_state=42)),
        'boosting': make_pipeline(TfidfVectorizer(), FunctionTransformer(dense, accept_sparse=True), GradientBoostingClassifier(random_state=42))}
    scores = {}
    for name, model in candidates.items():
        model.fit(train.text, train.label)
        scores[name] = f1_score(validation.label, model.predict(validation.text), average='macro')
    # Ties prefer the simpler model, in the insertion order above.
    selected = max(scores, key=scores.get)
    chosen = candidates[selected]
    chosen.fit(pd.concat([train, validation]).text, pd.concat([train, validation]).label)
    predictions = chosen.predict(test.text)
    return {'validation_macro_f1': scores, 'selected': selected,
            'test': classification_report(test.label, predictions, output_dict=True, zero_division=0),
            'confusion_matrix': confusion_matrix(test.label, predictions, labels=chosen.classes_).tolist(),
            'classes': chosen.classes_.tolist(),
            'errors': [{'text': text, 'expected': actual, 'predicted': pred} for text,actual,pred in zip(test.text,test.label,predictions) if actual != pred],
            'limitation': '36 authored examples are a smoke dataset; collect independent real examples before claiming useful accuracy.'}

if __name__ == '__main__': print(json.dumps(run(), indent=2))
