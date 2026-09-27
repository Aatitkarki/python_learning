# Stage 04 — worked project answer

Read after saving your own attempt. The reference is one implementation, not the only acceptable design.

## Reference artifacts

- [Local classifier API](api.py) — run `python -m uvicorn projects.stage04.api:app --host 127.0.0.1 --port 8001`, then POST JSON `{"text":"reset my login password"}` to `/predict`. It trains only on fixture training rows and returns explicitly uncalibrated scores.

- [solution.py](solution.py)

## Expected behavior and reasoning

Validation chooses the model; test evaluates that final choice. TF-IDF belongs inside the pipeline, and boosting uses a bounded dense representation in this tiny example. No universal score is promised: inspect the generated report. A perfect score on 36 authored examples is weak evidence. Demand regression must beat a mean baseline on unseen data; random targets should not yield credible performance. KMeans tends to fail on curved clusters; DBSCAN is sensitive to density and scale.

## How to review your work

Compare the input/output contract first, then edge behavior, data boundaries, and failure modes. Different implementation details are acceptable when you can explain them and demonstrate the same or stronger guarantees. Record actual observed model/latency results instead of treating example scores as universal answers.

## Transfer and extension answer key

The [extra lab answer guide](../../curriculum/EXTRA_LABS.md) supplies derivations, query examples, algorithms, and design answers for the larger extensions. The corresponding solved notebooks answer each checked exercise and each oral question:

- [04a practice](../../curriculum/notebooks/04a_supervised_learning_without_leakage.ipynb) · [worked answers](../../curriculum/solutions/04a_supervised_learning_without_leakage.ipynb)
- [04b practice](../../curriculum/notebooks/04b_metrics_clustering_and_error_analysis.ipynb) · [worked answers](../../curriculum/solutions/04b_metrics_clustering_and_error_analysis.ipynb)

## Common wrong answer

A runnable happy path alone does not satisfy the project. A missing dependency or unavailable external service is pending evidence; a mock is useful for unit testing but does not prove the actual integration. Copying the reference does not pass the independent gate.
