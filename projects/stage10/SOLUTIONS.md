# Stage 10: question-by-question solutions

[All-stage answer index](../../curriculum/ANSWER_INDEX.md) · [Project brief](README.md)

`solution.py` is the main project reference. It does not contain every answer. Use the exact question IDs below to find the smaller exercises and extra programs.

**Suggested workflow:** notebook → independent assignment in your own `.py` files → stage project → closed-book gate. Compare answers only after an attempt; then close them and rebuild with changed input.

## Notebook questions and independent assignments

### 10a: Reliability and observability

[Test your independent assignment](../../curriculum/assignments/10a.md)

| ID | Question | Answer |
|---|---|---|
| 10a-E1 | Return fraction of events with ok=True and latency_ms<=target. Empty input raises ValueError. | [Worked solution](../../curriculum/answers/10a.md#10a-e1) |
| 10a-E2 | Keep request_id,status,latency_ms only; omit every other key. | [Worked solution](../../curriculum/answers/10a.md#10a-e2) |
| 10a-E3 | Given a mutable cache and key,payload,result, save (payload,result) on first call, return existing result for same payload, reject changed payload. | [Worked solution](../../curriculum/answers/10a.md#10a-e3) |
| 10a-O1 | Liveness versus readiness? | [Worked solution](../../curriculum/answers/10a.md#10a-o1) |
| 10a-O2 | What proves a backup works? | [Worked solution](../../curriculum/answers/10a.md#10a-o2) |
| 10a-T | Inject a database outage, model timeout, invalid auth, malformed body, oversized prompt, and corrupt document. Record status, latency, logs, recovery steps, and whether retries could duplicate work. | [Worked solution](../../curriculum/answers/10a.md#10a-t) |

### 10b: Containers, configuration, and deployment

[Test your independent assignment](../../curriculum/assignments/10b.md)

| ID | Question | Answer |
|---|---|---|
| 10b-E1 | Read a mapping with DATABASE_URL and API_KEY; reject missing/blank values or API_KEY shorter than 24 characters. | [Worked solution](../../curriculum/answers/10b.md#10b-e1) |
| 10b-E2 | Return True only when tests, evals, migration_rehearsal, and restore_drill are all exactly True. | [Worked solution](../../curriculum/answers/10b.md#10b-e2) |
| 10b-E3 | A service supports schema versions inclusive [minimum,maximum]. Return whether current is compatible; reject inverted bounds. | [Worked solution](../../curriculum/answers/10b.md#10b-e3) |
| 10b-O1 | Why is localhost often wrong in Compose? | [Worked solution](../../curriculum/answers/10b.md#10b-o1) |
| 10b-O2 | Why pin release artifacts? | [Worked solution](../../curriculum/answers/10b.md#10b-o2) |
| 10b-T | Use the provided Dockerfile/Compose, run API+PostgreSQL, test persistence after restart, and rehearse backup/restore into a separate database. Add CI and document a Coolify deployment and rollback without publishing secrets. | [Worked solution](../../curriculum/answers/10b.md#10b-t) |

## Project tasks, in brief order

<a id="10-p1"></a>
### 10-P1

**Question:** Run the API and PostgreSQL using the provided Dockerfile/Compose, then inspect networking and persistent data.

**Answer:** [10b worked implementation and explanation](../../curriculum/answers/10b.md#10b-t)

<a id="10-p2"></a>
### 10-P2

**Question:** Add request IDs, versioned events, safe logs, latency/error metrics, and an operational dashboard or report.

**Answer:** [10a worked implementation and explanation](../../curriculum/answers/10a.md#10a-t)

<a id="10-p3"></a>
### 10-P3

**Question:** Simulate database/model outages, bad auth, malformed/huge input, corrupt files, and exhausted capacity.

**Answer:** [10a worked implementation and explanation](../../curriculum/answers/10a.md#10a-t)

<a id="10-p4"></a>
### 10-P4

**Question:** Perform backup and restore into a separate database; prove row counts and application reads after restore.

**Answer:** [10b worked implementation and explanation](../../curriculum/answers/10b.md#10b-t)

<a id="10-p5"></a>
### 10-P5

**Question:** Add CI, create a release lock and image digest, rehearse rollback, and document a Coolify deployment with private database networking and HTTPS.

**Answer:** [10b worked implementation and explanation](../../curriculum/answers/10b.md#10b-t)

<a id="10-g"></a>
## Mastery gate: 10-G

**Task:** Reproduce deployment from a fresh checkout, survive an injected outage, restore a backup, identify a slow component from measurements, and execute a documented rollback.

**Expected reasoning and invariant outputs:** See RUNBOOK.md for concrete startup, backup, restore, and failure commands. The supplied Compose is a local teaching environment bound to loopback. Its tags/ranges should be locked before deployment. The API has process-local limits and shared tenant API keys for learning; production needs an identity provider, durable distributed rate limiting, monitoring, migration tooling, and operational review. Liveness is not readiness, and a backup file without a restore test is not evidence of recovery.

Use the question-specific implementations above and [the reviewer answers](../../curriculum/assessments/ANSWERS.md). For deployment or model experiments, use [the worked operational procedures](../../curriculum/answers/OPERATIONS.md).

**Pass criteria:** 80/100 across correctness/reasoning (40), independent implementation (25), tests/debugging (20), and explanation/reproducibility (15). No permission leak, future-data leakage, invented evidence, or unreproducible core result. Live requirements remain pending until actually run. Running the answer files does not establish your independent mastery.

**If the gate fails:** If container networking fails, inspect service DNS/ports from inside the container; if restore fails, stop rollout and practice in a separate database.
