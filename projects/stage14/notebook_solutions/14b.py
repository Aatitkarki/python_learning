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

import pandas as pd
prices = pd.Series([100., 105., 102., 110.])
print(prices.pct_change())
print(prices.shift(1).rolling(2).mean())

# 14b-E1: Past-only feature

def lagged_mean(prices, window=2):
    return prices.shift(1).rolling(window).mean()

values = lagged_mean(pd.Series([10, 20, 100, 200]))
assert values.iloc[2] == 15 and values.iloc[3] == 60

print("14b-E1: checks passed")

# 14b-E2: Chronological split

def temporal_split(n, cut, gap=0):
    if not 0 <= gap < cut < n: raise ValueError("Invalid split")
    return list(range(cut-gap)), list(range(cut,n))

assert temporal_split(10, 6, 2) == ([0, 1, 2, 3], [6, 7, 8, 9])

print("14b-E2: checks passed")

# 14b-E3: Net strategy return

def net_returns(returns, positions, fee=.001):
    if len(returns) != len(positions): raise ValueError("Length mismatch")
    previous, result = 0, []
    for ret, position in zip(returns, positions):
        result.append(position*ret-fee*abs(position-previous))
        previous = position
    return result

assert abs(net_returns([.1, .1], [1, 0])[0]-.099) < 1e-12
assert net_returns([.1, .1], [1, 0])[1] == -.001

print("14b-E3: checks passed")
