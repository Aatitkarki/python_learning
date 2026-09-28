"""Your 08b independent assignment. Contract: curriculum/assignments/08b.md
Run: python tools/test_assignment.py 08b --solution PATH_TO_THIS_FILE
Keep your work in work/; this template may be regenerated.
"""

def build():
    raise NotImplementedError('Write your implementation here')

def fingerprint(state):
    raise NotImplementedError('Write your implementation here')

class ReviewStore:

    def __init__(self, path):
        raise NotImplementedError('Write your implementation here')

    def propose(self, run_id, actor, proposal, now=None, ttl=300):
        raise NotImplementedError('Write your implementation here')

    def resume(self, run_id, actor, fingerprint, approved, execute, now=None):
        raise NotImplementedError('Write your implementation here')
