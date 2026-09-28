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

message = "Hello, AI engineering"
print(message)
print(3 * 5)
assert 3 * 5 == 15

# 00a-E1: Study budget

def study_hours(weeks, hours_per_week):
    if weeks < 0 or hours_per_week < 0:
        raise ValueError("Time cannot be negative")
    return weeks * hours_per_week

assert study_hours(80, 15) == 1200
assert study_hours(0, 15) == 0
expect_error(ValueError, lambda: study_hours(-1, 15))

print("00a-E1: checks passed")

# 00a-E2: Experiment manifest

def manifest(seed):
    import sys
    return {"seed": seed, "python": sys.version.split()[0]}

assert manifest(42)["seed"] == 42
assert len(manifest(42)["python"].split(".")) == 3

print("00a-E2: checks passed")

# 00a-E3: Reproducible randomness

def rolls(n, seed):
    import random
    rng = random.Random(seed)
    return [rng.randint(1, 6) for _ in range(n)]

assert rolls(20, 7) == rolls(20, 7)
assert len(rolls(20, 7)) == 20
assert all(1 <= x <= 6 for x in rolls(20, 7))

print("00a-E3: checks passed")
