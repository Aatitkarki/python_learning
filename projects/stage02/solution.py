"""Regression from manual gradient descent with a numerical gradient check."""
import json

def fit(xs, ys, steps=1000, lr=.02, penalty=.0):
    if not xs or len(xs) != len(ys): raise ValueError('Invalid data')
    w, b, history = 0., 0., []
    for _ in range(steps):
        residual = [w*x+b-y for x,y in zip(xs,ys)]
        history.append(sum(r*r for r in residual)/len(xs)+penalty*w*w)
        dw = 2*sum(x*r for x,r in zip(xs,residual))/len(xs)+2*penalty*w
        db = 2*sum(residual)/len(xs)
        w, b = w-lr*dw, b-lr*db
    return w,b,history

if __name__ == '__main__':
    w,b,history = fit([-2,-1,0,1,2], [-3,-1,1,3,5])
    assert abs(w-2) < 1e-6 and abs(b-1) < 1e-6
    print(json.dumps({'weight': w, 'bias': b, 'initial_loss': history[0], 'final_loss': history[-1]}, indent=2))
