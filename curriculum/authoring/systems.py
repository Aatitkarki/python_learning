from schema import lesson, exercise as E

lesson('07a', 'Retrieval from first principles', 'stdlib',
['Chunk documents with stable provenance', 'Rank keyword matches', 'Measure retrieval separately from answers'],
'''Retrieval selects evidence before an answer is generated. Parsing converts PDF, Markdown, HTML, DOCX, JSON, or database records into text and metadata. Preserve document ID, page or section, source version, tenant, and permissions. OCR and tables need special care; a parser can silently scramble numbers.

Chunking balances context completeness against retrieval precision. Fixed-size chunks are simple; paragraph and semantic chunks follow content boundaries. Overlap can preserve context but also duplicates evidence and consumes space. Use the model tokenizer for actual token limits; the exercise uses whitespace words as a transparent baseline.

Keyword methods match literal terms. BM25 adjusts term frequency using document length and rarity. Dense embeddings can retrieve paraphrases but may miss exact identifiers. Hybrid retrieval combines complementary ranked lists; reranking scores query-candidate pairs with a more expensive model. First establish a measured lexical baseline so you can tell whether embeddings add value.''',
'''import re
print(re.findall(r"[a-z0-9]+", "Revenue grew 12% in 2025.".lower()))''', [
E('Overlapping chunks', 'Return word chunks with size>0 and 0<=overlap<size. Avoid an extra final chunk made only of overlap.', 'def chunks(text, size=4, overlap=1):\n    raise NotImplementedError', '''def chunks(text, size=4, overlap=1):
    if size <= 0 or not 0 <= overlap < size: raise ValueError("Invalid chunk configuration")
    words, result = text.split(), []
    start = 0
    while start < len(words):
        result.append(" ".join(words[start:start+size]))
        if start+size >= len(words): break
        start += size-overlap
    return result''', '''assert chunks("a b c d e f", 4, 1) == ["a b c d", "d e f"]
assert chunks("") == []
expect_error(ValueError, lambda: chunks("a", 2, 2))''', 'Stop when the current chunk reaches the final word.', 'Poor stopping conditions create redundant tail chunks that skew ranking.'),
E('Lexical retrieval', 'For dicts with id,text, rank documents by number of shared unique lowercase alphanumeric terms; omit zero scores, break ties by id.', 'def retrieve(query, documents, k=3):\n    raise NotImplementedError', '''def retrieve(query, documents, k=3):
    import re
    terms = lambda s: set(re.findall(r"[a-z0-9]+", s.lower()))
    q = terms(query)
    scored = [(len(q & terms(d["text"])), d["id"]) for d in documents]
    return [id for score, id in sorted(scored, key=lambda pair: (-pair[0], pair[1])) if score > 0][:k]''', '''docs = [{"id": "a", "text": "Revenue margin"}, {"id": "b", "text": "Password reset"}]
assert retrieve("revenue", docs) == ["a"]
assert retrieve("unicorn", docs) == []''', 'Score first; sort with explicit tie-breaking.', 'This is an inspectable baseline, not semantic retrieval or BM25.'),
E('Reciprocal rank fusion', 'Combine ranked ID lists using sum(1/(c+rank)), rank starting at 1. Count an ID at most once per list; tie-break by ID.', 'def rrf(rankings, c=60):\n    raise NotImplementedError', '''def rrf(rankings, c=60):
    scores = {}
    for ranking in rankings:
        seen = set()
        for rank, id in enumerate(ranking, 1):
            if id not in seen:
                scores[id] = scores.get(id, 0)+1/(c+rank)
                seen.add(id)
    return sorted(scores, key=lambda id: (-scores[id], id))''', '''assert rrf([["a", "b"], ["b", "c"]])[0] == "b"''', 'Fuse ranks when raw score scales differ.', 'Raw cosine and keyword scores are not directly comparable without calibration.')],
'Build a private document index with chunk IDs, source offsets, parser version, and content hashes. Compare keyword, embedding, hybrid, and reranked recall on the same labeled questions.',
[('Why keep source offsets?', 'To verify citations and trace a parsing or chunking error to the original document.'), ('What can reranking fix?', 'Ordering among retrieved candidates; it cannot recover evidence that never entered the candidate set.')], ['https://github.com/pgvector/pgvector'])

