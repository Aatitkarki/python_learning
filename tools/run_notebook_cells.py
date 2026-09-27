"""Fresh-process runner for ordinary Python notebook cells (no IPython magic)."""
import json
import sys
from pathlib import Path
path=Path(sys.argv[1])
namespace={'__name__':'__notebook__'}
for index,cell in enumerate(json.loads(path.read_text())['cells']):
    if cell['cell_type']=='code':
        source=cell['source']; source=''.join(source) if isinstance(source,list) else source
        exec(compile(source,f'{path.name}:cell{index}','exec'),namespace)
