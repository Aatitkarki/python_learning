"""Guard the learner-file boundary and additive notebook enrichment."""
import ast
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from enrich_notebooks import enriched

def test_enrichment_keeps_existing_answers_outputs_and_metadata():
    original={'nbformat':4,'nbformat_minor':5,'metadata':{'personal_note':'keep'},'cells':[
        {'cell_type':'markdown','id':'intro','metadata':{},'source':'My custom introduction'},
        {'cell_type':'code','id':'my-answer','metadata':{'learner':True},'source':'answer = 42','execution_count':9,'outputs':[{'output_type':'stream','name':'stdout','text':'my result'}]},
        {'cell_type':'markdown','id':'lesson','metadata':{},'source':'## Lesson\nMy own note'},
        {'cell_type':'markdown','id':'transfer','metadata':{},'source':'## Independent transfer\nMy plan'}]}
    before=copy.deepcopy(original);updated=enriched(original,'01a','curriculum/notebooks/example.ipynb')
    assert original==before
    assert [c for c in updated['cells'] if not c['metadata'].get('course_supplement')]==before['cells']
    assert updated['metadata']==before['metadata']
    assert enriched(updated,'01a','curriculum/notebooks/example.ipynb')==updated

def test_enrichment_refuses_to_overwrite_edited_supplement():
    original={'cells':[{'cell_type':'markdown','metadata':{},'source':'## Independent transfer\nTask'}]}
    updated=enriched(original,'01a','curriculum/notebooks/example.ipynb')
    next(c for c in updated['cells'] if c['metadata'].get('course_supplement'))['source']+='\nMy handwritten note'
    with pytest.raises(ValueError,match='was edited'):enriched(updated,'01a','curriculum/notebooks/example.ipynb')

def test_every_transfer_has_tests_starter_concepts_and_evidence():
    lessons=json.loads((ROOT/'curriculum/manifest.json').read_text())
    assignments=json.loads((ROOT/'curriculum/assignment_manifest.json').read_text())
    assert {r['id'] for r in assignments}=={r['id'] for r in lessons}
    for row in assignments:
        for key in ['tests','starter','reference','guide']:assert (ROOT/row[key]).is_file()
        assert row['test_functions'] and row['evidence']
        source=(ROOT/row['starter']).read_text();ast.parse(source)
        assert 'NotImplementedError' in source and 'from projects.' not in source
        assert (ROOT/f'curriculum/concepts/{row["id"]}.md').stat().st_size>1000

def test_default_runner_does_not_fall_back_to_reference(tmp_path):
    result=subprocess.run([sys.executable,str(ROOT/'tools/test_assignment.py'),'01a','--solution',str(tmp_path/'missing.py')],capture_output=True,text=True)
    assert result.returncode!=0 and 'No learner solution' in result.stderr
    assert 'Testing REFERENCE' not in result.stdout

def test_runner_really_executes_chosen_learner_file(tmp_path):
    target=tmp_path/'my_hello.py'
    target.write_text('import sys\ndef main():\n    print("Hello from MY file",sys.executable,1200)\n')
    command=[sys.executable,str(ROOT/'tools/test_assignment.py'),'00a','--solution',str(target)]
    success=subprocess.run(command,capture_output=True,text=True)
    assert success.returncode==0 and 'Testing YOUR solution' in success.stdout
    # The wrong implementation must fail; a hidden reference fallback would still pass.
    target.write_text('def main():\n    print("WRONG learner implementation")\n')
    failed=subprocess.run(command,capture_output=True,text=True)
    assert failed.returncode!=0 and 'FAILED' in failed.stdout