lesson('07b', 'Grounding, permissions, and vector search', 'data',
['Filter access before ranking', 'Return traceable citations and abstentions', 'Use actual embeddings and pgvector in the project'],
'''RAG combines retrieved evidence with generation. It cannot guarantee truth: wrong sources, stale versions, weak retrieval, or unsupported synthesis can each cause failure. Return an explicit abstention when the evidence does not support the question. Separate retrieval recall from citation support and answer correctness.

Permissions must constrain the candidate set before evidence reaches a model. Filtering only the displayed citations is too late. Caches, rerankers, logging, and backups also need tenant boundaries. A vector database stores embeddings and metadata; similarity is meaningful only when the embedding model, dimension, preprocessing, and distance convention agree.

Approximate indexes trade recall for speed. Test recall after metadata filtering and inspect query plans. The notebook uses TF-IDF vectors to teach the interface offline; the project includes learned sentence embeddings, PostgreSQL/pgvector, and a model adapter. These are distinct experiments and must be reported as such.''',
'''from sklearn.feature_extraction.text import TfidfVectorizer
texts = ["revenue grew", "password reset"]
x = TfidfVectorizer().fit_transform(texts)
print(x.shape)''', [
E('Authorized candidates', 'Return public documents or documents with tenant equal to the authenticated tenant. Do not infer identity from the query text.', 'def authorized(documents, tenant):\n    raise NotImplementedError', '''def authorized(documents, tenant):
    return [d for d in documents if d.get("public", False) or d["tenant"] == tenant]''', '''docs = [{"id": "a", "tenant": "a"}, {"id": "b", "tenant": "b"}, {"id": "p", "tenant": "b", "public": True}]
assert [d["id"] for d in authorized(docs, "a")] == ["a", "p"]''', 'Authorization is a server-side predicate.', 'Public access must be deliberate metadata, not a phrase found in document text.'),
E('Cosine vector ranking', 'Using TF-IDF, rank authorized nonzero-scoring documents. Return (id,score) pairs, sorted descending then id. Empty input returns [].', 'def vector_search(query, documents, tenant, k=3):\n    raise NotImplementedError', '''def vector_search(query, documents, tenant, k=3):
    from sklearn.feature_extraction.text import TfidfVectorizer
    allowed = authorized(documents, tenant)
    if not allowed: return []
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform([d["text"] for d in allowed])
    scores = (matrix @ vectorizer.transform([query]).T).toarray().ravel()
    pairs = [(d["id"], float(s)) for d, s in zip(allowed, scores) if s > 0]
    return sorted(pairs, key=lambda p: (-p[1], p[0]))[:k]''', '''docs = [{"id": "a", "tenant": "A", "text": "annual revenue"}, {"id": "b", "tenant": "B", "text": "secret revenue"}]
assert vector_search("revenue", docs, "A")[0][0] == "a"
assert vector_search("missing", docs, "A") == []''', 'TF-IDF normalizes rows by default, so dot products are cosine scores.', 'Fit an index once per stable authorized corpus in a real service; rebuilding per query is only a teaching simplification.'),
E('Evidence contract', 'Return status=unsupported with empty citations when no hits; else status=evidence with exact quotes and IDs. Do not synthesize a claim.', 'def evidence_response(hits, by_id):\n    raise NotImplementedError', '''def evidence_response(hits, by_id):
    if not hits: return {"status": "unsupported", "citations": []}
    return {"status": "evidence", "citations": [{"id": id, "quote": by_id[id]["text"]} for id, score in hits]}''', '''assert evidence_response([], {}) == {"status": "unsupported", "citations": []}
assert evidence_response([("a", .5)], {"a": {"text": "Revenue 10"}})["citations"][0]["quote"] == "Revenue 10"''', 'Preserve the exact evidence before adding a generator.', 'Extractive evidence is easier to audit; a generated answer needs claim-level support checks.')],
'Run the pgvector lab, ingest Markdown plus one PDF, and answer through Ollama. Evaluate access isolation, paraphrases, exact numbers, unsupported questions, and malicious retrieved instructions.',
[('Can a citation be valid but misleading?', 'Yes. The cited document may exist without supporting the associated claim.'), ('Why filter before model access?', 'Once unauthorized text reaches a model, output filtering cannot undo the disclosure.')], ['https://github.com/pgvector/pgvector', 'https://docs.ollama.com/api/chat'])

