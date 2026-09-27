"""Two-layer tanh network, full analytical backpropagation and finite differences."""
import numpy as np

def loss_grad(x,y,params):
    w1,b1,w2,b2 = params
    h = np.tanh(x@w1+b1)
    pred = h@w2+b2
    residual = pred-y
    d = 2*residual/len(x)
    dh = (d@w2.T)*(1-h*h)
    return float((residual**2).mean()), [x.T@dh, dh.sum(0), h.T@d, d.sum(0)]

def run():
    rng = np.random.default_rng(42)
    x=np.array([[0.,0.],[0.,1.],[1.,0.],[1.,1.]])
    y=np.array([[0.],[1.],[1.],[0.]])
    params=[rng.normal(0,.5,(2,8)),np.zeros(8),rng.normal(0,.5,(8,1)),np.zeros(1)]
    _,grads=loss_grad(x,y,params)
    max_error=0.
    for pi,index in [(0,(0,0)),(0,(1,3)),(1,(2,)),(2,(3,0)),(3,(0,))]:
        original=params[pi][index]; h=1e-5
        params[pi][index]=original+h; plus=loss_grad(x,y,params)[0]
        params[pi][index]=original-h; minus=loss_grad(x,y,params)[0]
        params[pi][index]=original
        max_error=max(max_error,abs((plus-minus)/(2*h)-grads[pi][index]))
    assert max_error < 1e-6
    for _ in range(3000):
        loss,grads=loss_grad(x,y,params)
        for param,grad in zip(params,grads): param -= .05*grad
    assert loss < 1e-4
    return {'loss': loss, 'max_gradient_error': max_error}

if __name__ == '__main__': print(run())
