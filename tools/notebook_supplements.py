"""Beginner explanations and learner-test instructions shared by both notebook writers."""
import hashlib
import os
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]

def managed_cell(id,kind,source):
    return {'cell_type':'markdown','id':f'{kind}-{id}-v1','metadata':{
        'tags':['course-supplement',kind],
        'course_supplement':{'kind':kind,'source_sha256':hashlib.sha256(source.encode()).hexdigest()}},'source':source}

def concept_cell(id,notebook_path):
    path=ROOT/f'curriculum/concepts/{id}.md';text=path.read_text()
    def rebase(match):
        target=match.group(2)
        if '://' in target or target.startswith('#'):return match.group(0)
        relative=os.path.relpath(path.parent/target,(ROOT/notebook_path).parent)
        return match.group(1)+Path(relative).as_posix()+match.group(3)
    return managed_cell(id,'concepts',re.sub(r'(\[[^\]]+\]\()([^\)]+)(\))',rebase,text))

def assignment_cell(id):
    text=f'''## Test your independent assignment

The assignment is work you build separately from the small notebook exercises. Use your own Python file under `work/`; notebooks remain useful for exploration and notes.

1. Read the [{id} interface and acceptance cases](../assignments/{id}.md).
2. Copy the [blank starter](../assignments/starters/{id}.py) to `work/assignments/{id}.py`, or adapt your existing implementation to the documented interface. Do not overwrite earlier work.
3. Implement one piece, then run this command **in your terminal from the repository root**, with your course environment activated:

```bash
python tools/test_assignment.py {id} --solution work/assignments/{id}.py
```

The runner tests the file you specify. It never silently substitutes the reference answer. `NotImplementedError` is expected while the starter is incomplete. Read a failed assertion, calculate its expected answer by hand, fix your implementation, and rerun. See [how to read tests](../assignments/README.md) if pytest is new to you.

After a serious attempt, compare the [worked implementation](../answers/{id}.md#{id}-t). To check the provided answer explicitly:

```bash
python tools/test_assignment.py {id} --reference
```

**Completion:** pass the relevant automated cases, complete the additional experiment/live-evidence checklist in the assignment guide, and explain your approach without the answer open. An automated pass does not certify a live server, a deployment, a human review, or independent mastery.
'''
    return managed_cell(id,'assignment-tests',text)
