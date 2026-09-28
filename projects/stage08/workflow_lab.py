"""08a/08b: equivalent graph, durable reviewed actions, and a two-worker comparison."""
import argparse
import hashlib
import json
import sqlite3
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import TypedDict
from langgraph.graph import StateGraph,START,END
from projects.stage08.research import ResearchWorkflow
from projects.reference import Store

class State(TypedDict,total=False):
    calls:list
    result:dict

def graph_workflow(workflow):
    graph=StateGraph(State)
    graph.add_node('execute',lambda state:{'result':workflow.run(state['calls'])})
    graph.add_edge(START,'execute');graph.add_edge('execute',END)
    return graph.compile()

def digest(actor,proposal):
    return hashlib.sha256(json.dumps([actor,proposal],sort_keys=True,separators=(',',':')).encode()).hexdigest()

class ReviewStore:
    """Durable application approval journal, independent of LangGraph's checkpointer.
    Identity arguments must come from verified server identity, never model text.
    """
    def __init__(self,path):
        self.path=str(path)
        with sqlite3.connect(self.path) as db:
            db.execute('CREATE TABLE IF NOT EXISTS reviews (run_id TEXT PRIMARY KEY,actor TEXT,proposal TEXT,fingerprint TEXT,expires REAL,status TEXT,result TEXT)')
    def propose(self,run_id,actor,proposal,now=None,ttl=300):
        if ttl<=0:raise ValueError('Positive expiry required')
        now=time.time() if now is None else now;fingerprint=digest(actor,proposal)
        with sqlite3.connect(self.path) as db:
            db.execute('INSERT INTO reviews VALUES(?,?,?,?,?,?,?)',(run_id,actor,json.dumps(proposal),fingerprint,now+ttl,'pending',None))
        return fingerprint
    def resume(self,run_id,actor,fingerprint,approved,execute,now=None):
        now=time.time() if now is None else now
        with sqlite3.connect(self.path) as db:
            db.execute('BEGIN IMMEDIATE')
            row=db.execute('SELECT actor,proposal,fingerprint,expires,status FROM reviews WHERE run_id=?',(run_id,)).fetchone()
            if row is None or row[0]!=actor:raise PermissionError('Unknown review')
            if row[2]!=fingerprint or row[3]<=now or row[4]!='pending':raise ValueError('Invalid, expired, or consumed review')
            if approved is not True:
                db.execute('UPDATE reviews SET status=? WHERE run_id=?',('denied',run_id));return {'status':'denied'}
            # Only pure calculations in this example. External writes need their own idempotency/transaction protocol.
            result=execute(json.loads(row[1]))
            db.execute('UPDATE reviews SET status=?,result=? WHERE run_id=?',('complete',json.dumps(result),run_id))
        return {'status':'complete','result':result}

def compare_workers(workflow,calls):
    started=time.perf_counter();single=workflow.run(calls);single_time=time.perf_counter()-started
    def verify(result):
        return result['status']=='complete' and all(o['status']=='ok' for o in result['observations'])
    started=time.perf_counter()
    with ThreadPoolExecutor(max_workers=2) as pool:
        research=pool.submit(workflow.run,calls).result()
        checked=pool.submit(verify,research).result()
    return {'single_seconds':single_time,'two_worker_seconds':time.perf_counter()-started,'same_results':single==research,
            'verified':checked,'tool_calls_per_run':len(single['observations']),'model_calls':0,'monetary_cost':None,
            'limit':'Deterministic research/checking workers; not an empirical comparison of two LLM agents. Measure model tokens/costs when adding models.'}

def run(output):
    out=Path(output);out.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as folder:
        store=Store(Path(folder)/'data.db');store.seed();workflow=ResearchWorkflow(store,'A')
        calls=[{'tool':'search','arguments':{'query':'Aurora 2025 revenue'}},{'tool':'divide','arguments':{'numerator':144,'denominator':120}}]
        plain=workflow.run(calls);graph=graph_workflow(workflow).invoke({'calls':calls})['result'];assert plain==graph
        db_path=Path(folder)/'reviews.db';fingerprint=ReviewStore(db_path).propose('run-A','A',calls[1],now=100)
        restarted=ReviewStore(db_path)
        approval=restarted.resume('run-A','A',fingerprint,True,workflow.execute,now=101)
        try:restarted.resume('run-A','A',fingerprint,True,workflow.execute,now=102)
        except ValueError:replay_denied=True
        else:replay_denied=False
        report={'plain_graph_equal':plain==graph,'trace':plain,'durable_approval':approval,'replay_denied':replay_denied,'workers':compare_workers(workflow,calls)}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='work/reference_answers/stage08');a=p.parse_args();print(json.dumps(run(a.output),indent=2))
