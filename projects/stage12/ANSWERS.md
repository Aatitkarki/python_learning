# Stage 12 — worked project answer

<!-- question-answer-index -->
**Looking for a particular answer?** [Question-by-question solutions](SOLUTIONS.md) includes notebook exercises, explanations, independent assignments, and project tasks.


Read after saving your own attempt. The reference is one implementation, not the only acceptable design.

## Reference artifacts

- [solution.py](solution.py)

## Expected behavior and reasoning

The six reference checks verify actual API outcomes, including permitted access for tenant B and denial for tenant A. A model never receives privileged execution authority from document text. HTML escaping is context-specific, SQL parameters handle values, and tools use allowlists. A zero-failure finite test suite does not prove universal injection resistance; preserve residual risks and add new cases as attacks are discovered.

## How to review your work

Compare the input/output contract first, then edge behavior, data boundaries, and failure modes. Different implementation details are acceptable when you can explain them and demonstrate the same or stronger guarantees. Record actual observed model/latency results instead of treating example scores as universal answers.

## Transfer and extension answer key

The [extra lab answer guide](../../curriculum/EXTRA_LABS.md) supplies derivations, query examples, algorithms, and design answers for the larger extensions. The corresponding solved notebooks answer each checked exercise and each oral question:

- [12a practice](../../curriculum/notebooks/12a_threat_models_and_untrusted_content.ipynb) · [worked answers](../../curriculum/solutions/12a_threat_models_and_untrusted_content.ipynb)
- [12b practice](../../curriculum/notebooks/12b_authorization_caches_and_isolation.ipynb) · [worked answers](../../curriculum/solutions/12b_authorization_caches_and_isolation.ipynb)

## Common wrong answer

A runnable happy path alone does not satisfy the project. A missing dependency or unavailable external service is pending evidence; a mock is useful for unit testing but does not prove the actual integration. Copying the reference does not pass the independent gate.
