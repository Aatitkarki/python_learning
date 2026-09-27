"""Bounded tool executor for a research plan. Plans never carry trusted identity.

An optional model can propose JSON plans; this module is the authorization/execution boundary.
The CLI uses a deterministic plan so it is reproducible without a model service.
"""
import json
import math
import tempfile
import time
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, ValidationError
from projects.reference import Store

class SearchArgs(BaseModel):
    model_config=ConfigDict(extra='forbid')
    query: str=Field(min_length=1,max_length=1000)
    k: int=Field(default=3,ge=1,le=5)
class FinancialArgs(BaseModel):
    model_config=ConfigDict(extra='forbid')
    companies: list[str]=Field(min_length=1,max_length=3)
    years: list[int]=Field(min_length=1,max_length=5)
class DivideArgs(BaseModel):
    model_config=ConfigDict(extra='forbid')
    numerator: float=Field(allow_inf_nan=False)
    denominator: float=Field(allow_inf_nan=False)

class ResearchWorkflow:
    def __init__(self,store,tenant,max_calls=5,seconds=10):
        if max_calls<1 or seconds<=0: raise ValueError('Positive execution budget required')
        self.store,self.tenant,self.max_calls,self.seconds=store,tenant,max_calls,seconds
    def execute(self,call):
        if not isinstance(call,dict) or set(call)!={'tool','arguments'}: raise ValueError('Invalid call schema')
        name,args=call['tool'],call['arguments']
        if name=='search':
            parsed=SearchArgs.model_validate(args)
            return self.store.search(self.tenant,parsed.query,parsed.k)
        if name=='financials':
            parsed=FinancialArgs.model_validate(args)
            return self.store.compare(self.tenant,parsed.companies,parsed.years)
        if name=='divide':
            parsed=DivideArgs.model_validate(args)
            if parsed.denominator==0: raise ValueError('Zero denominator')
            result=parsed.numerator/parsed.denominator
            if not math.isfinite(result): raise ValueError('Nonfinite result')
            return result
        raise ValueError('Tool not allowed')
    def run(self,calls):
        if not isinstance(calls,list): raise ValueError('Plan must be a list')
        started=time.monotonic(); observations=[]
        for i,call in enumerate(calls):
            if i>=self.max_calls or time.monotonic()-started>=self.seconds:
                return {'status':'budget_exhausted','observations':observations}
            try:
                result=self.execute(call)
                observations.append({'step':i,'tool':call['tool'],'status':'ok','result':result})
            except (ValueError,LookupError,ValidationError) as exc:
                observations.append({'step':i,'status':'error','error':type(exc).__name__})
                return {'status':'failed','observations':observations}
        return {'status':'complete','observations':observations}

def run():
    with tempfile.TemporaryDirectory() as folder:
        store=Store(Path(folder)/'research.db');store.seed()
        plan=[{'tool':'search','arguments':{'query':'Aurora 2025 revenue'}},
              {'tool':'financials','arguments':{'companies':['Aurora','Beacon'],'years':[2023,2024,2025]}},
              {'tool':'divide','arguments':{'numerator':144,'denominator':120}}]
        return ResearchWorkflow(store,'A').run(plan)

if __name__=='__main__': print(json.dumps(run(),indent=2))
