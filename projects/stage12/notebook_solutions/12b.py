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

principal = {"user_id": "u1", "tenant": "A", "role": "reader"}
resource = {"id": "doc1", "tenant": "A", "public": False}
print(principal["tenant"] == resource["tenant"])

# 12b-E1: Read authorization

def can_read(principal, resource):
    return principal.get("role") in {"reader", "admin"} and (resource.get("public", False) or principal.get("tenant") == resource["tenant"])

assert can_read({"role": "reader", "tenant": "A"}, {"tenant": "A"})
assert not can_read({"role": "admin", "tenant": "B"}, {"tenant": "A"})
assert not can_read({"role": "unknown", "tenant": "A"}, {"tenant": "A"})

print("12b-E1: checks passed")

# 12b-E2: Cache identity

def cache_key(tenant, permission_version, index_version, model_version, query):
    import hashlib, json
    fields = [tenant, permission_version, index_version, model_version, query]
    return hashlib.sha256(json.dumps(fields, ensure_ascii=False).encode()).hexdigest()

assert cache_key("A", 1, 1, "m", "q") != cache_key("B", 1, 1, "m", "q")
assert cache_key("A", 1, 1, "m", "q") != cache_key("A", 2, 1, "m", "q")

print("12b-E2: checks passed")

# 12b-E3: Resource lookup

def get_document(resources, id, principal):
    resource = resources.get(id)
    if resource is None or not can_read(principal, resource): raise PermissionError("Not available")
    return resource

resources = {"d": {"tenant": "A", "text": "private"}}
expect_error(PermissionError, lambda: get_document(resources, "d", {"role": "reader", "tenant": "B"}))
assert get_document(resources, "d", {"role": "reader", "tenant": "A"})["text"] == "private"

print("12b-E3: checks passed")
