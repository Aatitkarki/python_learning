# Stage 00 project — Reproducible learning workspace

<!-- question-answer-index -->
**Looking for a particular answer?** [Question-by-question solutions](SOLUTIONS.md) includes notebook exercises, explanations, independent assignments, and project tasks.


[Stage study guide](../../curriculum/stages/00.md) · [Course plan](../../curriculum/PLAN.md)

**Scenario:** You own a small component of a private research platform. A teammate must be able to reproduce it, inspect its evidence, and understand its failure behavior.

## Your assignment

1. Create your own notes/, work/, tests/, and project folders; keep secrets and environments out of Git.
2. Run hello.py from terminal and notebook. Record the interpreter path and explain any differences.
3. Create a branch, make two commits, inspect a diff, resolve a small practice conflict, and push to your own GitHub repository.

## Acceptance criteria

On a fresh terminal, create an environment, run a script, recover from an intentional NameError, and show a commit. Explain AI, ML, DL, NLP, CV, RL, LLMs, agents, data science, and engineering in your own words.

Also require documented inputs/outputs, explicit units and limitations, tests for normal/boundary/error cases, and a fresh-process run. Use only data you have permission to use; the supplied fixtures are fictional. Do not report a synthetic-data score as real-world quality.

## Starter workflow

Create work/stage00/, write a short interface contract, and implement the smallest end-to-end slice first. Use the exercise stubs below for function signatures and visible checks. Add your own tests before consulting the reference.

- [00a practice](../../curriculum/notebooks/00a_your_first_reproducible_experiment.ipynb) · [worked answers](../../curriculum/solutions/00a_your_first_reproducible_experiment.ipynb)

## Run the reference after your attempt

From the repository root with the environment active:

```bash
python -m pip install -r requirements/core.txt
python -m projects.stage00.solution
```

For model/service labs, read [INTEGRATIONS.md](../../curriculum/INTEGRATIONS.md) before running. Stage 10 additionally needs a local .env and a running Docker daemon. Output paths under work/ belong to you.

## Deliver

- Runnable code and tests with a setup README.
- A results report containing actual measurements and source/data versions.
- A failure you reproduced, diagnosed, and fixed.
- A short explanation of tradeoffs and remaining limits.
- Closed-book gate evidence and a scheduled review date.

[Worked answer and design reasoning](ANSWERS.md) · [Additional lab answers](../../curriculum/EXTRA_LABS.md)
