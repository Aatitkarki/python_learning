# Stage 05 project — NumPy XOR and PyTorch digits classifier

<!-- question-answer-index -->
**Looking for a particular answer?** [Question-by-question solutions](SOLUTIONS.md) includes notebook exercises, explanations, independent assignments, and project tasks.


[Stage study guide](../../curriculum/stages/05.md) · [Course plan](../../curriculum/PLAN.md)

**Scenario:** You own a small component of a private research platform. A teammate must be able to reproduce it, inspect its evidence, and understand its failure behavior.

## Your assignment

1. Implement a two-layer NumPy XOR network and check analytical gradients against finite differences.
2. Train an MLP and CNN on the same digits split using CPU, with a real DataLoader and validation loop.
3. Save training curves and the best validation checkpoint; evaluate test once after selection.
4. Run controlled learning-rate, dropout, and normalization experiments; record seed, parameter count, runtime, and failure diagnosis.

## Acceptance criteria

Write a training loop from memory, overfit a tiny batch, explain tensor shapes and chain rule, then diagnose an injected gradient/mode bug.

Also require documented inputs/outputs, explicit units and limitations, tests for normal/boundary/error cases, and a fresh-process run. Use only data you have permission to use; the supplied fixtures are fictional. Do not report a synthetic-data score as real-world quality.

## Starter workflow

Create work/stage05/, write a short interface contract, and implement the smallest end-to-end slice first. Use the exercise stubs below for function signatures and visible checks. Add your own tests before consulting the reference.

- [05a practice](../../curriculum/notebooks/05a_a_neural_network_from_scratch.ipynb) · [worked answers](../../curriculum/solutions/05a_a_neural_network_from_scratch.ipynb)
- [05b practice](../../curriculum/notebooks/05b_pytorch_training_and_image_classification.ipynb) · [worked answers](../../curriculum/solutions/05b_pytorch_training_and_image_classification.ipynb)

## Run the reference after your attempt

From the repository root with the environment active:

```bash
python -m pip install -r requirements/deep.txt
python -m projects.stage05.solution
```

For model/service labs, read [INTEGRATIONS.md](../../curriculum/INTEGRATIONS.md) before running. Stage 10 additionally needs a local .env and a running Docker daemon. Output paths under work/ belong to you.

## Deliver

- Runnable code and tests with a setup README.
- A results report containing actual measurements and source/data versions.
- A failure you reproduced, diagnosed, and fixed.
- A short explanation of tradeoffs and remaining limits.
- Closed-book gate evidence and a scheduled review date.

[Worked answer and design reasoning](ANSWERS.md) · [Additional lab answers](../../curriculum/EXTRA_LABS.md)
