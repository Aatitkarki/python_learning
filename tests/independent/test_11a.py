import pytest

@pytest.mark.parametrize('n,batch',[(0,3),(1,1),(137,17),(1000000,10000)])
def test_streaming_total_against_independent_reference(assignment,n,batch):
    result=assignment.streaming_totals(n,batch_size=batch)
    expected={}
    for i in range(n):expected[i%50]=expected.get(i%50,0)+(i*17)%10000
    assert result['rows']==n and result['by_account']==expected
    assert result['total_cents']==sum(expected.values()) and result['groups']==len(expected)

def test_invalid_batch_size(assignment):
    with pytest.raises(ValueError):assignment.streaming_totals(10,batch_size=0)
