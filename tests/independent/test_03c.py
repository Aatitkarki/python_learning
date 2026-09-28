from fastapi.testclient import TestClient
from projects.reference import Store
import pytest
A='independent-A-012345678901234567';B='independent-B-012345678901234567'

def test_api_auth_validation_isolation_and_restart(assignment,tmp_path):
    path=tmp_path/'api.db';keys={A:'A',B:'B'};headers={'Authorization':'Bearer '+A}
    with TestClient(assignment.create_app(path,keys)) as client:
        assert client.get('/records').status_code==401
        response=client.post('/records',headers=headers,json={'category':'Food','cents':125})
        assert response.status_code==201 and response.headers.get('X-Request-ID')
        assert client.post('/records',headers=headers,json={'category':'Food','cents':-1}).status_code==422
        assert client.get('/records',headers={'Authorization':'Bearer '+B}).json()==[]
    with TestClient(assignment.create_app(path,keys)) as client:
        for endpoint in ['/summary','/statistics']:
            report=client.get(endpoint,headers=headers).json()
            assert report['count']==1 and report['total_cents']==125

def test_ingestion_is_atomic_and_repeatable(assignment,tmp_path):
    store=Store(tmp_path/'ledger.db');p=tmp_path/'data.csv'
    p.write_text('date,category,amount\n2025-01-01,Food,0.15\n2025-01-02,Food,0.20\n')
    assignment.ingest(store,'A',p);assignment.ingest(store,'A',p)
    assert store.summary('A')['total_cents']==35 and store.summary('A')['count']==2
    p.write_text('date,category,amount\n2025-01-01,Food,1\n2025-01-02,Food,NaN\n')
    with pytest.raises(ValueError):assignment.ingest(store,'A',p)
    assert store.summary('A')['total_cents']==35