lesson('08a', 'Tools and bounded workflows', 'stdlib',
['Validate tool names and arguments', 'Separate decisions from execution', 'Bound retries, steps, and side effects'],
'''A tool call is a structured request to execute a function. A model proposes a name and arguments; application code validates them, authorizes the operation, and executes it. Tool output is an observation, not a new instruction with higher authority. Never invent a result when a tool fails.

A workflow has state, transitions, and terminal outcomes. A fixed sequence is often sufficient. An agent adds model-selected transitions, which increases the need for budgets and evaluation. Bound calls, elapsed time, retries, response sizes, and concurrency. A deadline checked between calls does not cancel a blocking call; each I/O operation needs its own timeout.

Read-only tools can often be retried. Side effects need idempotency keys and explicit approval tied to the exact action, arguments, actor, and expiration. Persist only necessary state, separating users and runs. Multiple agents add coordination and failure paths; use them only if a measured comparison justifies the cost.''',
'''request = {"tool": "divide", "arguments": {"a": 12, "b": 3}}
print(request)''', [
E('Allowlisted calculator', 'Execute add or divide from a request with exactly tool,arguments and arguments exactly a,b; finite numeric values only (exclude booleans). Reject all other requests.', 'def execute_tool(request):\n    raise NotImplementedError', '''def execute_tool(request):
    import math
    if set(request) != {"tool", "arguments"}: raise ValueError("Invalid request")
    args = request["arguments"]
    if set(args) != {"a", "b"}: raise ValueError("Invalid arguments")
    if any(type(v) not in (int, float) or not math.isfinite(v) for v in args.values()): raise ValueError("Invalid number")
    a, b = args["a"], args["b"]
    if request["tool"] == "add": return a+b
    if request["tool"] == "divide": return a/b
    raise ValueError("Unknown tool")''', '''assert execute_tool({"tool": "divide", "arguments": {"a": 12, "b": 3}}) == 4
expect_error(ValueError, lambda: execute_tool({"tool": "shell", "arguments": {"a": 1, "b": 2}}))''', 'No eval and no dynamic imports.', 'A small typed allowlist prevents model text from becoming arbitrary code.'),
E('Call budget', 'Execute sequential requests up to max_calls. Return observations and status complete or budget_exhausted. Record tool errors as strings; do not pretend they succeeded.', 'def run_tools(requests, max_calls=3):\n    raise NotImplementedError', '''def run_tools(requests, max_calls=3):
    observations = []
    for request in requests[:max_calls]:
        try: observations.append({"result": execute_tool(request)})
        except (ValueError, ZeroDivisionError) as exc: observations.append({"error": type(exc).__name__})
    return observations, "budget_exhausted" if len(requests) > max_calls else "complete"''', '''request = {"tool": "add", "arguments": {"a": 1, "b": 2}}
observations, status = run_tools([request]*5, 2)
assert len(observations) == 2 and status == "budget_exhausted"''', 'The budget belongs outside the model.', 'A model instruction to stop is weaker than a code-enforced limit.'),
E('Retry only transient errors', 'Call operation at most attempts times; retry TimeoutError only. Raise the final error if exhausted.', 'def retry(operation, attempts=3):\n    raise NotImplementedError', '''def retry(operation, attempts=3):
    if attempts < 1: raise ValueError("Positive attempts required")
    for i in range(attempts):
        try: return operation()
        except TimeoutError:
            if i == attempts-1: raise''', '''calls = []
def flaky():
    calls.append(1)
    if len(calls) < 2: raise TimeoutError()
    return "ok"
assert retry(flaky) == "ok" and len(calls) == 2
expect_error(ValueError, lambda: retry(lambda: int("bad")))''', 'Do not catch permanent validation errors.', 'Real network retries also need backoff, jitter, and a total deadline.')],
'Extend document search with typed SQL read tools and a calculator. Add traces, step/deadline budgets, timeouts, approval records, and tests for malformed tool arguments and unavailable services.',
[('Who grants tool permission?', 'Application authorization policy using verified identity, never the model’s claim about its own authority.'), ('When is retry unsafe?', 'When a side effect may have happened and the request is not idempotent.')], ['https://docs.langchain.com/oss/python/langgraph/overview'])

