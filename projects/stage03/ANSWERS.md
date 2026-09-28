# Stage 03 — worked project answer

<!-- question-answer-index -->
**Looking for a particular answer?** [Question-by-question solutions](SOLUTIONS.md) includes notebook exercises, explanations, independent assignments, and project tasks.


Read after saving your own attempt. The reference is one implementation, not the only acceptable design.

## Reference artifacts

- [solution.py](solution.py)
- [reference.py](../reference.py)
- [api.py](../api.py)

## Expected behavior and reasoning

The offline demonstration creates two records totaling 2550 cents and proves they survive a new app instance. Invalid bodies return 422, missing auth 401, and cross-tenant lists are empty. Bind SQL values rather than interpolate. The reference API uses integer cents; schema, keys, and query plans belong in your independent design. PostgreSQL is an explicit integration milestone, not satisfied by SQLite tests.

## How to review your work

Compare the input/output contract first, then edge behavior, data boundaries, and failure modes. Different implementation details are acceptable when you can explain them and demonstrate the same or stronger guarantees. Record actual observed model/latency results instead of treating example scores as universal answers.

## Transfer and extension answer key

The [extra lab answer guide](../../curriculum/EXTRA_LABS.md) supplies derivations, query examples, algorithms, and design answers for the larger extensions. The corresponding solved notebooks answer each checked exercise and each oral question:

- [03a practice](../../curriculum/notebooks/03a_numpy_and_pandas_data_contracts.ipynb) · [worked answers](../../curriculum/solutions/03a_numpy_and_pandas_data_contracts.ipynb)
- [03b practice](../../curriculum/notebooks/03b_sql_transactions_and_schema_design.ipynb) · [worked answers](../../curriculum/solutions/03b_sql_transactions_and_schema_design.ipynb)
- [03c practice](../../curriculum/notebooks/03c_http_validation_and_fastapi.ipynb) · [worked answers](../../curriculum/solutions/03c_http_validation_and_fastapi.ipynb)

## Common wrong answer

A runnable happy path alone does not satisfy the project. A missing dependency or unavailable external service is pending evidence; a mock is useful for unit testing but does not prove the actual integration. Copying the reference does not pass the independent gate.
