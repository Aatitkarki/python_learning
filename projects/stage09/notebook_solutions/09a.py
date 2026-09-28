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

print("7 billion FP16 weights, GiB:", 7_000_000_000*2/1024**3)

# 09a-E1: Weight estimate

def weight_gib(parameters, bits):
    if parameters <= 0 or bits <= 0: raise ValueError("Positive sizes required")
    return parameters*bits/8/1024**3

assert weight_gib(1024**3, 8) == 1
assert weight_gib(1024**3, 4) == .5

print("09a-E1: checks passed")

# 09a-E2: KV estimate

def kv_bytes(layers, kv_heads, head_dim, tokens, batch=1, bytes_per_value=2):
    return 2*layers*kv_heads*head_dim*tokens*batch*bytes_per_value

assert kv_bytes(2, 4, 8, 16) == 4096

print("09a-E2: checks passed")

# 09a-E3: Nearest-rank percentile

def percentile(values, p):
    import math
    if not values or not 0 < p <= 1: raise ValueError("Invalid percentile")
    return sorted(values)[math.ceil(p*len(values))-1]

assert percentile(list(range(1, 101)), .95) == 95
assert percentile([3], .5) == 3

print("09a-E3: checks passed")
