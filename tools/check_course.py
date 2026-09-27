"""Validate every notebook and execute solutions; skipped groups are reported explicitly."""
import argparse
import contextlib
import io
import json
import os
import subprocess
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--groups', default='stdlib,data,deep,agents')
    parser.add_argument('--kernel', action='store_true', help='Use real Jupyter kernels and save executed copies under work/executed/')
    parser.add_argument('--only', help='One lesson ID')
    args=parser.parse_args(); groups=set(args.groups.split(','))
    import nbformat
    entries=json.loads((ROOT/'curriculum/manifest.json').read_text())
    report=[]
    for entry in entries:
        for key in ('practice','solution'):
            path=ROOT/entry[key]; nb=nbformat.read(path,as_version=4); nbformat.validate(nb)
            for i,cell in enumerate(nb.cells):
                if cell.cell_type=='code': compile(cell.source,f'{path.name}:cell{i}','exec')
        if args.only and entry['id'] != args.only: continue
        if entry['group'] not in groups:
            report.append({'id':entry['id'],'status':'not_run','reason':'environment group '+entry['group']})
            continue
        path=ROOT/entry['solution']
        try:
            if args.kernel:
                from nbclient import NotebookClient
                nb=nbformat.read(path,as_version=4)
                NotebookClient(nb,timeout=180,kernel_name='python3',resources={'metadata':{'path':str(ROOT)}}).execute()
                out=ROOT/'work/executed'; out.mkdir(parents=True,exist_ok=True)
                nbformat.write(nb,out/path.name)
            else:
                result=subprocess.run([sys.executable,str(ROOT/'tools/run_notebook_cells.py'),str(path)],cwd=ROOT,text=True,capture_output=True,timeout=240)
                if result.returncode: raise RuntimeError(result.stderr or result.stdout)
            report.append({'id':entry['id'],'status':'passed','mode':'jupyter' if args.kernel else 'fresh Python process'})
            print('PASS', entry['id'], flush=True)
        except Exception as exc:
            report.append({'id':entry['id'],'status':'failed','error':str(exc)})
            print('FAIL',entry['id'],str(exc)[-1500:],flush=True)
    target=ROOT/'work'; target.mkdir(exist_ok=True)
    (target/'notebook-validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print({status:sum(r['status']==status for r in report) for status in ('passed','failed','not_run')})
    return int(any(r['status']=='failed' for r in report))

if __name__=='__main__': raise SystemExit(main())
