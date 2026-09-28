import pytest

def test_success_lengths_tokens_and_percentiles(assignment):
    result=assignment.measure(lambda:{'text':'hello','tokens':2},runs=30,concurrency=2)
    assert result['runs']==30 and len(result['observations'])==30 and result['failures']==0
    assert all(r['output_characters']==5 and r['tokens']==2 for r in result['observations'])
    assert result['p95_seconds_all_attempts']>=result['p50_seconds_all_attempts']>=0
    assert result['tokens_per_wall_second']==pytest.approx(60/result['wall_seconds'])

def test_failures_are_preserved(assignment):
    def fail():raise TimeoutError('private diagnostic')
    result=assignment.measure(fail,runs=3,concurrency=1)
    assert result['failures']==3 and len(result['observations'])==3
    assert result['tokens_per_wall_second'] is None
    assert all(not r['ok'] and r['error']=='TimeoutError' for r in result['observations'])

def test_no_tokens_means_unknown_throughput(assignment):
    assert assignment.measure(lambda:{'text':'hello'},runs=2)['tokens_per_wall_second'] is None
    with pytest.raises(ValueError):assignment.measure(lambda:None,runs=0)
