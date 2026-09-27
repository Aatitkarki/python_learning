"""Generate navigable stage/project guides from the authored curriculum specification."""
import json
import math
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'curriculum/authoring'))
from stages import STAGES
manifest=json.loads((ROOT/'curriculum/manifest.json').read_text())
assert sum(s[2] for s in STAGES)==1200
plan=['# Your AI engineering learning plan\n',
      'Designed for a beginner, based on all 16 stages in [the original roadmap](../readme.md). Budget **1,200 focused hours**, approximately **80 weeks at 15 hours/week**. At 10/20/25 hours per week, the same work takes about 120/60/48 weeks. These are planning estimates; repeat weak checkpoints before advancing. The README’s 1,000 hours is a broad estimate; this plan adds deliberate practice and review.\n',
      'Start with [START_HERE.md](../START_HERE.md), then [the first 30 days](FIRST_30_DAYS.md). Every stage includes practice notebooks, separate answers, a work brief, reference implementation or operational lab, and a closed-book gate.\n',
      '## How to study\n\nUse five 3-hour sessions per week. A typical session: 20 minutes retrieval from memory, 40 minutes reading/experimenting, 90 minutes coding, 20 minutes testing/debugging, 10 minutes updating your log. During project weeks, move reading time into implementation. Take breaks inside your chosen schedule. Review each major concept after 2, 7, and 30 days.\n',
      'Try exercises before opening answers. Record your attempt and error first, use a hint next, and only then compare a solution. Close it and rebuild with changed inputs two days later. Passing visible checks is a starting point; add edge cases and explain the contract.\n',
      '## Stage map\n\n| Stage | Hours | Approx. weeks | Practical outcome |\n|---|---:|---:|---|']
progress=['# Learning progress\n','This file starts unassessed. The original README marks Statistics complete; keep that history, but use Stage 02’s diagnostic to confirm it before skipping any practice.\n',
          '| Stage | Hours logged | Exercise evidence | Project evidence | Gate score / date | 7-day review | 30-day review |\n|---|---:|---|---|---|---|---|']
coverage=['# Roadmap coverage and completion evidence\n','Every original stage is represented below. “Notebook” means guided mechanics; “project” means implementation work; an integration requirement is not complete until you run it and save evidence. Models/frameworks mentioned for comparison do not all require separate installations.\n',
          '| Original stage | Notebook IDs | Topic coverage | Evidence required |\n|---|---|---|---|']
