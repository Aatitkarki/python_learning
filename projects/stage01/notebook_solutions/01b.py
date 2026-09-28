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

totals = {}
for category, amount in [("food", 10), ("bus", 5), ("food", 8)]:
    totals[category] = totals.get(category, 0) + amount
print(totals)

# 01b-E1: Word frequencies

def word_counts(text):
    import re
    counts = {}
    for word in re.findall(r"[a-z]+", text.lower()):
        counts[word] = counts.get(word, 0) + 1
    return counts

assert word_counts("AI, ai! Data.") == {"ai": 2, "data": 1}
assert word_counts("") == {}

print("01b-E1: checks passed")

# 01b-E2: Stable deduplication

def unique(items):
    seen, result = set(), []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

assert unique([3, 1, 3, 2, 1]) == [3, 1, 2]
assert unique([]) == []

print("01b-E2: checks passed")

# 01b-E3: Inventory update

def update_stock(stock, deltas):
    result = dict(stock)
    for item, delta in deltas.items():
        result[item] = result.get(item, 0) + delta
        if result[item] < 0: raise ValueError("Insufficient stock")
    return result

original = {"pen": 3}
assert update_stock(original, {"pen": -2, "book": 1}) == {"pen": 1, "book": 1}
assert original == {"pen": 3}
expect_error(ValueError, lambda: update_stock(original, {"pen": -4}))

print("01b-E3: checks passed")
