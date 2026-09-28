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

def loss(w):
    return (w - 3) ** 2
w = 0.0
for _ in range(5):
    w -= 0.1 * 2 * (w - 3)
    print(round(w, 4), round(loss(w), 4))

# 02b-E1: Numerical derivative

def derivative(f, x, h=1e-5):
    if h <= 0: raise ValueError("Positive step required")
    return (f(x+h)-f(x-h))/(2*h)

assert abs(derivative(lambda x: x*x, 3)-6) < 1e-6
expect_error(ValueError, lambda: derivative(lambda x: x, 0, 0))

print("02b-E1: checks passed")

# 02b-E2: Linear gradient

def mse_gradient(w, xs, ys):
    if not xs or len(xs) != len(ys): raise ValueError("Invalid data")
    return sum(2*x*(w*x-y) for x, y in zip(xs, ys))/len(xs)

xs, ys = [1, 2, 3], [2, 4, 6]
f = lambda w: sum((w*x-y)**2 for x,y in zip(xs,ys))/len(xs)
assert abs(mse_gradient(1, xs, ys)-derivative(f, 1)) < 1e-6

print("02b-E2: checks passed")

# 02b-E3: Fit one weight

def fit_weight(xs, ys, lr=0.05, steps=100):
    w = 0.0
    for _ in range(steps):
        w -= lr * mse_gradient(w, xs, ys)
    return w

assert abs(fit_weight([1, 2, 3], [2, 4, 6])-2) < 1e-6

print("02b-E3: checks passed")
