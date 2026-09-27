# Stage 12 project — Threat model and adversarial test suite

[Stage study guide](../../curriculum/stages/12.md) · [Course plan](../../curriculum/PLAN.md)

**Scenario:** You own a small component of a private research platform. A teammate must be able to reproduce it, inspect its evidence, and understand its failure behavior.

## Your assignment

1. Map assets, actors, entry points, trust boundaries, controls, tests, and residual risks.
2. Write at least 20 attacks against your own app: cross-tenant access, prompt injection, malformed tool calls, oversized inputs, and forged citations.
3. Test allowed access alongside every denial; cover warm caches, revocation, graph state, logs, and document fetches.
4. Record observed behavior and fix failures with code-enforced policy rather than a stronger-sounding prompt.

## Acceptance criteria

Demonstrate access boundaries with positive/negative tests, explain why prompt-only defenses fail, and trace one incident without exposing secrets.

Also require documented inputs/outputs, explicit units and limitations, tests for normal/boundary/error cases, and a fresh-process run. Use only data you have permission to use; the supplied fixtures are fictional. Do not report a synthetic-data score as real-world quality.

## Starter workflow

Create work/stage12/, write a short interface contract, and implement the smallest end-to-end slice first. Use the exercise stubs below for function signatures and visible checks. Add your own tests before consulting the reference.

- [12a practice](../../curriculum/notebooks/12a_threat_models_and_untrusted_content.ipynb) · [worked answers](../../curriculum/solutions/12a_threat_models_and_untrusted_content.ipynb)
- [12b practice](../../curriculum/notebooks/12b_authorization_caches_and_isolation.ipynb) · [worked answers](../../curriculum/solutions/12b_authorization_caches_and_isolation.ipynb)

## Run the reference after your attempt

From the repository root with the environment active:

```bash
python -m pip install -r requirements/core.txt
python -m projects.stage12.solution
```

For model/service labs, read [INTEGRATIONS.md](../../curriculum/INTEGRATIONS.md) before running. Stage 10 additionally needs a local .env and a running Docker daemon. Output paths under work/ belong to you.

## Deliver

- Runnable code and tests with a setup README.
- A results report containing actual measurements and source/data versions.
- A failure you reproduced, diagnosed, and fixed.
- A short explanation of tradeoffs and remaining limits.
- Closed-book gate evidence and a scheduled review date.

[Worked answer and design reasoning](ANSWERS.md) · [Additional lab answers](../../curriculum/EXTRA_LABS.md)
