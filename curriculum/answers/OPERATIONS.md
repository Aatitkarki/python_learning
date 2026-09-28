# Worked operational answers

[All answers](../ANSWER_INDEX.md) · [Integration prerequisites](../INTEGRATIONS.md) · [Deployment and recovery commands](../../projects/stage10/RUNBOOK.md)

These are executable procedures for assignments whose outputs depend on your server, model, GPU, or deployment. Commands run from the repository root with the course environment activated. Replace uppercase model/revision placeholders with your selected values. Save observed outputs under `work/`; the examples below are expected behavior, not claims that a live service was run during answer validation.

## PostgreSQL ingestion, query plans, and persistence — 03b/03c

Start the disposable course stack using the runbook. In your local terminal:

```bash
set -a
source .env
set +a
export DATABASE_URL="postgresql://learner:${POSTGRES_PASSWORD}@127.0.0.1:15432/learning"
python -m projects.stage03.ingest datasets/expenses.csv
python -m projects.stage03.ingest datasets/expenses.csv
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f projects/stage03/queries.sql
docker compose restart api
```

Both ingestion calls should leave **six expense records, 10,000 cents** in a fresh tenant A ledger. A populated ledger may contain additional records; compare the count before and after the second call. The worksheet creates its own `answer_lab` schema; it preserves existing rows on key conflicts. Use a fresh schema/database when you need an uncontaminated fixture. The customer totals are A=300, B=50, C=0; the rolled-back sentinel has count zero. The temporary 100,000-row table provides the before/after index experiment. Read the actual plan's scan type, actual rows, buffers, and execution time. A sequential scan is a legitimate planner choice.

Use the same authorization key to call `/summary` before/after restart. Run this from a terminal with the generated `.env` loaded; it never prints the key:

```python
import json, os
from urllib.request import Request, urlopen
keys = json.loads(os.environ['COURSE_API_KEYS'])
key = next(key for key, tenant in keys.items() if tenant == 'A')
request = Request('http://127.0.0.1:8000/summary', headers={'Authorization': 'Bearer ' + key})
with urlopen(request, timeout=10) as response:
    print(json.load(response))
```

An invalid CSV must leave the previous ledger unchanged. [The ingestion tests](../../tests/test_answer_labs.py) exercise that atomicity locally; repeat with the same invalid file against your PostgreSQL lab.

## Pinned pretrained model and optional QLoRA — 06c

First run the offline adapter check, then the actual model-specific experiment:

```bash
python -m projects.stage06.pretrained --offline-smoke
python -m projects.stage06.pretrained --model SELECTED_CLASSIFICATION_MODEL --revision IMMUTABLE_COMMIT --epochs 3
```

The worked implementation is [pretrained.py](../../projects/stage06/pretrained.py). It evaluates the unchanged base/task-head configuration, adapts on training examples, chooses an epoch on validation, and evaluates the final test. For a base language encoder the task head starts untrained; this baseline is explicitly weaker than a supervised classifier. Record the model card's license, commit, task head, trainable parameters, elapsed time, observed memory, and scores. Use an isolated supported CUDA environment for the optional quantized path:

```bash
python -m pip install -r requirements/qlora.txt
python -m projects.stage06.qlora --model SELECTED_CLASSIFICATION_MODEL --revision IMMUTABLE_COMMIT --epochs 3
```

