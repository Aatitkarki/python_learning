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

import os, sys
os.environ["PYSPARK_PYTHON"] = sys.executable  # Local workers must use this notebook's Python.
from pyspark.sql import SparkSession, functions as F, Window
spark = SparkSession.builder.master("local[2]").appName("ai-learning").config("spark.ui.enabled", "false").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
df = spark.createDataFrame([(1, "A", 10), (2, "A", 20), (3, "B", 5)], "id long, account string, cents long")
df.show()

# 11b-E1: Group totals

def totals(df):
    return df.groupBy("account").agg(F.sum("cents").alias("sum_cents")).orderBy("account")

assert [(r.account, r.sum_cents) for r in totals(df).collect()] == [("A", 30), ("B", 5)]

print("11b-E1: checks passed")

# 11b-E2: Running total

def with_running(df):
    window = Window.partitionBy("account").orderBy("id").rowsBetween(Window.unboundedPreceding, Window.currentRow)
    return df.withColumn("running_cents", F.sum("cents").over(window))

assert [r.running_cents for r in with_running(df).orderBy("id").collect()] == [10, 30, 5]

print("11b-E2: checks passed")

# 11b-E3: Parquet round trip

def parquet_roundtrip(df, path):
    df.write.mode("errorifexists").parquet(str(path))
    return spark.read.parquet(str(path)).count()

import tempfile
from pathlib import Path
with tempfile.TemporaryDirectory() as folder:
    assert parquet_roundtrip(df, Path(folder)/"data") == 3
spark.stop()

print("11b-E3: checks passed")
