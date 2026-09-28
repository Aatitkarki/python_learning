"""Run independent assignment acceptance tests against a chosen learner file."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('lesson',nargs='?',help='Lesson ID, such as 01a')
    p.add_argument('--solution',type=Path,help='Your Python file; it must expose the documented interface')
    p.add_argument('--reference',action='store_true',help='Check the provided answer instead of your work')
    p.add_argument('--all',action='store_true',help='All reference assignments (requires --reference)')
    p.add_argument('--case',help='Run only matching test names (pytest -k expression); this is a partial check')
    p.add_argument('--live-spark',action='store_true',help='Include the real local Spark check')
    a=p.parse_args()
    ids={x['id'] for x in json.loads((ROOT/'curriculum/manifest.json').read_text())}
    if a.solution and a.reference:p.error('Choose --solution or --reference, not both')
    if a.all:
        if not a.reference or a.lesson or a.solution:p.error('--all requires --reference and no lesson/solution')
        target=ROOT/'tests/independent'
    else:
        if a.lesson not in ids:p.error('Choose a lesson ID from the course manifest')
        target=ROOT/f'tests/independent/test_{a.lesson}.py'
        if not a.reference:
            a.solution=(a.solution or ROOT/f'work/assignments/{a.lesson}.py').resolve()
            if not a.solution.is_file():p.error(f'No learner solution at {a.solution}. Copy curriculum/assignments/starters/{a.lesson}.py to your work folder and implement it. Reference answers are only used with --reference.')
    command=[sys.executable,'-m','pytest',str(target),'-q','-ra']
    command+=['--reference-assignments'] if a.reference else ['--assignment-solution',str(a.solution)]
    if a.case:command+=['-k',a.case]
    if a.live_spark:command+=['--live-spark-assignments']
    env=dict(os.environ,MPLBACKEND='Agg',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
    print('Testing REFERENCE answers.' if a.reference else f'Testing YOUR solution: {a.solution}',flush=True)
    if a.case:print(f'Partial check only: test names matching {a.case!r}',flush=True)
    return subprocess.call(command,cwd=ROOT,env=env)

if __name__=='__main__':raise SystemExit(main())
