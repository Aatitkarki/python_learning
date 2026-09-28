# Stage 02: question-by-question solutions

[All-stage answer index](../../curriculum/ANSWER_INDEX.md) · [Project brief](README.md)

`solution.py` is the main project reference. It does not contain every answer. Use the exact question IDs below to find the smaller exercises and extra programs.

**Suggested workflow:** notebook → independent assignment in your own `.py` files → stage project → closed-book gate. Compare answers only after an attempt; then close them and rebuild with changed input.

## Notebook questions and independent assignments

### 02a: Vectors, matrices, and algebra

[Test your independent assignment](../../curriculum/assignments/02a.md)

| ID | Question | Answer |
|---|---|---|
| 02a-E1 | Return sum(a_i*b_i); reject unequal lengths. | [Worked solution](../../curriculum/answers/02a.md#02a-e1) |
| 02a-E2 | Use dot to return cosine similarity; reject a zero vector. | [Worked solution](../../curriculum/answers/02a.md#02a-e2) |
| 02a-E3 | Multiply nonempty rectangular nested lists. Validate rectangularity and inner dimensions. | [Worked solution](../../curriculum/answers/02a.md#02a-e3) |
| 02a-O1 | What does a dot product measure? | [Worked solution](../../curriculum/answers/02a.md#02a-o1) |
| 02a-O2 | Why does shape matter? | [Worked solution](../../curriculum/answers/02a.md#02a-o2) |
| 02a-T | Implement vector addition, transpose, norms, distances, and a 2D rotation. Draw original/transformed vectors. Check an eigenvector for diagonal matrix diag(2,3). Repeat using NumPy in Stage 03. | [Worked solution](../../curriculum/answers/02a.md#02a-t) |

### 02b: Derivatives and optimization

[Test your independent assignment](../../curriculum/assignments/02b.md)

| ID | Question | Answer |
|---|---|---|
| 02b-E1 | Approximate f prime at x using a central difference with h > 0. | [Worked solution](../../curriculum/answers/02b.md#02b-e1) |
| 02b-E2 | Return the MSE gradient for scalar w on equally sized nonempty xs, ys. | [Worked solution](../../curriculum/answers/02b.md#02b-e2) |
| 02b-E3 | Start at w=0, apply steps gradient updates, and return w. Defaults should fit y=2x. | [Worked solution](../../curriculum/answers/02b.md#02b-e3) |
| 02b-O1 | What does the chain rule do? | [Worked solution](../../curriculum/answers/02b.md#02b-o1) |
| 02b-O2 | Does low training loss imply good predictions? | [Worked solution](../../curriculum/answers/02b.md#02b-o2) |
| 02b-T | Add an intercept, L2 regularization, and loss history. Compare rates 0.001, 0.05, and 1.0. Explain divergence from the update equation; save a loss plot. | [Worked solution](../../curriculum/answers/02b.md#02b-t) |

### 02c: Probability, statistics, and uncertainty

[Test your independent assignment](../../curriculum/assignments/02c.md)

| ID | Question | Answer |
|---|---|---|
| 02c-E1 | Compute unbiased sample variance for n >= 2; reject smaller samples. | [Worked solution](../../curriculum/answers/02c.md#02c-e1) |
| 02c-E2 | Return P(event\|positive) from prevalence, sensitivity, and false_positive_rate in [0,1]. Reject an impossible positive event. | [Worked solution](../../curriculum/answers/02c.md#02c-e2) |
| 02c-E3 | Return the 2.5th and 97.5th percentile order statistics of 1000 bootstrap means using seed=42. Require nonempty data. | [Worked solution](../../curriculum/answers/02c.md#02c-e3) |
| 02c-O1 | What is a base-rate error? | [Worked solution](../../curriculum/answers/02c.md#02c-o1) |
| 02c-O2 | Why is correlation insufficient for causation? | [Worked solution](../../curriculum/answers/02c.md#02c-o2) |
| 02c-T | Simulate 10,000 Bernoulli trials, plot a binomial count histogram, calculate percentiles/covariance/correlation, and run a permutation test of a mean difference. Explain sampling bias and multiple testing. | [Worked solution](../../curriculum/answers/02c.md#02c-t) |

## Project tasks, in brief order

<a id="02-p1"></a>
### 02-P1

**Question:** Implement vector addition, dot product, cosine, matrix multiplication, transpose, mean, variance, and standard deviation without NumPy.

**Answer:** [02a worked implementation and explanation](../../curriculum/answers/02a.md#02a-t) · [02c worked implementation and explanation](../../curriculum/answers/02c.md#02c-t)

<a id="02-p2"></a>
### 02-P2

**Question:** Plot linear/quadratic/log functions, a 2D rotation, and an eigenvector example; label units and axes.

**Answer:** [02a worked implementation and explanation](../../curriculum/answers/02a.md#02a-t)

<a id="02-p3"></a>
### 02-P3

**Question:** Fit slope and intercept by gradient descent; verify gradients numerically and compare three learning rates.

**Answer:** [02b worked implementation and explanation](../../curriculum/answers/02b.md#02b-t)

<a id="02-p4"></a>
### 02-P4

**Question:** Simulate Bernoulli/binomial trials and a normal sample; bootstrap a mean interval, compute covariance/correlation, and perform a permutation test.

**Answer:** [02c worked implementation and explanation](../../curriculum/answers/02c.md#02c-t)

<a id="02-g"></a>
## Mastery gate: 02-G

**Task:** Derive MSE gradients on paper, implement them, diagnose a diverging rate, and explain Bayes using counts in a hypothetical population. Pass changed-shape matrix tests.

**Expected reasoning and invariant outputs:** For x=[-2,-1,0,1,2] and y=[-3,-1,1,3,5], the fitted line is y=2x+1. The central-difference gradient should agree to about 1e-6. Sample variance of [1,2,3] is 1; population variance is 2/3. A rotation preserves Euclidean norm; diag(2,3) maps [1,0] to twice itself. A permutation test shuffles group labels under exchangeability and compares absolute mean differences; use (extreme+1)/(repeats+1).

Use the question-specific implementations above and [the reviewer answers](../../curriculum/assessments/ANSWERS.md). For deployment or model experiments, use [the worked operational procedures](../../curriculum/answers/OPERATIONS.md).

**Pass criteria:** 80/100 across correctness/reasoning (40), independent implementation (25), tests/debugging (20), and explanation/reproducibility (15). No permission leak, future-data leakage, invented evidence, or unreproducible core result. Live requirements remain pending until actually run. Running the answer files does not establish your independent mastery.

**If the gate fails:** Draw dimensions and compute a two-element example by hand. If calculus is weak, repeat finite differences before attempting a network.
