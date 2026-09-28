# Stage 11 — worked project answer

<!-- question-answer-index -->
**Looking for a particular answer?** [Question-by-question solutions](SOLUTIONS.md) includes notebook exercises, explanations, independent assignments, and project tasks.


Read after saving your own attempt. The reference is one implementation, not the only acceptable design.

## Reference artifacts

- [solution.py](solution.py)

## Expected behavior and reasoning

The job uses Spark range and built-in expressions; amounts are ((id*17)%10000) cents and accounts=id%50. The expected total can be independently calculated by a streaming Python sum. A uniform synthetic distribution may have zero 3-sigma anomalies. ROWS(-2,0) means three observed rows, not automatically three calendar days. Do not collect the raw million rows to the driver. Existing output paths are rejected to protect previous results.

## How to review your work

Compare the input/output contract first, then edge behavior, data boundaries, and failure modes. Different implementation details are acceptable when you can explain them and demonstrate the same or stronger guarantees. Record actual observed model/latency results instead of treating example scores as universal answers.

## Transfer and extension answer key

The [extra lab answer guide](../../curriculum/EXTRA_LABS.md) supplies derivations, query examples, algorithms, and design answers for the larger extensions. The corresponding solved notebooks answer each checked exercise and each oral question:

- [11a practice](../../curriculum/notebooks/11a_distributed_data_and_associative_aggregation.ipynb) · [worked answers](../../curriculum/solutions/11a_distributed_data_and_associative_aggregation.ipynb)
- [11b practice](../../curriculum/notebooks/11b_pyspark_dataframes_and_windows.ipynb) · [worked answers](../../curriculum/solutions/11b_pyspark_dataframes_and_windows.ipynb)

## Common wrong answer

A runnable happy path alone does not satisfy the project. A missing dependency or unavailable external service is pending evidence; a mock is useful for unit testing but does not prove the actual integration. Copying the reference does not pass the independent gate.
