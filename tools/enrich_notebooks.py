"""Insert teaching/test markdown while preserving every existing learner cell.
No executable cells are replaced, re-run, cleared, or renumbered. Work notebooks
are deliberately excluded; current course notebooks receive backed-up additions.
"""
import copy
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
from notebook_supplements import ROOT,concept_cell,assignment_cell

def source(cell):
    value=cell.get('source','');return ''.join(value) if isinstance(value,list) else value

def enriched(original,id,path):
    result=copy.deepcopy(original);existing=result['cells'];managed={}
    for cell in existing:
        tag=cell.get('metadata',{}).get('course_supplement')
        if tag:
            if hashlib.sha256(source(cell).encode()).hexdigest()!=tag['source_sha256']:
                raise ValueError(f'{path}: a supplementary cell was edited; preserve/reconcile it manually before updating')
            if tag['kind'] in managed:raise ValueError(f'{path}: duplicate supplementary cells')
            managed[tag['kind']]=cell
    ordinary=[cell for cell in existing if not cell.get('metadata',{}).get('course_supplement')]
    intro=concept_cell(id,path);tests=assignment_cell(id)
    # Put prerequisite explanations before the original lesson and worked example.
    index=next((i for i,c in enumerate(ordinary) if c['cell_type']=='markdown' and source(c).startswith('## Lesson')),2)
    ordinary.insert(index,intro)
    # Keep the full original transfer prompt untouched; add its test guidance next.
    transfer=next((i for i,c in enumerate(ordinary) if c['cell_type']=='markdown' and source(c).startswith('## Independent transfer')),None)
    if transfer is None:raise ValueError(f'{path}: transfer prompt not found')
    ordinary.insert(transfer+1,tests);result['cells']=ordinary
    return result

def main():
    manifest=json.loads((ROOT/'curriculum/manifest.json').read_text());pending=[]
    # Validate all inputs before writing anything.
    for item in manifest:
        for kind in ['practice','solution']:
            relative=item[kind];path=ROOT/relative;original_bytes=path.read_bytes();original=json.loads(original_bytes)
            updated=enriched(original,item['id'],relative)
            if updated!=original:pending.append((relative,path,updated,original_bytes))
    backup=ROOT/'work/backups/notebook-enrichment'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    for relative,path,updated,original_bytes in pending:
        if path.read_bytes()!=original_bytes:
            raise RuntimeError(f'{relative} changed during enrichment; leaving that file untouched. Rerun after saving your editor.')
        target=backup/relative;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(original_bytes)
        path.write_text(json.dumps(updated,indent=1,ensure_ascii=False)+'\n',encoding='utf-8')
    print(f'Enriched {len(pending)} notebooks; all original cells/outputs preserved.')
    if pending:print('Original-file backups:',backup.relative_to(ROOT))

if __name__=='__main__':main()
