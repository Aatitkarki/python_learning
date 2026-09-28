import json

def test_injected_failure_report_and_restore(assignment,tmp_path):
    report=assignment.run(tmp_path)
    faults={r['case']:r for r in report['faults']}
    for case,status in [('invalid_auth',401),('malformed_body',422),('oversized_prompt',422),('missing_period',404),('database_outage',503)]:
        assert faults[case]['status']==status
    assert faults['invalid_auth']['request_id'] and faults['invalid_auth']['seconds']>=0
    assert faults['corrupt_document']['ok'] is True
    assert report['simulated_model_timeout']['failures']==3
    assert report['sqlite_restore']=={'rows':1,'cents':1550}
    assert json.loads((tmp_path/'report.json').read_text())['passed'] is True
    assert (tmp_path/'operations.html').exists()