start=0; spans=[]
for stage,title,hours,project,topics,tasks,command,answer,gate,remediation in STAGES:
    end=start+hours; selected=[m for m in manifest if m['id'].startswith(stage)]
    weeks=f'{start//15+1}–{math.ceil(end/15)}'
    plan.append(f'| [{stage} — {title}](stages/{stage}.md) | {hours} | {weeks} | [{project}](../projects/stage{stage}/README.md) |')
    progress.append(f'| [{stage} {title}](curriculum/stages/{stage}.md) | 0 / {hours} | pending | pending | unassessed | pending | pending |')
    coverage.append(f'| {stage} {title} | '+', '.join(m['id'] for m in selected)+' | '+'; '.join(topics)+' | '+gate+' |')
    spans.append((start,end,stage,title,tasks))
    notebook_links='\n'.join(f'- [{m["id"]} — {m["title"]}](../notebooks/{Path(m["practice"]).name}) · [Answers](../solutions/{Path(m["solution"]).name}) · environment: `{m["group"]}`' for m in selected)
    links='\n'.join(f'- [{m["id"]} practice](../../{m["practice"]}) · [worked answers](../../{m["solution"]})' for m in selected)
    budget=[round(hours*.2),round(hours*.3),round(hours*.4)]; budget.append(hours-sum(budget))
    prereq='No programming prerequisites.' if stage=='00' else f'Pass [Stage {int(stage)-1:02d}]({int(stage)-1:02d}.md) and complete the earlier notebooks in this stage.'
    guide=f'''# Stage {stage} — {title}

**Budget:** {hours} hours · **Suggested calendar:** weeks {weeks} at 15 hours/week · **Prerequisites:** {prereq}

## What you will learn

'''+ '\n'.join('- '+t for t in topics)+f'''

## Study sequence and hours

1. **Learn and explain — {budget[0]} hours.** Read the notebook lessons and linked primary references. Produce a one-page explanation with one worked example for each topic above. Use CS50P/CS50 SQL and D2L alongside this course where listed in RESOURCES.md.
2. **Practice and debug — {budget[1]} hours.** Complete the notebooks below, then change inputs, add edge tests, and reproduce every important result from a fresh process. Keep a mistake log and repair at least one deliberately introduced bug per notebook.
3. **Build independently — {budget[2]} hours.** Implement the project brief from an empty folder under work/. Produce the deliverables below and compare with the reference only after a serious attempt.
4. **Assess and revisit — {budget[3]} hours.** Complete the closed-book gate, explain decisions aloud, and schedule 7/30-day reviews. If the gate fails, use the remediation path and retry with changed inputs.

## Notebooks in order

{notebook_links}

## Real work: {project}

'''+ '\n'.join(f'{i}. {task}' for i,task in enumerate(tasks,1))+f'''

[Full brief and run instructions](../../projects/stage{stage}/README.md) · [Answer guide](../../projects/stage{stage}/ANSWERS.md)

## Mastery gate

{gate}

Score correctness and reasoning (40), independent implementation (25), tests/debugging (20), and explanation/reproducibility (15). Pass at **80/100**, with no unhandled leakage, permission breach, invented evidence, or non-reproducible core result. A live-integration requirement cannot be passed by a mock or offline substitute. Record links to evidence in [progress.md](../../progress.md).

## If you get stuck

{remediation}

Explain what failed, show the smallest reproduction, and ask for a hint. Do not replace your entire solution with an answer file. Rebuild the corrected idea after 48 hours and include one unseen case.

## Submission

Save code, tests, a brief report of observed results, one failed experiment, limitations, and your gate score in work/stage{stage}/. External integrations additionally need service/model versions, machine details, commands, and actual observed output. Optional hardware deferral must stay marked pending, not passed.
'''
    (ROOT/f'curriculum/stages/{stage}.md').write_text(guide)
    req={'05':'deep','06':'deep','08':'agents','11':'spark'}.get(stage,'core')
    readme=f'''# Stage {stage} project — {project}

[Stage study guide](../../curriculum/stages/{stage}.md) · [Course plan](../../curriculum/PLAN.md)

**Scenario:** You own a small component of a private research platform. A teammate must be able to reproduce it, inspect its evidence, and understand its failure behavior.

## Your assignment

'''+ '\n'.join(f'{i}. {task}' for i,task in enumerate(tasks,1))+f'''

## Acceptance criteria

{gate}

Also require documented inputs/outputs, explicit units and limitations, tests for normal/boundary/error cases, and a fresh-process run. Use only data you have permission to use; the supplied fixtures are fictional. Do not report a synthetic-data score as real-world quality.

## Starter workflow

Create work/stage{stage}/, write a short interface contract, and implement the smallest end-to-end slice first. Use the exercise stubs below for function signatures and visible checks. Add your own tests before consulting the reference.

{links}

## Run the reference after your attempt

From the repository root with the environment active:

```bash
python -m pip install -r requirements/{req}.txt
{command}
```

For model/service labs, read [INTEGRATIONS.md](../../curriculum/INTEGRATIONS.md) before running. Stage 10 additionally needs a local .env and a running Docker daemon. Output paths under work/ belong to you.

## Deliver

- Runnable code and tests with a setup README.
- A results report containing actual measurements and source/data versions.
- A failure you reproduced, diagnosed, and fixed.
- A short explanation of tradeoffs and remaining limits.
- Closed-book gate evidence and a scheduled review date.

[Worked answer and design reasoning](ANSWERS.md) · [Additional lab answers](../../curriculum/EXTRA_LABS.md)
'''
    (ROOT/f'projects/stage{stage}/README.md').write_text(readme)
    sources=sorted((ROOT/f'projects/stage{stage}').glob('*.py'))
    if stage in ('03','07','15'): sources += [ROOT/'projects/reference.py',ROOT/'projects/api.py']
    source_links='\n'.join(f'- [{p.name}]({p.relative_to(ROOT/f"projects/stage{stage}") if p.parent == ROOT/f"projects/stage{stage}" else "../"+p.name})' for p in sources)
    if stage=='09': source_links='- [Actual model-server client and benchmark](serve.py)'
    if stage=='10': source_links='- [Dockerfile](Dockerfile)\n- [Compose](../../compose.yaml)\n- [Operational answer/runbook](RUNBOOK.md)\n- [CI workflow](../../.github/workflows/course.yml)'
    answers=f'''# Stage {stage} — worked project answer

Read after saving your own attempt. The reference is one implementation, not the only acceptable design.

## Reference artifacts

{source_links}

## Expected behavior and reasoning

{answer}

## How to review your work

Compare the input/output contract first, then edge behavior, data boundaries, and failure modes. Different implementation details are acceptable when you can explain them and demonstrate the same or stronger guarantees. Record actual observed model/latency results instead of treating example scores as universal answers.

## Transfer and extension answer key

The [extra lab answer guide](../../curriculum/EXTRA_LABS.md) supplies derivations, query examples, algorithms, and design answers for the larger extensions. The corresponding solved notebooks answer each checked exercise and each oral question:

{links}

## Common wrong answer

A runnable happy path alone does not satisfy the project. A missing dependency or unavailable external service is pending evidence; a mock is useful for unit testing but does not prove the actual integration. Copying the reference does not pass the independent gate.
'''
    (ROOT/f'projects/stage{stage}/ANSWERS.md').write_text(answers)
    start=end
