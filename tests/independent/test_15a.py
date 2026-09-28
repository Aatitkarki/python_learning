import copy
from fastapi.testclient import TestClient

def test_report_via_http_and_tampered_values(assignment,tmp_path):
    keys={'capstone-A-012345678901234567':'A','capstone-B-012345678901234567':'B'}
    body={'companies':['Aurora','Beacon'],'years':[2023,2024,2025]}
    with TestClient(assignment.create_app(tmp_path/'api.db',keys,seed=True)) as client:
        headers={'Authorization':'Bearer '+next(iter(keys))}
        response=client.post('/compare',headers=headers,json=body)
        assert response.status_code==200
        rows=response.json()['rows'];assert assignment.verify_rows(rows)
        altered=copy.deepcopy(rows);altered[0]['revenue']='9999'
        assert not assignment.verify_rows(altered)
        altered=copy.deepcopy(rows);altered[0]['source_id']='fabricated'
        assert not assignment.verify_rows(altered)
        assert not assignment.verify_rows(rows[:5]+[rows[0]])
        assert client.post('/compare',headers={'Authorization':'Bearer '+list(keys)[1]},json=body).status_code==404
        for request in [{'companies':['Unknown'],'years':[2025]},{'companies':['Aurora'],'years':[1900]}]:
            assert client.post('/compare',headers=headers,json=request).status_code==404
