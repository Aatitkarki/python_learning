"""03a: inspect, quarantine, deduplicate, and report a time-based rolling mean."""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
from projects.reference import ROOT

def clean(frame):
    required={'date','category','amount'}
    if not required<=set(frame): raise ValueError('Missing required columns')
    data=frame.copy();data['source_row']=np.arange(len(data))+2
    dates=pd.to_datetime(data['date'],errors='coerce')
    amounts=pd.to_numeric(data['amount'],errors='coerce')
    categories=data['category'].fillna('').astype(str).str.strip()
    reasons=[]
    for i in range(len(data)):
        errors=[]
        if pd.isna(dates.iloc[i]):errors.append('invalid_date')
        if not np.isfinite(amounts.iloc[i]) or amounts.iloc[i]<0:errors.append('invalid_amount')
        if not categories.iloc[i]:errors.append('blank_category')
        reasons.append(';'.join(errors))
    data['reason']=reasons
    rejected=data[data.reason!=''].copy()
    valid=data[data.reason==''].copy()
    valid['date']=dates.loc[valid.index];valid['amount']=amounts.loc[valid.index];valid['category']=categories.loc[valid.index]
    duplicates=valid.duplicated(['date','category','amount'],keep='first')
    duplicate_rows=valid[duplicates].copy();duplicate_rows['reason']='exact_duplicate'
    valid=valid[~duplicates].sort_values(['date','source_row'])
    quarantine=pd.concat([rejected,duplicate_rows]).sort_values('source_row')
    # Complete calendar, explicit assumption: no rows on a day means zero recorded spending.
    daily=valid.groupby('date').amount.sum().resample('D').sum() if len(valid) else pd.Series(dtype=float,index=pd.DatetimeIndex([]))
    rolling=daily.rolling('3D',min_periods=1).mean()
    q1,q3=valid.amount.quantile([.25,.75]) if len(valid) else (np.nan,np.nan)
    outliers=valid[(valid.amount<q1-1.5*(q3-q1))|(valid.amount>q3+1.5*(q3-q1))]
    report={'input_rows':len(frame),'valid_rows':len(valid),'quarantined_rows':len(quarantine),
            'missing':{k:int(v) for k,v in frame.isna().sum().items()},'outlier_rows':outliers.source_row.tolist(),
            'date_min':str(valid.date.min()) if len(valid) else None,'date_max':str(valid.date.max()) if len(valid) else None,
            'policy':'Exact duplicates quarantined only for this fixture; real identical purchases may be legitimate. Outliers flagged, not deleted. Calendar gaps mean zero recorded spending, not proof of no activity.'}
    return valid,quarantine,rolling,report

def run(path,output):
    valid,rejected,rolling,report=clean(pd.read_csv(path));out=Path(output);out.mkdir(parents=True,exist_ok=True)
    valid.to_csv(out/'clean.csv',index=False);rejected.to_csv(out/'quarantine.csv',index=False)
    rolling.rename('three_day_mean').to_csv(out/'rolling.csv');(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',default=str(ROOT/'datasets/expenses.csv'));p.add_argument('--output',default='work/reference_answers/stage03');a=p.parse_args();print(json.dumps(run(a.input,a.output),indent=2))
