# Stage 13: question-by-question solutions

[All-stage answer index](../../curriculum/ANSWER_INDEX.md) · [Project brief](README.md)

`solution.py` is the main project reference. It does not contain every answer. Use the exact question IDs below to find the smaller exercises and extra programs.

**Suggested workflow:** notebook → independent assignment in your own `.py` files → stage project → closed-book gate. Compare answers only after an attempt; then close them and rebuild with changed input.

## Notebook questions and independent assignments

### 13a: Evaluation datasets and retrieval metrics

[Test your independent assignment](../../curriculum/assignments/13a.md)

| ID | Question | Answer |
|---|---|---|
| 13a-E1 | Use unique IDs in top k; return relevant-hit count / number of relevant IDs. An empty relevance set raises ValueError. | [Worked solution](../../curriculum/answers/13a.md#13a-e1) |
| 13a-E2 | Return reciprocal rank of first relevant ID, else 0. | [Worked solution](../../curriculum/answers/13a.md#13a-e2) |
| 13a-E3 | Given one boolean human support judgment per citation, return supported/total; no citations returns None. | [Worked solution](../../curriculum/answers/13a.md#13a-e3) |
| 13a-O1 | Why component metrics? | [Worked solution](../../curriculum/answers/13a.md#13a-o1) |
| 13a-O2 | Can a judge replace all human review? | [Worked solution](../../curriculum/answers/13a.md#13a-o2) |
| 13a-T | Label at least 40 development and 20 locked holdout questions before tuning the retriever. Grow to 100–500 curated cases over the capstone. Include permission denials, unsupported questions, multi-document comparisons, and exact numbers. | [Worked solution](../../curriculum/answers/13a.md#13a-t) |

### 13b: Regression gates and uncertainty

[Test your independent assignment](../../curriculum/assignments/13b.md)

| ID | Question | Answer |
|---|---|---|
| 13b-E1 | Return mean(candidate-baseline); require equal nonzero lengths. | [Worked solution](../../curriculum/answers/13b.md#13b-e1) |
| 13b-E2 | Require recall>=.8, groundedness>=.9, unauthorized=0, p95_ms<=2000. Missing metrics fail. | [Worked solution](../../curriculum/answers/13b.md#13b-e2) |
| 13b-E3 | For rows with category and correct boolean, return category→{n,accuracy}. | [Worked solution](../../curriculum/answers/13b.md#13b-e3) |
| 13b-O1 | Why predeclare thresholds? | [Worked solution](../../curriculum/answers/13b.md#13b-o1) |
| 13b-O2 | When is ordinary bootstrap inappropriate? | [Worked solution](../../curriculum/answers/13b.md#13b-o2) |
| 13b-T | Build the evaluation CLI with machine-readable reports and a nonzero exit on regression. Compare chunk sizes and models while keeping labels fixed; explain uncertainty and any excluded cases. | [Worked solution](../../curriculum/answers/13b.md#13b-t) |

## Project tasks, in brief order

<a id="13-p1"></a>
### 13-P1

**Question:** Expand the nine-case fixture to at least 60 reviewed cases; preserve 20 as a locked holdout.

**Answer:** [13a worked implementation and explanation](../../curriculum/answers/13a.md#13a-t)

<a id="13-p2"></a>
### 13-P2

**Question:** Separate retrieval, numeric correctness, citation support, abstention, permissions, tool behavior, and service quality.

**Answer:** [13a worked implementation and explanation](../../curriculum/answers/13a.md#13a-t) · [13b worked implementation and explanation](../../curriculum/answers/13b.md#13b-t)

<a id="13-p3"></a>
### 13-P3

**Question:** Compare two candidates on paired questions, report slices and uncertainty, and inspect regressions.

**Answer:** [13b worked implementation and explanation](../../curriculum/answers/13b.md#13b-t)

<a id="13-p4"></a>
### 13-P4

**Question:** Write machine-readable reports and fail CI on predeclared hard gates; version every component and label set.

**Answer:** [13b worked implementation and explanation](../../curriculum/answers/13b.md#13b-t)

<a id="13-g"></a>
## Mastery gate: 13-G

**Task:** Find a deliberately misleading evaluation, fix the split/metric, compare two systems, and defend a release decision including uncertainty and weak slices.

**Expected reasoning and invariant outputs:** The reference report measures real lexical retrieval with nine smoke cases and explicitly does not claim generation-groundedness. Recall uses unique relevant IDs; no-answer cases are evaluated as abstentions. A permission failure is a hard gate even if average quality rises. Use paired or group bootstrap according to dependence; document confidence and denominators. Human judges should verify claims against sources, not merely check that a citation ID exists.

Use the question-specific implementations above and [the reviewer answers](../../curriculum/assessments/ANSWERS.md). For deployment or model experiments, use [the worked operational procedures](../../curriculum/answers/OPERATIONS.md).

**Pass criteria:** 80/100 across correctness/reasoning (40), independent implementation (25), tests/debugging (20), and explanation/reproducibility (15). No permission leak, future-data leakage, invented evidence, or unreproducible core result. Live requirements remain pending until actually run. Running the answer files does not establish your independent mastery.

**If the gate fails:** If metrics disagree, inspect individual cases and definitions before aggregating; verify denominators and label consistency.
