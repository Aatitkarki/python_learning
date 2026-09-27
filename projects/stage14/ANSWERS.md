# Stage 14 — worked project answer

Read after saving your own attempt. The reference is one implementation, not the only acceptable design.

## Reference artifacts

- [solution.py](solution.py)

## Expected behavior and reasoning

Aurora 2025: revenue=144 million USD, operating margin=25%, FCF=24 million USD; Beacon 2025: revenue=108, margin=15/108≈13.89%, FCF=12. ROE/ROA use average balances; first-year values are unknown without prior balances. P/E with nonpositive EPS is undefined under the course policy. PEG uses P/E divided by a stated percentage-point growth rate, not silently by a fraction. Always align statement availability to the decision date.

## How to review your work

Compare the input/output contract first, then edge behavior, data boundaries, and failure modes. Different implementation details are acceptable when you can explain them and demonstrate the same or stronger guarantees. Record actual observed model/latency results instead of treating example scores as universal answers.

## Transfer and extension answer key

The [extra lab answer guide](../../curriculum/EXTRA_LABS.md) supplies derivations, query examples, algorithms, and design answers for the larger extensions. The corresponding solved notebooks answer each checked exercise and each oral question:

- [14a practice](../../curriculum/notebooks/14a_financial_statements_and_ratios.ipynb) · [worked answers](../../curriculum/solutions/14a_financial_statements_and_ratios.ipynb)
- [14b practice](../../curriculum/notebooks/14b_time_series_and_honest_backtests.ipynb) · [worked answers](../../curriculum/solutions/14b_time_series_and_honest_backtests.ipynb)

## Common wrong answer

A runnable happy path alone does not satisfy the project. A missing dependency or unavailable external service is pending evidence; a mock is useful for unit testing but does not prove the actual integration. Copying the reference does not pass the independent gate.
