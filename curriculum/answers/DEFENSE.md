# Worked capstone defense

[All answers](../ANSWER_INDEX.md) · [Capstone brief](../CAPSTONE.md) · [Stage-by-stage assessment answers](../assessments/ANSWERS.md)

This is a worked example and scoring aid. Your independent implementation, timed attempt, deployment observations, and another person's reproduction must still come from your own work.

## Unseen feature: compare revenue growth

**Request:** Return Aurora's 2025 revenue growth with both source rows and the date at which the comparison became possible. Handle missing history, zero prior revenue, incompatible units, and unauthorized requests.

**Worked contract:** Authenticate first; obtain both annual statements through a tenant-scoped repository; require the same company/currency/unit and consecutive years; calculate `(current-prior)/prior` using Decimal; return a fraction plus both source IDs and publication dates. Missing/nonpositive prior revenue makes growth unknown. Unauthorized or missing records must reveal no private values. A later restatement must not be used for an earlier as-of decision.

The arithmetic and comparison guards are implemented in [finance_lab.py](../../projects/stage14/finance_lab.py), and scoped HTTP behavior in [report_lab.py](../../projects/stage15/report_lab.py). For the provided data, `(144-120)/120 = .20`, so Aurora's growth is 20%. A result based on only `aurora-2025` lacks the necessary prior source. The first decision time allowed by the conservative as-of rule is strictly after the later publication timestamp.

Acceptance cases:

| Input | Expected answer |
|---|---|
| Aurora 2025 versus 2024, tenant A | .20 with both sources |
| Beacon 2025 versus 2024, tenant A | 9/99, approximately .090909, with both sources |
| Aurora first available year | unknown: missing comparable prior year |
| Prior revenue zero | unknown: denominator undefined |
| Mixed currencies, units, or nonconsecutive years | reject comparison or explicitly unknown |
| Tenant B requesting Aurora | unavailable, no financial content |
| Decision before the later filing | no growth based on that unavailable filing |

For a 90-minute attempt: spend 10 minutes writing the contract and cases, 45 implementing, 20 testing adverse cases, and 15 explaining the request trace. The answer need not match the reference's internal structure; it must satisfy the behavior and evidence contract.

## Explain the architecture aloud

**Where does identity come from?** An authenticated credential maps to a trusted principal/tenant. The prompt and document contents cannot change it. The repository scopes reads before results reach retrieval, tools, or the model. Resource authorization is checked again on source fetch and cache reuse.

**Which component owns the answer?** The repository supplies evidence, deterministic functions calculate ratios, and the optional model drafts prose from verified results. The response names sources and unknowns. Model confidence is not a replacement for arithmetic or authorization.

**Why retain a fixed workflow?** A known financial comparison has predictable steps and fewer failure modes. Model routing is useful only when the task requires a decision that the fixed workflow cannot express economically; it still receives typed tools and bounded authority.

**Why does a citation not prove a claim?** The cited source must contain the correct period, units, and inputs. A source can exist while failing to support the number or conclusion. Derived growth requires two statements and a reproducible formula.

**What prevents a repeated write?** An application-level idempotency key tied to the exact action and a transactionally enforced unique record. A UI approval boolean or prompt does not enforce this. The course approval-journal calculation is pure; it does not claim atomicity across an external write and a local database.

**How do you know retrieval improved?** Compare fixed labeled dev cases, report paired differences with source-group uncertainty and failure slices, keep runtime budgets comparable, and reserve the holdout for the selected version. An aggregate gain cannot offset a permission leak.

**What does the local test not establish?** Real model behavior, deployment availability, GPU throughput, distributed cache invalidation, and remote executor recovery require the corresponding live observations.

## Diagnose a failed answer

| Symptom | First observation | Worked correction |
|---|---|---|
| A PDF amount loses its minus sign | Compare parsed page against original | Repair extraction and reindex; do not tune the prompt around corrupted data |
| Relevant passage absent from candidates | Check parser, chunk boundaries, query/embedding version | Correct that stage and rerun fixed retrieval labels |
| Passage present but answer wrong | Check period/unit arithmetic and each claim | Fix calculation or reject unsupported drafting |
| Tenant B sees Aurora after cache warming | Inspect cache key and authorization before hit | Bind scope/version and reauthorize every fetch |
| API ready but model unavailable | Trace dependency request timeout | Return visible bounded failure; preserve verified table if contract permits |
| Totals double after retry | Inspect transaction IDs and join cardinality | Enforce idempotency and correct duplicate-producing joins |
| Rollback starts but old app cannot read new schema | Compare schema compatibility | Stop promotion and restore a tested compatible release/data path |

## Example architecture decisions

**Money representation:** Integer cents for expense records and Decimal with explicit statement units for financial ratios. This keeps exact ledger totals and avoids mixing million-dollar statements with per-share prices. Tradeoff: boundary conversion and rounding policies must be explicit.

**Model authority:** The local generator produces an unverified draft from a verified table. It cannot set tenant, execute unrestricted SQL, or approve writes. Tradeoff: some prose remains withheld until support checks/review pass.

**Deployment:** PostgreSQL on a private service/volume; API behind HTTPS; inference endpoint private; readiness separate from liveness. A named release captures dependencies/image/schema/model/index versions. Tradeoff: reproducing operations requires a real host and restore rehearsal, beyond local unit tests.

## Outage, restore, and reproduction evidence

Run [the failure lab](../../projects/stage10/failure_lab.py) and [the PostgreSQL restore procedure](../../projects/stage10/RUNBOOK.md). An acceptable incident record includes actual start/recovery times, a request ID, observed status, safe error type, changed component, pre/post row counts and sums, and a successful authenticated read from the restored database. A blank record marked pending is more accurate than fabricated success.

Give a reviewer a fresh checkout, environment setup, exact commands, fixture hashes, and expected invariant outputs. Ask them to run without your environment or hidden notebook state. Record the actual failed step and fix it. There is no reference file that can substitute for their reproduction.

## Reviewer rubric

Use each stage's `SOLUTIONS.md` mastery-gate entry to locate its implementations and expected reasoning. Score correctness/reasoning 40, independent implementation 25, meaningful tests/debugging 20, explanation/reproducibility 15. Pass at 80/100 only with no permission leak, future-data leakage, invented evidence, or unreproducible core result. Keep live requirements pending until demonstrated. After seven and thirty days repeat a changed-input problem from a blank file; do not award mastery for running the reference.
