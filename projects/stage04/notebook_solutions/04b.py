"""Generated worked answers; edit your own version under work/."""

from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
def expect_error(error_type, operation):
    try:
        operation()
    except error_type:
        return
    raise AssertionError(f"Expected {error_type.__name__}")


# Worked example

from sklearn.metrics import confusion_matrix
print(confusion_matrix([1, 1, 0, 0], [1, 0, 1, 0]))

# 04b-E1: Binary metrics

def binary_metrics(y, pred):
    if len(y) != len(pred): raise ValueError("Length mismatch")
    tp = sum(a == b == 1 for a, b in zip(y, pred))
    fp = sum(a == 0 and b == 1 for a, b in zip(y, pred))
    fn = sum(a == 1 and b == 0 for a, b in zip(y, pred))
    p = tp/(tp+fp) if tp+fp else 0
    r = tp/(tp+fn) if tp+fn else 0
    return p, r, 2*p*r/(p+r) if p+r else 0

assert binary_metrics([1, 1, 0], [1, 0, 1]) == (.5, .5, .5)
assert binary_metrics([0], [0]) == (0, 0, 0)

print("04b-E1: checks passed")

# 04b-E2: Cost-sensitive threshold

def decision_cost(y, scores, threshold):
    return sum(5 if actual == 1 and score < threshold else 1 if actual == 0 and score >= threshold else 0 for actual, score in zip(y, scores))

assert decision_cost([1, 0], [.4, .6], .5) == 6
assert decision_cost([1, 0], [.4, .6], .3) == 1

print("04b-E2: checks passed")

# 04b-E3: PCA pipeline

def reduce_dimension(x):
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.decomposition import PCA
    pipe = make_pipeline(StandardScaler(), PCA(n_components=1))
    return pipe.fit_transform(x), pipe

z, pipe = reduce_dimension([[1, 2], [2, 4], [3, 6]])
assert z.shape == (3, 1)
assert pipe[-1].explained_variance_ratio_[0] > .999

print("04b-E3: checks passed")
