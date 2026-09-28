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

import statistics
sample = [2, 4, 4, 6]
print(statistics.mean(sample), statistics.median(sample), statistics.variance(sample))

# 02c-E1: Sample variance

def variance(xs):
    if len(xs) < 2: raise ValueError("Need two observations")
    mean = sum(xs)/len(xs)
    return sum((x-mean)**2 for x in xs)/(len(xs)-1)

assert variance([1, 2, 3]) == 1
expect_error(ValueError, lambda: variance([1]))

print("02c-E1: checks passed")

# 02c-E2: Bayesian alert

def posterior(prevalence, sensitivity, false_positive_rate):
    if any(not 0 <= p <= 1 for p in (prevalence, sensitivity, false_positive_rate)):
        raise ValueError("Invalid probability")
    true = prevalence*sensitivity
    positive = true + (1-prevalence)*false_positive_rate
    if positive == 0: raise ValueError("Impossible conditioning event")
    return true/positive

assert abs(posterior(.01, .9, .1)-(.009/.108)) < 1e-12
expect_error(ValueError, lambda: posterior(0, 1, 0))

print("02c-E2: checks passed")

# 02c-E3: Bootstrap mean interval

def bootstrap_ci(xs, repeats=1000, seed=42):
    import random
    if not xs or repeats < 40: raise ValueError("Insufficient data or repeats")
    rng = random.Random(seed)
    means = sorted(sum(rng.choices(xs, k=len(xs)))/len(xs) for _ in range(repeats))
    return means[int(.025*repeats)], means[int(.975*repeats)]

lo, hi = bootstrap_ci([1, 2, 3, 4, 5])
assert lo <= 3 <= hi
assert bootstrap_ci([2]*10) == (2, 2)

print("02c-E3: checks passed")
