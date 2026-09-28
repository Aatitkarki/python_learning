# Stage 04 project — Support-ticket classifier and demand regression

<!-- question-answer-index -->
**Looking for a particular answer?** [Question-by-question solutions](SOLUTIONS.md) includes notebook exercises, explanations, independent assignments, and project tasks.


[Stage study guide](../../curriculum/stages/04.md) · [Course plan](../../curriculum/PLAN.md)

**Scenario:** You own a small component of a private research platform. A teammate must be able to reproduce it, inspect its evidence, and understand its failure behavior.

## Your assignment

1. Use the supplied fixed train/validation/test split; verify template groups never cross boundaries.
2. Compare majority, logistic, forest, and boosting classifiers; select on validation macro-F1, then evaluate once on test.
3. Create a demand regression dataset and compare mean, linear, tree, forest, and boosting models using MAE/RMSE/R².
4. Compare KMeans/DBSCAN on blobs and moons, investigate PCA, and collect 20+ independent ticket errors for a model card.
5. Expose one saved trusted classifier through a prediction API; validate input size and return label scores with calibration limitations.

## Acceptance criteria

Spot three leakage mechanisms, justify a split and metric, implement a pipeline, and explain five wrong predictions. Train on a new dataset without copying the notebook.

Also require documented inputs/outputs, explicit units and limitations, tests for normal/boundary/error cases, and a fresh-process run. Use only data you have permission to use; the supplied fixtures are fictional. Do not report a synthetic-data score as real-world quality.

## Starter workflow

Create work/stage04/, write a short interface contract, and implement the smallest end-to-end slice first. Use the exercise stubs below for function signatures and visible checks. Add your own tests before consulting the reference.

- [04a practice](../../curriculum/notebooks/04a_supervised_learning_without_leakage.ipynb) · [worked answers](../../curriculum/solutions/04a_supervised_learning_without_leakage.ipynb)
- [04b practice](../../curriculum/notebooks/04b_metrics_clustering_and_error_analysis.ipynb) · [worked answers](../../curriculum/solutions/04b_metrics_clustering_and_error_analysis.ipynb)

## Run the reference after your attempt

From the repository root with the environment active:

```bash
python -m pip install -r requirements/core.txt
python -m projects.stage04.solution
```

For model/service labs, read [INTEGRATIONS.md](../../curriculum/INTEGRATIONS.md) before running. Stage 10 additionally needs a local .env and a running Docker daemon. Output paths under work/ belong to you.

## Deliver

- Runnable code and tests with a setup README.
- A results report containing actual measurements and source/data versions.
- A failure you reproduced, diagnosed, and fixed.
- A short explanation of tradeoffs and remaining limits.
- Closed-book gate evidence and a scheduled review date.

[Worked answer and design reasoning](ANSWERS.md) · [Additional lab answers](../../curriculum/EXTRA_LABS.md)
