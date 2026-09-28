"""Build course templates. Use --force only to overwrite generated templates, never learner work."""
import argparse
import hashlib
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'curriculum/authoring'))
import foundations, models, systems, advanced
from schema import LESSONS
from notebook_supplements import concept_cell, assignment_cell

SETUP = '''from pathlib import Path
import sys

ROOT = next((p for p in [Path.cwd(), *Path.cwd().parents] if (p / "datasets" / "financials.csv").exists()), None)
if ROOT is None:
    raise RuntimeError("Open this notebook from inside the learning repository.")
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

def expect_error(error_type, operation):
    try:
        operation()
    except error_type:
        return
    raise AssertionError(f"Expected {error_type.__name__}")

print("Course root:", ROOT)
'''
GROUPS = {'stdlib': 'Python standard library only; Jupyter is needed for the notebook UI.',
          'data': 'Install requirements/core.txt.', 'deep': 'Install requirements/deep.txt. CPU is sufficient.',
          'agents': 'Install requirements/agents.txt. No model or API key is needed.',
          'spark': 'Install requirements/spark.txt and a compatible Java runtime. This starts local Spark.'}

def cell(kind, text, tags=()):
    result = dict(cell_type=kind, id=hashlib.sha256((kind+text).encode()).hexdigest()[:12],
                  metadata={'tags': list(tags)} if tags else {}, source=text.strip()+'\n')
    if kind == 'code': result.update(execution_count=None, outputs=[])
    return result

def notebook(item, solved):
    id = item['id']; stage=id[:2]
    title = '# '+id+' — '+item['title']+(' — Worked answers' if solved else ' — Practice')
    instructions = ('Compare reasoning as well as output. Close this file and repeat with changed inputs after 48 hours.' if solved else
        'Read the lesson and run the example. Implement each TODO, then run its checks. A NotImplementedError is expected until you write your answer. Try for 20–30 minutes before opening a hint; open the solution only after recording an attempt. Copy this notebook into work/ to keep your own version.')
    cells=[cell('markdown', title+'\n\n'+instructions+'\n\n**Prerequisites:** earlier lessons in the course order. **Environment:** '+GROUPS[item['group']]+ '\n\n[Stage guide](../stages/'+stage+'.md) · [Course map](../PLAN.md) · [Project](../../projects/stage'+stage+'/README.md)\n\n**Notebook time:** 2–4 hours for an initial pass; project, reading, retrieval practice, and independent transfer use the rest of the stage budget.\n\nLearning objectives:\n\n'+'\n'.join('- '+x for x in item['objectives'])),
        cell('code', SETUP, ['setup']), concept_cell(id, 'curriculum/notebooks/placeholder.ipynb'), cell('markdown','## Lesson\n\n'+item['theory']),
        cell('markdown','## Worked example\n\nPredict the output before running. Change one input and explain the result.'),cell('code',item['example'],['example'])]
    for i,e in enumerate(item['exercises'],1):
        cells += [cell('markdown', f'## Exercise {i}: {e["title"]}\n\n{e["task"]}\n\nWrite down one normal case, one boundary case, and one invalid case before coding.'),
                  cell('code',e['answer'] if solved else e['starter'],['answer' if solved else 'exercise']),
                  cell('code',e['checks']+f'\nprint("Exercise {i}: checks passed")',['check'])]
        cells.append(cell('markdown', ('**Why this works:** '+e['why']) if solved else '<details><summary>Hint — open after trying</summary>\n\n'+e['hint']+'\n\n</details>'))
    cells.append(cell('markdown','## Independent transfer\n\n'+item['transfer']+'\n\nRecord your implementation, errors, measurements, and explanation in work/. See the project’s ANSWERS.md after attempting the brief.'))
    cells.append(assignment_cell(id))
    oral='## Explain without code\n\n'+'\n\n'.join(f'{i}. {q}'+ ('\n\n   '+a if solved else '') for i,(q,a) in enumerate(item['oral'],1))
    cells.append(cell('markdown',oral))
    cells.append(cell('markdown','## Reading and review\n\n'+'\n'.join(f'- [Primary reference {i}]({url})' for i,url in enumerate(item['reading'],1))+'\n\nAfter 2, 7, and 30 days: explain the concept from memory, solve a changed-input version, and log any gaps in progress.md.'))
    return {'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3 (ipykernel)','language':'python','name':'python3'},'language_info':{'name':'python','version':'3.12'},'course':{'id':id,'group':item['group'],'solution':solved}},'nbformat':4,'nbformat_minor':5}

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--force',action='store_true'); args=parser.parse_args()
    paths=[ROOT/'curriculum'/folder/f'{x["id"]}_{x["title"].lower().replace(" ", "_").replace(",", "").replace("/", "_")}.ipynb' for x in LESSONS for folder in ('notebooks','solutions')]
    if not args.force and any(p.exists() for p in paths):
        raise SystemExit('Templates already exist. Use --force only if you intend to replace them; keep learner edits in work/.')
    entries=[]
    for item in LESSONS:
        stem=item['id']+'_'+item['title'].lower().replace(' ','_').replace(',','').replace('/','_')
        entry={k:item[k] for k in ('id','title','group','objectives')}
        for solved,folder in ((False,'notebooks'),(True,'solutions')):
            path=ROOT/'curriculum'/folder/(stem+'.ipynb')
            path.write_text(json.dumps(notebook(item,solved),indent=1,ensure_ascii=False)+'\n',encoding='utf-8')
            entry['solution' if solved else 'practice']=str(path.relative_to(ROOT))
        entries.append(entry)
    (ROOT/'curriculum/manifest.json').write_text(json.dumps(entries,indent=2)+'\n')
    print(f'Created {len(LESSONS)} practice and {len(LESSONS)} solution notebooks ({sum(len(x["exercises"]) for x in LESSONS)} checked exercises).')

if __name__=='__main__': main()
