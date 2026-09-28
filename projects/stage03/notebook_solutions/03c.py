"""Generated worked answers; edit your own version under work/."""

from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
def expect_error(error_type, operation):
    try:
        operation()
    except error_type:
        return
    raise AssertionError(f"Expected {error_type.__name__}")


# Worked example

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field
app = FastAPI()
@app.get("/health")
def health():
    return {"status": "ok"}
assert TestClient(app).get("/health").json() == {"status": "ok"}

# 03c-E1: Request schema

from pydantic import BaseModel, Field
class Record(BaseModel):
    category: str = Field(min_length=1, max_length=50)
    amount: float = Field(ge=0, allow_inf_nan=False)

assert Record(category="Food", amount=2).amount == 2
from pydantic import ValidationError
expect_error(ValidationError, lambda: Record(category="", amount=-1))

print("03c-E1: checks passed")

# 03c-E2: Create endpoint

def make_app():
    app = FastAPI()
    @app.post("/records", status_code=201)
    def create(record: Record):
        return record
    return app

client = TestClient(make_app())
assert client.post("/records", json={"category": "Food", "amount": 2}).status_code == 201
assert client.post("/records", json={"category": "", "amount": -1}).status_code == 422

print("03c-E2: checks passed")

# 03c-E3: Pagination contract

def paginate(rows, offset=0, limit=20):
    if offset < 0 or not 1 <= limit <= 100: raise ValueError("Invalid pagination")
    return rows[offset:offset+limit]

assert paginate(list(range(10)), 3, 2) == [3, 4]
expect_error(ValueError, lambda: paginate([], 0, 1000))

print("03c-E3: checks passed")
