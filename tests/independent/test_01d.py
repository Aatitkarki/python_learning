from pathlib import Path
from unittest.mock import patch
import pytest

@pytest.mark.parametrize('n,result',[(0,1),(1,1),(5,120),(7,5040)])
def test_factorial(assignment,n,result):assert assignment.factorial(n)==result
@pytest.mark.parametrize('n',[-1,1.5,True])
def test_invalid_factorial(assignment,n):
    with pytest.raises(ValueError):assignment.factorial(n)

def test_directory_size_and_symlink_cycle(assignment,tmp_path):
    (tmp_path/'sub').mkdir();(tmp_path/'a').write_bytes(b'abc');(tmp_path/'sub/b').write_bytes(b'12345')
    (tmp_path/'sub/loop').symlink_to(tmp_path,target_is_directory=True)
    assert assignment.directory_bytes(tmp_path)==8

def test_composition_uses_supplied_repository(assignment):
    class EmptyRepository:
        def read(self):return []
    assert assignment.ExpenseAnalyzer(EmptyRepository()).report()['count']==0

def test_cli_handles_file_error(assignment):
    with patch.object(Path,'open',side_effect=PermissionError('denied')):assert assignment.main(['unreadable.csv'])!=0

def test_search_experiment_records_both_measurements(assignment):
    report=assignment.compare_search(n=100,repetitions=5)
    assert report['linear_seconds']>=0 and report['binary_seconds']>=0
    assert report['n']==100 and report['repetitions']==5
    # Speed ordering is intentionally not asserted: tiny measurements are noisy.
