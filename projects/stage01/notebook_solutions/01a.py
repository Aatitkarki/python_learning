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

def celsius_to_fahrenheit(celsius):
    return celsius * 9 / 5 + 32

print(celsius_to_fahrenheit(20))
assert celsius_to_fahrenheit(0) == 32

# 01a-E1: Profit function

def profit(buy, sell, shares):
    if shares <= 0 or min(buy, sell) < 0:
        raise ValueError("Invalid price or quantity")
    return (sell - buy) * shares

assert profit(100, 110, 10) == 100
assert profit(10, 8, 2) == -4
expect_error(ValueError, lambda: profit(1, 2, 0))

print("01a-E1: checks passed")

# 01a-E2: Calculator

def calculate(a, op, b):
    if op == "+": return a + b
    if op == "-": return a - b
    if op == "*": return a * b
    if op == "/": return a / b
    raise ValueError("Unknown operator")

assert calculate(6, "/", 2) == 3
assert calculate(6, "-", 9) == -3
expect_error(ZeroDivisionError, lambda: calculate(2, "/", 0))
expect_error(ValueError, lambda: calculate(2, "**", 4))

print("01a-E2: checks passed")

# 01a-E3: Tiered shipping

def shipping(total):
    if total < 0: raise ValueError("Negative total")
    return 0 if total >= 100 else 5

assert [shipping(x) for x in (0, 99, 100)] == [5, 5, 0]
expect_error(ValueError, lambda: shipping(-1))

print("01a-E3: checks passed")