lesson('08b', 'LangGraph state and human review', 'agents',
['Translate a workflow into nodes and edges', 'Use explicit typed state', 'Compare framework and plain-Python behavior'],
'''LangGraph represents orchestration as a graph of state transitions. Nodes read state and return updates; edges define the next step. Conditional edges route using explicit outcomes. A reducer defines how parallel updates combine. LangChain’s tool and message abstractions can simplify interfaces, but domain validation must still live in application code.

Checkpointing stores progress so a run can resume. Persistence requires an appropriately durable backend and a stable run/thread identity. Human-in-the-loop interrupts suspend before a sensitive action and resume with a decision. A saved approval must identify the exact proposed action; a generic approved boolean can be reused incorrectly.

Start with one deterministic graph and compare it against a plain Python workflow using the same fixtures. Only add model routing after you can test each transition. A graph reaching END proves termination, not that the final answer is correct. Evaluate tool selection, arguments, permissions, costs, and answer support separately.''',
'''from typing import TypedDict
from langgraph.graph import StateGraph, START, END
class State(TypedDict, total=False):
    question: str
    route: str
    answer: str''', [
E('Route state', 'Return route=calculator when question contains the word ratio (case-insensitive), else search. Return only the update.', 'def route_node(state):\n    raise NotImplementedError', '''def route_node(state):
    return {"route": "calculator" if "ratio" in state["question"].lower().split() else "search"}''', '''assert route_node({"question": "calculate ratio"}) == {"route": "calculator"}''', 'A node can return a partial state update.', 'This deterministic router is a baseline; it has limited language coverage and must be evaluated.'),
E('Compile graph', 'Build START→route→conditional calculator/search→END. Calculator returns answer="calculator selected" and search returns "search selected".', 'def build_graph():\n    raise NotImplementedError', '''def build_graph():
    graph = StateGraph(State)
    graph.add_node("route", route_node)
    graph.add_node("calculator", lambda state: {"answer": "calculator selected"})
    graph.add_node("search", lambda state: {"answer": "search selected"})
    graph.add_edge(START, "route")
    graph.add_conditional_edges("route", lambda state: state["route"], {"calculator": "calculator", "search": "search"})
    graph.add_edge("calculator", END)
    graph.add_edge("search", END)
    return graph.compile()''', '''graph = build_graph()
assert graph.invoke({"question": "revenue ratio"})["answer"] == "calculator selected"
assert graph.invoke({"question": "find policy"})["answer"] == "search selected"''', 'Keep node names and state keys distinct.', 'Conditional routing is reviewable and can be tested without a model.'),
E('Approval binding', 'Return SHA-256 of canonical JSON containing actor, action, arguments. Same content in different key order must match.', 'def approval_fingerprint(actor, action, arguments):\n    raise NotImplementedError', '''def approval_fingerprint(actor, action, arguments):
    import json, hashlib
    body = json.dumps({"actor": actor, "action": action, "arguments": arguments}, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(body.encode()).hexdigest()''', '''assert approval_fingerprint("a", "write", {"x": 1, "y": 2}) == approval_fingerprint("a", "write", {"y": 2, "x": 1})
assert approval_fingerprint("a", "write", {"x": 1}) != approval_fingerprint("b", "write", {"x": 1})''', 'Hash a canonical representation.', 'A fingerprint binds content but is not authentication; store it server-side with approver, expiry, and single-use status.')],
'Run Stage 08’s checkpoint/interrupt example. Resume one approved action, reject a changed action, and verify two thread IDs cannot exchange state. Compare one graph versus a two-worker design on measured cost and correctness.',
[('What must persistence isolate?', 'Users, tenants, run IDs, and secret-bearing state.'), ('Does a framework remove authorization work?', 'No. It provides orchestration primitives; policy and enforcement remain application responsibilities.')], ['https://docs.langchain.com/oss/python/langgraph/interrupts'])

lesson('09a', 'Memory and serving performance', 'stdlib',
['Estimate weight and KV memory', 'Distinguish latency from throughput', 'Use measurements to choose serving settings'],
'''Weight memory is roughly parameter count × bits per parameter / 8. This estimate excludes quantization metadata, activations, temporary workspaces, runtime overhead, and KV cache. FP16 and BF16 both use two bytes but have different numerical ranges. CUDA is NVIDIA’s compute platform; other devices use other backends. A model fitting in RAM does not imply acceptable latency.

For a decoder, KV cache storage roughly scales with 2 × layers × KV heads × head dimension × sequence length × batch × bytes. Grouped-query attention can reduce KV heads relative to query heads. Longer contexts and more concurrent users can dominate memory.

Latency measures a request’s elapsed time; throughput measures completed work per unit time. Report time to first token, inter-token latency, tokens/second, concurrency, prompt/output lengths, and p50/p95. Batching amortizes work but can increase waiting time. Continuous batching allows sequences to enter/leave a running batch. Do not select hardware from weight size alone.''',
'''print("7 billion FP16 weights, GiB:", 7_000_000_000*2/1024**3)''', [
E('Weight estimate', 'Return GiB for parameters and bits; require positive values.', 'def weight_gib(parameters, bits):\n    raise NotImplementedError', '''def weight_gib(parameters, bits):
    if parameters <= 0 or bits <= 0: raise ValueError("Positive sizes required")
    return parameters*bits/8/1024**3''', '''assert weight_gib(1024**3, 8) == 1
assert weight_gib(1024**3, 4) == .5''', 'GiB uses powers of 1024.', 'Always label decimal GB versus binary GiB to avoid unit errors.'),
E('KV estimate', 'Return bytes for layers, kv_heads, head_dim, tokens, batch=1, bytes_per_value=2.', 'def kv_bytes(layers, kv_heads, head_dim, tokens, batch=1, bytes_per_value=2):\n    raise NotImplementedError', '''def kv_bytes(layers, kv_heads, head_dim, tokens, batch=1, bytes_per_value=2):
    return 2*layers*kv_heads*head_dim*tokens*batch*bytes_per_value''', '''assert kv_bytes(2, 4, 8, 16) == 4096''', 'The leading 2 counts keys and values.', 'This simplified estimate omits block allocation and implementation overhead.'),
E('Nearest-rank percentile', 'Return nearest-rank percentile p in (0,1] of nonempty values.', 'def percentile(values, p):\n    raise NotImplementedError', '''def percentile(values, p):
    import math
    if not values or not 0 < p <= 1: raise ValueError("Invalid percentile")
    return sorted(values)[math.ceil(p*len(values))-1]''', '''assert percentile(list(range(1, 101)), .95) == 95
assert percentile([3], .5) == 3''', 'Sort then select ceil(p*n)-1.', 'Percentile conventions differ; document yours and collect enough observations for tail estimates.')],
'Create a hardware budget for 1B, 7B, and 14B models at 4/8/16 bits and multiple context lengths. Measure your actual machine before buying hardware or choosing a deployment target.',
[('Why does concurrency consume memory?', 'Each active sequence needs state such as KV cache in addition to shared model weights.'), ('Is quantization always faster?', 'No. Speed depends on hardware support, kernels, batching, and memory/compute bottlenecks.')], ['https://docs.vllm.ai/en/latest/'])

