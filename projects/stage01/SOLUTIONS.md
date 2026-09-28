# Stage 01: question-by-question solutions

[All-stage answer index](../../curriculum/ANSWER_INDEX.md) · [Project brief](README.md)

`solution.py` is the main project reference. It does not contain every answer. Use the exact question IDs below to find the smaller exercises and extra programs.

**Suggested workflow:** notebook → independent assignment in your own `.py` files → stage project → closed-book gate. Compare answers only after an attempt; then close them and rebuild with changed input.

## Notebook questions and independent assignments

### 01a: Variables, decisions, and functions

[Test your independent assignment](../../curriculum/assignments/01a.md)

| ID | Question | Answer |
|---|---|---|
| 01a-E1 | Return (sell-buy)*shares. Require shares > 0 and prices >= 0. | [Worked solution](../../curriculum/answers/01a.md#01a-e1) |
| 01a-E2 | Support +, -, *, /. Reject unknown operators with ValueError and division by zero with ZeroDivisionError. | [Worked solution](../../curriculum/answers/01a.md#01a-e2) |
| 01a-E3 | Orders >= 100 ship free; smaller nonnegative orders cost 5. A negative total raises ValueError. | [Worked solution](../../curriculum/answers/01a.md#01a-e3) |
| 01a-O1 | Why return instead of print? | [Worked solution](../../curriculum/answers/01a.md#01a-o1) |
| 01a-O2 | What is scope? | [Worked solution](../../curriculum/answers/01a.md#01a-o2) |
| 01a-T | Build a terminal calculator and temperature converter with a loop. Handle invalid numeric input without hiding programming errors. Add five tests per function. | [Worked solution](../../curriculum/answers/01a.md#01a-t) |

### 01b: Collections, loops, and text

[Test your independent assignment](../../curriculum/assignments/01b.md)

| ID | Question | Answer |
|---|---|---|
| 01b-E1 | Count lowercase words matching [a-z]+; return a dictionary. Empty text returns {}. | [Worked solution](../../curriculum/answers/01b.md#01b-e1) |
| 01b-E2 | Return the first occurrence of each hashable item, preserving input order. | [Worked solution](../../curriculum/answers/01b.md#01b-e2) |
| 01b-E3 | Return a new dictionary with deltas applied. Reject a resulting negative count. Do not change the original. | [Worked solution](../../curriculum/answers/01b.md#01b-e3) |
| 01b-O1 | When is a set unsuitable? | [Worked solution](../../curriculum/answers/01b.md#01b-o1) |
| 01b-O2 | Why copy an input dictionary? | [Worked solution](../../curriculum/answers/01b.md#01b-o2) |
| 01b-T | Build a contact book with add, search, update, delete, and duplicate handling. Add a text analyzer that reports characters, word count, unique words, and deterministic top words. | [Worked solution](../../curriculum/answers/01b.md#01b-t) |

### 01c: Files, validation, and money

[Test your independent assignment](../../curriculum/assignments/01c.md)

| ID | Question | Answer |
|---|---|---|
| 01c-E1 | Parse a string as a finite, nonnegative Decimal; raise ValueError on invalid inputs including NaN. | [Worked solution](../../curriculum/answers/01c.md#01c-e1) |
| 01c-E2 | For CSV text with date,category,amount, return total Decimal and by_category dict. Validate ISO dates and nonblank categories; use parse_amount. | [Worked solution](../../curriculum/answers/01c.md#01c-e2) |
| 01c-E3 | Serialize a total Decimal and currency into JSON strings, using keys total and currency. Preserve the decimal text. | [Worked solution](../../curriculum/answers/01c.md#01c-e3) |
| 01c-O1 | Why not split CSV manually? | [Worked solution](../../curriculum/answers/01c.md#01c-o1) |
| 01c-O2 | What is a useful error message? | [Worked solution](../../curriculum/answers/01c.md#01c-o2) |
| 01c-T | Build the expense CLI in Stage 01: total, category/month summaries, mean, maximum, and bad-row diagnostics. Use a temporary directory for file tests. | [Worked solution](../../curriculum/answers/01c.md#01c-t) |

### 01d: Objects, algorithms, and debugging

[Test your independent assignment](../../curriculum/assignments/01d.md)

| ID | Question | Answer |
|---|---|---|
| 01d-E1 | Implement Inventory with fresh per-instance items and add(name, quantity); quantity must be positive. | [Worked solution](../../curriculum/answers/01d.md#01d-e1) |
| 01d-E2 | For sorted ascending values, return an index of target, else -1. Use an iterative halving algorithm. | [Worked solution](../../curriculum/answers/01d.md#01d-e2) |
| 01d-E3 | Return the arithmetic mean of values. Empty input raises ValueError; do not divide by len(values)-1. | [Worked solution](../../curriculum/answers/01d.md#01d-e3) |
| 01d-O1 | Why prefer composition here? | [Worked solution](../../curriculum/answers/01d.md#01d-o1) |
| 01d-O2 | What must a recursive function have? | [Worked solution](../../curriculum/answers/01d.md#01d-o2) |
| 01d-T | Refactor the expense analyzer into parser, domain, and CLI modules. Add pytest tests, one mock for a file failure, logging, a recursive directory-size exercise, and a measured linear-versus-binary search experiment. | [Worked solution](../../curriculum/answers/01d.md#01d-t) |

## Project tasks, in brief order

<a id="01-p1"></a>
### 01-P1

**Question:** Build calculator, temperature/profit tools, text analyzer, contact book, and inventory before the main project.

**Answer:** [01a worked implementation and explanation](../../curriculum/answers/01a.md#01a-t) · [01b worked implementation and explanation](../../curriculum/answers/01b.md#01b-t)

<a id="01-p2"></a>
### 01-P2

**Question:** Build a CSV expense CLI with total, category totals, monthly totals, average, highest expense, and clear line-numbered errors.

**Answer:** [01c worked implementation and explanation](../../curriculum/answers/01c.md#01c-t)

<a id="01-p3"></a>
### 01-P3

**Question:** Split parsing, calculation, and CLI code; add tests for empty files, quotes, malformed dates, NaN, negative amounts, and missing columns.

**Answer:** [01c worked implementation and explanation](../../curriculum/answers/01c.md#01c-t) · [01d worked implementation and explanation](../../curriculum/answers/01d.md#01d-t)

<a id="01-p4"></a>
### 01-P4

**Question:** Refactor one component to a class using composition; profile linear and binary search and explain recursion with a base case.

**Answer:** [01d worked implementation and explanation](../../curriculum/answers/01d.md#01d-t)

<a id="01-g"></a>
## Mastery gate: 01-G

**Task:** In 90 minutes build a new CSV inventory summarizer from a blank file, with validation and five meaningful tests. Explain each function and one time-complexity tradeoff without opening answers.

**Expected reasoning and invariant outputs:** The fixture total is 100.00 across 6 rows; January and February each total 50.00. Food=55.00, Transport=15.00, Books=30.00, highest=30.00, mean=100/6. Decimal avoids binary-money error. Reject malformed rows before aggregation. A CLI should catch expected input errors, return a nonzero exit, and leave programmer errors visible. Text normalization and stable tie-breaking must be explicit.

Use the question-specific implementations above and [the reviewer answers](../../curriculum/assessments/ANSWERS.md). For deployment or model experiments, use [the worked operational procedures](../../curriculum/answers/OPERATIONS.md).

**Pass criteria:** 80/100 across correctness/reasoning (40), independent implementation (25), tests/debugging (20), and explanation/reproducibility (15). No permission leak, future-data leakage, invented evidence, or unreproducible core result. Live requirements remain pending until actually run. Running the answer files does not establish your independent mastery.

**If the gate fails:** Repeat 01a/01b if control flow is unclear; repeat 01c for parsing errors; reproduce one failing test before every bug fix.
