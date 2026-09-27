# Stage 15 — worked project answer

Read after saving your own attempt. The reference is one implementation, not the only acceptable design.

## Reference artifacts

- [solution.py](solution.py)
- [reference.py](../reference.py)
- [api.py](../api.py)

## Expected behavior and reasoning

The reference emits six verified rows from authorized data. The local API can ingest documents, retrieve source quotes, and return deterministic comparison results. Optional integration scripts exercise embeddings, pgvector, and local generation but require external setup and must be connected and evaluated in your independent capstone. The full graduation checklist in CAPSTONE.md distinguishes baseline evidence from production deployment. No reading list or solution file can certify mastery without independent performance.

## How to review your work

Compare the input/output contract first, then edge behavior, data boundaries, and failure modes. Different implementation details are acceptable when you can explain them and demonstrate the same or stronger guarantees. Record actual observed model/latency results instead of treating example scores as universal answers.

## Transfer and extension answer key

The [extra lab answer guide](../../curriculum/EXTRA_LABS.md) supplies derivations, query examples, algorithms, and design answers for the larger extensions. The corresponding solved notebooks answer each checked exercise and each oral question:

- [15a practice](../../curriculum/notebooks/15a_an_evidence-backed_financial_research_pipeline.ipynb) · [worked answers](../../curriculum/solutions/15a_an_evidence-backed_financial_research_pipeline.ipynb)
- [15b practice](../../curriculum/notebooks/15b_architecture_review_and_mastery_defense.ipynb) · [worked answers](../../curriculum/solutions/15b_architecture_review_and_mastery_defense.ipynb)

## Common wrong answer

A runnable happy path alone does not satisfy the project. A missing dependency or unavailable external service is pending evidence; a mock is useful for unit testing but does not prove the actual integration. Copying the reference does not pass the independent gate.