lesson('09b', 'Local model API contracts', 'stdlib',
['Build request/response adapters', 'Apply explicit timeouts and output limits', 'Benchmark real model calls separately from offline checks'],
'''A model server exposes inference through a protocol. Ollama’s native chat API and a vLLM OpenAI-compatible endpoint use different request and response shapes. Keep an adapter boundary so orchestration does not depend on one wire format. Configure base URL, model ID, limits, and timeouts explicitly.

A non-streaming request is easier to inspect first; streaming reduces perceived latency but requires incremental parsing and cancellation. Model IDs, weights, licenses, hardware requirements, and endpoint behavior change. Read the server’s current docs and use a model installed on your machine. The offline notebook validates payload contracts only; the project performs actual localhost HTTP calls and records observed timing.

Private hosting still requires access control, secure networking, data retention policy, updates, and monitoring. Do not expose an unauthenticated inference port to the internet. On macOS, start with a server supported by the machine; the vLLM exercise belongs on a supported Linux accelerator host.''',
'''import json
payload = {"model": "configured-local-model", "messages": [{"role": "user", "content": "Hello"}], "stream": False}
print(json.dumps(payload))''', [
E('Ollama request', 'Return a native chat payload with model, one user message, stream=False, and options.num_predict=max_tokens. Require 1..1024 tokens and nonempty prompt <=4000 characters.', 'def ollama_payload(model, prompt, max_tokens=128):\n    raise NotImplementedError', '''def ollama_payload(model, prompt, max_tokens=128):
    if not prompt.strip() or len(prompt) > 4000 or not 1 <= max_tokens <= 1024: raise ValueError("Request bounds")
    return {"model": model, "messages": [{"role": "user", "content": prompt}], "stream": False, "options": {"num_predict": max_tokens}}''', '''assert ollama_payload("demo", "hello")["options"]["num_predict"] == 128
expect_error(ValueError, lambda: ollama_payload("demo", "x"*4001))''', 'The native API uses num_predict under options.', 'Character limits are a coarse guard; production admission must also count actual model tokens.'),
E('Response parsing', 'Extract message.content as a string from a native Ollama response; malformed responses raise ValueError.', 'def parse_ollama(body):\n    raise NotImplementedError', '''def parse_ollama(body):
    try: content = body["message"]["content"]
    except (KeyError, TypeError): raise ValueError("Malformed response") from None
    if not isinstance(content, str): raise ValueError("Malformed content")
    return content''', '''assert parse_ollama({"message": {"content": "hello"}}) == "hello"
expect_error(ValueError, lambda: parse_ollama({"error": "model missing"}))''', 'An error response is not a successful empty answer.', 'Failures should remain visible for retries, metrics, and user communication.'),
E('Throughput', 'Return tokens/second from token counts and total elapsed wall seconds; reject nonpositive elapsed.', 'def throughput(token_counts, elapsed):\n    raise NotImplementedError', '''def throughput(token_counts, elapsed):
    if elapsed <= 0: raise ValueError("Positive elapsed required")
    return sum(token_counts)/elapsed''', '''assert throughput([10, 20], 2) == 15
expect_error(ValueError, lambda: throughput([1], 0))''', 'Use wall duration for the whole concurrent workload.', 'Adding per-request durations would misrepresent concurrent server throughput.')],
'Run projects/stage09/serve.py against an installed model. Save at least 30 warm and cold observations, output lengths, failures, p50/p95, and machine details. Repeat on vLLM only on compatible hardware.',
[('What does an offline adapter test prove?', 'Request/response handling, not model availability, answer quality, or actual serving performance.'), ('Why cap output tokens?', 'To bound inference work and make latency/cost more predictable.')], ['https://docs.ollama.com/api/chat', 'https://docs.vllm.ai/en/latest/'])

