"""14a/14b: complete ratio conventions, EPS growth/PEG, as-of joins, and net returns."""
import argparse
import csv
import json
from decimal import Decimal
from pathlib import Path
import pandas as pd
from projects.reference import ROOT

def divide(numerator,denominator):return numerator/denominator if denominator>0 else None

def complete_ratios(rows):
    results=[];previous={};seen=set()
    for row in sorted(rows,key=lambda r:(r['company'],int(r['year']))):
        key=(row['company'],int(row['year']))
        if key in seen:raise ValueError('Duplicate company/period')
        seen.add(key);d=lambda name:Decimal(str(row[name]));prior=previous.get(row['company'])
        if d('assets')!=d('liabilities')+d('equity'):raise ValueError('Unbalanced statement')
        if d('shares')<=0:raise ValueError('Positive shares required')
        revenue=d('revenue');eps=d('net_income')/d('shares');market_cap=d('price')*d('shares');pe=divide(d('price'),eps)
        prior_is_comparable=prior is not None and int(row['year'])==int(prior['year'])+1 and row['currency']==prior['currency'] and row['unit']==prior['unit']
        old_eps=Decimal(prior['net_income'])/Decimal(prior['shares']) if prior_is_comparable else None
        eps_growth=divide(eps-old_eps,old_eps) if old_eps is not None else None
        avg_equity=(d('equity')+Decimal(prior['equity']))/2 if prior_is_comparable else None
        avg_assets=(d('assets')+Decimal(prior['assets']))/2 if prior_is_comparable else None
        result={'company':row['company'],'year':int(row['year']),'source_id':row['source_id'],'currency':row['currency'],'published_at':row['published_at'],
                'prior_source_id':prior['source_id'] if prior_is_comparable else None,
                'prior_published_at':prior['published_at'] if prior_is_comparable else None,
                'eps':eps,'eps_growth':eps_growth,'revenue_growth':divide(revenue-Decimal(prior['revenue']),Decimal(prior['revenue'])) if prior_is_comparable else None,
                'pe':pe,'peg_percentage_point_convention':divide(pe,eps_growth*100) if pe is not None and eps_growth is not None else None,
                'ps':divide(market_cap,revenue),'pb':divide(market_cap,d('equity')),'roe':divide(d('net_income'),avg_equity) if avg_equity is not None else None,
                'roa':divide(d('net_income'),avg_assets) if avg_assets is not None else None,'debt_equity':divide(d('debt'),d('equity')),
                'gross_margin':divide(revenue-d('cost_of_revenue'),revenue),'operating_margin':divide(d('operating_income'),revenue),
                'net_margin':divide(d('net_income'),revenue),'fcf':d('operating_cash_flow')-d('capex'),'fcf_yield':divide(d('operating_cash_flow')-d('capex'),market_cap)}
        results.append({k:str(v) if isinstance(v,Decimal) else v for k,v in result.items()});previous[row['company']]=row
    return results

def publication_join(decisions,filings):
    decisions=decisions.copy();filings=filings.copy()
    decisions['decision_time']=pd.to_datetime(decisions['decision_time']);filings['published_at']=pd.to_datetime(filings['published_at'])
    return pd.merge_asof(decisions.sort_values('decision_time'),filings.sort_values('published_at'),left_on='decision_time',right_on='published_at',by='company',direction='backward',allow_exact_matches=False)

def strategy(frame,fee=.001):
    returns=frame.close.pct_change().fillna(0)
    position=(returns.shift(1)>0).astype(float)
    turnover=position.diff().abs();turnover.iloc[0]=abs(position.iloc[0])
    net=position*returns-fee*turnover
    return pd.DataFrame({'return':returns,'position_before_period':position,'turnover':turnover,'net_return':net,'wealth':(1+net).cumprod()})

def run(output):
    from projects.stage14.solution import run as walk_forward
    with (ROOT/'datasets/financials.csv').open() as handle:rows=list(csv.DictReader(handle))
    decisions=pd.DataFrame({'company':['Aurora','Aurora'],'decision_time':['2024-02-01','2024-03-02']})
    joined=publication_join(decisions,pd.DataFrame(rows)[['company','source_id','published_at']])
    out=Path(output);out.mkdir(parents=True,exist_ok=True);joined.to_csv(out/'asof.csv',index=False)
    strategy(pd.read_csv(ROOT/'datasets/prices.csv')).to_csv(out/'strategy.csv',index=False)
    report={'ratios':complete_ratios(rows),'asof_sources':[None if pd.isna(v) else v for v in joined.source_id],
            'walk_forward':walk_forward()['walk_forward'],
            'limits':'Fictional financials and random prices. Net return example omits spread, slippage, financing, and market impact; it establishes no investment edge.'}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='work/reference_answers/stage14');a=p.parse_args();print(json.dumps(run(a.output),indent=2))
