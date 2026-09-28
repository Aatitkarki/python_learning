import pandas as pd
import pytest

def test_asof_only_previously_published_within_company(assignment):
    decisions=pd.DataFrame({'company':['A','A','A','B'],'decision_time':['2025-03-01','2025-03-02','2025-03-04','2025-03-04']})
    filings=pd.DataFrame({'company':['A','A'],'published_at':['2025-03-01','2025-03-03'],'value':[10,20]})
    result=assignment.publication_join(decisions,filings)
    assert pd.isna(result.iloc[0]['value']) and result.iloc[1]['value']==10
    assert result[result.company=='A'].iloc[-1]['value']==20
    assert result[result.company=='B']['value'].isna().all()

def test_position_precedes_return_and_costs_reduce_wealth(assignment):
    prices=pd.DataFrame({'close':[100,110,99,99]})
    free=assignment.strategy(prices,fee=0);paid=assignment.strategy(prices,fee=.01)
    assert free['position_before_period'].tolist()==[0,0,1,0]
    assert free['net_return'].iloc[2]==pytest.approx(-.1)
    assert paid['wealth'].iloc[-1]<free['wealth'].iloc[-1]
