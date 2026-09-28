import sqlite3
import pytest

@pytest.fixture
def db():
    with sqlite3.connect(':memory:') as connection:
        connection.execute("ATTACH DATABASE ':memory:' AS answer_lab")
        connection.executescript('CREATE TABLE answer_lab.customers(id INTEGER PRIMARY KEY,name TEXT); CREATE TABLE answer_lab.records(id INTEGER PRIMARY KEY,customer_id INTEGER,category_id INTEGER,cents INTEGER); INSERT INTO answer_lab.customers VALUES(1,"A"),(2,"B"),(3,"C"); INSERT INTO answer_lab.records VALUES(1,1,1,100),(2,1,2,200),(3,2,1,50);')
        connection.commit();yield connection

@pytest.mark.parametrize('name,expected',[('inner',[('A',100),('A',200),('B',50)]),('left',[('A',300),('B',50),('C',0)]),('having',[(1,300)]),('cte',[(1,300)]),('missing',[(3,)]),('union',[(1,)]),('window',[(1,100),(2,300),(3,50)])])
def test_query_results_on_fixed_schema(assignment,db,name,expected):
    query=assignment.queries()[name]
    assert isinstance(query,str)
    assert sorted(db.execute(query).fetchall())==sorted(expected)

def test_two_writes_roll_back(assignment,db):
    statements=[];db.set_trace_callback(statements.append)
    assignment.rollback_example(db)
    assert sum(s.lstrip().upper().startswith('INSERT') for s in statements)>=2, 'Demonstrate real writes before rollback; a no-op is not a transaction exercise'
    assert db.execute('SELECT COUNT(*) FROM answer_lab.customers').fetchone()[0]==3
    assert db.execute('SELECT SUM(cents) FROM answer_lab.records').fetchone()[0]==350
