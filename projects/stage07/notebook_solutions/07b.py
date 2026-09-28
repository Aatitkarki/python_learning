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

from sklearn.feature_extraction.text import TfidfVectorizer
texts = ["revenue grew", "password reset"]
x = TfidfVectorizer().fit_transform(texts)
print(x.shape)

# 07b-E1: Authorized candidates

def authorized(documents, tenant):
    return [d for d in documents if d.get("public", False) or d["tenant"] == tenant]

docs = [{"id": "a", "tenant": "a"}, {"id": "b", "tenant": "b"}, {"id": "p", "tenant": "b", "public": True}]
assert [d["id"] for d in authorized(docs, "a")] == ["a", "p"]

print("07b-E1: checks passed")

# 07b-E2: Cosine vector ranking

def vector_search(query, documents, tenant, k=3):
    from sklearn.feature_extraction.text import TfidfVectorizer
    allowed = authorized(documents, tenant)
    if not allowed: return []
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform([d["text"] for d in allowed])
    scores = (matrix @ vectorizer.transform([query]).T).toarray().ravel()
    pairs = [(d["id"], float(s)) for d, s in zip(allowed, scores) if s > 0]
    return sorted(pairs, key=lambda p: (-p[1], p[0]))[:k]

docs = [{"id": "a", "tenant": "A", "text": "annual revenue"}, {"id": "b", "tenant": "B", "text": "secret revenue"}]
assert vector_search("revenue", docs, "A")[0][0] == "a"
assert vector_search("missing", docs, "A") == []

print("07b-E2: checks passed")

# 07b-E3: Evidence contract

def evidence_response(hits, by_id):
    if not hits: return {"status": "unsupported", "citations": []}
    return {"status": "evidence", "citations": [{"id": id, "quote": by_id[id]["text"]} for id, score in hits]}

assert evidence_response([], {}) == {"status": "unsupported", "citations": []}
assert evidence_response([("a", .5)], {"a": {"text": "Revenue 10"}})["citations"][0]["quote"] == "Revenue 10"

print("07b-E3: checks passed")
