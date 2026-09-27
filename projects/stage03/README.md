# Stage 03 project — Persistent data analysis API

[Stage study guide](../../curriculum/stages/03.md) · [Course plan](../../curriculum/PLAN.md)

**Scenario:** You own a small component of a private research platform. A teammate must be able to reproduce it, inspect its evidence, and understand its failure behavior.

## Your assignment

1. Profile and clean a CSV with a data-quality report and quarantined invalid records.
2. Design a normalized relational schema and write the complete SQL worksheet in EXTRA_LABS.md; examine index plans.
3. Implement GET /records, /summary, /statistics and POST /records, with persistent storage and tenant isolation.
4. Run first on SQLite and then PostgreSQL via Compose. Ingest CSV, restart the API, verify totals, and test rollback and invalid requests.

## Acceptance criteria

Write a join and window query from scratch; explain a query plan; trace an HTTP request through auth, validation, transaction, and response. Demonstrate persistence and tenant isolation.

Also require documented inputs/outputs, explicit units and limitations, tests for normal/boundary/error cases, and a fresh-process run. Use only data you have permission to use; the supplied fixtures are fictional. Do not report a synthetic-data score as real-world quality.

## Starter workflow

Create work/stage03/, write a short interface contract, and implement the smallest end-to-end slice first. Use the exercise stubs below for function signatures and visible checks. Add your own tests before consulting the reference.

- [03a practice](../../curriculum/notebooks/03a_numpy_and_pandas_data_contracts.ipynb) · [worked answers](../../curriculum/solutions/03a_numpy_and_pandas_data_contracts.ipynb)
- [03b practice](../../curriculum/notebooks/03b_sql_transactions_and_schema_design.ipynb) · [worked answers](../../curriculum/solutions/03b_sql_transactions_and_schema_design.ipynb)
- [03c practice](../../curriculum/notebooks/03c_http_validation_and_fastapi.ipynb) · [worked answers](../../curriculum/solutions/03c_http_validation_and_fastapi.ipynb)

## Run the reference after your attempt

From the repository root with the environment active:

```bash
python -m pip install -r requirements/core.txt
python -m projects.stage03.solution
```

For model/service labs, read [INTEGRATIONS.md](../../curriculum/INTEGRATIONS.md) before running. Stage 10 additionally needs a local .env and a running Docker daemon. Output paths under work/ belong to you.

## Deliver

- Runnable code and tests with a setup README.
- A results report containing actual measurements and source/data versions.
- A failure you reproduced, diagnosed, and fixed.
- A short explanation of tradeoffs and remaining limits.
- Closed-book gate evidence and a scheduled review date.

[Worked answer and design reasoning](ANSWERS.md) · [Additional lab answers](../../curriculum/EXTRA_LABS.md)
