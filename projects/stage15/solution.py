"""Capstone smoke demo: two companies, three periods, verified numeric outputs."""
import json
import tempfile
from pathlib import Path
from projects.reference import Store

def run():
    with tempfile.TemporaryDirectory() as folder:
        store=Store(Path(folder)/'capstone.db'); store.seed()
        return store.compare('A',['Aurora','Beacon'],[2023,2024,2025])

if __name__=='__main__': print(json.dumps(run(),indent=2))
