import csv
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def test_labels_unique_and_group_disjoint(assignment):
    cases=assignment.reference_cases()
    assert len({c['id'] for c in cases})==len(cases)
    dev=[c for c in cases if c['split']=='dev'];holdout=[c for c in cases if c['split']=='holdout']
    assert len(dev)>=40 and len(holdout)>=20
    assert not {c['group'] for c in dev}&{c['group'] for c in holdout}
    assert all(c['question'] and c['label_status'] for c in cases)

def test_gold_values_recomputed_from_source(assignment):
    with (ROOT/'datasets/financials.csv').open() as file:source={r['source_id']:r for r in csv.DictReader(file)}
    for case in assignment.reference_cases():
        row=source[case['source_id']]
        expected={'revenue':Decimal(row['revenue']),
                  'operating_margin':Decimal(row['operating_income'])/Decimal(row['revenue']),
                  'free_cash_flow':Decimal(row['operating_cash_flow'])-Decimal(row['capex'])}
        assert Decimal(case['expected'])==expected[case['field']]
        assert case['company']==row['company'] and case['year']==int(row['year'])
