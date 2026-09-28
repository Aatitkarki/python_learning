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

import csv
rows = list(csv.DictReader((ROOT / "datasets" / "financials.csv").open()))
print(rows[0])

# 15a-E1: Period selection

def select_periods(rows, company, years):
    selected = {}
    for row in rows:
        year = int(row["year"])
        if row["company"] == company and year in years:
            if year in selected: raise ValueError("Duplicate period")
            selected[year] = row
    if set(selected) != set(years): raise ValueError("Missing period")
    return [selected[year] for year in sorted(selected)]

selected = select_periods(rows, "Aurora", [2023, 2024, 2025])
assert [int(r["year"]) for r in selected] == [2023, 2024, 2025]
expect_error(ValueError, lambda: select_periods(rows, "Aurora", [1999]))

print("15a-E1: checks passed")

# 15a-E2: Verified financial row

def calculate_row(row):
    from decimal import Decimal
    revenue = Decimal(row["revenue"])
    if revenue <= 0: raise ValueError("Invalid revenue")
    return {"company": row["company"], "year": int(row["year"]), "revenue": str(revenue), "operating_margin": str(Decimal(row["operating_income"])/revenue), "fcf": str(Decimal(row["operating_cash_flow"])-Decimal(row["capex"])), "source_id": row["source_id"]}

result = calculate_row(select_periods(rows, "Aurora", [2025])[0])
assert result["revenue"] == "144" and result["fcf"] == "24"
assert result["source_id"] == "aurora-2025"

print("15a-E2: checks passed")

# 15a-E3: Citation completeness

def citations_complete(report, allowed_source_ids):
    return bool(report) and all(row.get("source_id") in allowed_source_ids for row in report)

assert citations_complete([result], {"aurora-2025"})
assert not citations_complete([result], {"beacon-2025"})
assert not citations_complete([], set())

print("15a-E3: checks passed")
