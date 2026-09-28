# Stage 05 — worked project answer

<!-- question-answer-index -->
**Looking for a particular answer?** [Question-by-question solutions](SOLUTIONS.md) includes notebook exercises, explanations, independent assignments, and project tasks.


Read after saving your own attempt. The reference is one implementation, not the only acceptable design.

## Reference artifacts

- [numpy_xor.py](numpy_xor.py)
- [solution.py](solution.py)

## Expected behavior and reasoning

Also run python -m projects.stage05.numpy_xor. XOR loss should become very small and gradient error below 1e-6. The CNN uses 8×8 grayscale images with a held-out test split, eval mode, and no_grad. Record observed accuracy rather than copying a target. CrossEntropyLoss expects logits. Missing zero_grad accumulates gradients; missing step leaves weights unchanged; evaluating with dropout active adds avoidable variation.

## How to review your work

Compare the input/output contract first, then edge behavior, data boundaries, and failure modes. Different implementation details are acceptable when you can explain them and demonstrate the same or stronger guarantees. Record actual observed model/latency results instead of treating example scores as universal answers.

## Transfer and extension answer key

The [extra lab answer guide](../../curriculum/EXTRA_LABS.md) supplies derivations, query examples, algorithms, and design answers for the larger extensions. The corresponding solved notebooks answer each checked exercise and each oral question:

- [05a practice](../../curriculum/notebooks/05a_a_neural_network_from_scratch.ipynb) · [worked answers](../../curriculum/solutions/05a_a_neural_network_from_scratch.ipynb)
- [05b practice](../../curriculum/notebooks/05b_pytorch_training_and_image_classification.ipynb) · [worked answers](../../curriculum/solutions/05b_pytorch_training_and_image_classification.ipynb)

## Common wrong answer

A runnable happy path alone does not satisfy the project. A missing dependency or unavailable external service is pending evidence; a mock is useful for unit testing but does not prove the actual integration. Copying the reference does not pass the independent gate.
