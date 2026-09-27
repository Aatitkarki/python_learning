# Stage 02 project — Math lab and regression from scratch

[Stage study guide](../../curriculum/stages/02.md) · [Course plan](../../curriculum/PLAN.md)

**Scenario:** You own a small component of a private research platform. A teammate must be able to reproduce it, inspect its evidence, and understand its failure behavior.

## Your assignment

1. Implement vector addition, dot product, cosine, matrix multiplication, transpose, mean, variance, and standard deviation without NumPy.
2. Plot linear/quadratic/log functions, a 2D rotation, and an eigenvector example; label units and axes.
3. Fit slope and intercept by gradient descent; verify gradients numerically and compare three learning rates.
4. Simulate Bernoulli/binomial trials and a normal sample; bootstrap a mean interval, compute covariance/correlation, and perform a permutation test.

## Acceptance criteria

Derive MSE gradients on paper, implement them, diagnose a diverging rate, and explain Bayes using counts in a hypothetical population. Pass changed-shape matrix tests.

Also require documented inputs/outputs, explicit units and limitations, tests for normal/boundary/error cases, and a fresh-process run. Use only data you have permission to use; the supplied fixtures are fictional. Do not report a synthetic-data score as real-world quality.

## Starter workflow

Create work/stage02/, write a short interface contract, and implement the smallest end-to-end slice first. Use the exercise stubs below for function signatures and visible checks. Add your own tests before consulting the reference.

- [02a practice](../../curriculum/notebooks/02a_vectors_matrices_and_algebra.ipynb) · [worked answers](../../curriculum/solutions/02a_vectors_matrices_and_algebra.ipynb)
- [02b practice](../../curriculum/notebooks/02b_derivatives_and_optimization.ipynb) · [worked answers](../../curriculum/solutions/02b_derivatives_and_optimization.ipynb)
- [02c practice](../../curriculum/notebooks/02c_probability_statistics_and_uncertainty.ipynb) · [worked answers](../../curriculum/solutions/02c_probability_statistics_and_uncertainty.ipynb)

## Run the reference after your attempt

From the repository root with the environment active:

```bash
python -m pip install -r requirements/core.txt
python -m projects.stage02.solution
```

For model/service labs, read [INTEGRATIONS.md](../../curriculum/INTEGRATIONS.md) before running. Stage 10 additionally needs a local .env and a running Docker daemon. Output paths under work/ belong to you.

## Deliver

- Runnable code and tests with a setup README.
- A results report containing actual measurements and source/data versions.
- A failure you reproduced, diagnosed, and fixed.
- A short explanation of tradeoffs and remaining limits.
- Closed-book gate evidence and a scheduled review date.

[Worked answer and design reasoning](ANSWERS.md) · [Additional lab answers](../../curriculum/EXTRA_LABS.md)
