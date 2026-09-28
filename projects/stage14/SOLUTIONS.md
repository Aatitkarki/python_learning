# Stage 14: question-by-question solutions

[All-stage answer index](../../curriculum/ANSWER_INDEX.md) · [Project brief](README.md)

`solution.py` is the main project reference. It does not contain every answer. Use the exact question IDs below to find the smaller exercises and extra programs.

**Suggested workflow:** notebook → independent assignment in your own `.py` files → stage project → closed-book gate. Compare answers only after an attempt; then close them and rebuild with changed input.

## Notebook questions and independent assignments

### 14a: Financial statements and ratios

[Test your independent assignment](../../curriculum/assignments/14a.md)

| ID | Question | Answer |
|---|---|---|
| 14a-E1 | Return True if assets equals liabilities+equity within an absolute tolerance; inputs share the same units. | [Worked solution](../../curriculum/answers/14a.md#14a-e1) |
| 14a-E2 | For positive revenue and shares, return EPS, operating_margin, and FCF (capex given as positive cash outflow). | [Worked solution](../../curriculum/answers/14a.md#14a-e2) |
| 14a-E3 | Return (current-prior)/prior for positive prior; return None when prior<=0. | [Worked solution](../../curriculum/answers/14a.md#14a-e3) |
| 14a-O1 | Why compare like periods? | [Worked solution](../../curriculum/answers/14a.md#14a-o1) |
| 14a-O2 | Does low P/E prove undervaluation? | [Worked solution](../../curriculum/answers/14a.md#14a-o2) |
| 14a-T | Analyze fictional Aurora and Beacon statements. Calculate EPS, revenue/EPS growth, P/E, P/S, P/B, ROE, ROA, debt/equity, gross/operating/net margin, and FCF yield. State all units, conventions, and undefined cases; cite each source row. | [Worked solution](../../curriculum/answers/14a.md#14a-t) |

### 14b: Time series and honest backtests

[Test your independent assignment](../../curriculum/assignments/14b.md)

| ID | Question | Answer |
|---|---|---|
| 14b-E1 | Return a Series containing the mean of the previous window prices, excluding today; incomplete windows stay NaN. | [Worked solution](../../curriculum/answers/14b.md#14b-e1) |
| 14b-E2 | Return train indices [0,cut-gap) and test [cut,n); require 0<=gap<cut<n. | [Worked solution](../../curriculum/answers/14b.md#14b-e2) |
| 14b-E3 | Given period returns and positions decided before each period, subtract fee*absolute position change from each gross return; initial position is zero. | [Worked solution](../../curriculum/answers/14b.md#14b-e3) |
| 14b-O1 | Why is fiscal year insufficient? | [Worked solution](../../curriculum/answers/14b.md#14b-o1) |
| 14b-O2 | Does a good backtest establish an edge? | [Worked solution](../../curriculum/answers/14b.md#14b-o2) |
| 14b-T | Build walk-forward demand/return experiments and an as-of join on filing publication dates. Compare a naive forecast, report per-fold metrics, and document why random splits overstate performance. | [Worked solution](../../curriculum/answers/14b.md#14b-t) |

## Project tasks, in brief order

<a id="14-p1"></a>
### 14-P1

**Question:** Reconcile fictional statements and calculate all ratios in the roadmap with source IDs and undefined-case policy.

**Answer:** [14a worked implementation and explanation](../../curriculum/answers/14a.md#14a-t)

<a id="14-p2"></a>
### 14-P2

**Question:** Compare three years for two companies; distinguish period, currency, scale, average versus ending balances, and capex signs.

**Answer:** [14a worked implementation and explanation](../../curriculum/answers/14a.md#14a-t)

<a id="14-p3"></a>
### 14-P3

**Question:** Create past-only features, walk-forward splits, and an as-of publication-date join.

**Answer:** [14b worked implementation and explanation](../../curriculum/answers/14b.md#14b-t)

<a id="14-p4"></a>
### 14-P4

**Question:** Compare a forecast to naive baselines; include turnover/cost assumptions if building a strategy. Explain why no predictive edge is established.

**Answer:** [14b worked implementation and explanation](../../curriculum/answers/14b.md#14b-t)

<a id="14-g"></a>
## Mastery gate: 14-G

**Task:** Explain all units in a comparison, identify a publication-time leak, build a walk-forward baseline, and explain why a backtest is not proof of investment value.

**Expected reasoning and invariant outputs:** Aurora 2025: revenue=144 million USD, operating margin=25%, FCF=24 million USD; Beacon 2025: revenue=108, margin=15/108≈13.89%, FCF=12. ROE/ROA use average balances; first-year values are unknown without prior balances. P/E with nonpositive EPS is undefined under the course policy. PEG uses P/E divided by a stated percentage-point growth rate, not silently by a fraction. Always align statement availability to the decision date.

Use the question-specific implementations above and [the reviewer answers](../../curriculum/assessments/ANSWERS.md). For deployment or model experiments, use [the worked operational procedures](../../curriculum/answers/OPERATIONS.md).

**Pass criteria:** 80/100 across correctness/reasoning (40), independent implementation (25), tests/debugging (20), and explanation/reproducibility (15). No permission leak, future-data leakage, invented evidence, or unreproducible core result. Live requirements remain pending until actually run. Running the answer files does not establish your independent mastery.

**If the gate fails:** If ratios look implausible, inspect units and sign conventions first; if performance is too good, audit feature/label availability and split overlap.
