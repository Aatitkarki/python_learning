# Stage 10 — worked project answer

Read after saving your own attempt. The reference is one implementation, not the only acceptable design.

## Reference artifacts

- [Dockerfile](Dockerfile)
- [Compose](../../compose.yaml)
- [Operational answer/runbook](RUNBOOK.md)
- [CI workflow](../../.github/workflows/course.yml)

## Expected behavior and reasoning

See RUNBOOK.md for concrete startup, backup, restore, and failure commands. The supplied Compose is a local teaching environment bound to loopback. Its tags/ranges should be locked before deployment. The API has process-local limits and shared tenant API keys for learning; production needs an identity provider, durable distributed rate limiting, monitoring, migration tooling, and operational review. Liveness is not readiness, and a backup file without a restore test is not evidence of recovery.

## How to review your work

Compare the input/output contract first, then edge behavior, data boundaries, and failure modes. Different implementation details are acceptable when you can explain them and demonstrate the same or stronger guarantees. Record actual observed model/latency results instead of treating example scores as universal answers.

## Transfer and extension answer key

The [extra lab answer guide](../../curriculum/EXTRA_LABS.md) supplies derivations, query examples, algorithms, and design answers for the larger extensions. The corresponding solved notebooks answer each checked exercise and each oral question:

- [10a practice](../../curriculum/notebooks/10a_reliability_and_observability.ipynb) · [worked answers](../../curriculum/solutions/10a_reliability_and_observability.ipynb)
- [10b practice](../../curriculum/notebooks/10b_containers_configuration_and_deployment.ipynb) · [worked answers](../../curriculum/solutions/10b_containers_configuration_and_deployment.ipynb)

## Common wrong answer

A runnable happy path alone does not satisfy the project. A missing dependency or unavailable external service is pending evidence; a mock is useful for unit testing but does not prove the actual integration. Copying the reference does not pass the independent gate.
