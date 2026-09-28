from decimal import Decimal
import math
import pytest

@pytest.mark.parametrize('text,expected',[('Aurora revenue was $1.2 billion.',1200000000),('Beacon revenue was $25 million.',25000000)])
def test_extraction_units_and_exact_source_span(assignment,text,expected):
    result=assignment.extract_revenue(text)
    assert result['status']=='supported' and Decimal(result['revenue'])==expected
    assert text[result['start']:result['end']]==result['quote'] and result['currency']=='USD'

@pytest.mark.parametrize('text',['Revenue was not disclosed','Aurora revenue was 20 million.','Aurora revenue was $2 million. Beacon revenue was $3 million.'])
def test_unsupported_or_ambiguous_is_unknown(assignment,text):assert assignment.extract_revenue(text)['status']=='unknown'

def test_local_adapter_backward_step(assignment):
    result=assignment.offline_smoke()
    assert math.isfinite(result['loss']) and result['trainable_parameters']>0
    # This does not establish a downloaded pretrained model's quality.
