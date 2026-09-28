import pytest

def test_one_gradient_step_by_hand(assignment):
    w,b,history=assignment.fit([0,1],[1,3],steps=1,lr=.1)
    assert (w,b)==pytest.approx((.3,.4))
    assert history==pytest.approx([5])

def test_intercept_and_slope_converge(assignment):
    w,b,history=assignment.fit([-2,-1,0,1,2],[-8,-5,-2,1,4],steps=1000,lr=.02)
    assert (w,b)==pytest.approx((3,-2),abs=1e-5)
    assert history[-1]<history[0]

def test_regularization_changes_optimum(assignment):
    plain=assignment.fit([-1,0,1],[-1,1,3],steps=1500,lr=.02)
    regular=assignment.fit([-1,0,1],[-1,1,3],steps=1500,lr=.02,penalty=.5)
    assert abs(regular[0])<abs(plain[0]) and regular[1]==pytest.approx(1)
    assert assignment.objective(2,1,[0,1],[1,3],penalty=.5)==2

def test_gradient_check_and_divergence(assignment):
    assert assignment.gradient_check([-1,0,1],[-1,1,3],penalty=.2)<1e-6
    _,_,history=assignment.fit([-2,-1,0,1,2],[-3,-1,1,3,5],steps=20,lr=1)
    assert history[-1]>history[0]

def test_invalid_training_pairs(assignment):
    with pytest.raises(ValueError):assignment.fit([],[])
    with pytest.raises(ValueError):assignment.fit([1,2],[1])