[qlora.py](../../projects/stage06/qlora.py) loads a real NF4 base, prepares it for quantized training, adds LoRA to linear modules, restores validation-selected adapter weights, and records peak CUDA allocation. Compatibility depends on the selected architecture and backend. See the primary [PEFT quantization procedure](https://huggingface.co/docs/peft/developer_guides/quantization) and [Transformers bitsandbytes configuration](https://huggingface.co/docs/transformers/quantization/bitsandbytes). The CPU numerical quantization illustration does not count as a GPU training result.

## Multi-format learned retrieval and local drafting — 07a/07b

Prepare a Markdown file and a text-based PDF in `work/sources/`, plus a JSON or HTML document for the three-format project requirement. Use documents you can inspect. Run the PostgreSQL preparation above, then:

```bash
python -m projects.stage07.integration \
  --model SELECTED_EMBEDDING_MODEL --revision IMMUTABLE_COMMIT \
  --document work/sources/report.md --document work/sources/report.pdf \
  --document work/sources/report.json \
  --tenant A --query "Aurora 2025 revenue" \
  --reranker SELECTED_CROSS_ENCODER --reranker-revision RERANKER_COMMIT \
  --ollama INSTALLED_LOCAL_MODEL
```

The file adapter preserves a content hash and per-page PDF source. Empty PDF extraction stops with an OCR diagnostic. Examine ten numbers and table headers against the original before trusting the parsed content. The integration uses PostgreSQL text ranking, exact learned-vector cosine retrieval, RRF, and the selected reranker. For the separate **BM25** comparison:

```bash
python -m projects.stage07.retrieval_lab \
  --model SELECTED_EMBEDDING_MODEL --revision IMMUTABLE_COMMIT \
  --reranker SELECTED_CROSS_ENCODER --reranker-revision RERANKER_COMMIT
```

Compare the same dev labels for every method. Example acceptance cases: “Aurora sales in 2025” should find the Aurora source; “2030 revenue” must remain unsupported; tenant A must never receive `b-private`; a retrieved “ignore permissions” instruction must not change tenant scope. A relevant chunk's presence is only retrieval success. For every generated sentence, record claim, cited source/span, numeric calculation, and supported/unsupported/uncertain judgment. A fabricated source ID fails even when the number happens to be right.

## Warm/cold serving, concurrency, and actual memory — 09a/09b

Run the new bounded concurrency benchmark after starting your selected server:

```bash
python -m projects.stage09.benchmark --model INSTALLED_LOCAL_MODEL --runs 30
```

It measures a first request separately, then 30 attempts each at concurrency 1, 2, and 4, including failures, output lengths, token counts, and p50/p95. First request does not necessarily mean cold. For **30 cold model-load observations on your local Ollama instance**, save and run this Python procedure after replacing `MODEL`. Unloading happens before the request timer; it affects only the specified model.

```python
import json, math, platform, subprocess, time
from pathlib import Path
from projects.stage09.serve import chat
MODEL = 'INSTALLED_LOCAL_MODEL'
rows = []
for index in range(30):
    subprocess.run(['ollama', 'stop', MODEL], check=True, capture_output=True)
    started = time.perf_counter()
    try:
        result = chat('http://127.0.0.1:11434', MODEL,
                      'Explain a database index in two sentences.', timeout=120)
        rows.append(dict(index=index, ok=True, seconds=result['seconds'],
                         tokens=result['tokens'], output_characters=len(result['text'])))
    except Exception as error:
        rows.append(dict(index=index, ok=False, seconds=time.perf_counter()-started,
                         error=type(error).__name__))
times = sorted(row['seconds'] for row in rows)
report = dict(model=MODEL, machine=platform.platform(), observations=rows,
              p50=times[math.ceil(.5*len(times))-1], p95=times[math.ceil(.95*len(times))-1],
              failures=sum(not row['ok'] for row in rows),
              definition='Model unloaded before each request; OS file cache may remain warm. Not TTFT.')
path = Path('work/reference_answers/stage09/cold.json')
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(json.dumps(report, indent=2))
```

Confirm that unloading succeeds. Failure to unload is a setup failure, not a cold inference observation. For vLLM use the benchmark's `--backend vllm --url http://127.0.0.1:PORT`; repeat cold observations by stopping/restarting your isolated server and waiting for readiness before each timed request. Record **server startup-to-ready** separately from **request latency** because vLLM generally loads weights during startup. No universal cold-start numbers can be provided without the actual host/model.

Record physical RAM, runtime/backend versions, model revision/quantization, input length, actual output tokens, and peak process/GPU memory. On macOS use Activity Monitor's process Memory and system Memory Pressure; on Linux record `/usr/bin/time -v` for a fresh server plus `nvidia-smi --query-gpu=timestamp,memory.used,utilization.gpu --format=csv -l 1` when applicable. GPU allocation and process RSS are different measurements. Compare actual usage to the 27 explicit architecture scenarios in the memory-budget report. End-to-end tokens/sec includes loading/prefill overhead; streaming TTFT requires separate first-content instrumentation.

## Release, restore, outage, and deployment — 10a/10b

[The runbook](../../projects/stage10/RUNBOOK.md) contains the actual Compose startup, induced database outage, PostgreSQL backup, separate-database restore, and rollback sequence. Supplement it with:

```bash
python -m projects.stage10.failure_lab
python -m pytest -q
mkdir -p work/releases/answer-lab
python -m pip freeze > work/releases/answer-lab/environment.lock.txt
docker compose images --format json > work/releases/answer-lab/images.json
git rev-parse HEAD > work/releases/answer-lab/source-commit.txt
```

The offline lab records failure status/latency and proves a separate SQLite restore by integrity check, row count, and exact cents. Repeat against PostgreSQL; read the restored database through `Store` as well as SQL. Point a separate local API at `learning_restore`, use the same tenant scope, and compare `/summary` and `/compare` with saved pre-backup results. Do not direct your running application at the backup file itself.

A release record must identify the **built image**, dependencies, source commit, schema, model/index versions, and evaluation result. `pip freeze` captures the environment; a reproducible deployment additionally resolves target-platform wheels/hashes and pins the base image. A local image ID is not a registry digest: after publishing to your own chosen registry, record `RepoDigests` using `docker image inspect YOUR_IMAGE`; if none exists, mark the registry digest pending. The supplied [CI workflow](../../.github/workflows/course.yml) provides tests and image build.

Worked Coolify configuration: repository root build context; Dockerfile `projects/stage10/Dockerfile`; application port 8000; readiness `/ready`; platform-managed secret `COURSE_API_KEYS`; PostgreSQL DSN pointing to the private service; persistent PostgreSQL volume; HTTPS on your chosen domain; no public database/model ports. Deploy a named release, check ready/auth/authorized/denied requests, insert a sentinel, restart, restore into a separate database, then switch back to the previously recorded **schema-compatible** release and rerun checks. Record observed timestamps and statuses. Account, domain, image digest, successful deployment, and third-party review cannot be supplied as invented outputs.

For an incident answer: database failure → readiness/data 503; preserve request IDs and safe exception type; restore service; retry an idempotent read; verify data totals. A write retry needs an idempotency key/unique transaction identity. Do not blindly retry a non-idempotent external action after an uncertain timeout.

## Actual Spark partitions and cluster evidence — 11a/11b

With the supported JDK and Spark environment configured:

```bash
python -m projects.stage11.partition_lab --spark --rows 1000000
python -m projects.stage11.solution --rows 1000000 --output work/reference_answers/stage11-parquet
```

Expected total is **4,999,500,000 cents**, with 50 account aggregates. The new lab compares 2/8/32 partitions, hot-key salting, and broadcast plans. Inspect `Exchange` operators and reconcile every aggregate. The original job writes Parquet, anomalies, and rolling statistics; its three-row window is not three calendar days. Use a fresh output folder when repeating.

For an actual cluster, adapt the example's `SparkSession.builder.master('local[2]')` to the cluster-provided master configuration and replace local paths with shared storage. Supply the same Python dependencies to executors, run via that cluster's submission mechanism, record application/executor IDs and task distribution, then rerun row/schema/total/group checks after writing and reading Parquet. Until those observations exist, the correct status is **local engine tested; cluster operation pending**.

## Evaluation labels, model comparisons, and human review — 13a/13b

Run the worked labeling and paired-comparison harness:

```bash
python -m projects.stage13.evaluation_lab --split dev
python -m projects.stage13.solution --split dev
```

The sixty numeric reference questions span six fictional statement families with a source-disjoint 40/20 split. They illustrate golden labels and citations; they are not sixty independent human annotations. Freeze a reviewed version before tuning. Expand the capstone to 100–500 cases across genuinely new source families with this explicit record contract:

```json
{
  "id": "aurora-comparison-001",
  "split": "dev",
  "group": "aurora-2024-2025",
  "tenant": "A",
  "question": "How much did Aurora revenue grow from 2024 to 2025?",
  "category": "multi_source_numeric",
  "expected_status": "answered",
  "expected_value": "0.20",
  "expected_unit": "fraction",
  "source_ids": ["aurora-2024", "aurora-2025"],
  "derivation": "(144 - 120) / 120",
  "label_status": "reference; human review pending"
}
```

Companion worked labels: same question for tenant B → unavailable/404 and no source content; unknown company → unknown/404; unavailable model → visible dependency failure, never a made-up answer; Aurora 2030 → unsupported; a draft citing `made-up-2030` → citation failure. Keep cases using related source families together when making your own train/holdout split. The schema above is an expansion template; adapt the harness loader explicitly instead of assuming arbitrary JSON will be accepted by the existing numerical evaluator.

Compare embedding models with `retrieval_lab --model ... --revision ...` using identical dev cases, and compare chunk sizes with `evaluation_lab`. Use independent output directories; resample paired differences by shared source groups. Record sample counts, failure rates, latency, numerical accuracy, retrieval recall/MRR, and abstention separately. Holdout is for the selected release, not repeated tuning.

Worked judge decision: “Aurora revenue grew 20%, source aurora-2025” has a correct percentage but incomplete evidence because growth needs both years. Supply both statements; the arithmetic is `(144-120)/120=.2`. “Aurora is guaranteed to outperform” is unsupported regardless of the citation. Human reviewers mark each claim supported/unsupported/uncertain and reconcile disagreements while blinded to model identity. Calibrate an automated judge against that reviewed subset and include text attempting to manipulate the judge. A deterministic numerical pass cannot certify narrative support.
