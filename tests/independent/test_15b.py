from decimal import Decimal
import pytest

def pair():
    prior=dict(company='Example',year=2024,revenue='80',currency='USD',unit='millions',source_id='old')
    return {**prior,'year':2025,'revenue':'100','source_id':'new'},prior

def test_unseen_feature_calculation_and_both_sources(assignment):
    current,prior=pair();result=assignment.growth(current,prior)
    assert result['status']=='answered' and Decimal(result['value'])==Decimal('.25')
    assert set(result['sources'])=={'old','new'}
    current['revenue']='60';assert Decimal(assignment.growth(current,prior)['value'])==Decimal('-.25')

def test_missing_nonpositive_and_incompatible_history(assignment):
    current,prior=pair()
    assert assignment.growth(current,None)['status']=='unknown'
    for bad in [{**prior,'revenue':'0'},{**prior,'revenue':'-1'},{**prior,'company':'Other'},{**prior,'currency':'EUR'},{**prior,'unit':'thousands'},{**prior,'year':2022}]:
        result=assignment.growth(current,bad)
        assert result['status']=='unknown' and result['value'] is None

def test_nonfinite_data_is_rejected(assignment):
    current,prior=pair();current['revenue']='NaN'
    with pytest.raises(ValueError):assignment.growth(current,prior)
