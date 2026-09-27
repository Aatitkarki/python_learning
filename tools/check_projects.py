"""Execute offline reference applications and preserve their observed outputs."""
import json
import subprocess
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
commands=[['-m','projects.'+name] for name in [
    'stage00.solution','stage01.solution','stage02.solution','stage03.solution','stage04.solution',
    'stage05.solution','stage05.numpy_xor','stage06.tiny_lm','stage07.solution','stage08.solution',
    'stage08.research','stage12.solution','stage13.solution','stage14.solution','stage15.solution']]
commands.append(['-m','projects.stage06.pretrained','--offline-smoke'])
results=[]
for args in commands:
    result=subprocess.run([sys.executable,*args],cwd=ROOT,text=True,capture_output=True,timeout=240)
    results.append({'command':args,'returncode':result.returncode,'stdout':result.stdout,'stderr':result.stderr})
    print('PASS' if result.returncode==0 else 'FAIL',' '.join(args),flush=True)
work=ROOT/'work';work.mkdir(exist_ok=True)
(work/'project-validation.json').write_text(json.dumps(results,indent=2)+'\n')
raise SystemExit(any(r['returncode'] for r in results))
