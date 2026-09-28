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

import torch
from torch import nn
torch.manual_seed(42)
torch.set_num_threads(1)
sequence = torch.tensor([1, 2, 3, 4])
print(sequence[:-1], sequence[1:])

# 06b-E1: Shifted examples

def shifted(sequence):
    if sequence.ndim != 1 or len(sequence) < 2: raise ValueError("Need a token sequence")
    return sequence[:-1], sequence[1:]

x, y = shifted(torch.tensor([3, 1, 4]))
assert x.tolist() == [3, 1] and y.tolist() == [1, 4]

print("06b-E1: checks passed")

# 06b-E2: Future mask

def causal_mask(n):
    return torch.triu(torch.ones(n, n, dtype=torch.bool), diagonal=1)

mask = causal_mask(3)
assert mask.tolist() == [[False, True, True], [False, False, True], [False, False, False]]

print("06b-E2: checks passed")

# 06b-E3: Transformer block

class TinyBlock(nn.Module):
    def __init__(self, d=8):
        super().__init__()
        self.attn = nn.MultiheadAttention(d, 2, batch_first=True)
        self.norm = nn.LayerNorm(d)
    def forward(self, x):
        out, _ = self.attn(x, x, x, attn_mask=causal_mask(x.shape[1]).to(x.device), need_weights=False)
        return self.norm(x+out)

block = TinyBlock().eval()
x = torch.randn(1, 4, 8)
changed = x.clone(); changed[:, 3] += 10
assert block(x).shape == x.shape
assert torch.allclose(block(x)[:, :3], block(changed)[:, :3], atol=1e-6)

print("06b-E3: checks passed")
