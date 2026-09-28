# Stage 08 project — Bounded research assistant with approval

<!-- question-answer-index -->
**Looking for a particular answer?** [Question-by-question solutions](SOLUTIONS.md) includes notebook exercises, explanations, independent assignments, and project tasks.


[Stage study guide](../../curriculum/stages/08.md) · [Course plan](../../curriculum/PLAN.md)

**Scenario:** You own a small component of a private research platform. A teammate must be able to reproduce it, inspect its evidence, and understand its failure behavior.

## Your assignment

1. Implement document-search, financial-record lookup, and calculator tools with schemas and server-side scope.
2. Create a plain Python workflow, then the equivalent LangGraph; compare traces on the same requests.
3. Persist a checkpoint, interrupt before a proposed action, bind approval to exact content, resume or deny, and isolate run IDs.
4. Inject transient failures, malformed arguments, repeated calls, timeouts, and budget exhaustion.
5. Only as an experiment, split research and checking into two workers and compare task success, calls, latency, and cost.

## Acceptance criteria

Show correct tool selection, arguments, bounded termination, visible failures, denied altered approvals, and isolated state. Explain when a fixed workflow is preferable.

Also require documented inputs/outputs, explicit units and limitations, tests for normal/boundary/error cases, and a fresh-process run. Use only data you have permission to use; the supplied fixtures are fictional. Do not report a synthetic-data score as real-world quality.

## Starter workflow

Create work/stage08/, write a short interface contract, and implement the smallest end-to-end slice first. Use the exercise stubs below for function signatures and visible checks. Add your own tests before consulting the reference.

- [08a practice](../../curriculum/notebooks/08a_tools_and_bounded_workflows.ipynb) · [worked answers](../../curriculum/solutions/08a_tools_and_bounded_workflows.ipynb)
- [08b practice](../../curriculum/notebooks/08b_langgraph_state_and_human_review.ipynb) · [worked answers](../../curriculum/solutions/08b_langgraph_state_and_human_review.ipynb)

## Run the reference after your attempt

From the repository root with the environment active:

```bash
python -m pip install -r requirements/agents.txt
python -m projects.stage08.solution
```

For model/service labs, read [INTEGRATIONS.md](../../curriculum/INTEGRATIONS.md) before running. Stage 10 additionally needs a local .env and a running Docker daemon. Output paths under work/ belong to you.

## Deliver

- Runnable code and tests with a setup README.
- A results report containing actual measurements and source/data versions.
- A failure you reproduced, diagnosed, and fixed.
- A short explanation of tradeoffs and remaining limits.
- Closed-book gate evidence and a scheduled review date.

[Worked answer and design reasoning](ANSWERS.md) · [Additional lab answers](../../curriculum/EXTRA_LABS.md)
