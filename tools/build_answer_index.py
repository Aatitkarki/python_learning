"""Build reference answers only. Never rewrite practice notebooks or learner work."""
import json
import os
import sys
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'curriculum/authoring'))
import foundations, models, systems, advanced  # register authored lessons
from schema import LESSONS
from stages import STAGES
from answer_catalog import TRANSFERS, PROJECT_MAP

SETUP = '''from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
def expect_error(error_type, operation):
    try:
        operation()
    except error_type:
        return
    raise AssertionError(f"Expected {error_type.__name__}")
'''

def link(label, target, source):
    path, _, anchor = str(target).partition('#')
    relative = Path(os.path.relpath(ROOT / path, (ROOT / source).parent)).as_posix()
    return f'[{label}]({relative}' + (f'#{anchor}' if anchor else '') + ')'

def add_banner(path, target):
    """Idempotent insertion preserving all existing prose below the title."""
    text = path.read_text()
    marker = '<!-- question-answer-index -->'
    if marker in text:
        return
    head, sep, body = text.partition('\n')
    banner = marker + '\n**Looking for a particular answer?** ' + link('Question-by-question solutions', target, path.relative_to(ROOT)) + ' includes notebook exercises, explanations, independent assignments, and project tasks.\n'
    path.write_text(head + '\n\n' + banner + sep + body)

