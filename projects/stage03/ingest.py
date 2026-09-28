"""03c: atomic CSV ingestion using either the course SQLite or PostgreSQL store."""
import argparse
import uuid
from decimal import Decimal
from projects.reference import Store
from projects.stage01.solution import load_expenses

def ingest(store,tenant,path):
    rows=load_expenses(path)  # Entire file validated before opening a transaction.
    for row in rows:
        cents=row['amount']*100
        if cents!=cents.to_integral_value(): raise ValueError('Ledger accepts at most two decimal places')
    with store.connection() as db:
        for index,row in enumerate(rows):
            # Deterministic ingestion identity includes row position to preserve legitimate identical purchases.
            key=uuid.uuid5(uuid.NAMESPACE_URL,repr((tenant,index,str(row['date']),row['category'],str(row['amount'])))).hex
            store.execute(db,'INSERT INTO records VALUES(?,?,?,?) ON CONFLICT DO NOTHING',
                          (key,tenant,row['category'],int(row['amount']*100)))
    return store.summary(tenant)

if __name__=='__main__':
    import os
    p=argparse.ArgumentParser();p.add_argument('csv');p.add_argument('--database',default=os.environ.get('DATABASE_URL','work/ingestion-answer.db'));p.add_argument('--tenant',default='A');a=p.parse_args()
    print(ingest(Store(a.database),a.tenant,a.csv))
