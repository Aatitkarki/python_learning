from projects.reference import Store

def test_typed_tool_success_and_budgets(assignment,tmp_path):
    store=Store(tmp_path/'tools.db');store.seed()
    workflow=assignment.ResearchWorkflow(store,'A',max_calls=1)
    call={'tool':'divide','arguments':{'numerator':9,'denominator':3}}
    result=workflow.run([call]);assert result['status']=='complete' and result['observations'][0]['result']==3
    result=workflow.run([call,call]);assert result['status']=='budget_exhausted' and len(result['observations'])==1

def test_unknown_tool_bad_arguments_and_tenant_spoofing(assignment,tmp_path):
    store=Store(tmp_path/'tools.db');store.seed();workflow=assignment.ResearchWorkflow(store,'A')
    for call in [{'tool':'shell','arguments':{}},{'tool':'divide','arguments':{'numerator':1,'denominator':0}},
                 {'tool':'search','arguments':{'query':'Cedar','tenant':'B'}},{'tool':'divide','arguments':{'numerator':float('nan'),'denominator':2}}]:
        assert workflow.run([call])['status']=='failed'
    result=workflow.run([{'tool':'search','arguments':{'query':'Cedar'}}])
    assert not any(d['id']=='b-private' for d in result['observations'][0]['result'])
