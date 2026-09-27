"""Real LangGraph interrupt/resume, exact-action binding, and isolated run IDs."""
import hashlib
import json
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command

class State(TypedDict, total=False):
    actor: str
    proposal: dict
    status: str
    result: float

def fingerprint(state):
    return hashlib.sha256(json.dumps({'actor':state['actor'],'proposal':state['proposal']},sort_keys=True).encode()).hexdigest()

def reviewed_calculation(state):
    expected=fingerprint(state)
    decision=interrupt({'proposal':state['proposal'],'fingerprint':expected})
    if not isinstance(decision,dict) or decision.get('approved') is not True or decision.get('fingerprint')!=expected:
        return {'status':'denied'}
    proposal=state['proposal']
    if set(proposal)!={'operation','a','b'} or proposal['operation']!='divide':
        return {'status':'invalid'}
    a,b=proposal['a'],proposal['b']
    import math
    if any(type(v) not in (int,float) or not math.isfinite(v) for v in (a,b)) or b==0:
        return {'status':'invalid'}
    return {'status':'complete','result':a/b}

def build():
    graph=StateGraph(State)
    graph.add_node('review',reviewed_calculation)
    graph.add_edge(START,'review'); graph.add_edge('review',END)
    return graph.compile(checkpointer=InMemorySaver())

def run():
    graph=build(); config={'configurable':{'thread_id':'learning-run-1'}}
    state={'actor':'student-A','proposal':{'operation':'divide','a':144,'b':120}}
    paused=graph.invoke(state,config)
    assert '__interrupt__' in paused
    result=graph.invoke(Command(resume={'approved':True,'fingerprint':fingerprint(state)}),config)
    assert result['result']==1.2
    assert not graph.get_state({'configurable':{'thread_id':'another-run'}}).values
    return result

if __name__=='__main__': print(json.dumps(run(),indent=2))
