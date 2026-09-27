"""Check local Markdown links in guides and notebook Markdown cells."""
import json
import re
from pathlib import Path
from urllib.parse import unquote
ROOT=Path(__file__).resolve().parents[1]
paths=[ROOT/'START_HERE.md',ROOT/'readme.md',ROOT/'progress.md',*ROOT.glob('curriculum/**/*.md'),*ROOT.glob('projects/**/*.md'),*ROOT.glob('datasets/*.md'),*ROOT.glob('curriculum/**/*.ipynb')]
errors=[]; checked=0
for path in paths:
    if path.suffix=='.ipynb':
        data=json.loads(path.read_text())
        text='\n'.join(''.join(c['source']) if isinstance(c['source'],list) else c['source'] for c in data['cells'] if c['cell_type']=='markdown')
    else: text=path.read_text()
    for target in re.findall(r'\]\(([^)]+)\)',text):
        if '://' in target or target.startswith(('#','mailto:')): continue
        target=unquote(target.split('#')[0].strip('<>'))
        checked+=1
        if not (path.parent/target).exists(): errors.append(f'{path.relative_to(ROOT)} -> {target}')
for error in errors: print(error)
print(f'Checked {checked} local links; {len(errors)} missing targets.')
raise SystemExit(bool(errors))
