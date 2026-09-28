"""Detect omitted/stale questions, missing implementations, and broken answer anchors."""
import ast
import json
import sys
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'curriculum/authoring'))
import foundations, models, systems, advanced
from schema import LESSONS
from stages import STAGES

def expected_questions():
    result = {}
    for lesson in LESSONS:
        id = lesson['id']
        for number, exercise in enumerate(lesson['exercises'], 1):
            result[f'{id}-E{number}'] = ('exercise', exercise['task'])
        for number, (question, answer) in enumerate(lesson['oral'], 1):
            result[f'{id}-O{number}'] = ('oral', question)
        result[f'{id}-T'] = ('transfer', lesson['transfer'])
    for stage in STAGES:
        for number, question in enumerate(stage[5], 1):
            result[f'{stage[0]}-P{number}'] = ('project', question)
        result[f'{stage[0]}-G'] = ('gate', stage[8])
    return result

def check(records=None):
    if records is None:
        records = json.loads((ROOT / 'curriculum/answer_manifest.json').read_text())
    expected = expected_questions(); ids = [r['id'] for r in records]; errors = []
    if len(ids) != len(set(ids)): errors.append('Duplicate answer IDs')
    if set(ids) != set(expected): errors.append(f'Coverage mismatch: missing={set(expected)-set(ids)}, extra={set(ids)-set(expected)}')
    for record in records:
        id = record['id']
        if expected.get(id) != (record['kind'], record['question']): errors.append(f'{id}: stale question/kind')
        path, _, anchor = record['answer'].partition('#'); file = ROOT / path
        if not file.is_file(): errors.append(f'{id}: missing answer {path}'); continue
        text = file.read_text()
        marker = f'<a id="{anchor}"></a>'
        if not anchor or marker not in text: errors.append(f'{id}: missing explicit anchor'); continue
        section = text.split(marker, 1)[1].split('<a id=', 1)[0]
        if record['question'] not in section: errors.append(f'{id}: original question missing from answer section')
        if record['kind'] in ('exercise','transfer','project') and not record['implementations']:
            errors.append(f'{id}: no implementation')
        for implementation in record['implementations']:
            target = ROOT / implementation
            if not target.is_file(): errors.append(f'{id}: missing implementation {implementation}')
    for lesson in LESSONS:
        script = ROOT / f'projects/stage{lesson["id"][:2]}/notebook_solutions/{lesson["id"]}.py'
        if not script.exists(): errors.append(f'Missing script {script}'); continue
        text = script.read_text()
        try: ast.parse(text)
        except SyntaxError as exc: errors.append(f'{script}: {exc}')
        for exercise in lesson['exercises']:
            if exercise['answer'] not in text or exercise['checks'] not in text:
                errors.append(f'{lesson["id"]}: script missing exact authored answer/checks')
    if errors: raise ValueError('\n'.join(errors))
    return {'answers':len(records), 'counts':dict(Counter(r['kind'] for r in records)), 'status':'passed'}

if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
