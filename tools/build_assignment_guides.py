"""Generate assignment interfaces, blank starters, and explicit reference adapters."""
import ast
import copy
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'curriculum/authoring'))
from assignment_catalog import EXPORTS,CONTRACTS,EVIDENCE

def stub(node,name):
    node=copy.deepcopy(node);node.name=name
    def blank(fn):
        fn.body=[ast.Raise(exc=ast.Call(func=ast.Name(id='NotImplementedError',ctx=ast.Load()),args=[ast.Constant('Write your implementation here')],keywords=[]),cause=None)]
        fn.returns=None
        for arg in [*fn.args.posonlyargs,*fn.args.args,*fn.args.kwonlyargs]:arg.annotation=None
        return fn
    if isinstance(node,ast.FunctionDef):return ast.unparse(blank(node))
    node.body=[blank(n) for n in node.body if isinstance(n,ast.FunctionDef)]
    return ast.unparse(node)

def main():
    entries=json.loads((ROOT/'curriculum/manifest.json').read_text());ids={x['id'] for x in entries}
    assert ids==set(EXPORTS)==set(CONTRACTS)==set(EVIDENCE)
    index=['# Test your independent assignments','','These tests run against **your chosen Python file**. They do not silently import the reference solution. The original assignment brief remains in your notebook; the pages below specify interfaces so the tests can call your implementation.','','## First run: calculator assignment 01a','','1. Create `work/assignments/`. Copy the blank [01a starter](starters/01a.py) to `work/assignments/01a.py` without overwriting existing work.','2. Read the [01a contract and cases](01a.md). Implement the functions in your copy.','3. From the repository root with your course environment activated, run:','','```bash\npython tools/test_assignment.py 01a --solution work/assignments/01a.py\n```','','`FAILED` or `NotImplementedError` is expected before you implement a starter. Read the failing assertion: it shows the input and expected behavior. Fix one case at a time. If you use another filename, pass its path with `--solution`. To test your solution across multiple modules, import your own functions into this one entry file.','','After a serious attempt, verify the supplied answer separately:','','```bash\npython tools/test_assignment.py 01a --reference\n```','','The terminal says whether it is testing YOUR solution or REFERENCE answers. A reference pass does not assess your work. Existing code can use a thin adapter to the public interface; you do not have to reorganize your entire project.','','## Work on one function at a time', '', 'Use `--case` to select matching test names while learning:', '', '```bash\npython tools/test_assignment.py 01a --solution work/assignments/01a.py --case calculator\n```', '', 'This runs only part of the pack. Remove `--case` for the full assignment check.', '', '## How to read a test','','- Arrange: build input data, often in a temporary folder.','- Act: call your function or app.','- Assert: compare the result with an independently calculated expectation.','- `pytest.raises(ValueError)` means invalid input should raise that exception.','- `pytest.approx(...)` compares floating-point values with a small tolerance.','- A mock deliberately replaces a boundary with a failure; it does not prove a real service was exercised.','','Example: `assert calculate(2, "+", 3) == 5` checks a normal case; division by zero checks an invalid case. For the converter, -40 is a useful boundary-related check because Celsius and Fahrenheit agree there.','','## Assignment packs','','| Lesson | Contract, starter, automated cases, remaining evidence |','|---|---|']
    manifest=[]
    for item in entries:
        id=item['id'];signatures=[];adapter=['"""Explicit reference adapter. This is an answer, not a learner starter."""'];body=[f'"""Your {id} independent assignment. Contract: curriculum/assignments/{id}.md\nRun: python tools/test_assignment.py {id} --solution PATH_TO_THIS_FILE\nKeep your work in work/; this template may be regenerated.\n"""']
        if id=='06b':body+=['import torch\nfrom torch import nn']
        for export in EXPORTS[id]:
            module,name,*alias=export;public=alias[0] if alias else name
            file=ROOT/(module.replace('.','/')+'.py');tree=ast.parse(file.read_text())
            node=next(n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name==name)
            adapter.append(f'from {module} import {name}'+(f' as {public}' if public!=name else ''))
            body.append(stub(node,public))
            signatures.append(public+'('+ast.unparse(node.args)+')' if isinstance(node,ast.FunctionDef) else public+' (class; see starter methods)')
        (ROOT/f'curriculum/assignments/starters/{id}.py').write_text('\n\n'.join(body)+'\n')
        (ROOT/f'curriculum/assignments/reference_adapters/{id}.py').write_text('\n'.join(adapter)+'\n')
        tests=ROOT/f'tests/independent/test_{id}.py';tree=ast.parse(tests.read_text())
        names=[n.name for n in tree.body if isinstance(n,ast.FunctionDef) and n.name.startswith('test_')]
        doc=[f'# {id}: independent assignment tests','',f'[All test packs](README.md) · [Blank starter](starters/{id}.py) · [Test source](../../tests/independent/test_{id}.py) · [Worked answer](../answers/{id}.md#{id}-t)','','## Public interface','',CONTRACTS[id],'','```python\n'+'\n'.join(signatures)+'\n```','','The starter shows callable signatures, including class methods. Implement the behavior in your own file. The tests provide concrete input/output examples; implementation details can differ from the reference.','','## Run against your work','','```bash\n'+f'python tools/test_assignment.py {id} --solution work/assignments/{id}.py'+'\n```','','Use the notebook environment group as a starting point, then install any extra packages listed below. The reference adapter may use more packages than your implementation.','','## Automated cases','']
        doc+=['- '+name.removeprefix('test_').replace('_',' ') for name in names]
        doc+=['','## Additional completion evidence','', 'Automated checks cover the cases above. The following items still need your experiment, explanation, or live run; they are **not** automatically marked passed.','']
        doc+=['- [ ] '+case for case in EVIDENCE[id]]
        if id in ['06c','07a','07b']:doc+=['','**Extra dependencies:** 06c uses `requirements/deep.txt`; 07a uses `requirements/core.txt`; 07b parsing uses `requirements/integration.txt`. No model download is performed by the offline tests.']
        if id=='11b':doc+=['','**Run the actual local Spark check:**','','```bash\npython tools/test_assignment.py 11b --solution work/assignments/11b.py --live-spark\n```','','Requires PySpark, a compatible full JDK, and local loopback sockets. A skipped Spark check remains pending.']
        doc+=['','[Live procedures and expected evidence](../answers/OPERATIONS.md) · [Concept explanation](../concepts/'+id+'.md)','','## Compare only after trying','','```bash\n'+f'python tools/test_assignment.py {id} --reference'+'\n```','','Report-based tests inspect measured fields and artifacts but cannot prove all internal training/permission choices. Review the implementation and retain the additional evidence. Passing these tests is a useful checkpoint, not a guarantee of mastery.','']
        (ROOT/f'curriculum/assignments/{id}.md').write_text('\n'.join(doc))
        index.append(f'| {id} — {item["title"]} | [Open test pack]({id}.md) |')
        manifest.append(dict(id=id,starter=f'curriculum/assignments/starters/{id}.py',tests=f'tests/independent/test_{id}.py',reference=f'curriculum/assignments/reference_adapters/{id}.py',guide=f'curriculum/assignments/{id}.md',test_functions=names,evidence=EVIDENCE[id]))
    index+=['','## All-reference maintenance check','','```bash\npython tools/test_assignment.py --all --reference\n```','','This needs the core, deep, agents, and integration parsing dependencies. Local Spark is skipped unless `--live-spark` is added with the supported JDK. PostgreSQL/model-serving/deployment evidence remains separate. Ordinary `pytest` skips assignment packs until you explicitly select a learner solution or the references.','']
    (ROOT/'curriculum/assignments/README.md').write_text('\n'.join(index))
    (ROOT/'curriculum/assignment_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(f'Built {len(manifest)} assignment contracts, blank starters, and reference adapters')

if __name__=='__main__':main()
