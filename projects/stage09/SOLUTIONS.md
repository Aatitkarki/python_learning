# Stage 09: question-by-question solutions

[All-stage answer index](../../curriculum/ANSWER_INDEX.md) · [Project brief](README.md)

`solution.py` is the main project reference. It does not contain every answer. Use the exact question IDs below to find the smaller exercises and extra programs.

**Suggested workflow:** notebook → independent assignment in your own `.py` files → stage project → closed-book gate. Compare answers only after an attempt; then close them and rebuild with changed input.

## Notebook questions and independent assignments

### 09a: Memory and serving performance

[Test your independent assignment](../../curriculum/assignments/09a.md)

| ID | Question | Answer |
|---|---|---|
| 09a-E1 | Return GiB for parameters and bits; require positive values. | [Worked solution](../../curriculum/answers/09a.md#09a-e1) |
| 09a-E2 | Return bytes for layers, kv_heads, head_dim, tokens, batch=1, bytes_per_value=2. | [Worked solution](../../curriculum/answers/09a.md#09a-e2) |
| 09a-E3 | Return nearest-rank percentile p in (0,1] of nonempty values. | [Worked solution](../../curriculum/answers/09a.md#09a-e3) |
| 09a-O1 | Why does concurrency consume memory? | [Worked solution](../../curriculum/answers/09a.md#09a-o1) |
| 09a-O2 | Is quantization always faster? | [Worked solution](../../curriculum/answers/09a.md#09a-o2) |
| 09a-T | Create a hardware budget for 1B, 7B, and 14B models at 4/8/16 bits and multiple context lengths. Measure your actual machine before buying hardware or choosing a deployment target. | [Worked solution](../../curriculum/answers/09a.md#09a-t) |

### 09b: Local model API contracts

[Test your independent assignment](../../curriculum/assignments/09b.md)

| ID | Question | Answer |
|---|---|---|
| 09b-E1 | Return a native chat payload with model, one user message, stream=False, and options.num_predict=max_tokens. Require 1..1024 tokens and nonempty prompt <=4000 characters. | [Worked solution](../../curriculum/answers/09b.md#09b-e1) |
| 09b-E2 | Extract message.content as a string from a native Ollama response; malformed responses raise ValueError. | [Worked solution](../../curriculum/answers/09b.md#09b-e2) |
| 09b-E3 | Return tokens/second from token counts and total elapsed wall seconds; reject nonpositive elapsed. | [Worked solution](../../curriculum/answers/09b.md#09b-e3) |
| 09b-O1 | What does an offline adapter test prove? | [Worked solution](../../curriculum/answers/09b.md#09b-o1) |
| 09b-O2 | Why cap output tokens? | [Worked solution](../../curriculum/answers/09b.md#09b-o2) |
| 09b-T | Run projects/stage09/serve.py against an installed model. Save at least 30 warm and cold observations, output lengths, failures, p50/p95, and machine details. Repeat on vLLM only on compatible hardware. | [Worked solution](../../curriculum/answers/09b.md#09b-t) |

## Project tasks, in brief order

<a id="09-p1"></a>
### 09-P1

**Question:** Estimate weights and KV cache for three sizes/precisions/context lengths, then compare to actual memory.

**Answer:** [09a worked implementation and explanation](../../curriculum/answers/09a.md#09a-t)

<a id="09-p2"></a>
### 09-P2

**Question:** Install a compatible local server and select a licensed model that fits; record exact model ID/revision.

**Answer:** [09b worked implementation and explanation](../../curriculum/answers/09b.md#09b-t)

<a id="09-p3"></a>
### 09-P3

**Question:** Run native Ollama requests and, on supported hardware, vLLM-compatible requests.

**Answer:** [09b worked implementation and explanation](../../curriculum/answers/09b.md#09b-t)

<a id="09-p4"></a>
### 09-P4

**Question:** Measure 30+ warm/cold observations and concurrency levels with prompt/output lengths, p50/p95, failures, and resource use.

**Answer:** [09b worked implementation and explanation](../../curriculum/answers/09b.md#09b-t)

<a id="09-p5"></a>
### 09-P5

**Question:** Connect the Stage 07 assistant to the local endpoint and verify data does not leave the intended host.

**Answer:** [07b worked implementation and explanation](../../curriculum/answers/07b.md#07b-t) · [09b worked implementation and explanation](../../curriculum/answers/09b.md#09b-t)

<a id="09-g"></a>
## Mastery gate: 09-G

**Task:** Explain a measured bottleneck, enforce timeouts/output bounds, demonstrate model-unavailable failure, and justify a hardware/precision choice from evidence.

**Expected reasoning and invariant outputs:** Use an actually installed model ID; the command intentionally does not guess one or download it. serve.py measures sequential non-streaming end-to-end latency and server-reported token counts. It does not measure TTFT or continuous batching by itself. Add streaming instrumentation for TTFT and bounded concurrent clients for throughput. A 7B FP16 weight estimate is roughly 13.04 GiB before runtime/KV overhead. vLLM must run on a supported host, not assumed to work on every Mac.

Use the question-specific implementations above and [the reviewer answers](../../curriculum/assessments/ANSWERS.md). For deployment or model experiments, use [the worked operational procedures](../../curriculum/answers/OPERATIONS.md).

**Pass criteria:** 80/100 across correctness/reasoning (40), independent implementation (25), tests/debugging (20), and explanation/reproducibility (15). No permission leak, future-data leakage, invented evidence, or unreproducible core result. Live requirements remain pending until actually run. Running the answer files does not establish your independent mastery.

**If the gate fails:** If the model will not load, verify model ID, server logs, compatible backend, memory estimate, and context size before changing application code.
