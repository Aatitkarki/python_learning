import numpy as np
import pytest

def test_stable_normalization_and_entropy(assignment):
    p=assignment.probabilities([1000,1001,1002]);assert np.isfinite(p).all() and p.sum()==pytest.approx(1)
    assert assignment.entropy([.5,.5])==pytest.approx(np.log(2))
    assert assignment.entropy([1.,0.])==0
    assert assignment.entropy(assignment.probabilities([1,2,3],temperature=.2))<assignment.entropy(assignment.probabilities([1,2,3]))

def test_top_k_and_crossing_top_p(assignment):
    assert np.count_nonzero(assignment.probabilities([1,2,3,4],top_k=2))==2
    p=assignment.probabilities(np.log([.6,.25,.15]),top_p=.8)
    assert p==pytest.approx([.6/.85,.25/.85,0])

def test_future_value_cannot_change_past(assignment):
    q=np.eye(4);v=np.arange(12,dtype=float).reshape(4,3)
    out,weights=assignment.causal_attention(q,q,v)
    changed=v.copy();changed[-1]+=1000
    assert np.allclose(out[:-1],assignment.causal_attention(q,q,changed)[0][:-1])
    assert np.allclose(weights.sum(axis=1),1) and np.allclose(np.triu(weights,1),0)

@pytest.mark.parametrize('kwargs',[{'temperature':0},{'top_k':0},{'top_p':1.1}])
def test_invalid_sampling(assignment,kwargs):
    with pytest.raises(ValueError):assignment.probabilities([1,2],**kwargs)
