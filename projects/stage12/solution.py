"""Black-box isolation checks against actual API endpoints."""
import tempfile
from pathlib import Path
from fastapi.testclient import TestClient
from projects.api import create_app

def run():
    key_a,key_b='tenant-A-demo-key-0123456789','tenant-B-demo-key-0123456789'
    with tempfile.TemporaryDirectory() as folder, TestClient(create_app(Path(folder)/'security.db',{key_a:'A',key_b:'B'},seed=True)) as client:
        auth=lambda key: {'Authorization':'Bearer '+key}
        denied=client.get('/search',params={'q':'Cedar merger'},headers=auth(key_a)).json()
        allowed=client.get('/search',params={'q':'Cedar merger'},headers=auth(key_b)).json()
        assert all(d['id']!='b-private' for d in denied)
        assert any(d['id']=='b-private' for d in allowed)
        assert client.post('/compare',json={'companies':['Aurora'],'years':[2025]},headers=auth(key_b)).status_code==404
        assert client.post('/documents',json={'text':'x','source':'x','tenant':'B'},headers=auth(key_a)).status_code==422
        assert client.get('/records').status_code==401
        assert client.post('/answer',json={'question':'x'*4001},headers=auth(key_a)).status_code==422
        return {'checks':6,'result':'passed','scope':'Deterministic API policy tests; no proof of universal prompt-injection resistance.'}

if __name__=='__main__': print(run())
