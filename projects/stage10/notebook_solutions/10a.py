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

event = {"request_id": "example-001", "status": "ok", "latency_ms": 12.5, "model_version": "offline"}
print(event)

# 10a-E1: SLO calculation

def slo_fraction(events, target=500):
    if not events: raise ValueError("No observations")
    return sum(e["ok"] and e["latency_ms"] <= target for e in events)/len(events)

assert slo_fraction([{"ok": True, "latency_ms": 100}, {"ok": False, "latency_ms": 10}]) == .5

print("10a-E1: checks passed")

# 10a-E2: Log allowlist

def safe_log(event):
    return {k: event[k] for k in ("request_id", "status", "latency_ms") if k in event}

assert safe_log({"request_id": "x", "token": "secret", "prompt": "private"}) == {"request_id": "x"}

print("10a-E2: checks passed")

# 10a-E3: Idempotency conflict

def remember(cache, key, payload, result):
    if key in cache:
        previous_payload, previous_result = cache[key]
        if previous_payload != payload: raise ValueError("Idempotency conflict")
        return previous_result
    cache[key] = (payload, result)
    return result

cache = {}
assert remember(cache, "k", {"x": 1}, 3) == 3
assert remember(cache, "k", {"x": 1}, 8) == 3
expect_error(ValueError, lambda: remember(cache, "k", {"x": 2}, 4))

print("10a-E3: checks passed")
