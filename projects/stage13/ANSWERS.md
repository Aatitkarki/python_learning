# Stage 13 — worked project answer

<!-- question-answer-index -->
**Looking for a particular answer?** [Question-by-question solutions](SOLUTIONS.md) includes notebook exercises, explanations, independent assignments, and project tasks.


Read after saving your own attempt. The reference is one implementation, not the only acceptable design.

## Reference artifacts

- [solution.py](solution.py)

## Expected behavior and reasoning

The reference report measures real lexical retrieval with nine smoke cases and explicitly does not claim generation-groundedness. Recall uses unique relevant IDs; no-answer cases are evaluated as abstentions. A permission failure is a hard gate even if average quality rises. Use paired or group bootstrap according to dependence; document confidence and denominators. Human judges should verify claims against sources, not merely check that a citation ID exists.

## How to review your work

Compare the input/output contract first, then edge behavior, data boundaries, and failure modes. Different implementation details are acceptable when you can explain them and demonstrate the same or stronger guarantees. Record actual observed model/latency results instead of treating example scores as universal answers.

## Transfer and extension answer key

The [extra lab answer guide](../../curriculum/EXTRA_LABS.md) supplies derivations, query examples, algorithms, and design answers for the larger extensions. The corresponding solved notebooks answer each checked exercise and each oral question:

- [13a practice](../../curriculum/notebooks/13a_evaluation_datasets_and_retrieval_metrics.ipynb) · [worked answers](../../curriculum/solutions/13a_evaluation_datasets_and_retrieval_metrics.ipynb)
- [13b practice](../../curriculum/notebooks/13b_regression_gates_and_uncertainty.ipynb) · [worked answers](../../curriculum/solutions/13b_regression_gates_and_uncertainty.ipynb)

## Common wrong answer

A runnable happy path alone does not satisfy the project. A missing dependency or unavailable external service is pending evidence; a mock is useful for unit testing but does not prove the actual integration. Copying the reference does not pass the independent gate.
