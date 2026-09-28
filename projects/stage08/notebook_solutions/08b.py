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

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
class State(TypedDict, total=False):
    question: str
    route: str
    answer: str

# 08b-E1: Route state

def route_node(state):
    return {"route": "calculator" if "ratio" in state["question"].lower().split() else "search"}

assert route_node({"question": "calculate ratio"}) == {"route": "calculator"}

print("08b-E1: checks passed")

# 08b-E2: Compile graph

def build_graph():
    graph = StateGraph(State)
    graph.add_node("route", route_node)
    graph.add_node("calculator", lambda state: {"answer": "calculator selected"})
    graph.add_node("search", lambda state: {"answer": "search selected"})
    graph.add_edge(START, "route")
    graph.add_conditional_edges("route", lambda state: state["route"], {"calculator": "calculator", "search": "search"})
    graph.add_edge("calculator", END)
    graph.add_edge("search", END)
    return graph.compile()

graph = build_graph()
assert graph.invoke({"question": "revenue ratio"})["answer"] == "calculator selected"
assert graph.invoke({"question": "find policy"})["answer"] == "search selected"

print("08b-E2: checks passed")

# 08b-E3: Approval binding

def approval_fingerprint(actor, action, arguments):
    import json, hashlib
    body = json.dumps({"actor": actor, "action": action, "arguments": arguments}, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(body.encode()).hexdigest()

assert approval_fingerprint("a", "write", {"x": 1, "y": 2}) == approval_fingerprint("a", "write", {"y": 2, "x": 1})
assert approval_fingerprint("a", "write", {"x": 1}) != approval_fingerprint("b", "write", {"x": 1})

print("08b-E3: checks passed")
