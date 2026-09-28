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

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
pipeline = make_pipeline(StandardScaler(), LogisticRegression(max_iter=500))
print(pipeline)

# 04a-E1: Regression baseline

def mean_baseline(train_y, n):
    if len(train_y) == 0: raise ValueError("Empty training labels")
    return [sum(train_y)/len(train_y)]*n

assert mean_baseline([2, 4, 6], 2) == [4, 4]

print("04a-E1: checks passed")

# 04a-E2: Text pipeline

def text_pipeline():
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    return make_pipeline(TfidfVectorizer(ngram_range=(1, 2)), LogisticRegression(max_iter=500, random_state=42))

model = text_pipeline().fit(["login password", "account login", "refund invoice", "billing invoice"], [0, 0, 1, 1])
assert model.predict(["password login", "invoice refund"]).tolist() == [0, 1]

print("04a-E2: checks passed")

# 04a-E3: Group separation

def groups_are_separate(rows):
    seen = {}
    for row in rows:
        group, split = row["group"], row["split"]
        if group in seen and seen[group] != split: return False
        seen[group] = split
    return True

assert groups_are_separate([{"group": "a", "split": "train"}, {"group": "b", "split": "test"}])
assert not groups_are_separate([{"group": "a", "split": "train"}, {"group": "a", "split": "test"}])

print("04a-E3: checks passed")
