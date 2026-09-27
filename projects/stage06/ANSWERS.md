# Stage 06 — worked project answer

Read after saving your own attempt. The reference is one implementation, not the only acceptable design.

## Reference artifacts

- [pretrained.py](pretrained.py)
- [tiny_lm.py](tiny_lm.py)

## Expected behavior and reasoning

Targets are shifted by one position, and text is split before overlapping windows. A causal-mask test must modify future inputs, not merely inspect tensor dimensions. The repeating corpus teaches mechanics and cannot establish broad language capability. pretrained.py --offline-smoke tests a real PEFT adapter without downloaded weights; it is distinct from the pretrained lab. Extraction of “100 billion” requires multiplication by 1e9 and evidence containing the unit. Quantization saves weight storage but may not improve latency.

## How to review your work

Compare the input/output contract first, then edge behavior, data boundaries, and failure modes. Different implementation details are acceptable when you can explain them and demonstrate the same or stronger guarantees. Record actual observed model/latency results instead of treating example scores as universal answers.

## Transfer and extension answer key

The [extra lab answer guide](../../curriculum/EXTRA_LABS.md) supplies derivations, query examples, algorithms, and design answers for the larger extensions. The corresponding solved notebooks answer each checked exercise and each oral question:

- [06a practice](../../curriculum/notebooks/06a_tokens_attention_and_decoding.ipynb) · [worked answers](../../curriculum/solutions/06a_tokens_attention_and_decoding.ipynb)
- [06b practice](../../curriculum/notebooks/06b_a_tiny_causal_transformer.ipynb) · [worked answers](../../curriculum/solutions/06b_a_tiny_causal_transformer.ipynb)
- [06c practice](../../curriculum/notebooks/06c_adaptation_extraction_and_quantization.ipynb) · [worked answers](../../curriculum/solutions/06c_adaptation_extraction_and_quantization.ipynb)

## Common wrong answer

A runnable happy path alone does not satisfy the project. A missing dependency or unavailable external service is pending evidence; a mock is useful for unit testing but does not prove the actual integration. Copying the reference does not pass the independent gate.
