import pytest

def test_all_memory_scenarios_and_weight_units(assignment):
    rows=assignment.memory_budget()
    assert len(rows)==27 and len({(r['parameters'],r['bits'],r['context']) for r in rows})==27
    for row in rows:
        assert row['weight_gib']==pytest.approx(row['parameters']*row['bits']/8/(2**30))
        assert row['kv_gib']>0 and row['assumption']

def test_context_changes_cache_not_weights(assignment):
    rows=sorted([r for r in assignment.memory_budget() if r['parameters']==7_000_000_000 and r['bits']==16],key=lambda r:r['context'])
    assert len(rows)==3
    assert rows[0]['weight_gib']==rows[1]['weight_gib']
    assert rows[1]['kv_gib']/rows[0]['kv_gib']==pytest.approx(rows[1]['context']/rows[0]['context'])
