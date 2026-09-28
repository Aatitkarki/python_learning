# Stage 08: question-by-question solutions

[All-stage answer index](../../curriculum/ANSWER_INDEX.md) · [Project brief](README.md)

`solution.py` is the main project reference. It does not contain every answer. Use the exact question IDs below to find the smaller exercises and extra programs.

**Suggested workflow:** notebook → independent assignment in your own `.py` files → stage project → closed-book gate. Compare answers only after an attempt; then close them and rebuild with changed input.

## Notebook questions and independent assignments

### 08a: Tools and bounded workflows

[Test your independent assignment](../../curriculum/assignments/08a.md)

| ID | Question | Answer |
|---|---|---|
| 08a-E1 | Execute add or divide from a request with exactly tool,arguments and arguments exactly a,b; finite numeric values only (exclude booleans). Reject all other requests. | [Worked solution](../../curriculum/answers/08a.md#08a-e1) |
| 08a-E2 | Execute sequential requests up to max_calls. Return observations and status complete or budget_exhausted. Record tool errors as strings; do not pretend they succeeded. | [Worked solution](../../curriculum/answers/08a.md#08a-e2) |
| 08a-E3 | Call operation at most attempts times; retry TimeoutError only. Raise the final error if exhausted. | [Worked solution](../../curriculum/answers/08a.md#08a-e3) |
| 08a-O1 | Who grants tool permission? | [Worked solution](../../curriculum/answers/08a.md#08a-o1) |
| 08a-O2 | When is retry unsafe? | [Worked solution](../../curriculum/answers/08a.md#08a-o2) |
| 08a-T | Extend document search with typed SQL read tools and a calculator. Add traces, step/deadline budgets, timeouts, approval records, and tests for malformed tool arguments and unavailable services. | [Worked solution](../../curriculum/answers/08a.md#08a-t) |

### 08b: LangGraph state and human review

[Test your independent assignment](../../curriculum/assignments/08b.md)

| ID | Question | Answer |
|---|---|---|
| 08b-E1 | Return route=calculator when question contains the word ratio (case-insensitive), else search. Return only the update. | [Worked solution](../../curriculum/answers/08b.md#08b-e1) |
| 08b-E2 | Build START→route→conditional calculator/search→END. Calculator returns answer="calculator selected" and search returns "search selected". | [Worked solution](../../curriculum/answers/08b.md#08b-e2) |
| 08b-E3 | Return SHA-256 of canonical JSON containing actor, action, arguments. Same content in different key order must match. | [Worked solution](../../curriculum/answers/08b.md#08b-e3) |
| 08b-O1 | What must persistence isolate? | [Worked solution](../../curriculum/answers/08b.md#08b-o1) |
| 08b-O2 | Does a framework remove authorization work? | [Worked solution](../../curriculum/answers/08b.md#08b-o2) |
| 08b-T | Run Stage 08’s checkpoint/interrupt example. Resume one approved action, reject a changed action, and verify two thread IDs cannot exchange state. Compare one graph versus a two-worker design on measured cost and correctness. | [Worked solution](../../curriculum/answers/08b.md#08b-t) |

## Project tasks, in brief order

<a id="08-p1"></a>
### 08-P1

**Question:** Implement document-search, financial-record lookup, and calculator tools with schemas and server-side scope.

**Answer:** [08a worked implementation and explanation](../../curriculum/answers/08a.md#08a-t)

<a id="08-p2"></a>
### 08-P2

**Question:** Create a plain Python workflow, then the equivalent LangGraph; compare traces on the same requests.

**Answer:** [08b worked implementation and explanation](../../curriculum/answers/08b.md#08b-t)

<a id="08-p3"></a>
### 08-P3

**Question:** Persist a checkpoint, interrupt before a proposed action, bind approval to exact content, resume or deny, and isolate run IDs.

**Answer:** [08b worked implementation and explanation](../../curriculum/answers/08b.md#08b-t)

<a id="08-p4"></a>
### 08-P4

**Question:** Inject transient failures, malformed arguments, repeated calls, timeouts, and budget exhaustion.

**Answer:** [08a worked implementation and explanation](../../curriculum/answers/08a.md#08a-t)

<a id="08-p5"></a>
### 08-P5

**Question:** Only as an experiment, split research and checking into two workers and compare task success, calls, latency, and cost.

**Answer:** [08b worked implementation and explanation](../../curriculum/answers/08b.md#08b-t)

<a id="08-g"></a>
## Mastery gate: 08-G

**Task:** Show correct tool selection, arguments, bounded termination, visible failures, denied altered approvals, and isolated state. Explain when a fixed workflow is preferable.

**Expected reasoning and invariant outputs:** The runnable graph interrupts before a division, checks a fingerprint bound to actor/proposal, and resumes to result 1.2. InMemorySaver is not durable storage. For crash recovery choose a supported durable checkpointer and isolate credentials/run IDs. A fingerprint does not authenticate an approver; verify identity and expire/consume approvals in the service. Count budgets in code and use network timeouts; a between-step timer cannot interrupt blocked I/O.

Use the question-specific implementations above and [the reviewer answers](../../curriculum/assessments/ANSWERS.md). For deployment or model experiments, use [the worked operational procedures](../../curriculum/answers/OPERATIONS.md).

**Pass criteria:** 80/100 across correctness/reasoning (40), independent implementation (25), tests/debugging (20), and explanation/reproducibility (15). No permission leak, future-data leakage, invented evidence, or unreproducible core result. Live requirements remain pending until actually run. Running the answer files does not establish your independent mastery.

**If the gate fails:** Remove model routing until deterministic tool execution and transitions pass tests; then add one decision at a time.
