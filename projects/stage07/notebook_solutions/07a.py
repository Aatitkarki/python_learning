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

import re
print(re.findall(r"[a-z0-9]+", "Revenue grew 12% in 2025.".lower()))

# 07a-E1: Overlapping chunks

def chunks(text, size=4, overlap=1):
    if size <= 0 or not 0 <= overlap < size: raise ValueError("Invalid chunk configuration")
    words, result = text.split(), []
    start = 0
    while start < len(words):
        result.append(" ".join(words[start:start+size]))
        if start+size >= len(words): break
        start += size-overlap
    return result

assert chunks("a b c d e f", 4, 1) == ["a b c d", "d e f"]
assert chunks("") == []
expect_error(ValueError, lambda: chunks("a", 2, 2))

print("07a-E1: checks passed")

# 07a-E2: Lexical retrieval

def retrieve(query, documents, k=3):
    import re
    terms = lambda s: set(re.findall(r"[a-z0-9]+", s.lower()))
    q = terms(query)
    scored = [(len(q & terms(d["text"])), d["id"]) for d in documents]
    return [id for score, id in sorted(scored, key=lambda pair: (-pair[0], pair[1])) if score > 0][:k]

docs = [{"id": "a", "text": "Revenue margin"}, {"id": "b", "text": "Password reset"}]
assert retrieve("revenue", docs) == ["a"]
assert retrieve("unicorn", docs) == []

print("07a-E2: checks passed")

# 07a-E3: Reciprocal rank fusion

def rrf(rankings, c=60):
    scores = {}
    for ranking in rankings:
        seen = set()
        for rank, id in enumerate(ranking, 1):
            if id not in seen:
                scores[id] = scores.get(id, 0)+1/(c+rank)
                seen.add(id)
    return sorted(scores, key=lambda id: (-scores[id], id))

assert rrf([["a", "b"], ["b", "c"]])[0] == "b"

print("07a-E3: checks passed")
