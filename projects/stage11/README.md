# Stage 11 project — Transaction analytics pipeline

[Stage study guide](../../curriculum/stages/11.md) · [Course plan](../../curriculum/PLAN.md)

**Scenario:** You own a small component of a private research platform. A teammate must be able to reproduce it, inspect its evidence, and understand its failure behavior.

## Your assignment

1. Generate at least one million deterministic transactions without collecting them to the driver.
2. Calculate grouped sums/counts, daily trends, anomalies, and window statistics; write Parquet.
3. Compare partitions and inspect physical plans; demonstrate skew and a broadcast-join tradeoff.
4. Check row count, schema, total cents, and a sampled group against a Python reference.
5. Repeat on an actual cluster or document the operational gap if only local mode is available.

## Acceptance criteria

Explain a shuffle in an actual plan, fix a skewed aggregation, reconcile distributed totals, and justify a storage format.

Also require documented inputs/outputs, explicit units and limitations, tests for normal/boundary/error cases, and a fresh-process run. Use only data you have permission to use; the supplied fixtures are fictional. Do not report a synthetic-data score as real-world quality.

## Starter workflow

Create work/stage11/, write a short interface contract, and implement the smallest end-to-end slice first. Use the exercise stubs below for function signatures and visible checks. Add your own tests before consulting the reference.

- [11a practice](../../curriculum/notebooks/11a_distributed_data_and_associative_aggregation.ipynb) · [worked answers](../../curriculum/solutions/11a_distributed_data_and_associative_aggregation.ipynb)
- [11b practice](../../curriculum/notebooks/11b_pyspark_dataframes_and_windows.ipynb) · [worked answers](../../curriculum/solutions/11b_pyspark_dataframes_and_windows.ipynb)

## Run the reference after your attempt

From the repository root with the environment active:

```bash
python -m pip install -r requirements/spark.txt
python -m projects.stage11.solution --rows 1000000 --output work/spark-million
```

For model/service labs, read [INTEGRATIONS.md](../../curriculum/INTEGRATIONS.md) before running. Stage 10 additionally needs a local .env and a running Docker daemon. Output paths under work/ belong to you.

## Deliver

- Runnable code and tests with a setup README.
- A results report containing actual measurements and source/data versions.
- A failure you reproduced, diagnosed, and fixed.
- A short explanation of tradeoffs and remaining limits.
- Closed-book gate evidence and a scheduled review date.

[Worked answer and design reasoning](ANSWERS.md) · [Additional lab answers](../../curriculum/EXTRA_LABS.md)
