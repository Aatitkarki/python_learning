import hashlib
import json
import platform
from pathlib import Path

def manifest(path):
    path = Path(path)
    return {'python': platform.python_version(), 'file': path.name,
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'seed': 42}

if __name__ == '__main__':
    print(json.dumps(manifest('datasets/expenses.csv'), indent=2))
