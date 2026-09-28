# Stage 04: question-by-question solutions

[All-stage answer index](../../curriculum/ANSWER_INDEX.md) · [Project brief](README.md)

`solution.py` is the main project reference. It does not contain every answer. Use the exact question IDs below to find the smaller exercises and extra programs.

**Suggested workflow:** notebook → independent assignment in your own `.py` files → stage project → closed-book gate. Compare answers only after an attempt; then close them and rebuild with changed input.

## Notebook questions and independent assignments

### 04a: Supervised learning without leakage

[Test your independent assignment](../../curriculum/assignments/04a.md)

| ID | Question | Answer |
|---|---|---|
| 04a-E1 | Predict the training-label mean for every test item. Reject empty training labels. | [Worked solution](../../curriculum/answers/04a.md#04a-e1) |
| 04a-E2 | Return an unfitted TF-IDF + LogisticRegression pipeline with max_iter=500, random_state=42. | [Worked solution](../../curriculum/answers/04a.md#04a-e2) |
| 04a-E3 | Given rows with group and split keys, return True only if no group appears in multiple splits. | [Worked solution](../../curriculum/answers/04a.md#04a-e3) |
| 04a-O1 | What is leakage? | [Worked solution](../../curriculum/answers/04a.md#04a-o1) |
| 04a-O2 | Why can a simple model win? | [Worked solution](../../curriculum/answers/04a.md#04a-o2) |
| 04a-T | Train the support-ticket project with DummyClassifier, logistic regression, random forest, and gradient boosting. Fit a separate synthetic demand regression task with linear, tree, forest, and boosting models. Record MAE, RMSE, R² and classification macro-F1. | [Worked solution](../../curriculum/answers/04a.md#04a-t) |

### 04b: Metrics, clustering, and error analysis

[Test your independent assignment](../../curriculum/assignments/04b.md)

| ID | Question | Answer |
|---|---|---|
| 04b-E1 | Return precision, recall, f1 for 0/1 truth and predictions of equal length. Zero denominators yield zero. | [Worked solution](../../curriculum/answers/04b.md#04b-e1) |
| 04b-E2 | Return total cost with false negatives costing 5 and false positives 1; score >= threshold predicts 1. | [Worked solution](../../curriculum/answers/04b.md#04b-e2) |
| 04b-E3 | Fit StandardScaler then PCA(n_components=1) on X and return transformed data plus pipeline. | [Worked solution](../../curriculum/answers/04b.md#04b-e3) |
| 04b-O1 | Can AUC select a deployment threshold? | [Worked solution](../../curriculum/answers/04b.md#04b-o1) |
| 04b-O2 | Are clusters ground-truth categories? | [Worked solution](../../curriculum/answers/04b.md#04b-o2) |
| 04b-T | Compare KMeans and DBSCAN on two-moons and blob datasets. Explain failure shapes, outliers, and scale sensitivity. Write a ticket error taxonomy with at least 20 independently labeled new examples. | [Worked solution](../../curriculum/answers/04b.md#04b-t) |

## Project tasks, in brief order

<a id="04-p1"></a>
### 04-P1

**Question:** Use the supplied fixed train/validation/test split; verify template groups never cross boundaries.

**Answer:** [04a worked implementation and explanation](../../curriculum/answers/04a.md#04a-t)

<a id="04-p2"></a>
### 04-P2

**Question:** Compare majority, logistic, forest, and boosting classifiers; select on validation macro-F1, then evaluate once on test.

**Answer:** [04a worked implementation and explanation](../../curriculum/answers/04a.md#04a-t)

<a id="04-p3"></a>
### 04-P3

**Question:** Create a demand regression dataset and compare mean, linear, tree, forest, and boosting models using MAE/RMSE/R².

**Answer:** [04a worked implementation and explanation](../../curriculum/answers/04a.md#04a-t)

<a id="04-p4"></a>
### 04-P4

**Question:** Compare KMeans/DBSCAN on blobs and moons, investigate PCA, and collect 20+ independent ticket errors for a model card.

**Answer:** [04b worked implementation and explanation](../../curriculum/answers/04b.md#04b-t)

<a id="04-p5"></a>
### 04-P5

**Question:** Expose one saved trusted classifier through a prediction API; validate input size and return label scores with calibration limitations.

**Answer:** [04a worked implementation and explanation](../../curriculum/answers/04a.md#04a-t)

<a id="04-g"></a>
## Mastery gate: 04-G

**Task:** Spot three leakage mechanisms, justify a split and metric, implement a pipeline, and explain five wrong predictions. Train on a new dataset without copying the notebook.

**Expected reasoning and invariant outputs:** Validation chooses the model; test evaluates that final choice. TF-IDF belongs inside the pipeline, and boosting uses a bounded dense representation in this tiny example. No universal score is promised: inspect the generated report. A perfect score on 36 authored examples is weak evidence. Demand regression must beat a mean baseline on unseen data; random targets should not yield credible performance. KMeans tends to fail on curved clusters; DBSCAN is sensitive to density and scale.

Use the question-specific implementations above and [the reviewer answers](../../curriculum/assessments/ANSWERS.md). For deployment or model experiments, use [the worked operational procedures](../../curriculum/answers/OPERATIONS.md).

**Pass criteria:** 80/100 across correctness/reasoning (40), independent implementation (25), tests/debugging (20), and explanation/reproducibility (15). No permission leak, future-data leakage, invented evidence, or unreproducible core result. Live requirements remain pending until actually run. Running the answer files does not establish your independent mastery.

**If the gate fails:** If evaluation is confusing, calculate a 2×2 confusion matrix by hand and implement a dummy baseline first.
