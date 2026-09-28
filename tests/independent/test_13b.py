import pytest

def test_paired_bootstrap_known_difference_and_groups(assignment):
    report=assignment.paired_interval([0,0,1,1],[1,1,1,1],['a','a','b','b'],repeats=200,seed=1)
    assert report['delta']==.5 and report['groups']==2
    assert report['ci95'][0]<=.5<=report['ci95'][1]
    assert report==assignment.paired_interval([0,0,1,1],[1,1,1,1],['a','a','b','b'],repeats=200,seed=1)
    same=assignment.paired_interval([1,0],[1,0],repeats=100)
    assert same['delta']==0 and same['ci95']==[0,0]

def test_gate_cannot_hide_access_or_citation_failure(assignment):
    good={'correct':True,'citation_correct':True,'authorized':True}
    assert assignment.release_gate({'cases':[good]}) is True
    assert assignment.release_gate({'cases':[]}) is False
    for key in good:
        bad={**good,key:False}
        assert assignment.release_gate({'cases':[good]*100+[bad]}) is False

def test_invalid_comparison(assignment):
    with pytest.raises(ValueError):assignment.paired_interval([],[])
    with pytest.raises(ValueError):assignment.paired_interval([1],[1,2])
