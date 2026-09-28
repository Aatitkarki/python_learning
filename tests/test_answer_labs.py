"""Regression checks for formerly missing answers, including required beginner cases."""
import json
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch
import numpy as np
import pandas as pd
import pytest
from projects.stage01.calculator import calculate,temperature,profit,bmi
from projects.stage01.contacts import ContactBook
from projects.stage01.text_analyzer import analyze
from projects.stage01.inventory import Inventory,summarize_inventory
from projects.stage01.algorithms import factorial,directory_bytes
from projects.stage02.math_lab import rotate,matmul,gradient_check,variance,permutation_test
from projects.stage03.data_lab import clean
from projects.stage03.ingest import ingest
from projects.reference import Store,ROOT

@pytest.mark.parametrize('a,op,b,expected',[(1,'+',2,3),(2,'-',5,-3),(2,'*',3,6),(9,'/',2,4.5),(0,'+',0,0)])
def test_calculator_valid(a,op,b,expected):assert calculate(a,op,b)==expected
@pytest.mark.parametrize('a,op,b,error',[(1,'/',0,ZeroDivisionError),('bad','+',1,ValueError),(float('nan'),'+',1,ValueError),(1,'eval',1,ValueError),(1e308,'*',1e308,ValueError)])
def test_calculator_invalid(a,op,b,error):
    with pytest.raises(error):calculate(a,op,b)
@pytest.mark.parametrize('value,source,target,expected',[(0,'C','F',32),(100,'C','F',212),(32,'F','C',0),(-40,'F','C',-40),(20,'C','C',20)])
def test_temperature(value,source,target,expected):assert temperature(value,source,target)==expected
@pytest.mark.parametrize('values,expected',[((100,110,10),100),((10,5,2),-10),((0,3,2),6),((1,1,1),0),((1,2,.5),.5)])
def test_profit(values,expected):assert profit(*values)==expected
@pytest.mark.parametrize('mass,height,expected',[(80,2,20),(45,1.5,20),(100,2,25),(18,1,18),(50,2,12.5)])
def test_bmi_arithmetic(mass,height,expected):assert bmi(mass,height)==expected

def test_loop_recovers_and_does_not_hide_unexpected_error():
    from projects.stage01.calculator import main
    commands=iter(['calc bad + 2','temp 0 C F','calc 1 / 0','profit 10 12 5','quit']);output=[]
    main(lambda prompt:next(commands),output.append)
    assert '32.0' in output and '10.0' in output and sum(x.startswith('Input error') for x in output)==2
    with pytest.raises(RuntimeError):main(lambda prompt:(_ for _ in ()).throw(RuntimeError('bug')),output.append)

def test_contact_crud_copy_and_roundtrip(tmp_path):
    book=ContactBook();book.add(' ADA@example.test ','Ada','123')
    with pytest.raises(ValueError):book.add('ada@EXAMPLE.test','Other')
    found=book.search('ada');found[0]['name']='changed';assert book.search('ada')[0]['name']=='Ada'
    book.update('ada@example.test',phone='456');path=tmp_path/'contacts.json';book.save(path)
    loaded=ContactBook.load(path);assert loaded.search('456')[0]['email']=='ada@example.test'
    assert loaded.delete('ada@example.test') and not loaded.delete('ada@example.test')
    with pytest.raises(KeyError):loaded.update('unknown@example.test',name='X')

def test_text_and_inventory_boundaries(tmp_path):
    assert analyze('B a b A!')['top_words']==[('a',2),('b',2)]
    assert analyze('...')['most_common'] is None
    first,second=Inventory(),Inventory();first.change('book',2)
    with pytest.raises(ValueError):first.change('book',-3)
    assert first.items=={'book':2} and second.items=={}
    path=tmp_path/'stock.csv';path.write_text('sku,quantity,unit_price\nbook,3,0.10\n')
    assert Decimal(summarize_inventory(path)['total_value'])==Decimal('.30')

@pytest.mark.parametrize('contents',['sku,quantity,unit_price\n','sku,quantity,unit_price\na,0,2\n'])
def test_inventory_empty_or_zero(tmp_path,contents):
    p=tmp_path/'stock.csv';p.write_text(contents);assert Decimal(summarize_inventory(p)['total_value'])==0
@pytest.mark.parametrize('row',['a,-1,1','a,1,NaN','a,1,Infinity','a,1.5,2','a,1,2\na,2,2'])
def test_inventory_rejections(tmp_path,row):
    p=tmp_path/'stock.csv';p.write_text('sku,quantity,unit_price\n'+row+'\n')
    with pytest.raises(ValueError):summarize_inventory(p)

def test_composed_expense_file_failure():
    from projects.stage01.expense_app.domain import ExpenseAnalyzer
    from projects.stage01.expense_app.parser import CsvRepository
    from projects.stage01.expense_app.cli import main
    with patch.object(Path,'open',side_effect=PermissionError('denied')):
        assert main(['unreadable.csv'])==2
    assert ExpenseAnalyzer(CsvRepository(ROOT/'datasets/expenses.csv')).report()['total']=='100.00'

