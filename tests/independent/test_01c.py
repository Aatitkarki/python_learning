from decimal import Decimal
import pytest

def test_exact_csv_totals_quoted_field_and_months(assignment,tmp_path):
    p=tmp_path/'expenses.csv';p.write_text('date,category,amount\n2025-01-01,"Food, cafe",0.10\n2025-02-02,Books,0.20\n')
    rows=assignment.load_expenses(p);result=assignment.summarize(rows)
    assert Decimal(result['total'])==Decimal('.30') and result['count']==2
    assert Decimal(result['highest'])==Decimal('.20') and Decimal(result['average'])==Decimal('.15')
    assert 'Food, cafe' in result['by_category']
    assert set(result['by_month'])=={'2025-01','2025-02'}

def test_empty_csv_contract(assignment,tmp_path):
    p=tmp_path/'empty.csv';p.write_text('date,category,amount\n')
    result=assignment.summarize(assignment.load_expenses(p))
    assert result['count']==0 and Decimal(result['total'])==0
    assert result['average'] is None and result['highest'] is None

@pytest.mark.parametrize('row',['bad,Food,1','2025-01-01,Food,NaN','2025-01-01,Food,-1','2025-01-01,,1'])
def test_bad_row_points_to_line(assignment,tmp_path,row):
    p=tmp_path/'bad.csv';p.write_text('date,category,amount\n'+row+'\n')
    with pytest.raises(ValueError,match='(?i)line 2'):assignment.load_expenses(p)

def test_missing_columns(assignment,tmp_path):
    p=tmp_path/'bad.csv';p.write_text('category,amount\nFood,1\n')
    with pytest.raises(ValueError):assignment.load_expenses(p)
