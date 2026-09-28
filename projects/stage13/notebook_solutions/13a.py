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

case = {"id": "q01", "tenant": "A", "question": "What was 2025 revenue?", "relevant_ids": ["A-2025"], "expected_value": 120}
print(case)

# 13a-E1: Recall at k

def recall_at_k(retrieved, relevant, k):
    relevant = set(relevant)
    if not relevant or k < 1: raise ValueError("Invalid evaluation case")
    return len(set(retrieved[:k]) & relevant)/len(relevant)

assert recall_at_k(["a", "a", "b"], {"a", "b"}, 2) == .5
assert recall_at_k([], {"a"}, 3) == 0

print("13a-E1: checks passed")

# 13a-E2: Reciprocal rank

def reciprocal_rank(retrieved, relevant):
    return next((1/rank for rank, id in enumerate(retrieved, 1) if id in relevant), 0.)

assert reciprocal_rank(["x", "a"], {"a"}) == .5
assert reciprocal_rank(["x"], {"a"}) == 0

print("13a-E2: checks passed")

# 13a-E3: Citation precision

def citation_precision(supports):
    return sum(supports)/len(supports) if supports else None

assert citation_precision([True, False, True]) == 2/3
assert citation_precision([]) is None

print("13a-E3: checks passed")
