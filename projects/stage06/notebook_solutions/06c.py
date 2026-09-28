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

import numpy as np
from pydantic import BaseModel, Field
print("A 1000×1000 matrix has", 1000*1000, "parameters")
print("Rank-8 adapters have", 8*(1000+1000), "parameters")

# 06c-E1: Validated extraction

def validate_extraction(text):
    from pydantic import BaseModel, Field, ConfigDict
    class Report(BaseModel):
        model_config = ConfigDict(extra="forbid")
        company: str = Field(min_length=1)
        revenue: float = Field(ge=0, allow_inf_nan=False)
    return Report.model_validate_json(text).model_dump()

assert validate_extraction('{"company":"Example","revenue":100000000000}')["revenue"] == 1e11
from pydantic import ValidationError
expect_error(ValidationError, lambda: validate_extraction('{"company":"","revenue":-1}'))

print("06c-E1: checks passed")

# 06c-E2: LoRA update

def lora_weight(w, a, b, alpha):
    return w + (alpha/a.shape[0])*(b@a)

w = np.zeros((3, 4)); a = np.ones((2, 4)); b = np.ones((3, 2))
assert np.allclose(lora_weight(w, a, b, 2), np.full((3, 4), 2))

print("06c-E2: checks passed")

# 06c-E3: Symmetric INT8 simulation

def quantize(w):
    w = np.asarray(w, dtype=float)
    scale = float(np.max(np.abs(w)))/127 or 1.
    codes = np.clip(np.round(w/scale), -127, 127).astype(np.int8)
    return codes, scale, codes.astype(float)*scale

codes, scale, restored = quantize([-.7, .1, 1.])
assert codes.dtype == np.int8
assert np.max(np.abs(restored-[-.7, .1, 1.])) <= scale/2+1e-12
assert np.allclose(quantize([0, 0])[2], 0)

print("06c-E3: checks passed")
