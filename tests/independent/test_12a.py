
def test_attack_suite_has_explicit_cases(assignment):
    rows=assignment.fixtures()
    assert len(rows)>=20 and len({r['id'] for r in rows})==len(rows)
    assert all(r['method'] in {'get','post'} and r['path'].startswith('/') and isinstance(r['expected'],int) for r in rows)

def test_threat_model_contains_controls_and_limits(assignment):
    rows=assignment.threat_model()
    assert len(rows)>=8
    for row in rows:assert all(row[k] for k in ['asset','entry','impact','control','residual'])

def test_observed_attacks_and_allowed_controls(assignment,tmp_path):
    report=assignment.run(tmp_path)
    assert all(r['passed'] for r in report['checks']) and len(report['checks'])>=20
    matrix=report['permission_matrix']
    assert any(r['expected'] is True and r['observed'] is True for r in matrix)
    assert any(r['expected'] is False and r['observed'] is False for r in matrix)
    assert report['limits'], 'Document that application checks do not prove model prompt behavior'
