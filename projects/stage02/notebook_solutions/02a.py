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

import math
v = [3, 4]
print(math.sqrt(sum(x*x for x in v)))
print(math.log(math.e))

# 02a-E1: Dot product

def dot(a, b):
    if len(a) != len(b): raise ValueError("Shape mismatch")
    return sum(x*y for x, y in zip(a, b))

assert dot([1, 2], [3, 4]) == 11
expect_error(ValueError, lambda: dot([1], [2, 3]))

print("02a-E1: checks passed")

# 02a-E2: Cosine similarity

def cosine(a, b):
    import math
    numerator = dot(a, b)
    denominator = math.sqrt(dot(a, a) * dot(b, b))
    if denominator == 0: raise ValueError("Zero vector")
    return numerator / denominator

assert abs(cosine([1, 0], [0, 1])) < 1e-12
assert abs(cosine([2, 2], [1, 1])-1) < 1e-12
expect_error(ValueError, lambda: cosine([0, 0], [1, 2]))

print("02a-E2: checks passed")

# 02a-E3: Matrix multiplication

def matmul(a, b):
    if not a or not b or not a[0] or not b[0]: raise ValueError("Empty matrix")
    if any(len(row) != len(a[0]) for row in a) or any(len(row) != len(b[0]) for row in b):
        raise ValueError("Ragged matrix")
    if len(a[0]) != len(b): raise ValueError("Shape mismatch")
    return [[dot(row, col) for col in zip(*b)] for row in a]

assert matmul([[1, 2]], [[3], [4]]) == [[11]]
assert matmul([[2, 3]], [[1, 0], [0, 1]]) == [[2, 3]]
expect_error(ValueError, lambda: matmul([[1, 2]], [[1, 2]]))

print("02a-E3: checks passed")
