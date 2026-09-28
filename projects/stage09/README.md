# Stage 09 project — Local inference benchmark

<!-- question-answer-index -->
**Looking for a particular answer?** [Question-by-question solutions](SOLUTIONS.md) includes notebook exercises, explanations, independent assignments, and project tasks.


[Stage study guide](../../curriculum/stages/09.md) · [Course plan](../../curriculum/PLAN.md)

**Scenario:** You own a small component of a private research platform. A teammate must be able to reproduce it, inspect its evidence, and understand its failure behavior.

## Your assignment

1. Estimate weights and KV cache for three sizes/precisions/context lengths, then compare to actual memory.
2. Install a compatible local server and select a licensed model that fits; record exact model ID/revision.
3. Run native Ollama requests and, on supported hardware, vLLM-compatible requests.
4. Measure 30+ warm/cold observations and concurrency levels with prompt/output lengths, p50/p95, failures, and resource use.
5. Connect the Stage 07 assistant to the local endpoint and verify data does not leave the intended host.

## Acceptance criteria

Explain a measured bottleneck, enforce timeouts/output bounds, demonstrate model-unavailable failure, and justify a hardware/precision choice from evidence.

Also require documented inputs/outputs, explicit units and limitations, tests for normal/boundary/error cases, and a fresh-process run. Use only data you have permission to use; the supplied fixtures are fictional. Do not report a synthetic-data score as real-world quality.

## Starter workflow

Create work/stage09/, write a short interface contract, and implement the smallest end-to-end slice first. Use the exercise stubs below for function signatures and visible checks. Add your own tests before consulting the reference.

- [09a practice](../../curriculum/notebooks/09a_memory_and_serving_performance.ipynb) · [worked answers](../../curriculum/solutions/09a_memory_and_serving_performance.ipynb)
- [09b practice](../../curriculum/notebooks/09b_local_model_api_contracts.ipynb) · [worked answers](../../curriculum/solutions/09b_local_model_api_contracts.ipynb)

## Run the reference after your attempt

From the repository root with the environment active:

```bash
python -m pip install -r requirements/core.txt
python -m projects.stage09.serve --model YOUR_INSTALLED_MODEL --runs 3
```

For model/service labs, read [INTEGRATIONS.md](../../curriculum/INTEGRATIONS.md) before running. Stage 10 additionally needs a local .env and a running Docker daemon. Output paths under work/ belong to you.

## Deliver

- Runnable code and tests with a setup README.
- A results report containing actual measurements and source/data versions.
- A failure you reproduced, diagnosed, and fixed.
- A short explanation of tradeoffs and remaining limits.
- Closed-book gate evidence and a scheduled review date.

[Worked answer and design reasoning](ANSWERS.md) · [Additional lab answers](../../curriculum/EXTRA_LABS.md)
