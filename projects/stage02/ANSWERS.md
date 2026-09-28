# Stage 02 — worked project answer

<!-- question-answer-index -->
**Looking for a particular answer?** [Question-by-question solutions](SOLUTIONS.md) includes notebook exercises, explanations, independent assignments, and project tasks.


Read after saving your own attempt. The reference is one implementation, not the only acceptable design.

## Reference artifacts

- [solution.py](solution.py)

## Expected behavior and reasoning

For x=[-2,-1,0,1,2] and y=[-3,-1,1,3,5], the fitted line is y=2x+1. The central-difference gradient should agree to about 1e-6. Sample variance of [1,2,3] is 1; population variance is 2/3. A rotation preserves Euclidean norm; diag(2,3) maps [1,0] to twice itself. A permutation test shuffles group labels under exchangeability and compares absolute mean differences; use (extreme+1)/(repeats+1).

## How to review your work

Compare the input/output contract first, then edge behavior, data boundaries, and failure modes. Different implementation details are acceptable when you can explain them and demonstrate the same or stronger guarantees. Record actual observed model/latency results instead of treating example scores as universal answers.

## Transfer and extension answer key

The [extra lab answer guide](../../curriculum/EXTRA_LABS.md) supplies derivations, query examples, algorithms, and design answers for the larger extensions. The corresponding solved notebooks answer each checked exercise and each oral question:

- [02a practice](../../curriculum/notebooks/02a_vectors_matrices_and_algebra.ipynb) · [worked answers](../../curriculum/solutions/02a_vectors_matrices_and_algebra.ipynb)
- [02b practice](../../curriculum/notebooks/02b_derivatives_and_optimization.ipynb) · [worked answers](../../curriculum/solutions/02b_derivatives_and_optimization.ipynb)
- [02c practice](../../curriculum/notebooks/02c_probability_statistics_and_uncertainty.ipynb) · [worked answers](../../curriculum/solutions/02c_probability_statistics_and_uncertainty.ipynb)

## Common wrong answer

A runnable happy path alone does not satisfy the project. A missing dependency or unavailable external service is pending evidence; a mock is useful for unit testing but does not prove the actual integration. Copying the reference does not pass the independent gate.
