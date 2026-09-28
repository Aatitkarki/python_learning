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
x = torch.tensor(3., requires_grad=True)
(x*x).backward()
print(x.grad)

# 05b-E1: Gradient with autograd

def squared_gradient(values):
    x = torch.tensor(values, dtype=torch.float32, requires_grad=True)
    (x*x).sum().backward()
    return x.grad

assert torch.allclose(squared_gradient([1, -2]), torch.tensor([2., -4.]))

print("05b-E1: checks passed")

# 05b-E2: CNN shape

def make_cnn():
    return nn.Sequential(nn.Conv2d(1, 4, 3, padding=1), nn.ReLU(), nn.Flatten(), nn.Linear(4*8*8, 10))

assert make_cnn()(torch.zeros(2, 1, 8, 8)).shape == (2, 10)

print("05b-E2: checks passed")

# 05b-E3: One update

def train_step(model, optimizer, x, y):
    model.train()
    optimizer.zero_grad()
    loss = nn.functional.cross_entropy(model(x), y)
    loss.backward()
    optimizer.step()
    return loss.item()

model = make_cnn()
optimizer = torch.optim.AdamW(model.parameters(), lr=.01)
x, y = torch.randn(4, 1, 8, 8), torch.tensor([0, 1, 2, 3])
before = model[-1].weight.detach().clone()
assert train_step(model, optimizer, x, y) > 0
assert not torch.equal(before, model[-1].weight)

print("05b-E3: checks passed")
