# Stage 03: question-by-question solutions

[All-stage answer index](../../curriculum/ANSWER_INDEX.md) · [Project brief](README.md)

`solution.py` is the main project reference. It does not contain every answer. Use the exact question IDs below to find the smaller exercises and extra programs.

**Suggested workflow:** notebook → independent assignment in your own `.py` files → stage project → closed-book gate. Compare answers only after an attempt; then close them and rebuild with changed input.

## Notebook questions and independent assignments

### 03a: NumPy and Pandas data contracts

[Test your independent assignment](../../curriculum/assignments/03a.md)

| ID | Question | Answer |
|---|---|---|
| 03a-E1 | Standardize each column using population std. Constant columns become zeros. Return a NumPy array. | [Worked solution](../../curriculum/answers/03a.md#03a-e1) |
| 03a-E2 | Parse dates and amounts, group by calendar month string YYYY-MM, return a sorted Series. Use a copied frame. | [Worked solution](../../curriculum/answers/03a.md#03a-e2) |
| 03a-E3 | Left-join orders and customers on customer_id; enforce many-to-one and preserve row count. | [Worked solution](../../curriculum/answers/03a.md#03a-e3) |
| 03a-O1 | What is broadcasting? | [Worked solution](../../curriculum/answers/03a.md#03a-o1) |
| 03a-O2 | Why validate a join? | [Worked solution](../../curriculum/answers/03a.md#03a-o2) |
| 03a-T | Profile missing values, duplicates, date ranges, and outliers in expenses.csv. Write a cleaning report and a three-day rolling mean. Explain every exclusion. | [Worked solution](../../curriculum/answers/03a.md#03a-t) |

### 03b: SQL, transactions, and schema design

[Test your independent assignment](../../curriculum/assignments/03b.md)

| ID | Question | Answer |
|---|---|---|
| 03b-E1 | Return (id,amount) rows for a customer ordered by id, using SQL parameters. | [Worked solution](../../curriculum/answers/03b.md#03b-e1) |
| 03b-E2 | Return (id,running_amount) per customer, ordered by id. Use SUM OVER with an explicit ROWS frame. | [Worked solution](../../curriculum/answers/03b.md#03b-e2) |
| 03b-E3 | Insert rows inside a transaction; any duplicate key rolls back the entire batch. | [Worked solution](../../curriculum/answers/03b.md#03b-e3) |
| 03b-O1 | Why a LEFT JOIN? | [Worked solution](../../curriculum/answers/03b.md#03b-o1) |
| 03b-O2 | Are indexes free? | [Worked solution](../../curriculum/answers/03b.md#03b-o2) |
| 03b-T | Design customers, records, and categories tables with keys; write INNER/LEFT joins, CTE, HAVING, UNION, and correlated subquery examples. Use PostgreSQL EXPLAIN before/after an index and demonstrate rollback. | [Worked solution](../../curriculum/answers/03b.md#03b-t) |

### 03c: HTTP, validation, and FastAPI

[Test your independent assignment](../../curriculum/assignments/03c.md)

| ID | Question | Answer |
|---|---|---|
| 03c-E1 | Define Record(BaseModel) with category length 1..50 and amount finite >=0. | [Worked solution](../../curriculum/answers/03c.md#03c-e1) |
| 03c-E2 | Write make_app() with POST /records returning the validated record with status 201. | [Worked solution](../../curriculum/answers/03c.md#03c-e2) |
| 03c-E3 | Return a slice for offset>=0 and 1<=limit<=100; reject other bounds. | [Worked solution](../../curriculum/answers/03c.md#03c-e3) |
| 03c-O1 | What does 422 mean here? | [Worked solution](../../curriculum/answers/03c.md#03c-o1) |
| 03c-O2 | Why inject a database session? | [Worked solution](../../curriculum/answers/03c.md#03c-o2) |
| 03c-T | Build Stage 03’s persistent API with GET /records, /summary, /statistics and POST /records. Add auth, request IDs, tests, and PostgreSQL ingestion. Restart it and prove persistence. | [Worked solution](../../curriculum/answers/03c.md#03c-t) |

## Project tasks, in brief order

<a id="03-p1"></a>
### 03-P1

**Question:** Profile and clean a CSV with a data-quality report and quarantined invalid records.

**Answer:** [03a worked implementation and explanation](../../curriculum/answers/03a.md#03a-t)

<a id="03-p2"></a>
### 03-P2

**Question:** Design a normalized relational schema and write the complete SQL worksheet in EXTRA_LABS.md; examine index plans.

**Answer:** [03b worked implementation and explanation](../../curriculum/answers/03b.md#03b-t)

<a id="03-p3"></a>
### 03-P3

**Question:** Implement GET /records, /summary, /statistics and POST /records, with persistent storage and tenant isolation.

**Answer:** [03c worked implementation and explanation](../../curriculum/answers/03c.md#03c-t)

<a id="03-p4"></a>
### 03-P4

**Question:** Run first on SQLite and then PostgreSQL via Compose. Ingest CSV, restart the API, verify totals, and test rollback and invalid requests.

**Answer:** [03b worked implementation and explanation](../../curriculum/answers/03b.md#03b-t) · [03c worked implementation and explanation](../../curriculum/answers/03c.md#03c-t)

<a id="03-g"></a>
## Mastery gate: 03-G

**Task:** Write a join and window query from scratch; explain a query plan; trace an HTTP request through auth, validation, transaction, and response. Demonstrate persistence and tenant isolation.

**Expected reasoning and invariant outputs:** The offline demonstration creates two records totaling 2550 cents and proves they survive a new app instance. Invalid bodies return 422, missing auth 401, and cross-tenant lists are empty. Bind SQL values rather than interpolate. The reference API uses integer cents; schema, keys, and query plans belong in your independent design. PostgreSQL is an explicit integration milestone, not satisfied by SQLite tests.

Use the question-specific implementations above and [the reviewer answers](../../curriculum/assessments/ANSWERS.md). For deployment or model experiments, use [the worked operational procedures](../../curriculum/answers/OPERATIONS.md).

**Pass criteria:** 80/100 across correctness/reasoning (40), independent implementation (25), tests/debugging (20), and explanation/reproducibility (15). No permission leak, future-data leakage, invented evidence, or unreproducible core result. Live requirements remain pending until actually run. Running the answer files does not establish your independent mastery.

**If the gate fails:** If joins multiply totals, inspect key cardinality; if API tests fail, isolate schema validation from repository behavior.
