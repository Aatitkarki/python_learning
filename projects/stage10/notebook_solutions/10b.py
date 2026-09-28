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

config = {"host": "database", "port": 5432}
print("Containers connect using service DNS:", config)

# 10b-E1: Required configuration

def validate_config(env):
    result = {k: env.get(k, "").strip() for k in ("DATABASE_URL", "API_KEY")}
    if not all(result.values()) or len(result["API_KEY"]) < 24: raise ValueError("Incomplete configuration")
    return result

assert validate_config({"DATABASE_URL": "postgresql://db/example", "API_KEY": "x"*32})["API_KEY"] == "x"*32
expect_error(ValueError, lambda: validate_config({}))

print("10b-E1: checks passed")

# 10b-E2: Release gate

def release_ready(evidence):
    return all(evidence.get(k) is True for k in ("tests", "evals", "migration_rehearsal", "restore_drill"))

assert not release_ready({"tests": True, "evals": True})
assert release_ready(dict.fromkeys(["tests", "evals", "migration_rehearsal", "restore_drill"], True))

print("10b-E2: checks passed")

# 10b-E3: Schema compatibility

def compatible(current, minimum, maximum):
    if minimum > maximum: raise ValueError("Invalid range")
    return minimum <= current <= maximum

assert compatible(3, 2, 4)
assert not compatible(5, 2, 4)

print("10b-E3: checks passed")
