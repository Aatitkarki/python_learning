"""Validate all enriched notebooks and independent assignment navigation."""
import ast
import hashlib
import json
from pathlib import Path
import re
import sys
import nbformat
ROOT=Path(__file__).resolve().parents[1]

def main():
    lessons=json.loads((ROOT/'curriculum/manifest.json').read_text())
    assignments=json.loads((ROOT/'curriculum/assignment_manifest.json').read_text())
    assert {r['id'] for r in assignments}=={r['id'] for r in lessons}
    local_links=0
    for lesson in lessons:
        for kind in ['practice','solution']:
            path=ROOT/lesson[kind];notebook=nbformat.read(path,as_version=4);nbformat.validate(notebook)
            supplements=[c for c in notebook.cells if c.metadata.get('course_supplement')]
            assert {c.metadata.course_supplement.kind for c in supplements}=={'concepts','assignment-tests'}
            assert len(supplements)==2
            for cell in supplements:
                assert hashlib.sha256(cell.source.encode()).hexdigest()==cell.metadata.course_supplement.source_sha256
                for target in re.findall(r'\[[^\]]*\]\(([^\)]+)\)',cell.source):
                    if '://' in target or target.startswith('#'):continue
                    assert (path.parent/target.split('#')[0]).exists(),f'{path}: {target}'
                    local_links+=1
    for item in assignments:
        for key in ['tests','starter','reference','guide']:assert (ROOT/item[key]).is_file()
        for key in ['tests','starter','reference']:ast.parse((ROOT/item[key]).read_text())
        assert item['evidence'] and item['test_functions']
    print(f'Validated {len(lessons)*2} enriched notebooks, {len(assignments)} assignment packs, and {local_links} embedded local links.')

if __name__=='__main__':main()
