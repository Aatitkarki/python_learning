# Stage 05: question-by-question solutions

[All-stage answer index](../../curriculum/ANSWER_INDEX.md) · [Project brief](README.md)

`solution.py` is the main project reference. It does not contain every answer. Use the exact question IDs below to find the smaller exercises and extra programs.

**Suggested workflow:** notebook → independent assignment in your own `.py` files → stage project → closed-book gate. Compare answers only after an attempt; then close them and rebuild with changed input.

## Notebook questions and independent assignments

### 05a: A neural network from scratch

[Test your independent assignment](../../curriculum/assignments/05a.md)

| ID | Question | Answer |
|---|---|---|
| 05a-E1 | Return a sigmoid for NumPy input without overflowing exp on large magnitudes. | [Worked solution](../../curriculum/answers/05a.md#05a-e1) |
| 05a-E2 | For X(n,d), y(n,1), w(d,1), scalar b, return MSE, dw, db. | [Worked solution](../../curriculum/answers/05a.md#05a-e2) |
| 05a-E3 | Use backward to fit w,b from zeros with 500 updates and lr=.05. Return w,b,loss history. | [Worked solution](../../curriculum/answers/05a.md#05a-e3) |
| 05a-O1 | Why an activation? | [Worked solution](../../curriculum/answers/05a.md#05a-o1) |
| 05a-O2 | What is backpropagation? | [Worked solution](../../curriculum/answers/05a.md#05a-o2) |
| 05a-T | Implement a NumPy two-layer tanh network for XOR. Check 10 random gradient entries, overfit four examples, then compare SGD and momentum. Plot loss versus epoch. | [Worked solution](../../curriculum/answers/05a.md#05a-t) |

### 05b: PyTorch training and image classification

[Test your independent assignment](../../curriculum/assignments/05b.md)

| ID | Question | Answer |
|---|---|---|
| 05b-E1 | Return derivative of sum(x²) as a tensor; create a fresh float tensor with gradients enabled. | [Worked solution](../../curriculum/answers/05b.md#05b-e1) |
| 05b-E2 | Return a network mapping (N,1,8,8) to (N,10): Conv2d(1,4,3,padding=1), ReLU, Flatten, Linear(256,10). | [Worked solution](../../curriculum/answers/05b.md#05b-e2) |
| 05b-E3 | Set training mode, zero gradients, compute cross entropy, backpropagate, step optimizer; return float loss. | [Worked solution](../../curriculum/answers/05b.md#05b-e3) |
| 05b-O1 | Why both eval and no_grad? | [Worked solution](../../curriculum/answers/05b.md#05b-o1) |
| 05b-O2 | Why can gradients explode? | [Worked solution](../../curriculum/answers/05b.md#05b-o2) |
| 05b-T | Run the digits CNN project with train/validation/test splits, DataLoader, loss curves, best-checkpoint restore, per-class errors, and a model card. Compare an MLP and CNN using the same split. | [Worked solution](../../curriculum/answers/05b.md#05b-t) |

## Project tasks, in brief order

<a id="05-p1"></a>
### 05-P1

**Question:** Implement a two-layer NumPy XOR network and check analytical gradients against finite differences.

**Answer:** [05a worked implementation and explanation](../../curriculum/answers/05a.md#05a-t)

<a id="05-p2"></a>
### 05-P2

**Question:** Train an MLP and CNN on the same digits split using CPU, with a real DataLoader and validation loop.

**Answer:** [05b worked implementation and explanation](../../curriculum/answers/05b.md#05b-t)

<a id="05-p3"></a>
### 05-P3

**Question:** Save training curves and the best validation checkpoint; evaluate test once after selection.

**Answer:** [05b worked implementation and explanation](../../curriculum/answers/05b.md#05b-t)

<a id="05-p4"></a>
### 05-P4

**Question:** Run controlled learning-rate, dropout, and normalization experiments; record seed, parameter count, runtime, and failure diagnosis.

**Answer:** [05b worked implementation and explanation](../../curriculum/answers/05b.md#05b-t)

<a id="05-g"></a>
## Mastery gate: 05-G

**Task:** Write a training loop from memory, overfit a tiny batch, explain tensor shapes and chain rule, then diagnose an injected gradient/mode bug.

**Expected reasoning and invariant outputs:** Also run python -m projects.stage05.numpy_xor. XOR loss should become very small and gradient error below 1e-6. The CNN uses 8×8 grayscale images with a held-out test split, eval mode, and no_grad. Record observed accuracy rather than copying a target. CrossEntropyLoss expects logits. Missing zero_grad accumulates gradients; missing step leaves weights unchanged; evaluating with dropout active adds avoidable variation.

Use the question-specific implementations above and [the reviewer answers](../../curriculum/assessments/ANSWERS.md). For deployment or model experiments, use [the worked operational procedures](../../curriculum/answers/OPERATIONS.md).

**Pass criteria:** 80/100 across correctness/reasoning (40), independent implementation (25), tests/debugging (20), and explanation/reproducibility (15). No permission leak, future-data leakage, invented evidence, or unreproducible core result. Live requirements remain pending until actually run. Running the answer files does not establish your independent mastery.

**If the gate fails:** If training fails, first overfit four examples and compare one analytical gradient to finite differences.
