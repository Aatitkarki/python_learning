"""10a: concrete failure injection, restore evidence, and an operational report."""
import argparse
import json
import sqlite3
import tempfile
import time
from pathlib import Path
from unittest.mock import patch
from fastapi.testclient import TestClient
from projects.api import create_app
from projects.stage09.benchmark import measure
from projects.stage01.solution import load_expenses

KEY='answer-lab-test-key-0123456789'

def restore_copy(source,target):
    if Path(target).exists():raise FileExistsError('Choose a new restore path')
    with sqlite3.connect(source) as original,sqlite3.connect(target) as restored:
        original.backup(restored)
        assert restored.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
        return restored.execute('SELECT COUNT(*),COALESCE(SUM(cents),0) FROM records').fetchone()

def run(output):
    observations=[]
    with tempfile.TemporaryDirectory() as folder:
        db=Path(folder)/'service.db';app=create_app(db,{KEY:'A'},seed=True,limit_per_minute=1000)
        with TestClient(app) as client:
            headers={'Authorization':'Bearer '+KEY}
            checks=[('invalid_auth','get','/records',{},401),('malformed_body','post','/records',{'headers':headers,'json':{'cents':-1}},422),
                    ('oversized_prompt','post','/answer',{'headers':headers,'json':{'question':'x'*4001}},422),
                    ('missing_period','post','/compare',{'headers':headers,'json':{'companies':['Aurora'],'years':[1900]}},404)]
            for name,method,url,kwargs,expected in checks:
                start=time.perf_counter();response=getattr(client,method)(url,**kwargs)
                observations.append({'case':name,'status':response.status_code,'expected':expected,'ok':response.status_code==expected,'seconds':time.perf_counter()-start,'request_id':response.headers.get('X-Request-ID')})
            with patch.object(app.state.store,'summary',side_effect=sqlite3.OperationalError('private DSN detail')):
                response=client.get('/summary',headers=headers)
                observations.append({'case':'database_outage','ok':response.status_code==503 and 'private' not in response.text,'status':response.status_code,'expected':503})
            assert client.post('/records',headers=headers,json={'category':'Food','cents':1550}).status_code==201
        count,total=restore_copy(db,Path(folder)/'restored.db')
        bad=Path(folder)/'corrupt.csv';bad.write_text('date,category,amount\nnot-a-date,Food,NaN\n')
        try:load_expenses(bad)
        except ValueError:observations.append({'case':'corrupt_document','ok':True})
        else:observations.append({'case':'corrupt_document','ok':False})
        def timeout():raise TimeoutError('simulated dependency timeout')
        timeout_report=measure(timeout,runs=3)
    report={'faults':observations,'simulated_model_timeout':timeout_report,'sqlite_restore':{'rows':count,'cents':total},
            'passed':all(r['ok'] for r in observations) and count==1 and total==1550,
            'limits':'HTTP boundary fault injection and actual SQLite backup/restore. Live Docker/PostgreSQL/model outages require the operational procedure.'}
    out=Path(output);out.mkdir(parents=True,exist_ok=True);(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    (out/'operations.html').write_text('<!doctype html><meta charset="utf-8"><title>Operational checks</title><h1>Observed checks</h1><pre>'+__import__('html').escape(json.dumps(report,indent=2))+'</pre>')
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='work/reference_answers/stage10');a=p.parse_args();report=run(a.output);print(json.dumps(report,indent=2));raise SystemExit(0 if report['passed'] else 1)
