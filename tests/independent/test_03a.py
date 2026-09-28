import pandas as pd
import pytest

def test_quarantine_and_calendar_arithmetic(assignment):
    frame=pd.DataFrame({'date':['2025-01-01','2025-01-01','bad','2025-01-03'],'category':['Food']*4,'amount':[9,9,2,3]})
    original=frame.copy(deep=True);valid,bad,rolling,report=assignment.clean(frame)
    pd.testing.assert_frame_equal(frame,original)
    assert len(valid)==2 and set(bad['reason'])=={'invalid_date','exact_duplicate'}
    assert set(bad['source_row'])=={3,4}
    assert rolling.loc['2025-01-03']==4
    assert report['input_rows']==report['valid_rows']+report['quarantined_rows']

def test_blank_nonfinite_and_empty_input(assignment):
    frame=pd.DataFrame({'date':['2025-01-01']*2,'category':['','Food'],'amount':[1,float('inf')]})
    valid,bad,rolling,report=assignment.clean(frame)
    assert len(valid)==0 and len(bad)==2 and len(rolling)==0
    with pytest.raises(ValueError):assignment.clean(pd.DataFrame({'amount':[1]}))
