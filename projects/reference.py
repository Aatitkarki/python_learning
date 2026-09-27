"""Shared instructional application: typed data, tenant-scoped queries, grounded reports.

SQLite is the zero-service default. A PostgreSQL DSN selects psycopg instead.
This is a teaching baseline; see the operational completion gates before deployment.
"""
import csv
import hashlib
import json
import math
import re
import sqlite3
from contextlib import contextmanager
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def terms(text): return set(re.findall(r'[a-z0-9]+', text.lower()))

class Store:
    def __init__(self, location):
        self.location = str(location)
        self.postgres = self.location.startswith(('postgresql://','postgres://'))
        if not self.postgres:
            if self.location == ':memory:': raise ValueError('Use a temporary file: each operation opens its own connection')
            Path(self.location).parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as db:
            for statement in [
                'CREATE TABLE IF NOT EXISTS documents (id TEXT NOT NULL, tenant TEXT NOT NULL, public INTEGER NOT NULL DEFAULT 0, text TEXT NOT NULL, source TEXT NOT NULL, PRIMARY KEY (tenant,id))',
                'CREATE TABLE IF NOT EXISTS financials (tenant TEXT NOT NULL, company TEXT NOT NULL, year INTEGER NOT NULL, body TEXT NOT NULL, PRIMARY KEY (tenant,company,year))',
                'CREATE TABLE IF NOT EXISTS records (id TEXT PRIMARY KEY, tenant TEXT NOT NULL, category TEXT NOT NULL, cents BIGINT NOT NULL CHECK(cents >= 0))']:
                db.execute(statement)
    @contextmanager
    def connection(self):
        if self.postgres:
            import psycopg
            from psycopg.rows import dict_row
            db=psycopg.connect(self.location, row_factory=dict_row, connect_timeout=5,
                                options='-c statement_timeout=5000')
        else:
            db=sqlite3.connect(self.location,timeout=5)
            db.row_factory=sqlite3.Row
        try:
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally: db.close()
    def execute(self, db, sql, values=()):
        # Only fixed, developer-authored SQL reaches this method.
        return db.execute(sql.replace('?', '%s') if self.postgres else sql, values)
    def seed(self):
        with self.connection() as db:
            for d in json.loads((ROOT/'datasets/documents.json').read_text()):
                self.execute(db,'INSERT INTO documents VALUES(?,?,?,?,?) ON CONFLICT DO NOTHING',
                    (d['id'],d['tenant'],int(d['public']),d['text'],d['source']))
            with (ROOT/'datasets/financials.csv').open(newline='',encoding='utf-8') as handle:
                for row in csv.DictReader(handle):
                    self.execute(db,'INSERT INTO financials VALUES(?,?,?,?) ON CONFLICT DO NOTHING',
                        (row['tenant'],row['company'],int(row['year']),json.dumps(row)))
    def documents(self, tenant):
        with self.connection() as db:
            return [dict(row) for row in self.execute(db,
                'SELECT id,tenant,public,text,source FROM documents WHERE tenant=? OR public=1 ORDER BY tenant,id',(tenant,))]
    def add_document(self, tenant, text, source, public=False):
        digest=hashlib.sha256((tenant+'\0'+source+'\0'+text).encode()).hexdigest()[:24]
        with self.connection() as db:
            self.execute(db,'INSERT INTO documents VALUES(?,?,?,?,?) ON CONFLICT DO NOTHING',
                         (digest,tenant,int(public),text,source))
        return digest
    def search(self, tenant, query, k=3):
        query_terms=terms(query)
        scored=[]
        for d in self.documents(tenant):
            shared=query_terms & terms(d['text'])
            score=len(shared)/len(query_terms) if query_terms else 0.
            if score:
                scored.append({**d,'score':score})
        return sorted(scored,key=lambda d:(-d['score'],d['tenant'],d['id']))[:k]
    def compare(self, tenant, companies, years):
        result=[]
        with self.connection() as db:
            for company in companies:
                for year in sorted(years):
                    row=self.execute(db,'SELECT body FROM financials WHERE tenant=? AND company=? AND year=?',
                                     (tenant,company,year)).fetchone()
                    if row is None: raise LookupError('Requested company/period is unavailable')
                    data=json.loads(row['body']); revenue=Decimal(data['revenue'])
                    result.append({'company':company,'year':year,'currency':data['currency'],'unit':'millions',
                        'revenue':str(revenue),'operating_margin':str(Decimal(data['operating_income'])/revenue),
                        'free_cash_flow':str(Decimal(data['operating_cash_flow'])-Decimal(data['capex'])),
                        'source_id':data['source_id'],'published_at':data['published_at']})
        return result
    def add_record(self, tenant, category, cents):
        import uuid
        id=uuid.uuid4().hex
        with self.connection() as db:
            self.execute(db,'INSERT INTO records VALUES(?,?,?,?)',(id,tenant,category,cents))
        return {'id':id,'category':category,'cents':cents}
    def records(self, tenant, limit=100, offset=0):
        with self.connection() as db:
            return [dict(row) for row in self.execute(db,'SELECT id,category,cents FROM records WHERE tenant=? ORDER BY id LIMIT ? OFFSET ?', (tenant,limit,offset))]
    def summary(self, tenant):
        with self.connection() as db:
            row=self.execute(db,'SELECT COUNT(*) AS count, COALESCE(SUM(cents),0) AS total_cents, AVG(cents) AS average_cents, MAX(cents) AS max_cents FROM records WHERE tenant=?',(tenant,)).fetchone()
            return dict(row)

def evidence_answer(store, tenant, question):
    hits=store.search(tenant,question)
    # Evidence-only: no unsupported synthesized answer and no claim of semantic QA.
    return {'status':'evidence' if hits else 'unsupported',
            'citations':[{'id':d['id'],'source':d['source'],'quote':d['text']} for d in hits],
            'answer': None, 'mode':'lexical evidence baseline'}
