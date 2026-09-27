"""Deterministic retrieval baseline, with authorization before scoring."""
import json
import tempfile
from pathlib import Path
from projects.reference import Store, evidence_answer

def run():
    with tempfile.TemporaryDirectory() as folder:
        store=Store(Path(folder)/'research.db'); store.seed()
        return evidence_answer(store,'A','Aurora 2025 revenue')

if __name__=='__main__': print(json.dumps(run(),indent=2))
