"""Run: python -m uvicorn projects.api:app --host 127.0.0.1 --port 8000."""
import hmac
import json
import logging
import os
import sqlite3
import time
import uuid
from collections import defaultdict, deque
from threading import Lock
from fastapi import FastAPI, Depends, Header, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ConfigDict
from projects.reference import Store, evidence_answer, ROOT

class RecordInput(BaseModel):
    model_config=ConfigDict(extra='forbid')
    category: str = Field(min_length=1,max_length=50,pattern=r'.*\S.*')
    cents: int = Field(ge=0,le=10**12,strict=True)
class DocumentInput(BaseModel):
    model_config=ConfigDict(extra='forbid')
    text: str = Field(min_length=1,max_length=20000,pattern=r'.*\S.*')
    source: str = Field(min_length=1,max_length=200)
class Question(BaseModel):
    model_config=ConfigDict(extra='forbid')
    question: str = Field(min_length=1,max_length=4000,pattern=r'.*\S.*')
class Comparison(BaseModel):
    model_config=ConfigDict(extra='forbid')
    companies: list[str] = Field(min_length=1,max_length=5)
    years: list[int] = Field(min_length=1,max_length=10)

def create_app(location=None, keys=None, seed=False, limit_per_minute=60):
    app=FastAPI(title='Learning Research API',version='1.0')
    store=Store(location or os.environ.get('DATABASE_URL',str(ROOT/'work/course.db')))
    if seed: store.seed()
    raw=keys if keys is not None else json.loads(os.environ.get('COURSE_API_KEYS','{}'))
    if not isinstance(raw,dict) or any(not isinstance(k,str) or len(k)<24 or not isinstance(v,str) or not v for k,v in raw.items()):
        raise ValueError('COURSE_API_KEYS must map keys of at least 24 characters to tenant names')
    # Store only hashes for request comparison. The source environment still needs protection.
    principals=[( __import__('hashlib').sha256(k.encode()).digest(),v) for k,v in raw.items()]
    buckets=defaultdict(deque); lock=Lock()
    def principal(authorization: str=Header(default='')):
        import hashlib
        if not authorization.startswith('Bearer '): raise HTTPException(401,'Authentication required')
        digest=hashlib.sha256(authorization[7:].encode()).digest()
        tenant=next((t for expected,t in principals if hmac.compare_digest(digest,expected)),None)
        if tenant is None: raise HTTPException(401,'Invalid credentials')
        now=time.monotonic()
        with lock:
            bucket=buckets[digest]
            while bucket and now-bucket[0]>=60: bucket.popleft()
            if len(bucket)>=limit_per_minute: raise HTTPException(429,'Rate limit exceeded',headers={'Retry-After':'60'})
            bucket.append(now)
        return tenant
    @app.middleware('http')
    async def audit(request, call_next):
        request_id=uuid.uuid4().hex; started=time.monotonic()
        response=await call_next(request)
        response.headers['X-Request-ID']=request_id
        logging.getLogger('course').info(json.dumps({'request_id':request_id,'status':response.status_code,'latency_ms':round((time.monotonic()-started)*1000,2)}))
        return response
    @app.get('/health')
    def health(): return {'status':'alive'}
    @app.get('/ready')
    def ready():
        try:
            with store.connection() as db: db.execute('SELECT 1')
        except Exception: raise HTTPException(503,'Database unavailable') from None
        return {'status':'ready'}
    @app.get('/records')
    def records(limit:int=Query(default=20,ge=1,le=100),offset:int=Query(default=0,ge=0),tenant=Depends(principal)):
        return store.records(tenant,limit,offset)
    @app.post('/records',status_code=201)
    def record(body:RecordInput,tenant=Depends(principal)):
        return store.add_record(tenant,body.category,body.cents)
    @app.get('/summary')
    def summary(tenant=Depends(principal)): return store.summary(tenant)
    @app.get('/statistics')
    def statistics(tenant=Depends(principal)): return store.summary(tenant)
    @app.post('/documents',status_code=201)
    def ingest(body:DocumentInput,tenant=Depends(principal)):
        return {'id':store.add_document(tenant,body.text,body.source)}
    @app.get('/search')
    def search(q:str=Query(min_length=1,max_length=4000),k:int=Query(default=3,ge=1,le=10),tenant=Depends(principal)):
        return store.search(tenant,q,k)
    @app.post('/answer')
    def answer(body:Question,tenant=Depends(principal)):
        return evidence_answer(store,tenant,body.question)
    @app.post('/compare')
    def compare(body:Comparison,tenant=Depends(principal)):
        try: return {'rows':store.compare(tenant,body.companies,body.years),'mode':'deterministic calculation'}
        except LookupError: raise HTTPException(404,'Requested data unavailable') from None
    app.state.store=store
    async def database_error(request, exc):
        return JSONResponse(status_code=503, content={'detail':'Database unavailable'})
    app.add_exception_handler(sqlite3.Error, database_error)
    if store.postgres:
        import psycopg
        app.add_exception_handler(psycopg.Error, database_error)
    return app

app=create_app(seed=os.environ.get('COURSE_SEED')=='1')
