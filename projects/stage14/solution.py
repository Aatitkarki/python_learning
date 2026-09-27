"""Fictional financial analysis and chronological evaluation, not a trading recommendation."""
import json
from pathlib import Path
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
ROOT=Path(__file__).resolve().parents[2]

def ratios(row):
    r=lambda name:float(row[name])
    revenue=r('revenue'); eps=r('net_income')/r('shares'); market_cap=r('price')*r('shares')
    return {'company':row['company'],'year':int(row['year']),'source_id':row['source_id'],
            'eps':eps,'pe':r('price')/eps if eps>0 else None,'ps':market_cap/revenue,
            'pb':market_cap/r('equity'),'debt_equity':r('debt')/r('equity'),
            'gross_margin':(revenue-r('cost_of_revenue'))/revenue,
            'operating_margin':r('operating_income')/revenue,'net_margin':r('net_income')/revenue,
            'fcf_yield':(r('operating_cash_flow')-r('capex'))/market_cap}

def run():
    financials=pd.read_csv(ROOT/'datasets/financials.csv')
    financials=financials.sort_values(['company','year'])
    financials['avg_equity']=financials.groupby('company').equity.transform(lambda s:(s+s.shift(1))/2)
    financials['avg_assets']=financials.groupby('company').assets.transform(lambda s:(s+s.shift(1))/2)
    financials['revenue_growth']=financials.groupby('company').revenue.pct_change()
    reports=[]
    for _,row in financials.iterrows():
        report=ratios(row)
        report['roe']=float(row.net_income/row.avg_equity) if pd.notna(row.avg_equity) else None
        report['roa']=float(row.net_income/row.avg_assets) if pd.notna(row.avg_assets) else None
        report['revenue_growth']=float(row.revenue_growth) if pd.notna(row.revenue_growth) else None
        reports.append(report)
    prices=pd.read_csv(ROOT/'datasets/prices.csv')
    prices['return']=prices.close.pct_change()
    prices['lag_return']=prices['return'].shift(1)
    prices['lag_mean']=prices['return'].shift(1).rolling(5).mean()
    frame=prices.dropna(); folds=[]
    for train,test in TimeSeriesSplit(n_splits=4,gap=1).split(frame):
        x=frame[['lag_return','lag_mean']]; y=frame['return']
        model=LinearRegression().fit(x.iloc[train],y.iloc[train])
        folds.append({'train_end':int(train[-1]),'test_start':int(test[0]),
                      'model_mae':mean_absolute_error(y.iloc[test],model.predict(x.iloc[test])),
                      'zero_baseline_mae':mean_absolute_error(y.iloc[test],[0]*len(test))})
    return {'ratios':reports,'walk_forward':folds,'units':'Statement amounts and shares in millions; prices per share.',
            'limitation':'Synthetic prices contain no established predictable edge. Market data needs publication-time and corporate-action handling.'}

if __name__=='__main__': print(json.dumps(run(),indent=2,allow_nan=False))
