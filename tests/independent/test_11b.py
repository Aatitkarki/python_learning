import pytest

def test_reconciliation_reference_before_spark(assignment):
    assert assignment.streaming_totals(10000)['total_cents']==49995000

@pytest.mark.live_spark
def test_actual_partition_skew_and_broadcast_experiment(assignment,tmp_path):
    report=assignment.spark_comparison(10000,tmp_path)
    assert [r['partitions'] for r in report['runs']]==[2,8,32]
    assert all(r['total_cents']==49995000 for r in report['runs'])
    assert report['salted_totals_match'] and report['broadcast_join_rows']==10000
    assert all((tmp_path/f'plan-{n}.txt').exists() for n in [2,8,32])
    assert 'Broadcast' in (tmp_path/'broadcast-plan.txt').read_text()
