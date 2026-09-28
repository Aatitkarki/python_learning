# Stage 08 — worked project answer

<!-- question-answer-index -->
**Looking for a particular answer?** [Question-by-question solutions](SOLUTIONS.md) includes notebook exercises, explanations, independent assignments, and project tasks.


Read after saving your own attempt. The reference is one implementation, not the only acceptable design.

## Reference artifacts

- [Bounded search, SQL, and calculator workflow](research.py) — run `python -m projects.stage08.research`. The tenant is trusted application state, not a model argument.

- [solution.py](solution.py)

## Expected behavior and reasoning

The runnable graph interrupts before a division, checks a fingerprint bound to actor/proposal, and resumes to result 1.2. InMemorySaver is not durable storage. For crash recovery choose a supported durable checkpointer and isolate credentials/run IDs. A fingerprint does not authenticate an approver; verify identity and expire/consume approvals in the service. Count budgets in code and use network timeouts; a between-step timer cannot interrupt blocked I/O.

## How to review your work

Compare the input/output contract first, then edge behavior, data boundaries, and failure modes. Different implementation details are acceptable when you can explain them and demonstrate the same or stronger guarantees. Record actual observed model/latency results instead of treating example scores as universal answers.

## Transfer and extension answer key

The [extra lab answer guide](../../curriculum/EXTRA_LABS.md) supplies derivations, query examples, algorithms, and design answers for the larger extensions. The corresponding solved notebooks answer each checked exercise and each oral question:

- [08a practice](../../curriculum/notebooks/08a_tools_and_bounded_workflows.ipynb) · [worked answers](../../curriculum/solutions/08a_tools_and_bounded_workflows.ipynb)
- [08b practice](../../curriculum/notebooks/08b_langgraph_state_and_human_review.ipynb) · [worked answers](../../curriculum/solutions/08b_langgraph_state_and_human_review.ipynb)

## Common wrong answer

A runnable happy path alone does not satisfy the project. A missing dependency or unavailable external service is pending evidence; a mock is useful for unit testing but does not prove the actual integration. Copying the reference does not pass the independent gate.
