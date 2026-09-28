# Stage 15: question-by-question solutions

[All-stage answer index](../../curriculum/ANSWER_INDEX.md) · [Project brief](README.md)

`solution.py` is the main project reference. It does not contain every answer. Use the exact question IDs below to find the smaller exercises and extra programs.

**Suggested workflow:** notebook → independent assignment in your own `.py` files → stage project → closed-book gate. Compare answers only after an attempt; then close them and rebuild with changed input.

## Notebook questions and independent assignments

### 15a: An evidence-backed financial research pipeline

[Test your independent assignment](../../curriculum/assignments/15a.md)

| ID | Question | Answer |
|---|---|---|
| 15a-E1 | Select requested company and years from rows, rejecting duplicate company-year records or missing years. Return chronological rows. | [Worked solution](../../curriculum/answers/15a.md#15a-e1) |
| 15a-E2 | Return company,year,revenue,operating_margin,fcf,source_id using Decimal inputs; revenue must be positive. | [Worked solution](../../curriculum/answers/15a.md#15a-e2) |
| 15a-E3 | Return True when every report row has a nonempty source_id contained in allowed_source_ids. | [Worked solution](../../curriculum/answers/15a.md#15a-e3) |
| 15a-O1 | Why compute outside the model? | [Worked solution](../../curriculum/answers/15a.md#15a-o1) |
| 15a-O2 | What makes a comparison invalid? | [Worked solution](../../curriculum/answers/15a.md#15a-o2) |
| 15a-T | Build the two-company, three-year report through the API. Demonstrate citations, tenant isolation, unknown-company abstention, missing-period handling, and a local-model narrative constrained to verified numbers. | [Worked solution](../../curriculum/answers/15a.md#15a-t) |

### 15b: Architecture review and mastery defense

[Test your independent assignment](../../curriculum/assignments/15b.md)

| ID | Question | Answer |
|---|---|---|
| 15b-E1 | Map parsing, retrieval, arithmetic, permission, timeout to data, search, calculator, authorization, infrastructure. Unknown labels return investigate. | [Worked solution](../../curriculum/answers/15b.md#15b-e1) |
| 15b-E2 | Return sum of nonnegative stage budgets and whether it fits the total target. | [Worked solution](../../curriculum/answers/15b.md#15b-e2) |
| 15b-E3 | Require nonempty artifact paths for code,tests,evaluation,threat_model,restore,incident,defense. Return missing keys. | [Worked solution](../../curriculum/answers/15b.md#15b-e3) |
| 15b-O1 | What demonstrates transfer? | [Worked solution](../../curriculum/answers/15b.md#15b-o1) |
| 15b-O2 | What remains after this course? | [Worked solution](../../curriculum/answers/15b.md#15b-o2) |
| 15b-T | Complete the closed-book capstone defense, implement an unseen request in 90 minutes, perform one outage/restore drill, and have another person reproduce the project from your README. Revisit weak checkpoints after 7 and 30 days. | [Worked solution](../../curriculum/answers/15b.md#15b-t) |

## Project tasks, in brief order

<a id="15-p1"></a>
### 15-P1

**Question:** Build an independent version from the brief; use reference code only after attempting each component.

**Answer:** [15b worked implementation and explanation](../../curriculum/answers/15b.md#15b-t)

<a id="15-p2"></a>
### 15-P2

**Question:** Answer a two-company three-year revenue/margin/FCF comparison with deterministic calculations and citations.

**Answer:** [15a worked implementation and explanation](../../curriculum/answers/15a.md#15a-t)

<a id="15-p3"></a>
### 15-P3

**Question:** Integrate learned embeddings, PostgreSQL, local model serving, bounded tools, permissions, and a usable client such as the API docs or a small CLI.

**Answer:** [07b worked implementation and explanation](../../curriculum/answers/07b.md#07b-t) · [08a worked implementation and explanation](../../curriculum/answers/08a.md#08a-t) · [09b worked implementation and explanation](../../curriculum/answers/09b.md#09b-t) · [15a worked implementation and explanation](../../curriculum/answers/15a.md#15a-t)

<a id="15-p4"></a>
### 15-P4

**Question:** Run the full failure matrix, restore backup, rehearse deployment/rollback, and write an architecture decision record.

**Answer:** [10a worked implementation and explanation](../../curriculum/answers/10a.md#10a-t) · [10b worked implementation and explanation](../../curriculum/answers/10b.md#10b-t) · [12a worked implementation and explanation](../../curriculum/answers/12a.md#12a-t) · [15b worked implementation and explanation](../../curriculum/answers/15b.md#15b-t)

<a id="15-p5"></a>
### 15-P5

**Question:** Grow the evaluation corpus to at least 100 reviewed cases and target 500 as the domain expands; preserve a locked holdout.

**Answer:** [13a worked implementation and explanation](../../curriculum/answers/13a.md#13a-t) · [13b worked implementation and explanation](../../curriculum/answers/13b.md#13b-t)

<a id="15-p6"></a>
### 15-P6

**Question:** Complete a 90-minute unseen feature, explain every component, and have another person reproduce the system.

**Answer:** [15b worked implementation and explanation](../../curriculum/answers/15b.md#15b-t)

<a id="15-g"></a>
## Mastery gate: 15-G

**Task:** Score at least 80/100 with every critical gate passed; demonstrate an unseen task, permission isolation, correct citations/calculations, safe failures, restore, and reproducibility.

**Expected reasoning and invariant outputs:** The reference emits six verified rows from authorized data. The local API can ingest documents, retrieve source quotes, and return deterministic comparison results. Optional integration scripts exercise embeddings, pgvector, and local generation but require external setup and must be connected and evaluated in your independent capstone. The full graduation checklist in CAPSTONE.md distinguishes baseline evidence from production deployment. No reading list or solution file can certify mastery without independent performance.

Use the question-specific implementations above and [the reviewer answers](../../curriculum/assessments/ANSWERS.md). For deployment or model experiments, use [the worked operational procedures](../../curriculum/answers/OPERATIONS.md).

**Pass criteria:** 80/100 across correctness/reasoning (40), independent implementation (25), tests/debugging (20), and explanation/reproducibility (15). No permission leak, future-data leakage, invented evidence, or unreproducible core result. Live requirements remain pending until actually run. Running the answer files does not establish your independent mastery.

**If the gate fails:** Return to the earliest failed boundary: Python/data before models, retrieval before generation, deterministic tools before autonomous routing. Retest after 7 and 30 days.