lesson('10a', 'Reliability and observability', 'stdlib',
['Define service-level indicators', 'Design idempotent writes and safe logs', 'Plan timeout and dependency failure behavior'],
'''Production work includes availability, correct failures, deployment, recovery, and maintenance. Logs describe events, metrics aggregate measurements, and traces connect work across components. Use request IDs and model/prompt/index versions so an answer can be reconstructed. Do not log raw credentials or confidential retrieved text by default.

A health endpoint can report process liveness; readiness checks whether required dependencies are usable. A retry is useful only for a transient failure and can amplify overload. Set connect/read/total deadlines, bounded queues, rate limits, and circuit-breaking behavior. Idempotency avoids duplicate side effects after uncertain responses.

Define an SLO against user-visible outcomes: for example, a chosen fraction of eligible requests succeed below a latency target. An error budget quantifies permitted failures over a window. Backups are only useful after a restore drill. Migrations, rollback, secrets management, and capacity planning belong in the runbook, not in memory.''',
'''event = {"request_id": "example-001", "status": "ok", "latency_ms": 12.5, "model_version": "offline"}
print(event)''', [
E('SLO calculation', 'Return fraction of events with ok=True and latency_ms<=target. Empty input raises ValueError.', 'def slo_fraction(events, target=500):\n    raise NotImplementedError', '''def slo_fraction(events, target=500):
    if not events: raise ValueError("No observations")
    return sum(e["ok"] and e["latency_ms"] <= target for e in events)/len(events)''', '''assert slo_fraction([{"ok": True, "latency_ms": 100}, {"ok": False, "latency_ms": 10}]) == .5''', 'Fast errors are not successful requests.', 'A latency-only dashboard can look healthy while every request fails.'),
E('Log allowlist', 'Keep request_id,status,latency_ms only; omit every other key.', 'def safe_log(event):\n    raise NotImplementedError', '''def safe_log(event):
    return {k: event[k] for k in ("request_id", "status", "latency_ms") if k in event}''', '''assert safe_log({"request_id": "x", "token": "secret", "prompt": "private"}) == {"request_id": "x"}''', 'Prefer allowlisted fields over trying to name every possible secret.', 'Nested and newly added fields make denylist redaction fragile.'),
E('Idempotency conflict', 'Given a mutable cache and key,payload,result, save (payload,result) on first call, return existing result for same payload, reject changed payload.', 'def remember(cache, key, payload, result):\n    raise NotImplementedError', '''def remember(cache, key, payload, result):
    if key in cache:
        previous_payload, previous_result = cache[key]
        if previous_payload != payload: raise ValueError("Idempotency conflict")
        return previous_result
    cache[key] = (payload, result)
    return result''', '''cache = {}
assert remember(cache, "k", {"x": 1}, 3) == 3
assert remember(cache, "k", {"x": 1}, 8) == 3
expect_error(ValueError, lambda: remember(cache, "k", {"x": 2}, 4))''', 'Bind a key to the request content.', 'This in-memory teaching version is not atomic across processes; use a durable transactional store in production.')],
'Inject a database outage, model timeout, invalid auth, malformed body, oversized prompt, and corrupt document. Record status, latency, logs, recovery steps, and whether retries could duplicate work.',
[('Liveness versus readiness?', 'Liveness asks whether the process is running; readiness asks whether it can serve traffic with required dependencies.'), ('What proves a backup works?', 'A successful restore followed by integrity and application checks.')], ['https://docs.docker.com/compose/'])

