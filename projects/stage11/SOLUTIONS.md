# Stage 11: question-by-question solutions

[All-stage answer index](../../curriculum/ANSWER_INDEX.md) · [Project brief](README.md)

`solution.py` is the main project reference. It does not contain every answer. Use the exact question IDs below to find the smaller exercises and extra programs.

**Suggested workflow:** notebook → independent assignment in your own `.py` files → stage project → closed-book gate. Compare answers only after an attempt; then close them and rebuild with changed input.

## Notebook questions and independent assignments

### 11a: Distributed data and associative aggregation

[Test your independent assignment](../../curriculum/assignments/11a.md)

| ID | Question | Answer |
|---|---|---|
| 11a-E1 | Return (sum,count) for each partition, combine, and return the global mean; reject zero total count. | [Worked solution](../../curriculum/answers/11a.md#11a-e1) |
| 11a-E2 | Merge a list of key→sum dictionaries into a new dictionary. | [Worked solution](../../curriculum/answers/11a.md#11a-e2) |
| 11a-E3 | Return largest nonnegative partition size divided by mean size; reject empty or all-zero input. | [Worked solution](../../curriculum/answers/11a.md#11a-e3) |
| 11a-O1 | Why is collect dangerous? | [Worked solution](../../curriculum/answers/11a.md#11a-o1) |
| 11a-O2 | Why use an explicit schema? | [Worked solution](../../curriculum/answers/11a.md#11a-o2) |
| 11a-T | Generate a million synthetic transactions in batches, compute grouped totals without loading everything into memory, and compare output with Spark. Explain shuffle, broadcast joins, and skew. | [Worked solution](../../curriculum/answers/11a.md#11a-t) |

### 11b: PySpark DataFrames and windows

[Test your independent assignment](../../curriculum/assignments/11b.md)

| ID | Question | Answer |
|---|---|---|
| 11b-E1 | Return account,sum_cents sorted by account, using Spark DataFrame expressions. | [Worked solution](../../curriculum/answers/11b.md#11b-e1) |
| 11b-E2 | Add running_cents partitioned by account ordered by unique id with an unbounded preceding ROWS frame. | [Worked solution](../../curriculum/answers/11b.md#11b-e2) |
| 11b-E3 | Write df to a supplied new directory using errorifexists, read it, and return row count. Do not overwrite existing work. | [Worked solution](../../curriculum/answers/11b.md#11b-e3) |
| 11b-O1 | Why lazy execution? | [Worked solution](../../curriculum/answers/11b.md#11b-o1) |
| 11b-O2 | What does a shuffle cost? | [Worked solution](../../curriculum/answers/11b.md#11b-o2) |
| 11b-T | Run the Stage 11 job, compare partitions 2/8/32, capture explain plans and timings, and compute anomalies plus rolling statistics. Repeat on an actual cluster before claiming distributed operational experience. | [Worked solution](../../curriculum/answers/11b.md#11b-t) |

## Project tasks, in brief order

<a id="11-p1"></a>
### 11-P1

**Question:** Generate at least one million deterministic transactions without collecting them to the driver.

**Answer:** [11a worked implementation and explanation](../../curriculum/answers/11a.md#11a-t)

<a id="11-p2"></a>
### 11-P2

**Question:** Calculate grouped sums/counts, daily trends, anomalies, and window statistics; write Parquet.

**Answer:** [11b worked implementation and explanation](../../curriculum/answers/11b.md#11b-t)

<a id="11-p3"></a>
### 11-P3

**Question:** Compare partitions and inspect physical plans; demonstrate skew and a broadcast-join tradeoff.

**Answer:** [11b worked implementation and explanation](../../curriculum/answers/11b.md#11b-t)

<a id="11-p4"></a>
### 11-P4

**Question:** Check row count, schema, total cents, and a sampled group against a Python reference.

**Answer:** [11a worked implementation and explanation](../../curriculum/answers/11a.md#11a-t) · [11b worked implementation and explanation](../../curriculum/answers/11b.md#11b-t)

<a id="11-p5"></a>
### 11-P5

**Question:** Repeat on an actual cluster or document the operational gap if only local mode is available.

**Answer:** [11b worked implementation and explanation](../../curriculum/answers/11b.md#11b-t)

<a id="11-g"></a>
## Mastery gate: 11-G

**Task:** Explain a shuffle in an actual plan, fix a skewed aggregation, reconcile distributed totals, and justify a storage format.

**Expected reasoning and invariant outputs:** The job uses Spark range and built-in expressions; amounts are ((id*17)%10000) cents and accounts=id%50. The expected total can be independently calculated by a streaming Python sum. A uniform synthetic distribution may have zero 3-sigma anomalies. ROWS(-2,0) means three observed rows, not automatically three calendar days. Do not collect the raw million rows to the driver. Existing output paths are rejected to protect previous results.

Use the question-specific implementations above and [the reviewer answers](../../curriculum/assessments/ANSWERS.md). For deployment or model experiments, use [the worked operational procedures](../../curriculum/answers/OPERATIONS.md).

**Pass criteria:** 80/100 across correctness/reasoning (40), independent implementation (25), tests/debugging (20), and explanation/reproducibility (15). No permission leak, future-data leakage, invented evidence, or unreproducible core result. Live requirements remain pending until actually run. Running the answer files does not establish your independent mastery.

**If the gate fails:** If totals disagree, check duplicate rows, join cardinality, types, rounding, and partition aggregation logic before performance tuning.
