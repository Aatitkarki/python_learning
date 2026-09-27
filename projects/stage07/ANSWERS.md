# Stage 07 — worked project answer

Read after saving your own attempt. The reference is one implementation, not the only acceptable design.

## Reference artifacts

- [integration.py](integration.py)
- [solution.py](solution.py)
- [reference.py](../reference.py)
- [api.py](../api.py)

## Expected behavior and reasoning

The baseline returns source quotes only and explicitly does not synthesize an answer. integration.py performs actual model embeddings and pgvector exact cosine search, PostgreSQL text ranking, optional cross-encoder reranking, and optional Ollama drafting. PostgreSQL ts_rank_cd is not BM25; implement or choose a genuine BM25 scorer for that comparison. Candidate presence is not evidence support. Compare against labeled questions and return unknown when sources do not support an answer.

## How to review your work

Compare the input/output contract first, then edge behavior, data boundaries, and failure modes. Different implementation details are acceptable when you can explain them and demonstrate the same or stronger guarantees. Record actual observed model/latency results instead of treating example scores as universal answers.

## Transfer and extension answer key

The [extra lab answer guide](../../curriculum/EXTRA_LABS.md) supplies derivations, query examples, algorithms, and design answers for the larger extensions. The corresponding solved notebooks answer each checked exercise and each oral question:

- [07a practice](../../curriculum/notebooks/07a_retrieval_from_first_principles.ipynb) · [worked answers](../../curriculum/solutions/07a_retrieval_from_first_principles.ipynb)
- [07b practice](../../curriculum/notebooks/07b_grounding_permissions_and_vector_search.ipynb) · [worked answers](../../curriculum/solutions/07b_grounding_permissions_and_vector_search.ipynb)

## Common wrong answer

A runnable happy path alone does not satisfy the project. A missing dependency or unavailable external service is pending evidence; a mock is useful for unit testing but does not prove the actual integration. Copying the reference does not pass the independent gate.
