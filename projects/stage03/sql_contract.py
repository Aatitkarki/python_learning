"""Portable query/rollback adapter for testing the independent SQL assignment offline.
PostgreSQL-specific EXPLAIN and ingestion remain separate integration checks.
"""
from pathlib import Path

def queries():
    lines=(Path(__file__).with_name('queries.sql')).read_text().splitlines()
    return {
        'inner':next(x for x in lines if x.startswith('SELECT c.name,r.cents')),
        'left':next(x for x in lines if x.startswith('SELECT c.name,COALESCE')),
        'having':next(x for x in lines if 'HAVING SUM' in x),
        'cte':next(x for x in lines if x.startswith('WITH totals'))+' '+next(x for x in lines if x.startswith('SELECT * FROM totals')),
        'missing':next(x for x in lines if x.startswith('SELECT c.id')),
        'union':next(x for x in lines if ' UNION ' in x),
        'window':next(x for x in lines if 'OVER(PARTITION' in x),
    }

def rollback_example(connection):
    connection.execute('BEGIN')
    try:
        connection.execute("INSERT INTO answer_lab.customers VALUES (9001,'temporary')")
        connection.execute('INSERT INTO answer_lab.records VALUES (9001,9001,1,5)')
    finally:
        connection.rollback()
