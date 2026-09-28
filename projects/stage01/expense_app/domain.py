from projects.stage01.solution import summarize

class ExpenseAnalyzer:
    def __init__(self, repository): self.repository = repository
    def report(self): return summarize(self.repository.read())
