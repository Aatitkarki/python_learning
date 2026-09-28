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

from decimal import Decimal
revenue = Decimal("120")
operating_income = Decimal("24")
print("Operating margin:", operating_income/revenue)

# 14a-E1: Balance sheet check

def balanced(assets, liabilities, equity, tolerance=.01):
    return abs(assets-liabilities-equity) <= tolerance

assert balanced(100, 60, 40)
assert not balanced(100, 60, 30)

print("14a-E1: checks passed")

# 14a-E2: Financial metrics

def metrics(revenue, operating_income, net_income, shares, cfo, capex):
    if revenue <= 0 or shares <= 0 or capex < 0: raise ValueError("Invalid denominator or capex convention")
    return {"eps": net_income/shares, "operating_margin": operating_income/revenue, "fcf": cfo-capex}

assert metrics(100, 20, 10, 5, 15, 4) == {"eps": 2, "operating_margin": .2, "fcf": 11}

print("14a-E2: checks passed")

# 14a-E3: Growth with explicit policy

def growth(current, prior):
    return (current-prior)/prior if prior > 0 else None

assert growth(120, 100) == .2
assert growth(10, 0) is None
assert growth(10, -5) is None

print("14a-E3: checks passed")
