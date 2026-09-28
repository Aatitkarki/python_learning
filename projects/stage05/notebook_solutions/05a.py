"""Generated worked answers; edit your own version under work/."""

from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
def expect_error(error_type, operation):
    try:
        operation()
    except error_type:
        return
    raise AssertionError(f"Expected {error_type.__name__}")


# Worked example

import numpy as np
x = np.array([[1., 2.], [3., 4.]])
w = np.array([[.2], [.3]])
print((x @ w).shape)

# 05a-E1: Stable sigmoid

def sigmoid(x):
    import numpy as np
    x = np.asarray(x, dtype=float)
    z = np.exp(-np.abs(x))
    return np.where(x >= 0, 1/(1+z), z/(1+z))

assert np.allclose(sigmoid([-1000, 0, 1000]), [0, .5, 1])

print("05a-E1: checks passed")

# 05a-E2: Linear backward pass

def backward(x, y, w, b):
    residual = x @ w + b - y
    loss = float((residual**2).mean())
    return loss, 2*x.T@residual/len(x), float(2*residual.mean())

x = np.array([[1.], [2.]])
y = 2*x
w = np.zeros((1, 1))
loss, dw, db = backward(x, y, w, 0)
assert loss == 10 and np.allclose(dw, [[-10]]) and db == -6

print("05a-E2: checks passed")

# 05a-E3: Training loop

def train_linear(x, y, steps=500, lr=.05):
    import numpy as np
    w, b, history = np.zeros((x.shape[1], 1)), 0., []
    for _ in range(steps):
        loss, dw, db = backward(x, y, w, b)
        history.append(loss)
        w -= lr*dw
        b -= lr*db
    return w, b, history

w, b, history = train_linear(np.array([[-1.], [0.], [1.]]), np.array([[-1.], [1.], [3.]]))
assert history[-1] < 1e-8 and np.allclose(w, [[2]], atol=1e-3)

print("05a-E3: checks passed")
