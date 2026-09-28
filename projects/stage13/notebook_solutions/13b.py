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

baseline = [1, 0, 1, 1]
candidate = [1, 1, 1, 0]
print([b-a for a,b in zip(baseline,candidate)])

# 13b-E1: Paired improvement

def paired_delta(baseline, candidate):
    if not baseline or len(baseline) != len(candidate): raise ValueError("Unpaired cases")
    return sum(b-a for a,b in zip(baseline,candidate))/len(baseline)

assert paired_delta([0, 1], [1, 1]) == .5
expect_error(ValueError, lambda: paired_delta([1], [1, 0]))

print("13b-E1: checks passed")

# 13b-E2: Hard release gate

def passes_gate(metrics):
    required = {"recall", "groundedness", "unauthorized", "p95_ms"}
    if not required <= metrics.keys(): return False
    return metrics["recall"] >= .8 and metrics["groundedness"] >= .9 and metrics["unauthorized"] == 0 and metrics["p95_ms"] <= 2000

assert passes_gate(dict(recall=.9, groundedness=.95, unauthorized=0, p95_ms=1000))
assert not passes_gate(dict(recall=1, groundedness=1, unauthorized=1, p95_ms=100))
assert not passes_gate({})

print("13b-E2: checks passed")

# 13b-E3: Slice report

def slice_report(rows):
    groups = {}
    for row in rows: groups.setdefault(row["category"], []).append(row["correct"])
    return {key: {"n": len(values), "accuracy": sum(values)/len(values)} for key, values in groups.items()}

assert slice_report([{"category": "numeric", "correct": True}, {"category": "numeric", "correct": False}]) == {"numeric": {"n": 2, "accuracy": .5}}

print("13b-E3: checks passed")
