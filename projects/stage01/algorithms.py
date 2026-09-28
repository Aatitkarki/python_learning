"""01d: recursion, file traversal without following symlinks, and measured search."""
import bisect
import time
from pathlib import Path

def factorial(n):
    if type(n) is not int or n < 0: raise ValueError('Nonnegative integer required')
    return 1 if n < 2 else n * factorial(n-1)

def directory_bytes(path):
    path = Path(path)
    if path.is_symlink(): return 0  # Prevent symbolic-link cycles/double counting.
    if path.is_file(): return path.stat().st_size
    if path.is_dir(): return sum(directory_bytes(child) for child in path.iterdir())
    raise FileNotFoundError(path)

def compare_search(n=10000, repetitions=100):
    values = list(range(n)); target = n-1
    def linear(): return next((i for i, value in enumerate(values) if value == target), -1)
    def binary():
        i = bisect.bisect_left(values, target)
        return i if i < len(values) and values[i] == target else -1
    results = {}
    for name, operation in [('linear', linear), ('binary', binary)]:
        started = time.perf_counter()
        for _ in range(repetitions): assert operation() == target
        results[name+'_seconds'] = time.perf_counter()-started
    return {**results, 'n': n, 'repetitions': repetitions,
            'assumption': 'Input already sorted; sorting cost excluded and must be added for unsorted input.'}

if __name__ == '__main__': print(compare_search())
