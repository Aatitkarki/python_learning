# Stage 15 project — Private financial research platform

<!-- question-answer-index -->
**Looking for a particular answer?** [Question-by-question solutions](SOLUTIONS.md) includes notebook exercises, explanations, independent assignments, and project tasks.


[Stage study guide](../../curriculum/stages/15.md) · [Course plan](../../curriculum/PLAN.md)

**Scenario:** You own a small component of a private research platform. A teammate must be able to reproduce it, inspect its evidence, and understand its failure behavior.

## Your assignment

1. Build an independent version from the brief; use reference code only after attempting each component.
2. Answer a two-company three-year revenue/margin/FCF comparison with deterministic calculations and citations.
3. Integrate learned embeddings, PostgreSQL, local model serving, bounded tools, permissions, and a usable client such as the API docs or a small CLI.
4. Run the full failure matrix, restore backup, rehearse deployment/rollback, and write an architecture decision record.
5. Grow the evaluation corpus to at least 100 reviewed cases and target 500 as the domain expands; preserve a locked holdout.
6. Complete a 90-minute unseen feature, explain every component, and have another person reproduce the system.

## Acceptance criteria

Score at least 80/100 with every critical gate passed; demonstrate an unseen task, permission isolation, correct citations/calculations, safe failures, restore, and reproducibility.

Also require documented inputs/outputs, explicit units and limitations, tests for normal/boundary/error cases, and a fresh-process run. Use only data you have permission to use; the supplied fixtures are fictional. Do not report a synthetic-data score as real-world quality.

## Starter workflow

Create work/stage15/, write a short interface contract, and implement the smallest end-to-end slice first. Use the exercise stubs below for function signatures and visible checks. Add your own tests before consulting the reference.

- [15a practice](../../curriculum/notebooks/15a_an_evidence-backed_financial_research_pipeline.ipynb) · [worked answers](../../curriculum/solutions/15a_an_evidence-backed_financial_research_pipeline.ipynb)
- [15b practice](../../curriculum/notebooks/15b_architecture_review_and_mastery_defense.ipynb) · [worked answers](../../curriculum/solutions/15b_architecture_review_and_mastery_defense.ipynb)

## Run the reference after your attempt

From the repository root with the environment active:

```bash
python -m pip install -r requirements/core.txt
python -m projects.stage15.solution
```

For model/service labs, read [INTEGRATIONS.md](../../curriculum/INTEGRATIONS.md) before running. Stage 10 additionally needs a local .env and a running Docker daemon. Output paths under work/ belong to you.

## Deliver

- Runnable code and tests with a setup README.
- A results report containing actual measurements and source/data versions.
- A failure you reproduced, diagnosed, and fixed.
- A short explanation of tradeoffs and remaining limits.
- Closed-book gate evidence and a scheduled review date.

[Worked answer and design reasoning](ANSWERS.md) · [Additional lab answers](../../curriculum/EXTRA_LABS.md)
