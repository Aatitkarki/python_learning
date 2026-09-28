# Test your independent assignments

These tests run against **your chosen Python file**. They do not silently import the reference solution. The original assignment brief remains in your notebook; the pages below specify interfaces so the tests can call your implementation.

## First run: calculator assignment 01a

1. Create `work/assignments/`. Copy the blank [01a starter](starters/01a.py) to `work/assignments/01a.py` without overwriting existing work.
2. Read the [01a contract and cases](01a.md). Implement the functions in your copy.
3. From the repository root with your course environment activated, run:

```bash
python tools/test_assignment.py 01a --solution work/assignments/01a.py
```

`FAILED` or `NotImplementedError` is expected before you implement a starter. Read the failing assertion: it shows the input and expected behavior. Fix one case at a time. If you use another filename, pass its path with `--solution`. To test your solution across multiple modules, import your own functions into this one entry file.

After a serious attempt, verify the supplied answer separately:

```bash
python tools/test_assignment.py 01a --reference
```

The terminal says whether it is testing YOUR solution or REFERENCE answers. A reference pass does not assess your work. Existing code can use a thin adapter to the public interface; you do not have to reorganize your entire project.

## Work on one function at a time

Use `--case` to select matching test names while learning:

```bash
python tools/test_assignment.py 01a --solution work/assignments/01a.py --case calculator
```

This runs only part of the pack. Remove `--case` for the full assignment check.

## How to read a test

- Arrange: build input data, often in a temporary folder.
- Act: call your function or app.
- Assert: compare the result with an independently calculated expectation.
- `pytest.raises(ValueError)` means invalid input should raise that exception.
- `pytest.approx(...)` compares floating-point values with a small tolerance.
- A mock deliberately replaces a boundary with a failure; it does not prove a real service was exercised.

Example: `assert calculate(2, "+", 3) == 5` checks a normal case; division by zero checks an invalid case. For the converter, -40 is a useful boundary-related check because Celsius and Fahrenheit agree there.

## Assignment packs

| Lesson | Contract, starter, automated cases, remaining evidence |
|---|---|
| 00a — Your first reproducible experiment | [Open test pack](00a.md) |
| 01a — Variables, decisions, and functions | [Open test pack](01a.md) |
| 01b — Collections, loops, and text | [Open test pack](01b.md) |
| 01c — Files, validation, and money | [Open test pack](01c.md) |
| 01d — Objects, algorithms, and debugging | [Open test pack](01d.md) |
| 02a — Vectors, matrices, and algebra | [Open test pack](02a.md) |
| 02b — Derivatives and optimization | [Open test pack](02b.md) |
| 02c — Probability, statistics, and uncertainty | [Open test pack](02c.md) |
| 03a — NumPy and Pandas data contracts | [Open test pack](03a.md) |
| 03b — SQL, transactions, and schema design | [Open test pack](03b.md) |
| 03c — HTTP, validation, and FastAPI | [Open test pack](03c.md) |
| 04a — Supervised learning without leakage | [Open test pack](04a.md) |
| 04b — Metrics, clustering, and error analysis | [Open test pack](04b.md) |
| 05a — A neural network from scratch | [Open test pack](05a.md) |
| 05b — PyTorch training and image classification | [Open test pack](05b.md) |
| 06a — Tokens, attention, and decoding | [Open test pack](06a.md) |
| 06b — A tiny causal transformer | [Open test pack](06b.md) |
| 06c — Adaptation, extraction, and quantization | [Open test pack](06c.md) |
| 07a — Retrieval from first principles | [Open test pack](07a.md) |
| 07b — Grounding, permissions, and vector search | [Open test pack](07b.md) |
| 08a — Tools and bounded workflows | [Open test pack](08a.md) |
| 08b — LangGraph state and human review | [Open test pack](08b.md) |
| 09a — Memory and serving performance | [Open test pack](09a.md) |
| 09b — Local model API contracts | [Open test pack](09b.md) |
| 10a — Reliability and observability | [Open test pack](10a.md) |
| 10b — Containers, configuration, and deployment | [Open test pack](10b.md) |
| 11a — Distributed data and associative aggregation | [Open test pack](11a.md) |
| 11b — PySpark DataFrames and windows | [Open test pack](11b.md) |
| 12a — Threat models and untrusted content | [Open test pack](12a.md) |
| 12b — Authorization, caches, and isolation | [Open test pack](12b.md) |
| 13a — Evaluation datasets and retrieval metrics | [Open test pack](13a.md) |
| 13b — Regression gates and uncertainty | [Open test pack](13b.md) |
| 14a — Financial statements and ratios | [Open test pack](14a.md) |
| 14b — Time series and honest backtests | [Open test pack](14b.md) |
| 15a — An evidence-backed financial research pipeline | [Open test pack](15a.md) |
| 15b — Architecture review and mastery defense | [Open test pack](15b.md) |

## All-reference maintenance check

```bash
python tools/test_assignment.py --all --reference
```

This needs the core, deep, agents, and integration parsing dependencies. Local Spark is skipped unless `--live-spark` is added with the supported JDK. PostgreSQL/model-serving/deployment evidence remains separate. Ordinary `pytest` skips assignment packs until you explicitly select a learner solution or the references.
