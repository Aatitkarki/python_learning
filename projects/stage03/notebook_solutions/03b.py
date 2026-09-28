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

import sqlite3
conn = sqlite3.connect(":memory:")
conn.executescript("CREATE TABLE orders(id INTEGER PRIMARY KEY, customer TEXT, amount INTEGER); INSERT INTO orders VALUES(1,'A',10),(2,'A',20),(3,'B',7);")
print(conn.execute("SELECT customer, SUM(amount) FROM orders GROUP BY customer").fetchall())

# 03b-E1: Bound filter

def customer_orders(conn, customer):
    return conn.execute("SELECT id, amount FROM orders WHERE customer = ? ORDER BY id", (customer,)).fetchall()

assert customer_orders(conn, "A") == [(1, 10), (2, 20)]
assert customer_orders(conn, "' OR 1=1 --") == []

print("03b-E1: checks passed")

# 03b-E2: Running totals

def running_totals(conn):
    return conn.execute("SELECT id, SUM(amount) OVER (PARTITION BY customer ORDER BY id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) FROM orders ORDER BY id").fetchall()

assert running_totals(conn) == [(1, 10), (2, 30), (3, 7)]

print("03b-E2: checks passed")

# 03b-E3: Atomic batch

def insert_batch(conn, rows):
    with conn:
        conn.executemany("INSERT INTO orders VALUES (?, ?, ?)", rows)

expect_error(sqlite3.IntegrityError, lambda: insert_batch(conn, [(4, "C", 4), (1, "D", 5)]))
assert conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 3

print("03b-E3: checks passed")
