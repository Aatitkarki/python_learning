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

partitions = [[10, 20], [100]]
print("Wrong mean of means:", sum(sum(p)/len(p) for p in partitions)/len(partitions))
print("Correct:", sum(map(sum, partitions))/sum(map(len, partitions)))

# 11a-E1: Mergeable average

def distributed_mean(partitions):
    total, count = 0, 0
    for partition in partitions:
        total += sum(partition)
        count += len(partition)
    if count == 0: raise ValueError("No observations")
    return total/count

assert abs(distributed_mean([[10, 20], [100]])-130/3) < 1e-12
assert distributed_mean([[], [3]]) == 3

print("11a-E1: checks passed")

# 11a-E2: Grouped partial sums

def merge_groups(partials):
    result = {}
    for partial in partials:
        for key, value in partial.items(): result[key] = result.get(key, 0)+value
    return result

assert merge_groups([{"a": 2}, {"a": 3, "b": 4}]) == {"a": 5, "b": 4}

print("11a-E2: checks passed")

# 11a-E3: Skew ratio

def skew_ratio(sizes):
    if not sizes or min(sizes) < 0 or sum(sizes) == 0: raise ValueError("Invalid sizes")
    return max(sizes)/(sum(sizes)/len(sizes))

assert skew_ratio([10, 10, 10]) == 1
assert skew_ratio([0, 0, 30]) == 3

print("11a-E3: checks passed")
