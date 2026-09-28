import math

def test_cpu_training_artifacts_and_selection(assignment,tmp_path):
    report=assignment.digits_comparison(tmp_path,epochs=1)
    experiments=report['experiments']
    assert {'mlp','cnn'}<=set(r['architecture'] for r in experiments)
    assert report['selected']==min(experiments,key=lambda r:r['best_validation_loss'])['name']
    for row in experiments:
        assert row['parameters']>0 and row['seconds']>=0 and len(row['history'])==1
        assert all(math.isfinite(h['training']) and math.isfinite(h['validation']) for h in row['history'])
    assert 0<=report['test_report']['accuracy']<=1
    assert all(str(i) in report['test_report'] for i in range(10))
    assert (tmp_path/'best_weights.pt').stat().st_size>0
    assert (tmp_path/'validation.png').stat().st_size>100
    assert report['model_card']
    # No high accuracy requirement after one epoch: this is a mechanics check.
