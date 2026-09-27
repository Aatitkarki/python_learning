# Extended practice and worked-answer guide

These are the larger assignments referenced by notebook “Independent transfer” sections. Attempt them in work/ before reading the approach. The checked notebook answers cover the smaller functions; the project scripts show runnable end-to-end examples. For experiments, the answer is a reproducible method and an honest interpretation, not a predetermined favorable score.

## 00–01: programming extensions

**Contact book:** use a dictionary keyed by normalized email or an explicit unique ID. Store a record with name and phone. `add` rejects an existing key, `update` rejects a missing key, `delete` returns whether a record existed, and search returns a new list. Persist as JSON only after validation. A case-insensitive name is not necessarily a unique identity. Test repeated updates, non-ASCII names, missing keys, and an empty file.

**Text analyzer:** tokenize with an explicit policy, count with a dictionary/Counter, use `len(text)` for characters, sum counts for words, and count keys for unique words. Sort most-common words with `(-count, word)` to resolve ties. Punctuation-only text has no most-common word. “AI” and “ai” merge only if your normalization says they do.

**Calculator and units:** use an operation allowlist; reject invalid numeric input and division by zero. Temperature conversion is `F=C*9/5+32`; inverse is `(F-32)*5/9`. Validate units explicitly. For BMI as a programming exercise, calculate mass_kg / height_m² with positive inputs; do not add medical interpretation from a toy function.

**Recursion:** factorial has base case `n in (0,1)` returning 1 and step `n*factorial(n-1)` for nonnegative integers. Recursive directory walking also needs a policy for symbolic links and permission errors. An iterative approach avoids recursion-depth limits. Binary search requires sorted input; comparing one binary lookup after sorting against one unsorted linear lookup should include sorting cost.

**Mocking:** mock the file-opening or network boundary to raise a known exception, then assert that the CLI reports the expected input error and exits nonzero. Do not mock `summarize` and then claim that its totals were tested. Use temporary files for integration tests. Prefer composition, such as `Analyzer(repository)`, over inheritance solely to share a helper.

## 02: mathematics and statistics extensions

Vector addition: check equal length, then `[x+y for x,y in zip(a,b)]`. Transpose: `list(map(list, zip(*matrix)))` after checking rectangularity. Norm: `sqrt(dot(v,v))`; distance: norm of the difference. For rotation angle θ, multiply by `[[cos θ,-sin θ],[sin θ,cos θ]]`; verify norm preservation. The columns of the identity are eigenvectors of a diagonal matrix, with eigenvalues given by diagonal entries.

For `prediction=w*x+b`, residual `r=prediction-y`, MSE gradients are `dw=2*mean(x*r)` and `db=2*mean(r)`. Adding `λw²` contributes `2λw`; the intercept need not be penalized under this convention. For an arbitrary parameter θ, compare its analytical gradient with `(L(θ+h)-L(θ-h))/(2h)` while restoring θ afterward. Try several h values to distinguish calculus errors from floating-point cancellation.

For sample mean m and n observations, sample covariance is `sum((x-mx)*(y-my))/(n-1)`. Correlation divides covariance by the two sample standard deviations and is undefined if either is zero. Percentile interpolation conventions differ; name the one used. A normal sample does not guarantee normality of every quantity derived from it.

A permutation test of two independent groups under an exchangeable null:

```python
import random

def permutation_pvalue(a, b, repeats=5000, seed=42):
    if not a or not b or repeats < 1:
        raise ValueError("Nonempty groups and positive repeats required")
    rng = random.Random(seed)
    observed = abs(sum(a)/len(a) - sum(b)/len(b))
    combined = list(a) + list(b)
    extreme = 0
    for _ in range(repeats):
        shuffled = rng.sample(combined, len(combined))
        left, right = shuffled[:len(a)], shuffled[len(a):]
        statistic = abs(sum(left)/len(left) - sum(right)/len(right))
        extreme += statistic >= observed
    return (extreme + 1)/(repeats + 1)
```

The null assumes label exchangeability; time dependence or pairing requires a different permutation design. Statistical significance is not effect size. Repeatedly testing until a result is small invalidates the naive interpretation.

For plots, use labeled axes, units, and titles. Plot losses on a log scale if the positive values span many orders of magnitude. Save figures under work/ with the data, seed, and code needed to recreate them.

