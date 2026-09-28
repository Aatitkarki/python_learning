# Stage 13 project — Versioned evaluation and release gates

<!-- question-answer-index -->
**Looking for a particular answer?** [Question-by-question solutions](SOLUTIONS.md) includes notebook exercises, explanations, independent assignments, and project tasks.


[Stage study guide](../../curriculum/stages/13.md) · [Course plan](../../curriculum/PLAN.md)

**Scenario:** You own a small component of a private research platform. A teammate must be able to reproduce it, inspect its evidence, and understand its failure behavior.

## Your assignment

1. Expand the nine-case fixture to at least 60 reviewed cases; preserve 20 as a locked holdout.
2. Separate retrieval, numeric correctness, citation support, abstention, permissions, tool behavior, and service quality.
3. Compare two candidates on paired questions, report slices and uncertainty, and inspect regressions.
4. Write machine-readable reports and fail CI on predeclared hard gates; version every component and label set.

## Acceptance criteria

Find a deliberately misleading evaluation, fix the split/metric, compare two systems, and defend a release decision including uncertainty and weak slices.

Also require documented inputs/outputs, explicit units and limitations, tests for normal/boundary/error cases, and a fresh-process run. Use only data you have permission to use; the supplied fixtures are fictional. Do not report a synthetic-data score as real-world quality.

## Starter workflow

Create work/stage13/, write a short interface contract, and implement the smallest end-to-end slice first. Use the exercise stubs below for function signatures and visible checks. Add your own tests before consulting the reference.

- [13a practice](../../curriculum/notebooks/13a_evaluation_datasets_and_retrieval_metrics.ipynb) · [worked answers](../../curriculum/solutions/13a_evaluation_datasets_and_retrieval_metrics.ipynb)
- [13b practice](../../curriculum/notebooks/13b_regression_gates_and_uncertainty.ipynb) · [worked answers](../../curriculum/solutions/13b_regression_gates_and_uncertainty.ipynb)

## Run the reference after your attempt

From the repository root with the environment active:

```bash
python -m pip install -r requirements/core.txt
python -m projects.stage13.solution --split dev --output work/evaluation.json
```

For model/service labs, read [INTEGRATIONS.md](../../curriculum/INTEGRATIONS.md) before running. Stage 10 additionally needs a local .env and a running Docker daemon. Output paths under work/ belong to you.

## Deliver

- Runnable code and tests with a setup README.
- A results report containing actual measurements and source/data versions.
- A failure you reproduced, diagnosed, and fixed.
- A short explanation of tradeoffs and remaining limits.
- Closed-book gate evidence and a scheduled review date.

[Worked answer and design reasoning](ANSWERS.md) · [Additional lab answers](../../curriculum/EXTRA_LABS.md)
