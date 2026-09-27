# Stage 00 — worked project answer

Read after saving your own attempt. The reference is one implementation, not the only acceptable design.

## Reference artifacts

- [solution.py](solution.py)

## Expected behavior and reasoning

The manifest must contain Python version, seed 42, and the actual SHA-256 of expenses.csv. A changed byte changes the hash. Use git status/diff/log to explain exactly what a commit contains. Do not commit .venv, .env, or generated local databases.

## How to review your work

Compare the input/output contract first, then edge behavior, data boundaries, and failure modes. Different implementation details are acceptable when you can explain them and demonstrate the same or stronger guarantees. Record actual observed model/latency results instead of treating example scores as universal answers.

## Transfer and extension answer key

The [extra lab answer guide](../../curriculum/EXTRA_LABS.md) supplies derivations, query examples, algorithms, and design answers for the larger extensions. The corresponding solved notebooks answer each checked exercise and each oral question:

- [00a practice](../../curriculum/notebooks/00a_your_first_reproducible_experiment.ipynb) · [worked answers](../../curriculum/solutions/00a_your_first_reproducible_experiment.ipynb)

## Common wrong answer

A runnable happy path alone does not satisfy the project. A missing dependency or unavailable external service is pending evidence; a mock is useful for unit testing but does not prove the actual integration. Copying the reference does not pass the independent gate.
