# Your AI engineering learning plan

Designed for a beginner, based on all 16 stages in [the original roadmap](../readme.md). Budget **1,200 focused hours**, approximately **80 weeks at 15 hours/week**. At 10/20/25 hours per week, the same work takes about 120/60/48 weeks. These are planning estimates; repeat weak checkpoints before advancing. The README’s 1,000 hours is a broad estimate; this plan adds deliberate practice and review.

Start with [START_HERE.md](../START_HERE.md), then [the first 30 days](FIRST_30_DAYS.md). Every stage includes practice notebooks, separate answers, a work brief, reference implementation or operational lab, and a closed-book gate.

## How to study

Use five 3-hour sessions per week. A typical session: 20 minutes retrieval from memory, 40 minutes reading/experimenting, 90 minutes coding, 20 minutes testing/debugging, 10 minutes updating your log. During project weeks, move reading time into implementation. Take breaks inside your chosen schedule. Review each major concept after 2, 7, and 30 days.

Try exercises before opening answers. Record your attempt and error first, use a hint next, and only then compare a solution. Close it and rebuild with changed inputs two days later. Passing visible checks is a starting point; add edge cases and explain the contract.

## Stage map

| Stage | Hours | Approx. weeks | Practical outcome |
|---|---:|---:|---|
| [00 — Orientation and tools](stages/00.md) | 15 | 1–1 | [Reproducible learning workspace](../projects/stage00/README.md) |
| [01 — Python programming](stages/01.md) | 150 | 2–11 | [Expense analyzer and command-line utilities](../projects/stage01/README.md) |
| [02 — Mathematics for AI](stages/02.md) | 110 | 12–19 | [Math lab and regression from scratch](../projects/stage02/README.md) |
| [03 — Data, SQL, and APIs](stages/03.md) | 110 | 19–26 | [Persistent data analysis API](../projects/stage03/README.md) |
| [04 — Classical machine learning](stages/04.md) | 100 | 26–33 | [Support-ticket classifier and demand regression](../projects/stage04/README.md) |
| [05 — Deep learning](stages/05.md) | 90 | 33–39 | [NumPy XOR and PyTorch digits classifier](../projects/stage05/README.md) |
| [06 — Transformers and LLMs](stages/06.md) | 100 | 39–45 | [Tiny language model, pretrained classifier, and extraction](../projects/stage06/README.md) |
| [07 — Retrieval-augmented generation](stages/07.md) | 75 | 46–50 | [Private document assistant](../projects/stage07/README.md) |
| [08 — Agents and workflows](stages/08.md) | 70 | 51–55 | [Bounded research assistant with approval](../projects/stage08/README.md) |
| [09 — Local and self-hosted models](stages/09.md) | 40 | 55–58 | [Local inference benchmark](../projects/stage09/README.md) |
| [10 — Production engineering](stages/10.md) | 75 | 58–63 | [Containerized service and recovery runbook](../projects/stage10/README.md) |
| [11 — Spark and big data](stages/11.md) | 40 | 63–65 | [Transaction analytics pipeline](../projects/stage11/README.md) |
| [12 — AI security](stages/12.md) | 40 | 66–68 | [Threat model and adversarial test suite](../projects/stage12/README.md) |
| [13 — Evaluation engineering](stages/13.md) | 50 | 68–71 | [Versioned evaluation and release gates](../projects/stage13/README.md) |
| [14 — Financial AI specialization](stages/14.md) | 45 | 72–74 | [Statement comparison and time-series analysis](../projects/stage14/README.md) |
| [15 — Final capstone](stages/15.md) | 90 | 75–80 | [Private financial research platform](../projects/stage15/README.md) |

## Weekly pacing

The table below allocates every 15-hour week. Stage boundaries can share a week. Use the stage’s hour blocks to balance learning, practice, independent building, and review; the listed task is the main deliverable for that portion of the stage.

