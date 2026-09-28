import pytest

def test_mean_and_variance_conventions(assignment):
    assert assignment.mean([2,4,6])==4
    assert assignment.variance([2,4,6])==4
    assert assignment.variance([2,4,6],sample=False)==pytest.approx(8/3)
    assert assignment.standard_deviation([2,4,6])==2

def test_covariance_and_correlation(assignment):
    assert assignment.covariance([1,2,3],[2,4,6])==2
    assert assignment.correlation([1,2,3],[6,4,2])==pytest.approx(-1)

def test_statistical_undefined_cases(assignment):
    for name,args in [('mean',([],)),('variance',([1],)),('correlation',([1,1],[2,3])),('covariance',([1,2],[1],))]:
        with pytest.raises(ValueError):getattr(assignment,name)(*args)

def test_permutation_identical_and_separated(assignment):
    assert assignment.permutation_test([1,1],[1,1],repeats=100,seed=7)==1
    p=assignment.permutation_test([0]*5,[10]*5,repeats=999,seed=7)
    assert .001<=p<.05
    assert p==assignment.permutation_test([0]*5,[10]*5,repeats=999,seed=7)

def test_permutation_validates_repeats(assignment):
    with pytest.raises(ValueError):assignment.permutation_test([1],[2],repeats=0)
