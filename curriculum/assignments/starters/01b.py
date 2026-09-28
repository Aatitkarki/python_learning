"""Your 01b independent assignment. Contract: curriculum/assignments/01b.md
Run: python tools/test_assignment.py 01b --solution PATH_TO_THIS_FILE
Keep your work in work/; this template may be regenerated.
"""

class ContactBook:

    def __init__(self):
        raise NotImplementedError('Write your implementation here')

    @staticmethod
    def key(email):
        raise NotImplementedError('Write your implementation here')

    def add(self, email, name, phone=''):
        raise NotImplementedError('Write your implementation here')

    def update(self, email, *, name=None, phone=None):
        raise NotImplementedError('Write your implementation here')

    def search(self, query):
        raise NotImplementedError('Write your implementation here')

    def delete(self, email):
        raise NotImplementedError('Write your implementation here')

    def save(self, path):
        raise NotImplementedError('Write your implementation here')

    @classmethod
    def load(cls, path):
        raise NotImplementedError('Write your implementation here')

def analyze(text, limit=5):
    raise NotImplementedError('Write your implementation here')
