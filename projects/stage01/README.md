# Stage 01 project — Expense analyzer and command-line utilities

<!-- question-answer-index -->
**Looking for a particular answer?** [Question-by-question solutions](SOLUTIONS.md) includes notebook exercises, explanations, independent assignments, and project tasks.


[Stage study guide](../../curriculum/stages/01.md) · [Course plan](../../curriculum/PLAN.md)

**Scenario:** You own a small component of a private research platform. A teammate must be able to reproduce it, inspect its evidence, and understand its failure behavior.

## Your assignment

1. Build calculator, temperature/profit tools, text analyzer, contact book, and inventory before the main project.
2. Build a CSV expense CLI with total, category totals, monthly totals, average, highest expense, and clear line-numbered errors.
3. Split parsing, calculation, and CLI code; add tests for empty files, quotes, malformed dates, NaN, negative amounts, and missing columns.
4. Refactor one component to a class using composition; profile linear and binary search and explain recursion with a base case.

## Acceptance criteria

In 90 minutes build a new CSV inventory summarizer from a blank file, with validation and five meaningful tests. Explain each function and one time-complexity tradeoff without opening answers.

Also require documented inputs/outputs, explicit units and limitations, tests for normal/boundary/error cases, and a fresh-process run. Use only data you have permission to use; the supplied fixtures are fictional. Do not report a synthetic-data score as real-world quality.

## Starter workflow

Create work/stage01/, write a short interface contract, and implement the smallest end-to-end slice first. Use the exercise stubs below for function signatures and visible checks. Add your own tests before consulting the reference.

- [01a practice](../../curriculum/notebooks/01a_variables_decisions_and_functions.ipynb) · [worked answers](../../curriculum/solutions/01a_variables_decisions_and_functions.ipynb)
- [01b practice](../../curriculum/notebooks/01b_collections_loops_and_text.ipynb) · [worked answers](../../curriculum/solutions/01b_collections_loops_and_text.ipynb)
- [01c practice](../../curriculum/notebooks/01c_files_validation_and_money.ipynb) · [worked answers](../../curriculum/solutions/01c_files_validation_and_money.ipynb)
- [01d practice](../../curriculum/notebooks/01d_objects_algorithms_and_debugging.ipynb) · [worked answers](../../curriculum/solutions/01d_objects_algorithms_and_debugging.ipynb)

## Run the reference after your attempt

From the repository root with the environment active:

```bash
python -m pip install -r requirements/core.txt
python -m projects.stage01.solution datasets/expenses.csv
```

For model/service labs, read [INTEGRATIONS.md](../../curriculum/INTEGRATIONS.md) before running. Stage 10 additionally needs a local .env and a running Docker daemon. Output paths under work/ belong to you.

## Deliver

- Runnable code and tests with a setup README.
- A results report containing actual measurements and source/data versions.
- A failure you reproduced, diagnosed, and fixed.
- A short explanation of tradeoffs and remaining limits.
- Closed-book gate evidence and a scheduled review date.

[Worked answer and design reasoning](ANSWERS.md) · [Additional lab answers](../../curriculum/EXTRA_LABS.md)
