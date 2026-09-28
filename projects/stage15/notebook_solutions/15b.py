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

architecture = {"api": ["authorization", "orchestrator"], "orchestrator": ["retrieval", "calculator", "model"], "retrieval": ["database"]}
print(architecture)

# 15b-E1: Failure attribution

def owner(failure):
    return {"parsing": "data", "retrieval": "search", "arithmetic": "calculator", "permission": "authorization", "timeout": "infrastructure"}.get(failure, "investigate")

assert owner("permission") == "authorization"
assert owner("unknown") == "investigate"

print("15b-E1: checks passed")

# 15b-E2: Serial latency budget

def latency_budget(stages, target):
    if target < 0 or any(value < 0 for value in stages.values()): raise ValueError("Negative duration")
    total = sum(stages.values())
    return total, total <= target

assert latency_budget({"search": 100, "model": 800, "api": 50}, 1000) == (950, True)

print("15b-E2: checks passed")

# 15b-E3: Evidence readiness

def missing_evidence(artifacts):
    required = ["code", "tests", "evaluation", "threat_model", "restore", "incident", "defense"]
    return [key for key in required if not artifacts.get(key)]

assert "restore" in missing_evidence({"code": "src/"})
assert missing_evidence(dict.fromkeys(["code", "tests", "evaluation", "threat_model", "restore", "incident", "defense"], "evidence.md")) == []

print("15b-E3: checks passed")
