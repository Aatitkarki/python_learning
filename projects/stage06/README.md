# Stage 06 project — Tiny language model, pretrained classifier, and extraction

[Stage study guide](../../curriculum/stages/06.md) · [Course plan](../../curriculum/PLAN.md)

**Scenario:** You own a small component of a private research platform. A teammate must be able to reproduce it, inspect its evidence, and understand its failure behavior.

## Your assignment

1. Implement and visualize causal attention; perturb a future token and prove earlier outputs do not change.
2. Train the tiny transformer on the bundled corpus; log held-out loss and inspect generated text.
3. Run pretrained.py with an explicitly selected model and immutable revision; compare pre/post-adaptation validation and final test.
4. Build extraction with schema validation, exact source spans, currency/scale normalization, and unknown results for unsupported inputs.
5. Compare quantization reconstruction error and LoRA parameter count; document QLoRA hardware requirements and run it only on supported equipment.

## Acceptance criteria

Explain attention and KV cache, implement a causal block, debug target leakage, compare fine-tuning options, and validate a deliberately malformed or unsupported extraction.

Also require documented inputs/outputs, explicit units and limitations, tests for normal/boundary/error cases, and a fresh-process run. Use only data you have permission to use; the supplied fixtures are fictional. Do not report a synthetic-data score as real-world quality.

## Starter workflow

Create work/stage06/, write a short interface contract, and implement the smallest end-to-end slice first. Use the exercise stubs below for function signatures and visible checks. Add your own tests before consulting the reference.

- [06a practice](../../curriculum/notebooks/06a_tokens_attention_and_decoding.ipynb) · [worked answers](../../curriculum/solutions/06a_tokens_attention_and_decoding.ipynb)
- [06b practice](../../curriculum/notebooks/06b_a_tiny_causal_transformer.ipynb) · [worked answers](../../curriculum/solutions/06b_a_tiny_causal_transformer.ipynb)
- [06c practice](../../curriculum/notebooks/06c_adaptation_extraction_and_quantization.ipynb) · [worked answers](../../curriculum/solutions/06c_adaptation_extraction_and_quantization.ipynb)

## Run the reference after your attempt

From the repository root with the environment active:

```bash
python -m pip install -r requirements/deep.txt
python -m projects.stage06.tiny_lm
```

For model/service labs, read [INTEGRATIONS.md](../../curriculum/INTEGRATIONS.md) before running. Stage 10 additionally needs a local .env and a running Docker daemon. Output paths under work/ belong to you.

## Deliver

- Runnable code and tests with a setup README.
- A results report containing actual measurements and source/data versions.
- A failure you reproduced, diagnosed, and fixed.
- A short explanation of tradeoffs and remaining limits.
- Closed-book gate evidence and a scheduled review date.

[Worked answer and design reasoning](ANSWERS.md) · [Additional lab answers](../../curriculum/EXTRA_LABS.md)
