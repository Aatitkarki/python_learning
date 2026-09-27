# Stage 01 — worked project answer

Read after saving your own attempt. The reference is one implementation, not the only acceptable design.

## Reference artifacts

- [solution.py](solution.py)

## Expected behavior and reasoning

The fixture total is 100.00 across 6 rows; January and February each total 50.00. Food=55.00, Transport=15.00, Books=30.00, highest=30.00, mean=100/6. Decimal avoids binary-money error. Reject malformed rows before aggregation. A CLI should catch expected input errors, return a nonzero exit, and leave programmer errors visible. Text normalization and stable tie-breaking must be explicit.

## How to review your work

Compare the input/output contract first, then edge behavior, data boundaries, and failure modes. Different implementation details are acceptable when you can explain them and demonstrate the same or stronger guarantees. Record actual observed model/latency results instead of treating example scores as universal answers.

## Transfer and extension answer key

The [extra lab answer guide](../../curriculum/EXTRA_LABS.md) supplies derivations, query examples, algorithms, and design answers for the larger extensions. The corresponding solved notebooks answer each checked exercise and each oral question:

- [01a practice](../../curriculum/notebooks/01a_variables_decisions_and_functions.ipynb) · [worked answers](../../curriculum/solutions/01a_variables_decisions_and_functions.ipynb)
- [01b practice](../../curriculum/notebooks/01b_collections_loops_and_text.ipynb) · [worked answers](../../curriculum/solutions/01b_collections_loops_and_text.ipynb)
- [01c practice](../../curriculum/notebooks/01c_files_validation_and_money.ipynb) · [worked answers](../../curriculum/solutions/01c_files_validation_and_money.ipynb)
- [01d practice](../../curriculum/notebooks/01d_objects_algorithms_and_debugging.ipynb) · [worked answers](../../curriculum/solutions/01d_objects_algorithms_and_debugging.ipynb)

## Common wrong answer

A runnable happy path alone does not satisfy the project. A missing dependency or unavailable external service is pending evidence; a mock is useful for unit testing but does not prove the actual integration. Copying the reference does not pass the independent gate.
