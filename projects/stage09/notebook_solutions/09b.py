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

import json
payload = {"model": "configured-local-model", "messages": [{"role": "user", "content": "Hello"}], "stream": False}
print(json.dumps(payload))

# 09b-E1: Ollama request

def ollama_payload(model, prompt, max_tokens=128):
    if not prompt.strip() or len(prompt) > 4000 or not 1 <= max_tokens <= 1024: raise ValueError("Request bounds")
    return {"model": model, "messages": [{"role": "user", "content": prompt}], "stream": False, "options": {"num_predict": max_tokens}}

assert ollama_payload("demo", "hello")["options"]["num_predict"] == 128
expect_error(ValueError, lambda: ollama_payload("demo", "x"*4001))

print("09b-E1: checks passed")

# 09b-E2: Response parsing

def parse_ollama(body):
    try: content = body["message"]["content"]
    except (KeyError, TypeError): raise ValueError("Malformed response") from None
    if not isinstance(content, str): raise ValueError("Malformed content")
    return content

assert parse_ollama({"message": {"content": "hello"}}) == "hello"
expect_error(ValueError, lambda: parse_ollama({"error": "model missing"}))

print("09b-E2: checks passed")

# 09b-E3: Throughput

def throughput(token_counts, elapsed):
    if elapsed <= 0: raise ValueError("Positive elapsed required")
    return sum(token_counts)/elapsed

assert throughput([10, 20], 2) == 15
expect_error(ValueError, lambda: throughput([1], 0))

print("09b-E3: checks passed")