lesson('10b', 'Containers, configuration, and deployment', 'stdlib',
['Explain image/container/network/volume boundaries', 'Validate runtime configuration', 'Design release and rollback evidence'],
'''An image is a filesystem and runtime specification; a container is a running instance. A volume retains data beyond a container’s lifecycle. A network connects services by service name; localhost inside a container refers to that container. Bind only intended interfaces and ports. A reverse proxy terminates HTTPS/TLS and routes requests; DNS resolves names.

Keep configuration outside the image. Secrets belong in a secret store or protected runtime environment, never source control or image layers. Use a non-root user, a small build context, dependency locking, and scanned/pinned release artifacts. Development version ranges are not a release lock.

CI should run tests, evaluation gates, and image builds. Deployment should apply tested migrations, check readiness, and support rollback. Rolling back an image cannot undo an incompatible database migration. In Coolify or another platform, configure persistent volumes, private networks, TLS, health checks, and backups deliberately. Local Docker success is one checkpoint, not evidence of operational readiness.''',
'''config = {"host": "database", "port": 5432}
print("Containers connect using service DNS:", config)''', [
E('Required configuration', 'Read a mapping with DATABASE_URL and API_KEY; reject missing/blank values or API_KEY shorter than 24 characters.', 'def validate_config(env):\n    raise NotImplementedError', '''def validate_config(env):
    result = {k: env.get(k, "").strip() for k in ("DATABASE_URL", "API_KEY")}
    if not all(result.values()) or len(result["API_KEY"]) < 24: raise ValueError("Incomplete configuration")
    return result''', '''assert validate_config({"DATABASE_URL": "postgresql://db/example", "API_KEY": "x"*32})["API_KEY"] == "x"*32
expect_error(ValueError, lambda: validate_config({}))''', 'Fail at startup rather than using an insecure default.', 'The length check is only a local training guard, not a complete credential policy.'),
E('Release gate', 'Return True only when tests, evals, migration_rehearsal, and restore_drill are all exactly True.', 'def release_ready(evidence):\n    raise NotImplementedError', '''def release_ready(evidence):
    return all(evidence.get(k) is True for k in ("tests", "evals", "migration_rehearsal", "restore_drill"))''', '''assert not release_ready({"tests": True, "evals": True})
assert release_ready(dict.fromkeys(["tests", "evals", "migration_rehearsal", "restore_drill"], True))''', 'Missing evidence is not success.', 'A release checklist is useful only when each item points to an actual artifact.'),
E('Schema compatibility', 'A service supports schema versions inclusive [minimum,maximum]. Return whether current is compatible; reject inverted bounds.', 'def compatible(current, minimum, maximum):\n    raise NotImplementedError', '''def compatible(current, minimum, maximum):
    if minimum > maximum: raise ValueError("Invalid range")
    return minimum <= current <= maximum''', '''assert compatible(3, 2, 4)
assert not compatible(5, 2, 4)''', 'Consider both upgrade and rollback versions.', 'Expand-contract migrations can keep old and new application versions compatible during rollout.')],
'Use the provided Dockerfile/Compose, run API+PostgreSQL, test persistence after restart, and rehearse backup/restore into a separate database. Add CI and document a Coolify deployment and rollback without publishing secrets.',
[('Why is localhost often wrong in Compose?', 'It points at the current container rather than the database service.'), ('Why pin release artifacts?', 'To know exactly which dependencies and image are deployed and make rollback reproducible.')], ['https://docs.docker.com/get-started/', 'https://docs.docker.com/compose/'])

lesson('11a', 'Distributed data and associative aggregation', 'stdlib',
['Compute mergeable summaries', 'Recognize shuffle and skew', 'Choose analytical storage formats'],
'''Spark’s driver coordinates work; executors process partitions. Transformations build a lazy plan; actions trigger execution. A narrow transformation can operate locally; grouping and large joins often require a shuffle across machines. More partitions do not automatically improve performance because scheduling, network, and serialization have costs.

To average partitions correctly, merge sums and counts. Averaging partition means is wrong when partition sizes differ. Associative summaries allow distributed combination. Skew occurs when a few keys receive most records; one task can dominate runtime. Inspect partition sizes and physical plans before tuning.

CSV and JSON are broadly readable but weakly typed and expensive to scan. Parquet is columnar, typed, compressed, and suitable for analytical column selection. Avro is row-oriented with schema support and is often useful for record/event interchange. Choose a format based on access patterns, schema evolution, and interoperability. A laptop local-mode Spark lab teaches APIs, not cluster operations at scale.''',
'''partitions = [[10, 20], [100]]
print("Wrong mean of means:", sum(sum(p)/len(p) for p in partitions)/len(partitions))
print("Correct:", sum(map(sum, partitions))/sum(map(len, partitions)))''', [
E('Mergeable average', 'Return (sum,count) for each partition, combine, and return the global mean; reject zero total count.', 'def distributed_mean(partitions):\n    raise NotImplementedError', '''def distributed_mean(partitions):
    total, count = 0, 0
    for partition in partitions:
        total += sum(partition)
        count += len(partition)
    if count == 0: raise ValueError("No observations")
    return total/count''', '''assert abs(distributed_mean([[10, 20], [100]])-130/3) < 1e-12
assert distributed_mean([[], [3]]) == 3''', 'Carry the denominator through aggregation.', 'Many distributed bugs are caused by combining already-normalized results.'),
E('Grouped partial sums', 'Merge a list of key→sum dictionaries into a new dictionary.', 'def merge_groups(partials):\n    raise NotImplementedError', '''def merge_groups(partials):
    result = {}
    for partial in partials:
        for key, value in partial.items(): result[key] = result.get(key, 0)+value
    return result''', '''assert merge_groups([{"a": 2}, {"a": 3, "b": 4}]) == {"a": 5, "b": 4}''', 'Addition is associative for exact integers.', 'Floating-point reduction order can change low-order bits; compare with tolerances when appropriate.'),
E('Skew ratio', 'Return largest nonnegative partition size divided by mean size; reject empty or all-zero input.', 'def skew_ratio(sizes):\n    raise NotImplementedError', '''def skew_ratio(sizes):
    if not sizes or min(sizes) < 0 or sum(sizes) == 0: raise ValueError("Invalid sizes")
    return max(sizes)/(sum(sizes)/len(sizes))''', '''assert skew_ratio([10, 10, 10]) == 1
assert skew_ratio([0, 0, 30]) == 3''', 'Compare maximum to mean, then inspect the full distribution.', 'A single summary flags imbalance but does not explain its cause.')],
'Generate a million synthetic transactions in batches, compute grouped totals without loading everything into memory, and compare output with Spark. Explain shuffle, broadcast joins, and skew.',
[('Why is collect dangerous?', 'It brings all records to the driver and can exhaust its memory.'), ('Why use an explicit schema?', 'Inference can be slow or inconsistent and may silently turn dates/numbers into strings.')], ['https://spark.apache.org/docs/latest/api/python/'])

