"""Your 06b independent assignment. Contract: curriculum/assignments/06b.md
Run: python tools/test_assignment.py 06b --solution PATH_TO_THIS_FILE
Keep your work in work/; this template may be regenerated.
"""

import torch
from torch import nn

class CachedLM(nn.Module):

    def __init__(self, vocab, blocks=2, width=24, context=128):
        raise NotImplementedError('Write your implementation here')

    def forward(self, ids, cache=None):
        raise NotImplementedError('Write your implementation here')
