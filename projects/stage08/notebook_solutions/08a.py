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

request = {"tool": "divide", "arguments": {"a": 12, "b": 3}}
print(request)

# 08a-E1: Allowlisted calculator

def execute_tool(request):
    import math
    if set(request) != {"tool", "arguments"}: raise ValueError("Invalid request")
    args = request["arguments"]
    if set(args) != {"a", "b"}: raise ValueError("Invalid arguments")
    if any(type(v) not in (int, float) or not math.isfinite(v) for v in args.values()): raise ValueError("Invalid number")
    a, b = args["a"], args["b"]
    if request["tool"] == "add": return a+b
    if request["tool"] == "divide": return a/b
    raise ValueError("Unknown tool")

assert execute_tool({"tool": "divide", "arguments": {"a": 12, "b": 3}}) == 4
expect_error(ValueError, lambda: execute_tool({"tool": "shell", "arguments": {"a": 1, "b": 2}}))

print("08a-E1: checks passed")

# 08a-E2: Call budget

def run_tools(requests, max_calls=3):
    observations = []
    for request in requests[:max_calls]:
        try: observations.append({"result": execute_tool(request)})
        except (ValueError, ZeroDivisionError) as exc: observations.append({"error": type(exc).__name__})
    return observations, "budget_exhausted" if len(requests) > max_calls else "complete"

request = {"tool": "add", "arguments": {"a": 1, "b": 2}}
observations, status = run_tools([request]*5, 2)
assert len(observations) == 2 and status == "budget_exhausted"

print("08a-E2: checks passed")

# 08a-E3: Retry only transient errors

def retry(operation, attempts=3):
    if attempts < 1: raise ValueError("Positive attempts required")
    for i in range(attempts):
        try: return operation()
        except TimeoutError:
            if i == attempts-1: raise

calls = []
def flaky():
    calls.append(1)
    if len(calls) < 2: raise TimeoutError()
    return "ok"
assert retry(flaky) == "ok" and len(calls) == 2
expect_error(ValueError, lambda: retry(lambda: int("bad")))

print("08a-E3: checks passed")
