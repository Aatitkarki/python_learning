# Stage 07 project — Private document assistant

[Stage study guide](../../curriculum/stages/07.md) · [Course plan](../../curriculum/PLAN.md)

**Scenario:** You own a small component of a private research platform. A teammate must be able to reproduce it, inspect its evidence, and understand its failure behavior.

## Your assignment

1. Build the lexical baseline and label relevant source chunks for questions before tuning.
2. Ingest at least three formats, inspect extracted tables, and retain source/version/page or offset metadata.
3. Run learned embeddings and pgvector integration; compare keyword, dense, RRF hybrid, and cross-encoder reranking.
4. Add a local generator and claim-level citation review; distinguish unsupported answers from empty retrieval.
5. Test two tenants, public documents, permission changes, stale indexes, and malicious document instructions.

## Acceptance criteria

Diagnose one failure each from parsing, chunking, embedding, ranking, reranking, and generation. Prove no cross-tenant evidence reaches the model.

Also require documented inputs/outputs, explicit units and limitations, tests for normal/boundary/error cases, and a fresh-process run. Use only data you have permission to use; the supplied fixtures are fictional. Do not report a synthetic-data score as real-world quality.

## Starter workflow

Create work/stage07/, write a short interface contract, and implement the smallest end-to-end slice first. Use the exercise stubs below for function signatures and visible checks. Add your own tests before consulting the reference.

- [07a practice](../../curriculum/notebooks/07a_retrieval_from_first_principles.ipynb) · [worked answers](../../curriculum/solutions/07a_retrieval_from_first_principles.ipynb)
- [07b practice](../../curriculum/notebooks/07b_grounding_permissions_and_vector_search.ipynb) · [worked answers](../../curriculum/solutions/07b_grounding_permissions_and_vector_search.ipynb)

## Run the reference after your attempt

From the repository root with the environment active:

```bash
python -m pip install -r requirements/core.txt
python -m projects.stage07.solution
```

For model/service labs, read [INTEGRATIONS.md](../../curriculum/INTEGRATIONS.md) before running. Stage 10 additionally needs a local .env and a running Docker daemon. Output paths under work/ belong to you.

## Deliver

- Runnable code and tests with a setup README.
- A results report containing actual measurements and source/data versions.
- A failure you reproduced, diagnosed, and fixed.
- A short explanation of tradeoffs and remaining limits.
- Closed-book gate evidence and a scheduled review date.

[Worked answer and design reasoning](ANSWERS.md) · [Additional lab answers](../../curriculum/EXTRA_LABS.md)