## 03: SQL worksheet answer

Run in a disposable database. SQLite supports most of this syntax; PostgreSQL is required for the query-plan and concurrency portions of the stage.

```sql
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);
CREATE TABLE sales (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    cents INTEGER NOT NULL CHECK (cents >= 0)
);
INSERT INTO customers VALUES (1,'A'), (2,'B'), (3,'C');
INSERT INTO sales VALUES (1,1,100), (2,1,200), (3,2,50);

-- Preserve customers with no sales; SUM over no matching rows is NULL.
SELECT c.id, c.name, COALESCE(SUM(s.cents),0) AS total
FROM customers c LEFT JOIN sales s ON s.customer_id=c.id
GROUP BY c.id,c.name ORDER BY c.id;
-- Expected totals: A=300, B=50, C=0.

-- WHERE filters source rows; HAVING filters aggregated groups.
SELECT customer_id, SUM(cents) AS total
FROM sales WHERE cents >= 50
GROUP BY customer_id HAVING SUM(cents) > 100;
-- Expected: customer 1, 300.

WITH totals AS (
    SELECT customer_id, SUM(cents) AS total FROM sales GROUP BY customer_id
)
SELECT customer_id,total FROM totals
WHERE total > (SELECT AVG(total) FROM totals);
-- Expected: customer 1, 300.

SELECT id, customer_id,
       SUM(cents) OVER (PARTITION BY customer_id ORDER BY id
                       ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running
FROM sales ORDER BY id;
-- Expected running totals: 100,300,50.

SELECT c.id FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM sales s WHERE s.customer_id=c.id);
-- Expected: customer 3.

SELECT customer_id FROM sales WHERE cents=100
UNION
SELECT customer_id FROM sales WHERE cents=200;
-- UNION returns 1 once; UNION ALL would return two rows.

CREATE INDEX sales_customer_idx ON sales(customer_id);
```

For PostgreSQL, compare `EXPLAIN (ANALYZE, BUFFERS)` before/after an index on a larger table. A sequential scan on three rows is reasonable; forcing an index does not prove a performance benefit. Demonstrate `BEGIN`, two writes, and `ROLLBACK`, then verify neither write persisted. In SQLite, enable foreign keys with `PRAGMA foreign_keys=ON` for a foreign-key enforcement experiment.

For Pandas, parse dates with explicit error behavior, inspect null counts, choose a duplicate key based on domain identity, and use `merge(validate='many_to_one')`. A rolling statistic must define order, window length, minimum periods, and whether current observations are included. A production API uses Pydantic at the boundary, repository transactions, authentication-derived tenant scope, and parameterized SQL. Integer cents make ledger totals exact.

## 04: regression, clustering, and deployment answers

Generate regression data with a known relationship plus seeded noise. Split before fitting. Compare DummyRegressor, LinearRegression, DecisionTreeRegressor, RandomForestRegressor, and GradientBoostingRegressor on the same split. Use pipelines for learned preprocessing. Report MAE, `sqrt(MSE)`, and R²; R² can be negative when the model is worse than the test-mean reference used by that metric. Cross-validate only on development data. Random-target controls should not consistently outperform an honest baseline.

On blobs, KMeans usually matches its roughly spherical-cluster assumption. On two moons, DBSCAN can follow curved dense regions while KMeans partitions by distance to centers. Standardize when feature units differ. Vary epsilon/min_samples and inspect noise assignments; do not select parameters against labels and then describe the experiment as entirely unsupervised. PCA may discard low-variance but predictive directions.

For kNN, explain sensitivity to scale and k; for SVM, compare a linear margin with an RBF kernel and tune inside cross-validation. ROC-AUC uses ranking over thresholds; choose a deployment threshold on validation costs and report a confusion matrix there. Probability calibration needs its own held-out or cross-validated procedure.

A prediction API should load a trusted versioned artifact once, validate text length, transform with the saved pipeline, and return label plus clearly described scores. Never load an untrusted pickle/joblib artifact. Record model, data, and code versions. On unknown vocabulary or low confidence, route to review rather than inventing certainty.

## 05–06: networks and LLM experiments

