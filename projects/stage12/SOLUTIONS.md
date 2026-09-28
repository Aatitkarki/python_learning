# Stage 12: question-by-question solutions

[All-stage answer index](../../curriculum/ANSWER_INDEX.md) · [Project brief](README.md)

`solution.py` is the main project reference. It does not contain every answer. Use the exact question IDs below to find the smaller exercises and extra programs.

**Suggested workflow:** notebook → independent assignment in your own `.py` files → stage project → closed-book gate. Compare answers only after an attempt; then close them and rebuild with changed input.

## Notebook questions and independent assignments

### 12a: Threat models and untrusted content

[Test your independent assignment](../../curriculum/assignments/12a.md)

| ID | Question | Answer |
|---|---|---|
| 12a-E1 | Return a dictionary with asset,entry,impact,control; reject empty fields. | [Worked solution](../../curriculum/answers/12a.md#12a-e1) |
| 12a-E2 | Escape model text for display in an HTML text node, including quotes. | [Worked solution](../../curriculum/answers/12a.md#12a-e2) |
| 12a-E3 | Allow only when chars<=4000, requested_tokens<=512, pending<10; require all inputs nonnegative. | [Worked solution](../../curriculum/answers/12a.md#12a-e3) |
| 12a-O1 | Is the system prompt a secret vault? | [Worked solution](../../curriculum/answers/12a.md#12a-o1) |
| 12a-O2 | Why is filtering attack phrases insufficient? | [Worked solution](../../curriculum/answers/12a.md#12a-o2) |
| 12a-T | Write a threat model for the capstone and 20 adversarial fixtures. Include malicious document instructions, fabricated citations, oversized input, poisoned numbers, and cross-tenant requests. Record actual observed controls and residual risks. | [Worked solution](../../curriculum/answers/12a.md#12a-t) |

### 12b: Authorization, caches, and isolation

[Test your independent assignment](../../curriculum/assignments/12b.md)

| ID | Question | Answer |
|---|---|---|
| 12b-E1 | Return whether a reader/admin principal may read a public or same-tenant resource. Unknown roles are denied. | [Worked solution](../../curriculum/answers/12b.md#12b-e1) |
| 12b-E2 | Return a deterministic key from tenant, permission_version, index_version, model_version, query using canonical JSON and SHA256. | [Worked solution](../../curriculum/answers/12b.md#12b-e2) |
| 12b-E3 | Return a resource by ID only when authorized; otherwise raise PermissionError, including missing IDs, to avoid distinguishing existence. | [Worked solution](../../curriculum/answers/12b.md#12b-e3) |
| 12b-O1 | Does an unguessable ID replace authorization? | [Worked solution](../../curriculum/answers/12b.md#12b-o1) |
| 12b-O2 | What belongs in cache identity? | [Worked solution](../../curriculum/answers/12b.md#12b-o2) |
| 12b-T | Exercise every API endpoint as two users and two tenants. Test warm-cache access, revoked permissions, citation fetches, saved graph state, and backups. Produce a permission matrix with allowed and denied evidence. | [Worked solution](../../curriculum/answers/12b.md#12b-t) |

## Project tasks, in brief order

<a id="12-p1"></a>
### 12-P1

**Question:** Map assets, actors, entry points, trust boundaries, controls, tests, and residual risks.

**Answer:** [12a worked implementation and explanation](../../curriculum/answers/12a.md#12a-t)

<a id="12-p2"></a>
### 12-P2

**Question:** Write at least 20 attacks against your own app: cross-tenant access, prompt injection, malformed tool calls, oversized inputs, and forged citations.

**Answer:** [12a worked implementation and explanation](../../curriculum/answers/12a.md#12a-t)

<a id="12-p3"></a>
### 12-P3

**Question:** Test allowed access alongside every denial; cover warm caches, revocation, graph state, logs, and document fetches.

**Answer:** [12b worked implementation and explanation](../../curriculum/answers/12b.md#12b-t)

<a id="12-p4"></a>
### 12-P4

**Question:** Record observed behavior and fix failures with code-enforced policy rather than a stronger-sounding prompt.

**Answer:** [12a worked implementation and explanation](../../curriculum/answers/12a.md#12a-t) · [12b worked implementation and explanation](../../curriculum/answers/12b.md#12b-t)

<a id="12-g"></a>
## Mastery gate: 12-G

**Task:** Demonstrate access boundaries with positive/negative tests, explain why prompt-only defenses fail, and trace one incident without exposing secrets.

**Expected reasoning and invariant outputs:** The six reference checks verify actual API outcomes, including permitted access for tenant B and denial for tenant A. A model never receives privileged execution authority from document text. HTML escaping is context-specific, SQL parameters handle values, and tools use allowlists. A zero-failure finite test suite does not prove universal injection resistance; preserve residual risks and add new cases as attacks are discovered.

Use the question-specific implementations above and [the reviewer answers](../../curriculum/assessments/ANSWERS.md). For deployment or model experiments, use [the worked operational procedures](../../curriculum/answers/OPERATIONS.md).

**Pass criteria:** 80/100 across correctness/reasoning (40), independent implementation (25), tests/debugging (20), and explanation/reproducibility (15). No permission leak, future-data leakage, invented evidence, or unreproducible core result. Live requirements remain pending until actually run. Running the answer files does not establish your independent mastery.

**If the gate fails:** If a security test passes by denying all access, add a permitted control case and verify useful behavior remains.
