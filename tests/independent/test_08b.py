import pytest
from langgraph.types import Command

def test_graph_interrupt_fingerprint_and_isolation(assignment):
    graph=assignment.build();config={'configurable':{'thread_id':'learner-A'}}
    state={'actor':'A','proposal':{'operation':'divide','a':12,'b':10}}
    assert '__interrupt__' in graph.invoke(state,config)
    result=graph.invoke(Command(resume={'approved':True,'fingerprint':assignment.fingerprint(state)}),config)
    assert result['result']==1.2
    assert not graph.get_state({'configurable':{'thread_id':'learner-B'}}).values
    other={'configurable':{'thread_id':'altered'}};graph.invoke(state,other)
    result=graph.invoke(Command(resume={'approved':True,'fingerprint':'wrong'}),other)
    assert result['status']=='denied'

def test_durable_review_reopen_and_single_use(assignment,tmp_path):
    path=tmp_path/'approval.db';f=assignment.ReviewStore(path).propose('r','A',{'value':4},now=10,ttl=5)
    restarted=assignment.ReviewStore(path)
    with pytest.raises(PermissionError):restarted.resume('r','B',f,True,lambda p:p,now=11)
    assert restarted.resume('r','A',f,True,lambda p:p['value']*2,now=11)['result']==8
    with pytest.raises(ValueError):restarted.resume('r','A',f,True,lambda p:p,now=12)
    f=restarted.propose('expired','A',{},now=10,ttl=5)
    with pytest.raises(ValueError):restarted.resume('expired','A',f,True,lambda p:p,now=15)
