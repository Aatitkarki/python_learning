# Stage 10 project — Containerized service and recovery runbook

[Stage study guide](../../curriculum/stages/10.md) · [Course plan](../../curriculum/PLAN.md)

**Scenario:** You own a small component of a private research platform. A teammate must be able to reproduce it, inspect its evidence, and understand its failure behavior.

## Your assignment

1. Run the API and PostgreSQL using the provided Dockerfile/Compose, then inspect networking and persistent data.
2. Add request IDs, versioned events, safe logs, latency/error metrics, and an operational dashboard or report.
3. Simulate database/model outages, bad auth, malformed/huge input, corrupt files, and exhausted capacity.
4. Perform backup and restore into a separate database; prove row counts and application reads after restore.
5. Add CI, create a release lock and image digest, rehearse rollback, and document a Coolify deployment with private database networking and HTTPS.

## Acceptance criteria

Reproduce deployment from a fresh checkout, survive an injected outage, restore a backup, identify a slow component from measurements, and execute a documented rollback.

Also require documented inputs/outputs, explicit units and limitations, tests for normal/boundary/error cases, and a fresh-process run. Use only data you have permission to use; the supplied fixtures are fictional. Do not report a synthetic-data score as real-world quality.

## Starter workflow

Create work/stage10/, write a short interface contract, and implement the smallest end-to-end slice first. Use the exercise stubs below for function signatures and visible checks. Add your own tests before consulting the reference.

- [10a practice](../../curriculum/notebooks/10a_reliability_and_observability.ipynb) · [worked answers](../../curriculum/solutions/10a_reliability_and_observability.ipynb)
- [10b practice](../../curriculum/notebooks/10b_containers_configuration_and_deployment.ipynb) · [worked answers](../../curriculum/solutions/10b_containers_configuration_and_deployment.ipynb)

## Run the reference after your attempt

From the repository root with the environment active:

```bash
python -m pip install -r requirements/core.txt
docker compose up --build -d
```

For model/service labs, read [INTEGRATIONS.md](../../curriculum/INTEGRATIONS.md) before running. Stage 10 additionally needs a local .env and a running Docker daemon. Output paths under work/ belong to you.

## Deliver

- Runnable code and tests with a setup README.
- A results report containing actual measurements and source/data versions.
- A failure you reproduced, diagnosed, and fixed.
- A short explanation of tradeoffs and remaining limits.
- Closed-book gate evidence and a scheduled review date.

[Worked answer and design reasoning](ANSWERS.md) · [Additional lab answers](../../curriculum/EXTRA_LABS.md)
