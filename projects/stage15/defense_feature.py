"""Worked independent defense feature: comparable annual revenue growth with sources.
The caller must authorize both rows before invoking this pure arithmetic helper.
"""
from decimal import Decimal

def growth(current, prior):
    if prior is None:
        return {'status':'unknown','reason':'missing_prior','value':None,'sources':[]}
    if any(current[k]!=prior[k] for k in ['company','currency','unit']) or int(current['year'])!=int(prior['year'])+1:
        return {'status':'unknown','reason':'not_comparable','value':None,'sources':[]}
    new,old=Decimal(str(current['revenue'])),Decimal(str(prior['revenue']))
    if not new.is_finite() or not old.is_finite():raise ValueError('Finite revenue required')
    if old<=0:
        return {'status':'unknown','reason':'nonpositive_base','value':None,'sources':[]}
    return {'status':'answered','value':str((new-old)/old),'sources':[prior['source_id'],current['source_id']]}
