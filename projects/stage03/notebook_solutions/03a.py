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
import pandas as pd
x = np.array([[1., 2.], [3., 4.]])
print(x.shape, x.mean(axis=0))
print(pd.read_csv(ROOT / "datasets" / "expenses.csv").head())

# 03a-E1: Column standardization

def standardize(x):
    import numpy as np
    x = np.asarray(x, dtype=float)
    std = x.std(axis=0)
    return (x-x.mean(axis=0))/np.where(std == 0, 1, std)

z = standardize([[1, 7], [3, 7]])
assert np.allclose(z, [[-1, 0], [1, 0]])

print("03a-E1: checks passed")

# 03a-E2: Monthly spending

def monthly_spending(frame):
    import pandas as pd
    frame = frame.copy()
    frame["date"] = pd.to_datetime(frame["date"], errors="raise")
    frame["amount"] = pd.to_numeric(frame["amount"], errors="raise")
    return frame.groupby(frame["date"].dt.strftime("%Y-%m"))["amount"].sum().sort_index()

frame = pd.DataFrame({"date": ["2026-02-01", "2026-01-01", "2026-01-03"], "amount": [4, 2, 3]})
assert monthly_spending(frame).to_dict() == {"2026-01": 5, "2026-02": 4}

print("03a-E2: checks passed")

# 03a-E3: Safe join

def enrich(orders, customers):
    return orders.merge(customers, on="customer_id", how="left", validate="many_to_one")

orders = pd.DataFrame({"customer_id": [1, 1, 2], "amount": [1, 2, 3]})
customers = pd.DataFrame({"customer_id": [1, 2], "name": ["A", "B"]})
assert len(enrich(orders, customers)) == 3
expect_error(pd.errors.MergeError, lambda: enrich(orders, pd.concat([customers, customers])))

print("03a-E3: checks passed")