def test_recursion_symlink_and_math(tmp_path):
    (tmp_path/'a').write_bytes(b'abc');(tmp_path/'cycle').symlink_to(tmp_path,target_is_directory=True)
    assert directory_bytes(tmp_path)==3 and factorial(0)==1 and factorial(5)==120
    assert np.allclose(rotate([2,1],np.pi/2),[-1,2])
    assert matmul([[1,2]],[[3],[4]])==[[11]] and variance([1,2,3])==1
    assert gradient_check([-1,0,1],[-1,1,3])<1e-6
    assert permutation_test([1,2],[8,9],seed=42)==permutation_test([1,2],[8,9],seed=42)

def test_quarantine_and_calendar_window():
    frame=pd.DataFrame({'date':['2026-01-01','2026-01-01','bad','2026-01-03'], 'category':['Food']*4,'amount':[9,9,2,3]})
    valid,bad,rolling,report=clean(frame)
    assert len(valid)==2 and set(bad.reason)=={'invalid_date','exact_duplicate'}
    assert rolling.loc['2026-01-03']==4  # (9+0+3)/3, not three observed transactions.

def test_atomic_idempotent_ingestion(tmp_path):
    store=Store(tmp_path/'db.sqlite')
    assert ingest(store,'A',ROOT/'datasets/expenses.csv')['total_cents']==10000
    assert ingest(store,'A',ROOT/'datasets/expenses.csv')['count']==6
    invalid=tmp_path/'invalid.csv';invalid.write_text('date,category,amount\n2026-01-01,Food,2\n2026-01-02,Food,0.001\n')
    with pytest.raises(ValueError):ingest(store,'A',invalid)
    assert store.summary('A')['count']==6

def test_decoding_and_source_bound_extraction():
    from projects.stage06.attention_lab import probabilities,extract_revenue
    p=probabilities([1,2,3,4],top_k=2);assert sum(p>0)==2 and np.isclose(sum(p),1)
    p=probabilities([0,0,0,0],top_p=.5);assert sum(p>0)==2
    text='Aurora revenue was $1.2 billion.';result=extract_revenue(text)
    assert result['revenue']=='1200000000' and text[result['start']:result['end']]==result['quote']
    assert extract_revenue('Revenue might grow')['status']=='unknown'
    assert extract_revenue(text+' Beacon revenue was $1 million.')['status']=='unknown'

def test_real_kv_cache_matches_uncached_and_blocks_future():
    import torch
    from projects.stage06.cache_lab import CachedLM,cache_agreement
    torch.manual_seed(42);torch.set_num_threads(1);model=CachedLM(20,blocks=2).eval();ids=torch.tensor([[1,2,3,4]])
    assert cache_agreement(model,ids)<1e-5
    changed=ids.clone();changed[0,-1]=9
    assert torch.allclose(model(ids)[0][:,:3],model(changed)[0][:,:3],atol=1e-6)

def test_chunk_offsets_hashes_and_tenant_ranking():
    from projects.stage07.retrieval_lab import chunks,rankings
    document={'id':'d','tenant':'A','public':False,'text':'a  b\nc d e','source':'x'}
    parts=chunks(document,3,1)
    assert all(document['text'][c['start']:c['end']]==c['text'] for c in parts)
    private={'id':'b','tenant':'B','public':False,'text':'Cedar secret','source':'private'}
    modes=rankings('Cedar',parts+chunks(private),'A');assert all(not hits for hits in modes.values())

def test_durable_approval_restart_expiry_and_replay(tmp_path):
    from projects.stage08.workflow_lab import ReviewStore
    path=tmp_path/'review.sqlite';fingerprint=ReviewStore(path).propose('one','A',{'value':2},now=10,ttl=5)
    store=ReviewStore(path)
    with pytest.raises(PermissionError):store.resume('one','B',fingerprint,True,lambda p:p,now=11)
    with pytest.raises(ValueError):store.resume('one','A','altered',True,lambda p:p,now=11)
    assert store.resume('one','A',fingerprint,True,lambda p:p['value']*2,now=11)['result']==4
    with pytest.raises(ValueError):store.resume('one','A',fingerprint,True,lambda p:p,now=12)
    f=store.propose('two','A',{},now=10,ttl=5)
    with pytest.raises(ValueError):store.resume('two','A',f,True,lambda p:p,now=15)

def test_benchmark_counts_failed_requests():
    from projects.stage09.benchmark import measure,memory_budget
    def fail():raise TimeoutError()
    report=measure(fail,3,2);assert report['failures']==3 and report['tokens_per_wall_second'] is None
    assert len(memory_budget())==27

def test_paired_groups_and_gold_split():
    from projects.stage13.evaluation_lab import reference_cases,paired_interval
    cases=reference_cases();train={r['group'] for r in cases if r['split']=='dev'};test={r['group'] for r in cases if r['split']=='holdout'}
    assert not train&test
    interval=paired_interval([0,0,1,1],[1,1,1,1],['a','a','b','b'])
    assert interval['delta']==.5 and interval['groups']==2

def test_asof_excludes_not_yet_published_and_current_signal():
    from projects.stage14.finance_lab import publication_join,strategy
    decisions=pd.DataFrame({'company':['A','A'],'decision_time':['2025-03-01','2025-03-02']})
    filings=pd.DataFrame({'company':['A'],'published_at':['2025-03-01'],'value':[12]})
    joined=publication_join(decisions,filings);assert pd.isna(joined.value.iloc[0]) and joined.value.iloc[1]==12
    result=strategy(pd.DataFrame({'close':[100,110,99]}),fee=0)
    assert result.position_before_period.tolist()==[0,0,1]
