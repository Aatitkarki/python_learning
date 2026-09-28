import math

def test_regression_models_and_validation_selection(assignment):
    report=assignment.regression();scores=report['validation']
    assert {'mean','linear','tree','forest','boosting'}<=set(scores)
    assert report['selected']==min(scores,key=lambda name:scores[name]['mae'])
    for metrics in [*scores.values(),report['final_test']]:
        assert all(math.isfinite(metrics[k]) for k in ['mae','rmse','r2'])
        assert metrics['rmse']>=metrics['mae']-1e-10 and metrics['mae']>=0

def test_classifier_reports_heldout_errors(assignment):
    report=assignment.classification()
    assert {'majority','logistic','forest','boosting'}<=set(report['validation_macro_f1'])
    assert 0<=report['test']['macro avg']['f1-score']<=1
    assert sum(map(sum,report['confusion_matrix']))>0
    assert isinstance(report['errors'],list)
