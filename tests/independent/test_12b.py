import pytest
from projects.reference import Store

def test_allowed_denied_warm_cache_and_revocation(assignment,tmp_path):
    store=Store(tmp_path/'scope.db');store.seed()
    scoped=assignment.ScopedDocuments(store,{'userA':'A','userB':'B'})
    assert scoped.get('userB','b-private')['id']=='b-private'
    with pytest.raises(PermissionError):scoped.get('userA','b-private')
    assert scoped.get('userA','policy-public')['id']=='policy-public'
    scoped.revoke('userB')
    with pytest.raises(PermissionError):scoped.get('userB','b-private')

def test_every_endpoint_has_two_tenants_and_anonymous_checks(assignment,tmp_path):
    rows=assignment.endpoint_matrix(tmp_path/'api.db')
    expected={('get','/health'),('get','/ready'),('get','/records'),('post','/records'),('get','/summary'),('get','/statistics'),('post','/documents'),('get','/search?q=expense'),('post','/answer'),('post','/compare')}
    for user in ['alice','alex','bob','blair','anonymous']:
        selected=[r for r in rows if r['user']==user]
        assert {(r['method'],r['route']) for r in selected}==expected
        assert all(r['passed'] and r['expected']==r['observed'] for r in selected)
