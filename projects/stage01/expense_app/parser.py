from projects.stage01.solution import load_expenses

class CsvRepository:
    def __init__(self, path): self.path = path
    def read(self): return load_expenses(self.path)
