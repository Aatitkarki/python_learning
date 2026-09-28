import copy
import csv
from decimal import Decimal
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2]

def rows():
    with (ROOT/'datasets/financials.csv').open() as file:return list(csv.DictReader(file))

def test_ratios_and_sources(assignment):
    result=assignment.complete_ratios(rows());lookup={(r['company'],r['year']):r for r in result}
    first=lookup['Aurora',2023];last=lookup['Aurora',2025]
    assert first['revenue_growth'] is None and first['roe'] is None
    assert Decimal(last['revenue_growth'])==Decimal('.2')
    assert Decimal(last['operating_margin'])==Decimal('.25') and Decimal(last['fcf'])==24
    assert last['source_id']=='aurora-2025' and last['prior_source_id']=='aurora-2024'
    assert {'eps','eps_growth','pe','ps','pb','roe','roa','debt_equity','gross_margin','net_margin','fcf_yield'}<=set(last)

def test_incompatible_units_or_missing_year_has_no_growth(assignment):
    source=[r for r in rows() if r['company']=='Aurora']
    source[1]['unit']='different'
    result=assignment.complete_ratios(source)
    assert result[1]['revenue_growth'] is None and result[2]['revenue_growth'] is None
    result=assignment.complete_ratios([source[0],source[2]])
    assert result[1]['revenue_growth'] is None

def test_unbalanced_or_duplicate_statement_rejected(assignment):
    source=rows();bad=copy.deepcopy(source);bad[0]['assets']='99999'
    with pytest.raises(ValueError):assignment.complete_ratios(bad)
    with pytest.raises(ValueError):assignment.complete_ratios(source+[source[0]])
