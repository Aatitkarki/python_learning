"""Load the learner's file explicitly; never silently fall back to an answer."""
import importlib.util
import sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2]

def pytest_addoption(parser):
    parser.addoption('--assignment-solution',help='Path to YOUR .py solution for the selected assignment')
    parser.addoption('--reference-assignments',action='store_true',help='Explicitly run against reference adapters')
    parser.addoption('--live-spark-assignments',action='store_true',help='Run local Spark integration (requires JDK/PySpark and loopback sockets)')

def pytest_configure(config):
    config.addinivalue_line('markers','live_spark: real local Spark integration; opt in explicitly')

def pytest_collection_modifyitems(config,items):
    for item in items:
        if 'live_spark' in item.keywords and not config.getoption('--live-spark-assignments'):
            item.add_marker(pytest.mark.skip(reason='Live Spark integration pending: rerun with --live-spark'))

@pytest.fixture(scope='module')
def assignment(request):
    id=Path(request.module.__file__).stem.removeprefix('test_')
    chosen=request.config.getoption('--assignment-solution')
    reference=request.config.getoption('--reference-assignments')
    if chosen and reference:raise pytest.UsageError('Choose your solution OR the reference, not both')
    if not chosen and not reference:
        pytest.skip('Run tools/test_assignment.py LESSON --solution YOUR_FILE (or explicitly --reference)')
    path=Path(chosen).resolve() if chosen else ROOT/f'curriculum/assignments/reference_adapters/{id}.py'
    if not path.is_file():pytest.fail(f'Solution file does not exist: {path}',pytrace=False)
    sys.path.insert(0,str(ROOT));sys.path.insert(0,str(path.parent))
    name='_learner_assignment_'+id
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module
    try:spec.loader.exec_module(module)
    except Exception as exc:pytest.fail(f'Could not load {path}: {type(exc).__name__}: {exc}',pytrace=False)
    yield module
    sys.modules.pop(name,None)
    sys.path.remove(str(path.parent));sys.path.remove(str(ROOT))
