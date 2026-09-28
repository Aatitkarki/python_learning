# Stage 06: question-by-question solutions

[All-stage answer index](../../curriculum/ANSWER_INDEX.md) · [Project brief](README.md)

`solution.py` is the main project reference. It does not contain every answer. Use the exact question IDs below to find the smaller exercises and extra programs.

**Suggested workflow:** notebook → independent assignment in your own `.py` files → stage project → closed-book gate. Compare answers only after an attempt; then close them and rebuild with changed input.

## Notebook questions and independent assignments

### 06a: Tokens, attention, and decoding

[Test your independent assignment](../../curriculum/assignments/06a.md)

| ID | Question | Answer |
|---|---|---|
| 06a-E1 | Build sorted unique-character vocabulary. Return ids, encode mapping, and decoded text for the given nonempty string. | [Worked solution](../../curriculum/answers/06a.md#06a-e1) |
| 06a-E2 | Return output and attention weights for equal-length 2D Q,K,V. Mask all future positions before stable row softmax. | [Worked solution](../../curriculum/answers/06a.md#06a-e2) |
| 06a-E3 | Return stable softmax(logits/temperature). Reject nonpositive temperature. | [Worked solution](../../curriculum/answers/06a.md#06a-e3) |
| 06a-O1 | Why divide by square root of d? | [Worked solution](../../curriculum/answers/06a.md#06a-o1) |
| 06a-O2 | Does attention prove explanation? | [Worked solution](../../curriculum/answers/06a.md#06a-o2) |
| 06a-T | Visualize attention weights and prove changing a future value cannot affect an earlier output. Implement top-k/top-p and compare entropy. Read a subword tokenizer vocabulary and explain special tokens. | [Worked solution](../../curriculum/answers/06a.md#06a-t) |

### 06b: A tiny causal transformer

[Test your independent assignment](../../curriculum/assignments/06b.md)

| ID | Question | Answer |
|---|---|---|
| 06b-E1 | Return sequence[:-1] and sequence[1:] for a 1D tensor of at least two tokens. | [Worked solution](../../curriculum/answers/06b.md#06b-e1) |
| 06b-E2 | Return an n×n boolean mask where True blocks future keys; diagonal stays False. | [Worked solution](../../curriculum/answers/06b.md#06b-e2) |
| 06b-E3 | Implement TinyBlock with batch_first MultiheadAttention(d,2), LayerNorm, and residual connection. Forward accepts (N,T,d), uses causal_mask, returns same shape. | [Worked solution](../../curriculum/answers/06b.md#06b-e3) |
| 06b-O1 | Why split text before windowing? | [Worked solution](../../curriculum/answers/06b.md#06b-o1) |
| 06b-O2 | Why a residual path? | [Worked solution](../../curriculum/answers/06b.md#06b-o2) |
| 06b-T | Train projects/stage06/tiny_lm.py, add a second block, compare held-out loss and generation, then implement cached inference as an extension. Explain why train loss alone is insufficient. | [Worked solution](../../curriculum/answers/06b.md#06b-t) |

### 06c: Adaptation, extraction, and quantization

[Test your independent assignment](../../curriculum/assignments/06c.md)

| ID | Question | Answer |
|---|---|---|
| 06c-E1 | Parse JSON with company (nonempty str) and revenue (finite float >=0), forbid extra keys. Return a validated model_dump dictionary. | [Worked solution](../../curriculum/answers/06c.md#06c-e1) |
| 06c-E2 | For W(out,in), A(rank,in), B(out,rank), return W+(alpha/rank)*(B@A). | [Worked solution](../../curriculum/answers/06c.md#06c-e2) |
| 06c-E3 | Return int8 codes, scale, and dequantized weights using max(abs(w))/127; all-zero arrays use scale=1. | [Worked solution](../../curriculum/answers/06c.md#06c-e3) |
| 06c-O1 | Does valid JSON imply truth? | [Worked solution](../../curriculum/answers/06c.md#06c-o1) |
| 06c-O2 | What does LoRA change? | [Worked solution](../../curriculum/answers/06c.md#06c-o2) |
| 06c-T | Run the pretrained text-classification and PEFT lab in projects/stage06/pretrained.py after selecting/downloading a model. Compare frozen baseline versus fine-tuning on validation examples; record revision, license, cost, and test metrics. Audit extraction against source spans. | [Worked solution](../../curriculum/answers/06c.md#06c-t) |

## Project tasks, in brief order

<a id="06-p1"></a>
### 06-P1

**Question:** Implement and visualize causal attention; perturb a future token and prove earlier outputs do not change.

**Answer:** [06a worked implementation and explanation](../../curriculum/answers/06a.md#06a-t)

<a id="06-p2"></a>
### 06-P2

**Question:** Train the tiny transformer on the bundled corpus; log held-out loss and inspect generated text.

**Answer:** [06b worked implementation and explanation](../../curriculum/answers/06b.md#06b-t)

<a id="06-p3"></a>
### 06-P3

**Question:** Run pretrained.py with an explicitly selected model and immutable revision; compare pre/post-adaptation validation and final test.

**Answer:** [06c worked implementation and explanation](../../curriculum/answers/06c.md#06c-t)

<a id="06-p4"></a>
### 06-P4

**Question:** Build extraction with schema validation, exact source spans, currency/scale normalization, and unknown results for unsupported inputs.

**Answer:** [06c worked implementation and explanation](../../curriculum/answers/06c.md#06c-t)

<a id="06-p5"></a>
### 06-P5

**Question:** Compare quantization reconstruction error and LoRA parameter count; document QLoRA hardware requirements and run it only on supported equipment.

**Answer:** [06c worked implementation and explanation](../../curriculum/answers/06c.md#06c-t)

<a id="06-g"></a>
## Mastery gate: 06-G

**Task:** Explain attention and KV cache, implement a causal block, debug target leakage, compare fine-tuning options, and validate a deliberately malformed or unsupported extraction.

**Expected reasoning and invariant outputs:** Targets are shifted by one position, and text is split before overlapping windows. A causal-mask test must modify future inputs, not merely inspect tensor dimensions. The repeating corpus teaches mechanics and cannot establish broad language capability. pretrained.py --offline-smoke tests a real PEFT adapter without downloaded weights; it is distinct from the pretrained lab. Extraction of “100 billion” requires multiplication by 1e9 and evidence containing the unit. Quantization saves weight storage but may not improve latency.

Use the question-specific implementations above and [the reviewer answers](../../curriculum/assessments/ANSWERS.md). For deployment or model experiments, use [the worked operational procedures](../../curriculum/answers/OPERATIONS.md).

**Pass criteria:** 80/100 across correctness/reasoning (40), independent implementation (25), tests/debugging (20), and explanation/reproducibility (15). No permission leak, future-data leakage, invented evidence, or unreproducible core result. Live requirements remain pending until actually run. Running the answer files does not establish your independent mastery.

**If the gate fails:** If architecture is opaque, return to 02a shapes and 05a gradients; use one attention head on three tokens first.
