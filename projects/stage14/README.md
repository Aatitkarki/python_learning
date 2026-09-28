# Stage 14 project — Statement comparison and time-series analysis

<!-- question-answer-index -->
**Looking for a particular answer?** [Question-by-question solutions](SOLUTIONS.md) includes notebook exercises, explanations, independent assignments, and project tasks.


[Stage study guide](../../curriculum/stages/14.md) · [Course plan](../../curriculum/PLAN.md)

**Scenario:** You own a small component of a private research platform. A teammate must be able to reproduce it, inspect its evidence, and understand its failure behavior.

## Your assignment

1. Reconcile fictional statements and calculate all ratios in the roadmap with source IDs and undefined-case policy.
2. Compare three years for two companies; distinguish period, currency, scale, average versus ending balances, and capex signs.
3. Create past-only features, walk-forward splits, and an as-of publication-date join.
4. Compare a forecast to naive baselines; include turnover/cost assumptions if building a strategy. Explain why no predictive edge is established.

## Acceptance criteria

Explain all units in a comparison, identify a publication-time leak, build a walk-forward baseline, and explain why a backtest is not proof of investment value.

Also require documented inputs/outputs, explicit units and limitations, tests for normal/boundary/error cases, and a fresh-process run. Use only data you have permission to use; the supplied fixtures are fictional. Do not report a synthetic-data score as real-world quality.

## Starter workflow

Create work/stage14/, write a short interface contract, and implement the smallest end-to-end slice first. Use the exercise stubs below for function signatures and visible checks. Add your own tests before consulting the reference.

- [14a practice](../../curriculum/notebooks/14a_financial_statements_and_ratios.ipynb) · [worked answers](../../curriculum/solutions/14a_financial_statements_and_ratios.ipynb)
- [14b practice](../../curriculum/notebooks/14b_time_series_and_honest_backtests.ipynb) · [worked answers](../../curriculum/solutions/14b_time_series_and_honest_backtests.ipynb)

## Run the reference after your attempt

From the repository root with the environment active:

```bash
python -m pip install -r requirements/core.txt
python -m projects.stage14.solution
```

For model/service labs, read [INTEGRATIONS.md](../../curriculum/INTEGRATIONS.md) before running. Stage 10 additionally needs a local .env and a running Docker daemon. Output paths under work/ belong to you.

## Deliver

- Runnable code and tests with a setup README.
- A results report containing actual measurements and source/data versions.
- A failure you reproduced, diagnosed, and fixed.
- A short explanation of tradeoffs and remaining limits.
- Closed-book gate evidence and a scheduled review date.

[Worked answer and design reasoning](ANSWERS.md) · [Additional lab answers](../../curriculum/EXTRA_LABS.md)
