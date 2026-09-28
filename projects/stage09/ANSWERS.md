# Stage 09 — worked project answer

<!-- question-answer-index -->
**Looking for a particular answer?** [Question-by-question solutions](SOLUTIONS.md) includes notebook exercises, explanations, independent assignments, and project tasks.


Read after saving your own attempt. The reference is one implementation, not the only acceptable design.

## Reference artifacts

- [Actual model-server client and benchmark](serve.py)

## Expected behavior and reasoning

Use an actually installed model ID; the command intentionally does not guess one or download it. serve.py measures sequential non-streaming end-to-end latency and server-reported token counts. It does not measure TTFT or continuous batching by itself. Add streaming instrumentation for TTFT and bounded concurrent clients for throughput. A 7B FP16 weight estimate is roughly 13.04 GiB before runtime/KV overhead. vLLM must run on a supported host, not assumed to work on every Mac.

## How to review your work

Compare the input/output contract first, then edge behavior, data boundaries, and failure modes. Different implementation details are acceptable when you can explain them and demonstrate the same or stronger guarantees. Record actual observed model/latency results instead of treating example scores as universal answers.

## Transfer and extension answer key

The [extra lab answer guide](../../curriculum/EXTRA_LABS.md) supplies derivations, query examples, algorithms, and design answers for the larger extensions. The corresponding solved notebooks answer each checked exercise and each oral question:

- [09a practice](../../curriculum/notebooks/09a_memory_and_serving_performance.ipynb) · [worked answers](../../curriculum/solutions/09a_memory_and_serving_performance.ipynb)
- [09b practice](../../curriculum/notebooks/09b_local_model_api_contracts.ipynb) · [worked answers](../../curriculum/solutions/09b_local_model_api_contracts.ipynb)

## Common wrong answer

A runnable happy path alone does not satisfy the project. A missing dependency or unavailable external service is pending evidence; a mock is useful for unit testing but does not prove the actual integration. Copying the reference does not pass the independent gate.
