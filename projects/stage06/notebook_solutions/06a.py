"""Generated worked answers; edit your own version under work/."""

from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
def expect_error(error_type, operation):
    try:
        operation()
    except error_type:
        return
    raise AssertionError(f"Expected {error_type.__name__}")


# Worked example

import numpy as np
scores = np.array([1., 2., 3.])
p = np.exp(scores-scores.max())
print(p/p.sum())

# 06a-E1: Character tokenizer

def tokenize(text):
    vocabulary = sorted(set(text))
    encode = {char: i for i, char in enumerate(vocabulary)}
    ids = [encode[char] for char in text]
    return ids, encode, "".join(vocabulary[i] for i in ids)

ids, vocab, decoded = tokenize("banana")
assert decoded == "banana" and len(vocab) == 3

print("06a-E1: checks passed")

# 06a-E2: Causal attention

def attention(q, k, v):
    scores = q@k.T/np.sqrt(q.shape[-1])
    scores = np.where(np.triu(np.ones(scores.shape), 1).astype(bool), -np.inf, scores)
    weights = np.exp(scores-scores.max(axis=-1, keepdims=True))
    weights /= weights.sum(axis=-1, keepdims=True)
    return weights@v, weights

out, weights = attention(np.eye(3), np.eye(3), np.eye(3))
assert np.allclose(weights.sum(axis=1), 1)
assert np.allclose(np.triu(weights, 1), 0)
assert np.allclose(out[0], [1, 0, 0])

print("06a-E2: checks passed")

# 06a-E3: Temperature distribution

def distribution(logits, temperature=1.):
    if temperature <= 0: raise ValueError("Temperature must be positive")
    values = np.asarray(logits)/temperature
    p = np.exp(values-values.max())
    return p/p.sum()

assert distribution([0, 1], .1)[1] > distribution([0, 1], 2)[1]
expect_error(ValueError, lambda: distribution([1, 2], 0))

print("06a-E3: checks passed")