plan += ['\n## Weekly pacing\n\nThe table below allocates every 15-hour week. Stage boundaries can share a week. Use the stage’s hour blocks to balance learning, practice, independent building, and review; the listed task is the main deliverable for that portion of the stage.\n', '| Week | Stage allocation | Main work |\n|---:|---|---|']
for week in range(1,81):
    lo,hi=(week-1)*15,week*15; allocations=[]; tasks=[]
    for a,b,stage,title,items in spans:
        overlap=max(0,min(hi,b)-max(lo,a))
        if overlap:
            allocations.append(f'{stage}: {overlap}h')
            fraction=(min(hi,b)-a)/(b-a)
            index=min(len(items)-1,int(fraction*len(items)))
            tasks.append(items[index])
    plan.append(f'| {week} | '+', '.join(allocations)+' | '+' '.join(tasks)+' |')
plan += ['\n## Graduation and continued practice\n\nComplete [the capstone](CAPSTONE.md), retain four portfolio artifacts (classical ML, deep learning, private RAG, production workflow), and pass [the assessment](assessments/MASTERY.md). No fixed schedule guarantees mastery; the independent gates and delayed reviews determine readiness. Hardware-dependent work stays pending until demonstrated.\n']
(ROOT/'curriculum/PLAN.md').write_text('\n'.join(plan)+'\n')
(ROOT/'curriculum/COVERAGE.md').write_text('\n'.join(coverage)+'\n')
progress += ['\n## Session log template\n\nDate / stage / minutes / goal / what I built / what failed / fix / explanation from memory / next step / review dates.\n',
'## Monthly review\n\n1. What can I build independently now?\n2. Which explanation or test exposed a gap?\n3. Which mistakes recur?\n4. Where did I look at an answer too early?\n5. What changed in my evidence or confidence?\n6. Which stage needs another attempt?\n',
'## Evidence rules\n\nUse links to code, notebook output, tests, reports, and recordings. Mark **passed** only after an independent attempt. Mark external-service/hardware work **pending** until run. Never award mastery because the reference implementation passed its tests.\n']
if not (ROOT/'progress.md').exists():
    (ROOT/'progress.md').write_text('\n'.join(progress)+'\n')
print('Built 16 stage guides, 16 briefs, 16 answer guides, coverage map, 80-week plan, and progress tracker.')