lesson('11b', 'PySpark DataFrames and windows', 'spark',
['Create a real Spark session', 'Aggregate and window typed records', 'Read and write Parquet with validation'],
'''This notebook requires the Spark environment and a compatible Java runtime. It runs a genuine local Spark job. Local mode uses one machine; a distributed cluster adds scheduling, remote storage, executor failures, and resource configuration.

Prefer DataFrame expressions to Python row UDFs when an equivalent built-in exists: the optimizer can inspect expressions and avoid Python serialization. Use explicit types, push filters early, and select needed columns. Call explain to inspect scans, exchanges, and joins. Caching only helps reused expensive intermediates and must fit memory.

Window ordering needs a tie-breaker. A ROWS frame counts records; a RANGE frame follows ordering values. Three rows are not necessarily three calendar days. A production pipeline also needs ingestion IDs, deduplication, late-data policy, and idempotent output. Stop the session after the experiment to release resources.''',
'''import os, sys
os.environ["PYSPARK_PYTHON"] = sys.executable  # Local workers must use this notebook's Python.
from pyspark.sql import SparkSession, functions as F, Window
spark = SparkSession.builder.master("local[2]").appName("ai-learning").config("spark.ui.enabled", "false").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
df = spark.createDataFrame([(1, "A", 10), (2, "A", 20), (3, "B", 5)], "id long, account string, cents long")
df.show()''', [
E('Group totals', 'Return account,sum_cents sorted by account, using Spark DataFrame expressions.', 'def totals(df):\n    raise NotImplementedError', '''def totals(df):
    return df.groupBy("account").agg(F.sum("cents").alias("sum_cents")).orderBy("account")''', '''assert [(r.account, r.sum_cents) for r in totals(df).collect()] == [("A", 30), ("B", 5)]''', 'Only collect the tiny result in this test.', 'Production jobs should write large outputs instead of collecting to the driver.'),
E('Running total', 'Add running_cents partitioned by account ordered by unique id with an unbounded preceding ROWS frame.', 'def with_running(df):\n    raise NotImplementedError', '''def with_running(df):
    window = Window.partitionBy("account").orderBy("id").rowsBetween(Window.unboundedPreceding, Window.currentRow)
    return df.withColumn("running_cents", F.sum("cents").over(window))''', '''assert [r.running_cents for r in with_running(df).orderBy("id").collect()] == [10, 30, 5]''', 'Specify the frame explicitly.', 'Stable ordering is necessary for reproducible cumulative values.'),
E('Parquet round trip', 'Write df to a supplied new directory using errorifexists, read it, and return row count. Do not overwrite existing work.', 'def parquet_roundtrip(df, path):\n    raise NotImplementedError', '''def parquet_roundtrip(df, path):
    df.write.mode("errorifexists").parquet(str(path))
    return spark.read.parquet(str(path)).count()''', '''import tempfile
from pathlib import Path
with tempfile.TemporaryDirectory() as folder:
    assert parquet_roundtrip(df, Path(folder)/"data") == 3
spark.stop()''', 'Spark writes a directory of partition files.', 'A round trip must validate schema and aggregates too before being trusted with real data.')],
'Run the Stage 11 job, compare partitions 2/8/32, capture explain plans and timings, and compute anomalies plus rolling statistics. Repeat on an actual cluster before claiming distributed operational experience.',
[('Why lazy execution?', 'It lets Spark optimize a whole plan before running actions.'), ('What does a shuffle cost?', 'Network transfer, serialization, sorting, disk spill, and coordination.')], ['https://spark.apache.org/docs/latest/api/python/getting_started/install.html'])
