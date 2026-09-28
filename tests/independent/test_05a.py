import numpy as np
import pytest

def setup_network():
    rng=np.random.default_rng(7)
    return np.array([[0.,0.],[0.,1.],[1.,0.],[1.,1.]]),np.array([[0.],[1.],[1.],[0.]]),[rng.normal(0,.5,(2,4)),np.zeros(4),rng.normal(0,.5,(4,1)),np.zeros(1)]

def test_ten_independent_finite_differences(assignment):
    x,y,params=setup_network();original=[p.copy() for p in params];loss,grad=assignment.loss_grad(x,y,params)
    assert np.isfinite(loss)
    for p,g,old in zip(params,grad,original):
        assert g.shape==p.shape and np.array_equal(p,old), 'Gradient calculation must not update weights'
    coordinates=[(i,index) for i,p in enumerate(params) for index in np.ndindex(p.shape)]
    for choice in np.random.default_rng(19).choice(len(coordinates),10,replace=False):
        i,index=coordinates[choice];old=params[i][index];h=1e-5
        params[i][index]=old+h;plus=assignment.loss_grad(x,y,params)[0]
        params[i][index]=old-h;minus=assignment.loss_grad(x,y,params)[0]
        params[i][index]=old
        assert grad[i][index]==pytest.approx((plus-minus)/(2*h),abs=1e-6)

def test_gradient_steps_reduce_xor_loss(assignment):
    x,y,params=setup_network();initial=assignment.loss_grad(x,y,params)[0]
    for _ in range(2500):
        loss,grad=assignment.loss_grad(x,y,params)
        for p,g in zip(params,grad):p-=.05*g
    assert loss<initial/5 and loss<.05
