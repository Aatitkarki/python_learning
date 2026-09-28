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

from dataclasses import dataclass
@dataclass(frozen=True)
class Ticket:
    id: int
    category: str
print(Ticket(1, "access"))

# 01d-E1: Inventory object

class Inventory:
    def __init__(self):
        self.items = {}
    def add(self, name, quantity):
        if quantity <= 0: raise ValueError("Positive quantity required")
        self.items[name] = self.items.get(name, 0) + quantity

a, b = Inventory(), Inventory()
a.add("book", 2)
assert a.items == {"book": 2} and b.items == {}
expect_error(ValueError, lambda: a.add("book", 0))

print("01d-E1: checks passed")

# 01d-E2: Binary search

def binary_search(values, target):
    lo, hi = 0, len(values) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if values[mid] == target: return mid
        if values[mid] < target: lo = mid + 1
        else: hi = mid - 1
    return -1

assert binary_search([1, 3, 5, 7], 5) == 2
assert binary_search([], 1) == -1
assert binary_search([1, 3], 2) == -1

print("01d-E2: checks passed")

# 01d-E3: Regression fix

def average(values):
    if not values: raise ValueError("Empty sample")
    return sum(values) / len(values)

assert average([2, 4]) == 3
assert average([9]) == 9
expect_error(ValueError, lambda: average([]))

print("01d-E3: checks passed")
