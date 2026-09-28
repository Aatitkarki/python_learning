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
print(Decimal("0.1") + Decimal("0.2"))
from pathlib import Path
print((ROOT / "datasets" / "expenses.csv").exists())

# 01c-E1: Amount parser

def parse_amount(value):
    from decimal import Decimal, InvalidOperation
    try:
        amount = Decimal(value)
    except (InvalidOperation, TypeError):
        raise ValueError("Invalid amount") from None
    if not amount.is_finite() or amount < 0:
        raise ValueError("Invalid amount")
    return amount

from decimal import Decimal
assert parse_amount("12.50") == Decimal("12.50")
for bad in ("NaN", "-1", "oops", "Infinity"):
    expect_error(ValueError, lambda bad=bad: parse_amount(bad))

print("01c-E1: checks passed")

# 01c-E2: CSV summary

def summarize_csv(text):
    import csv, io
    from datetime import date
    from decimal import Decimal
    total, groups = Decimal("0"), {}
    for row in csv.DictReader(io.StringIO(text)):
        date.fromisoformat(row["date"])
        category = row["category"].strip()
        if not category: raise ValueError("Blank category")
        amount = parse_amount(row["amount"])
        total += amount
        groups[category] = groups.get(category, Decimal("0")) + amount
    return total, groups

sample = "date,category,amount\n2026-01-01,Food,0.10\n2026-01-02,Food,0.20\n"
total, groups = summarize_csv(sample)
assert str(total) == "0.30" and groups == {"Food": total}
assert summarize_csv("date,category,amount\n")[0] == 0

print("01c-E2: checks passed")

# 01c-E3: JSON contract

def report_json(total, currency="USD"):
    import json
    return json.dumps({"total": str(total), "currency": currency}, sort_keys=True)

import json
assert json.loads(report_json(Decimal("0.30"))) == {"total": "0.30", "currency": "USD"}

print("01c-E3: checks passed")