| Week | Stage allocation | Main work |
|---:|---|---|
| 1 | 00: 15h | Create a branch, make two commits, inspect a diff, resolve a small practice conflict, and push to your own GitHub repository. |
| 2 | 01: 15h | Build calculator, temperature/profit tools, text analyzer, contact book, and inventory before the main project. |
| 3 | 01: 15h | Build calculator, temperature/profit tools, text analyzer, contact book, and inventory before the main project. |
| 4 | 01: 15h | Build a CSV expense CLI with total, category totals, monthly totals, average, highest expense, and clear line-numbered errors. |
| 5 | 01: 15h | Build a CSV expense CLI with total, category totals, monthly totals, average, highest expense, and clear line-numbered errors. |
| 6 | 01: 15h | Split parsing, calculation, and CLI code; add tests for empty files, quotes, malformed dates, NaN, negative amounts, and missing columns. |
| 7 | 01: 15h | Split parsing, calculation, and CLI code; add tests for empty files, quotes, malformed dates, NaN, negative amounts, and missing columns. |
| 8 | 01: 15h | Split parsing, calculation, and CLI code; add tests for empty files, quotes, malformed dates, NaN, negative amounts, and missing columns. |
| 9 | 01: 15h | Refactor one component to a class using composition; profile linear and binary search and explain recursion with a base case. |
| 10 | 01: 15h | Refactor one component to a class using composition; profile linear and binary search and explain recursion with a base case. |
| 11 | 01: 15h | Refactor one component to a class using composition; profile linear and binary search and explain recursion with a base case. |
| 12 | 02: 15h | Implement vector addition, dot product, cosine, matrix multiplication, transpose, mean, variance, and standard deviation without NumPy. |
| 13 | 02: 15h | Plot linear/quadratic/log functions, a 2D rotation, and an eigenvector example; label units and axes. |
| 14 | 02: 15h | Plot linear/quadratic/log functions, a 2D rotation, and an eigenvector example; label units and axes. |
| 15 | 02: 15h | Fit slope and intercept by gradient descent; verify gradients numerically and compare three learning rates. |
| 16 | 02: 15h | Fit slope and intercept by gradient descent; verify gradients numerically and compare three learning rates. |
| 17 | 02: 15h | Simulate Bernoulli/binomial trials and a normal sample; bootstrap a mean interval, compute covariance/correlation, and perform a permutation test. |
| 18 | 02: 15h | Simulate Bernoulli/binomial trials and a normal sample; bootstrap a mean interval, compute covariance/correlation, and perform a permutation test. |
| 19 | 02: 5h, 03: 10h | Simulate Bernoulli/binomial trials and a normal sample; bootstrap a mean interval, compute covariance/correlation, and perform a permutation test. Profile and clean a CSV with a data-quality report and quarantined invalid records. |
| 20 | 03: 15h | Profile and clean a CSV with a data-quality report and quarantined invalid records. |
| 21 | 03: 15h | Design a normalized relational schema and write the complete SQL worksheet in EXTRA_LABS.md; examine index plans. |
| 22 | 03: 15h | Implement GET /records, /summary, /statistics and POST /records, with persistent storage and tenant isolation. |
| 23 | 03: 15h | Implement GET /records, /summary, /statistics and POST /records, with persistent storage and tenant isolation. |
| 24 | 03: 15h | Run first on SQLite and then PostgreSQL via Compose. Ingest CSV, restart the API, verify totals, and test rollback and invalid requests. |
| 25 | 03: 15h | Run first on SQLite and then PostgreSQL via Compose. Ingest CSV, restart the API, verify totals, and test rollback and invalid requests. |
| 26 | 03: 10h, 04: 5h | Run first on SQLite and then PostgreSQL via Compose. Ingest CSV, restart the API, verify totals, and test rollback and invalid requests. Use the supplied fixed train/validation/test split; verify template groups never cross boundaries. |
| 27 | 04: 15h | Compare majority, logistic, forest, and boosting classifiers; select on validation macro-F1, then evaluate once on test. |
| 28 | 04: 15h | Compare majority, logistic, forest, and boosting classifiers; select on validation macro-F1, then evaluate once on test. |
| 29 | 04: 15h | Create a demand regression dataset and compare mean, linear, tree, forest, and boosting models using MAE/RMSE/R². |
| 30 | 04: 15h | Compare KMeans/DBSCAN on blobs and moons, investigate PCA, and collect 20+ independent ticket errors for a model card. |
| 31 | 04: 15h | Expose one saved trusted classifier through a prediction API; validate input size and return label scores with calibration limitations. |
| 32 | 04: 15h | Expose one saved trusted classifier through a prediction API; validate input size and return label scores with calibration limitations. |
| 33 | 04: 5h, 05: 10h | Expose one saved trusted classifier through a prediction API; validate input size and return label scores with calibration limitations. Implement a two-layer NumPy XOR network and check analytical gradients against finite differences. |
| 34 | 05: 15h | Train an MLP and CNN on the same digits split using CPU, with a real DataLoader and validation loop. |
| 35 | 05: 15h | Train an MLP and CNN on the same digits split using CPU, with a real DataLoader and validation loop. |
| 36 | 05: 15h | Save training curves and the best validation checkpoint; evaluate test once after selection. |
| 37 | 05: 15h | Run controlled learning-rate, dropout, and normalization experiments; record seed, parameter count, runtime, and failure diagnosis. |
| 38 | 05: 15h | Run controlled learning-rate, dropout, and normalization experiments; record seed, parameter count, runtime, and failure diagnosis. |
| 39 | 05: 5h, 06: 10h | Run controlled learning-rate, dropout, and normalization experiments; record seed, parameter count, runtime, and failure diagnosis. Implement and visualize causal attention; perturb a future token and prove earlier outputs do not change. |
| 40 | 06: 15h | Train the tiny transformer on the bundled corpus; log held-out loss and inspect generated text. |
| 41 | 06: 15h | Run pretrained.py with an explicitly selected model and immutable revision; compare pre/post-adaptation validation and final test. |
| 42 | 06: 15h | Run pretrained.py with an explicitly selected model and immutable revision; compare pre/post-adaptation validation and final test. |
| 43 | 06: 15h | Build extraction with schema validation, exact source spans, currency/scale normalization, and unknown results for unsupported inputs. |
| 44 | 06: 15h | Compare quantization reconstruction error and LoRA parameter count; document QLoRA hardware requirements and run it only on supported equipment. |
| 45 | 06: 15h | Compare quantization reconstruction error and LoRA parameter count; document QLoRA hardware requirements and run it only on supported equipment. |
| 46 | 07: 15h | Ingest at least three formats, inspect extracted tables, and retain source/version/page or offset metadata. |
| 47 | 07: 15h | Run learned embeddings and pgvector integration; compare keyword, dense, RRF hybrid, and cross-encoder reranking. |
| 48 | 07: 15h | Add a local generator and claim-level citation review; distinguish unsupported answers from empty retrieval. |
| 49 | 07: 15h | Test two tenants, public documents, permission changes, stale indexes, and malicious document instructions. |
| 50 | 07: 15h | Test two tenants, public documents, permission changes, stale indexes, and malicious document instructions. |
| 51 | 08: 15h | Create a plain Python workflow, then the equivalent LangGraph; compare traces on the same requests. |
| 52 | 08: 15h | Persist a checkpoint, interrupt before a proposed action, bind approval to exact content, resume or deny, and isolate run IDs. |
| 53 | 08: 15h | Inject transient failures, malformed arguments, repeated calls, timeouts, and budget exhaustion. |
| 54 | 08: 15h | Only as an experiment, split research and checking into two workers and compare task success, calls, latency, and cost. |
| 55 | 08: 10h, 09: 5h | Only as an experiment, split research and checking into two workers and compare task success, calls, latency, and cost. Estimate weights and KV cache for three sizes/precisions/context lengths, then compare to actual memory. |
| 56 | 09: 15h | Run native Ollama requests and, on supported hardware, vLLM-compatible requests. |
| 57 | 09: 15h | Connect the Stage 07 assistant to the local endpoint and verify data does not leave the intended host. |
| 58 | 09: 5h, 10: 10h | Connect the Stage 07 assistant to the local endpoint and verify data does not leave the intended host. Run the API and PostgreSQL using the provided Dockerfile/Compose, then inspect networking and persistent data. |
| 59 | 10: 15h | Add request IDs, versioned events, safe logs, latency/error metrics, and an operational dashboard or report. |
| 60 | 10: 15h | Simulate database/model outages, bad auth, malformed/huge input, corrupt files, and exhausted capacity. |
| 61 | 10: 15h | Perform backup and restore into a separate database; prove row counts and application reads after restore. |
| 62 | 10: 15h | Add CI, create a release lock and image digest, rehearse rollback, and document a Coolify deployment with private database networking and HTTPS. |
| 63 | 10: 5h, 11: 10h | Add CI, create a release lock and image digest, rehearse rollback, and document a Coolify deployment with private database networking and HTTPS. Calculate grouped sums/counts, daily trends, anomalies, and window statistics; write Parquet. |
| 64 | 11: 15h | Check row count, schema, total cents, and a sampled group against a Python reference. |
| 65 | 11: 15h | Repeat on an actual cluster or document the operational gap if only local mode is available. |
| 66 | 12: 15h | Write at least 20 attacks against your own app: cross-tenant access, prompt injection, malformed tool calls, oversized inputs, and forged citations. |
| 67 | 12: 15h | Record observed behavior and fix failures with code-enforced policy rather than a stronger-sounding prompt. |
| 68 | 12: 10h, 13: 5h | Record observed behavior and fix failures with code-enforced policy rather than a stronger-sounding prompt. Expand the nine-case fixture to at least 60 reviewed cases; preserve 20 as a locked holdout. |
| 69 | 13: 15h | Separate retrieval, numeric correctness, citation support, abstention, permissions, tool behavior, and service quality. |
| 70 | 13: 15h | Compare two candidates on paired questions, report slices and uncertainty, and inspect regressions. |
| 71 | 13: 15h | Write machine-readable reports and fail CI on predeclared hard gates; version every component and label set. |
| 72 | 14: 15h | Compare three years for two companies; distinguish period, currency, scale, average versus ending balances, and capex signs. |
| 73 | 14: 15h | Create past-only features, walk-forward splits, and an as-of publication-date join. |
| 74 | 14: 15h | Compare a forecast to naive baselines; include turnover/cost assumptions if building a strategy. Explain why no predictive edge is established. |
| 75 | 15: 15h | Answer a two-company three-year revenue/margin/FCF comparison with deterministic calculations and citations. |
| 76 | 15: 15h | Integrate learned embeddings, PostgreSQL, local model serving, bounded tools, permissions, and a usable client such as the API docs or a small CLI. |
| 77 | 15: 15h | Run the full failure matrix, restore backup, rehearse deployment/rollback, and write an architecture decision record. |
| 78 | 15: 15h | Grow the evaluation corpus to at least 100 reviewed cases and target 500 as the domain expands; preserve a locked holdout. |
| 79 | 15: 15h | Complete a 90-minute unseen feature, explain every component, and have another person reproduce the system. |
| 80 | 15: 15h | Complete a 90-minute unseen feature, explain every component, and have another person reproduce the system. |

## Graduation and continued practice

Complete [the capstone](CAPSTONE.md), retain four portfolio artifacts (classical ML, deep learning, private RAG, production workflow), and pass [the assessment](assessments/MASTERY.md). No fixed schedule guarantees mastery; the independent gates and delayed reviews determine readiness. Hardware-dependent work stays pending until demonstrated.