The full XOR backward pass is in [numpy_xor.py](../projects/stage05/numpy_xor.py). For hidden `h=tanh(XW1+b1)` and output `ŷ=hW2+b2`, let `d=2(ŷ-y)/n`; then `dW2=hᵀd`, `db2=sum(d)`, `dh=(d @ W2.T)*(1-h²)`, `dW1=Xᵀdh`, and `db1=sum(dh)`. In the `dh` expression, `W2` is the weight matrix, not its gradient. Check shapes to avoid notation confusion.

When comparing optimizers, hold data split, architecture, training budget, and evaluation protocol fixed. SGD uses a gradient step; momentum accumulates direction; Adam adapts moments; AdamW decouples weight decay. Dropout is active during training and disabled during evaluation. Normalization and gradient clipping solve different problems; inspect gradients before applying fixes blindly.

Top-k decoding keeps the k largest logits and sets others to negative infinity before softmax. Top-p sorts probabilities descending and keeps the smallest prefix whose cumulative sum reaches p, including the crossing token, then renormalizes. Greedy is argmax. Beam search keeps the best partial sequences by a defined score and length policy; it is not automatically best for open-ended generation.

A true KV-cache implementation stores past per-layer keys and values and computes only the newest query’s attention against cached positions. Positional indexing must continue from the cached length. Verify cached and uncached logits agree within tolerance before benchmarking. A cache is not permission-safe if shared between unrelated users.

Extraction answer: identify the source span first, normalize units second, validate the schema third, and compare the output against the source. “Aurora revenue was $1.2 billion” becomes 1,200,000,000 USD, with that sentence cited. An unspecified currency stays unknown. A regex extractor is a narrow deterministic baseline, not a substitute for evaluating a model extractor on varied language.

LoRA parameter count is `r*(in+out)` versus `in*out` for a dense weight matrix, plus any task heads or biases you choose to train. QLoRA adds quantization-specific behavior and hardware constraints; use the library’s current supported configuration. Compare quality, memory, and latency separately. Naming a quantization dtype does not prove kernels are running efficiently.

## 07: retrieval and parsing answers

A chunk record needs stable ID, source ID/version, location, text, tenant/ACL, parser version, and embedding version. Fixed word chunks are a transparent teaching baseline; actual model-token budgets require the model tokenizer. For paragraphs, accumulate whole paragraphs up to a limit and split unusually long ones; for semantic chunking, define a measurable boundary criterion and compare retrieval recall.

BM25 term score is commonly expressed as `IDF(t) * f(t,d)*(k1+1)/(f(t,d)+k1*(1-b+b*len(d)/avgdl))`, summed across query terms. State the exact IDF convention. The notebook’s set-overlap scorer and PostgreSQL `ts_rank_cd` are different lexical baselines. RRF combines ranks without assuming comparable raw score scales. Reranking improves only the retrieved candidate set.

Measure chunk size, overlap, embedding model, hybrid fusion, and reranking one change at a time against a development set. Report recall@k, precision@k under a declared denominator convention, MRR, latency, and memory. Groundedness requires checking each answer claim against evidence, not merely finding matching words. Reindex after changing the embedding model; mixing vector spaces can produce meaningless similarities.

The parser helper extracts text from several formats. Scan a PDF table and compare at least ten numbers with the original; record page IDs. If extraction is empty, investigate scanned pages/OCR rather than embedding empty text. DOCX tables and HTML navigation need deliberate handling. Do not treat document text that says “I am public” as authorization metadata.

## 08–10: workflow and operational design answers

A research workflow should carry a verified principal separately from model-generated state. Tool schemas describe search queries, bounded financial queries, and numeric operations. Use a tool registry with per-tool authorization; SQL tools should expose named query operations rather than unrestricted SQL. Validate arguments, cap result sizes, set I/O timeouts, record observations, and stop on a step/deadline budget. Model output can propose a tool call, but only code authorizes and executes it.

For public-data tools, define a response schema, timeout, cache/freshness policy, citation URL, and explicit failure result. Mock the HTTP boundary in unit tests and run a live read-only integration separately. Do not fabricate a price when an endpoint is unavailable. Use fixtures so notebooks never require a paid market-data subscription.

Human approval needs actor, exact action/arguments, approver, expiry, and single-use status. Resume from a durable checkpoint only after rechecking authorization; permissions may change while paused. The reference fingerprint binds content but is not a signed identity token. Threads and caches must include tenant scope. A multi-agent experiment should compare the same tasks against one controlled workflow, with the same budget; extra model calls alone are not progress.

