"""Offline HTTP demonstration using the same persistent API as the later capstone."""
import json
import tempfile
from pathlib import Path
from fastapi.testclient import TestClient
from projects.api import create_app

def run():
    with tempfile.TemporaryDirectory() as folder:
        key='local-test-key-0123456789012345'
        path=Path(folder)/'records.db'
        app=create_app(path,{key:'A'})
        with TestClient(app) as client:
            headers={'Authorization':'Bearer '+key}
            for category,cents in [('Food',1550),('Transport',1000)]:
                assert client.post('/records',json={'category':category,'cents':cents},headers=headers).status_code==201
            assert client.get('/records').status_code==401
        with TestClient(create_app(path,{key:'A'})) as client:
            return client.get('/summary',headers=headers).json()

if __name__=='__main__': print(json.dumps(run(),indent=2))