def main():
    assert set(TRANSFERS) == {x['id'] for x in LESSONS}, 'Missing transfer answer'
    manifest = {x['id']: x for x in json.loads((ROOT / 'curriculum/manifest.json').read_text())}
    records = []
    def record(id, kind, stage, question, answer, implementations=()):
        records.append(dict(id=id, kind=kind, stage=stage, question=question,
                            answer=answer, implementations=list(implementations)))
    for item in LESSONS:
        id = item['id']; stage = id[:2]
        doc = f'curriculum/answers/{id}.md'
        script = f'projects/stage{stage}/notebook_solutions/{id}.py'
        lines = [f'# {id} — {item["title"]}: all answers', '',
                 link('Stage answer map', f'projects/stage{stage}/SOLUTIONS.md', doc) + ' · ' + link('Original solution notebook', manifest[id]['solution'], doc), '',
                 link('Independent assignment tests', f'curriculum/assignments/{id}.md', doc) + ' · ' + link('Beginner concept explanation', f'curriculum/concepts/{id}.md', doc), '',
                 'Attempt the question first. Each exercise below includes its exact brief, code, checks, and reasoning. The independent assignment has its own implementation after the notebook answers.', '',
                 '**Run all notebook examples and checks as a script:**', '', f'```bash\npython {script}\n```', '',
                 '**Environment:** `' + item['group'] + '`; use the requirements listed in the stage guide. Run commands from the repository root.', '',
                 '## Setup and worked example', '', 'The exercise code may use the imports or variables in this example. The downloadable script also defines `ROOT` and `expect_error`.', '',
                 '```python\n' + item['example'] + '\n```', '']
        program = ['"""Generated worked answers; edit your own version under work/."""', SETUP,
                   '# Worked example', item['example']]
        for number, exercise in enumerate(item['exercises'], 1):
            key = f'{id}-E{number}'; anchor = key.lower()
            lines += [f'<a id="{anchor}"></a>', f'## {key}: {exercise["title"]}', '',
                      '**Question:** ' + exercise['task'], '', '**Answer:**', '',
                      '```python\n' + exercise['answer'] + '\n```', '',
                      '**Checks:**', '', '```python\n' + exercise['checks'] + '\n```', '',
                      '**Why it works:** ' + exercise['why'], '']
            program += [f'# {key}: {exercise["title"]}', exercise['answer'], exercise['checks'], f'print("{key}: checks passed")']
            record(key, 'exercise', stage, exercise['task'], doc + '#' + anchor, [script])
        for number, (question, answer) in enumerate(item['oral'], 1):
            key = f'{id}-O{number}'; anchor = key.lower()
            lines += [f'<a id="{anchor}"></a>', f'## {key}: Explain without code', '', '**Question:** ' + question, '', '**Answer:** ' + answer, '']
            record(key, 'oral', stage, question, doc + '#' + anchor)
        files, commands, explanation = TRANSFERS[id]
        key = id + '-T'; anchor = key.lower()
        lines += [f'<a id="{anchor}"></a>', f'## {key}: Independent assignment', '', '**Question:** ' + item['transfer'], '',
                  '**Test your own work:** ' + link('Interface, starter, and acceptance tests', f'curriculum/assignments/{id}.md', doc), '', '**Worked answer:** ' + explanation, '', '**Implementation and supporting procedures:**', '']
        lines += ['- ' + link(path, path, doc) for path in files]
        lines += ['', '**Run / verify:**', '', '```bash\n' + '\n'.join(commands) + '\n```', '',
                  'Outputs from the extra labs normally go to `work/reference_answers/`. Service-dependent commands require the setup in ' + link('the operational answers', 'curriculum/answers/OPERATIONS.md', doc) + '. Do not mark a live lab passed just because the offline reference runs.', '']
        record(key, 'transfer', stage, item['transfer'], doc + '#' + anchor, files)
        (ROOT / doc).parent.mkdir(parents=True, exist_ok=True)
        (ROOT / doc).write_text('\n'.join(lines))
        (ROOT / script).parent.mkdir(parents=True, exist_ok=True)
        (ROOT / script).write_text('\n\n'.join(program) + '\n')
    for stage, title, hours, project, topics, tasks, command, answer, gate, remediation in STAGES:
        assert len(PROJECT_MAP[stage]) == len(tasks), f'Unmapped project task in {stage}'
        doc = f'projects/stage{stage}/SOLUTIONS.md'
        lines = [f'# Stage {stage}: question-by-question solutions', '',
                 link('All-stage answer index', 'curriculum/ANSWER_INDEX.md', doc) + ' · ' + link('Project brief', f'projects/stage{stage}/README.md', doc), '',
                 '`solution.py` is the main project reference. It does not contain every answer. Use the exact question IDs below to find the smaller exercises and extra programs.', '',
                 '**Suggested workflow:** notebook → independent assignment in your own `.py` files → stage project → closed-book gate. Compare answers only after an attempt; then close them and rebuild with changed input.', '',
                 '## Notebook questions and independent assignments', '']
        for item in [x for x in LESSONS if x['id'].startswith(stage)]:
            lines += [f'### {item["id"]}: {item["title"]}', '', link('Test your independent assignment', f'curriculum/assignments/{item["id"]}.md', doc), '', '| ID | Question | Answer |', '|---|---|---|']
            for entry in [r for r in records if r['id'].startswith(item['id']+'-')]:
                question = entry['question'].replace('\n', ' ').replace('|', '\\|')
                lines.append(f'| {entry["id"]} | {question} | ' + link('Worked solution', entry['answer'], doc) + ' |')
            lines += ['']
        lines += ['## Project tasks, in brief order', '']
        for number, (question, ids) in enumerate(zip(tasks, PROJECT_MAP[stage]), 1):
            key = f'{stage}-P{number}'; anchor = key.lower()
            implementations = list(dict.fromkeys(path for id in ids for path in TRANSFERS[id][0]))
            lines += [f'<a id="{anchor}"></a>', f'### {key}', '', '**Question:** ' + question, '',
                      '**Answer:** ' + ' · '.join(link(id+' worked implementation and explanation', f'curriculum/answers/{id}.md#{id}-t', doc) for id in ids), '']
            record(key, 'project', stage, question, doc + '#' + anchor, implementations)
        key = stage + '-G'; anchor = key.lower()
        lines += [f'<a id="{anchor}"></a>', '## Mastery gate: ' + key, '', '**Task:** ' + gate, '',
                  '**Expected reasoning and invariant outputs:** ' + answer, '',
                  'Use the question-specific implementations above and ' + link('the reviewer answers', 'curriculum/assessments/ANSWERS.md', doc) + '. For deployment or model experiments, use ' + link('the worked operational procedures', 'curriculum/answers/OPERATIONS.md', doc) + '.', '',
                  '**Pass criteria:** 80/100 across correctness/reasoning (40), independent implementation (25), tests/debugging (20), and explanation/reproducibility (15). No permission leak, future-data leakage, invented evidence, or unreproducible core result. Live requirements remain pending until actually run. Running the answer files does not establish your independent mastery.', '',
                  '**If the gate fails:** ' + remediation, '']
        record(key, 'gate', stage, gate, doc + '#' + anchor)
        (ROOT / doc).write_text('\n'.join(lines))
        for path in [f'projects/stage{stage}/README.md', f'projects/stage{stage}/ANSWERS.md', f'curriculum/stages/{stage}.md']:
            add_banner(ROOT/path, doc)
    counts = Counter(r['kind'] for r in records)
    doc = 'curriculum/ANSWER_INDEX.md'
    lines = ['# Find the answer to every curriculum question', '',
             'The main `projects/stageXX/solution.py` answers the stage project. **The separate files below also answer the smaller exercises and independent assignments.** Nothing in your practice notebooks or `work/` is regenerated by this answer update.', '',
             'For example, for Stage 01 open ' + link('Stage 01 SOLUTIONS.md', 'projects/stage01/SOLUTIONS.md', doc) + '. `01a-E1` is exercise 1, `01a-O1` is oral question 1, `01a-T` is the calculator assignment, `01-P1` is project task 1, and `01-G` is the mastery gate.', '',
             '**Study order:** complete a notebook; build its independent assignment in your own Python files; compare the matching answer; complete the stage project and closed-book gate before progressing. You should work both in notebooks and in ordinary Python files.', '',
             '**Coverage:** ' + ', '.join(f'{counts[k]} {label}' for k,label in [('exercise','notebook exercises'),('oral','oral questions'),('transfer','independent assignments'),('project','project tasks'),('gate','mastery gates')]) + '.', '',
             '| Stage | Questions and project answers |', '|---|---|']
    for s in STAGES:
        lines.append(f'| {s[0]} — {s[1]} | ' + link('Open complete stage answer map', f'projects/stage{s[0]}/SOLUTIONS.md', doc) + ' |')
    lines += ['', link('Run tests against your own assignments', 'curriculum/assignments/README.md', doc) + ' · ' + link('Start mathematics from the basics', 'curriculum/MATH_START_HERE.md', doc), '', '## What each answer includes', '',
              '- Notebook exercises: original question, working code, checks, and explanation; also exported as runnable `.py` files under each stage’s `notebook_solutions/`.',
              '- Independent assignments: separate implementation files, commands, expected behavior, and reasoning.',
              '- Project tasks: a numbered mapping to the relevant implementations, including additional labs beyond the original `solution.py`.',
              '- Hardware, servers, and deployment: ' + link('worked procedures and expected evidence', 'curriculum/answers/OPERATIONS.md', doc) + '; measured results depend on actually running your environment.',
              '- Final defense: ' + link('worked feature, design answers, failure diagnosis, and rubric', 'curriculum/answers/DEFENSE.md', doc) + '.', '',
              'Try first, compare second. Copying or running answers is useful for diagnosis but does not pass the independent gate. Keep your attempted solutions and mistake log.', '',
              'Maintainers: `python tools/build_answer_index.py` rebuilds only reference indexes/scripts; `python tools/check_answers.py` checks exact question coverage and links. Existing learner notebooks are never an output of either command.', '']
    (ROOT/doc).write_text('\n'.join(lines))
    (ROOT/'curriculum/answer_manifest.json').write_text(json.dumps(records, indent=2, ensure_ascii=False)+'\n')
    for path in ['START_HERE.md', 'curriculum/EXTRA_LABS.md']:
        add_banner(ROOT/path, doc)
    print(f'Built {len(LESSONS)} complete lesson answers, 16 stage maps, and {len(records)} indexed answers: {dict(counts)}')

if __name__ == '__main__':
    main()