For serving benchmarks, report cold-load separately, warm up deliberately, control input/output lengths, and collect enough observations for tail estimates. Record time to first token with streaming and total time separately. Bounded concurrent clients measure throughput using wall time of the whole batch, not summed per-request durations. Include failures and timeouts, not only successful requests.

Authentication options solve different problems: an API key identifies a caller/application; a session references server-side login state; a JWT is a signed claims format whose signature, issuer, audience, expiry, and algorithm must be verified; OAuth delegates access and is not by itself a complete user-identity protocol. Use an established identity provider/library for a real service rather than inventing cryptography. Authorize resources after authentication.

Operational evidence includes release/dependency locks, image digests, database migration history, restored-backup checks, request/error/latency metrics, traces across retrieval/model/database calls, and an incident record. Add a durable metrics backend and distributed rate limiting when using multiple API workers. The local reference’s in-memory quota is intentionally a single-process teaching example. The [runbook](../projects/stage10/RUNBOOK.md) supplies concrete commands.

## 11–13: distributed processing, security, and evaluation answers

Global average must combine sums and counts, not unweighted partition means. Associativity makes sum/count mergeable; exact floating-point results may vary with reduction order. Inspect physical plans for Exchange/shuffle operations. A broadcast join can avoid moving a large fact table if the other side truly fits executor memory. Hot-key salting distributes skew but requires a second aggregation and careful correctness checks.

A threat-model row should name asset, actor, entry point, trust boundary crossed, impact, enforced control, test, and residual risk. For a retrieved injection asking for another user’s report, the control is scoped retrieval/tool permissions before model context. Phrase blacklists do not cover all attacks. For poisoned financial numbers, the control includes trusted ingestion provenance, reconciliation, source review, and evaluation; authorization alone does not establish accuracy.

Evaluate abstention separately from retrieval recall when no source is relevant. Report sample size in every slice. For paired bootstrap, sample case indices with replacement and compute candidate-minus-baseline mean each time. If cases share documents, resample document groups. A confidence interval spanning zero is evidence that the sign is uncertain under the procedure, not proof the systems are identical. Hard safety gates are not averaged away.

A judge rubric should require evidence for each claim, allow “uncertain,” blind model identity, randomize answer order, and compare against human annotations. Track inter-rater disagreement. Evaluate judges against malicious answer text that tries to influence the grader. The release gate should be established before testing a favored candidate.

## 14–15: financial and capstone answers

Aurora 2023/2024/2025 revenue is 100/120/144 million USD; operating margin 15%/20%/25%; FCF 13/18/24 million. Beacon revenue is 90/99/108; operating margin 10%/approximately 12.12%/13.89%; FCF 8/9/12. Revenue growth is 20%/20% for Aurora and 10%/approximately 9.09% for Beacon after the first year. First-year growth is unknown without a prior year.

EPS divides net income in millions by weighted-average shares in millions, giving currency per share. ROE/ROA use average equity/assets; a first year without opening balance is unknown. P/S and FCF yield use market capitalization in the same scale as revenue/FCF. PEG conventions need care: if P/E=20 and annual growth=10%, a convention using percentage points gives PEG=20/10=2, not 20/0.10=200. A negative growth or earnings base may make this comparison meaningless.

An as-of join uses publication time, not fiscal year:

```python
# Both frames must be sorted by the merge key and have compatible datetime types.
joined = pd.merge_asof(
    decisions.sort_values("decision_time"),
    filings.sort_values("published_at"),
    left_on="decision_time", right_on="published_at",
    by="company", direction="backward", allow_exact_matches=True,
)
```

Specify whether an exact timestamp match was available before order placement. Keep original-vintage data when evaluating historical decisions; a later restatement was not known in the past. Lag return features, use time-aware folds/gaps, and include execution/cost assumptions. Synthetic random prices are a useful negative control, not a source of market predictions.

The capstone reference architecture is client → authenticated API → scoped repository/tools → deterministic calculation/evidence → optional local model draft → support validation → response with sources. PostgreSQL stores records/metadata; pgvector stores versioned embeddings; a model server owns inference; the orchestrator owns budgets/state; monitoring links request IDs across boundaries. Every claimed production property must be backed by a test or drill. See [CAPSTONE.md](CAPSTONE.md) for the acceptance matrix and defense.
