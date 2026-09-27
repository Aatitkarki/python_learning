# Course validation

Checked on **2026-09-27** on macOS arm64, Python **3.12.13**. This report describes checks of the supplied materials, not a learner’s mastery score or proof of production readiness.

## Completed checks

| Check | Result |
|---|---|
| Notebook structure and Python syntax | All 72 notebooks validated; all code cells compiled |
| Solution notebook execution | **36/36 passed in actual Jupyter kernels**, including PyTorch, LangGraph, and local Spark |
| Checked exercises | **108** exercises with worked answers, executable checks, hints, and explanations |
| Project/application tests | **29 passed**: parsing/money, persistence, API validation, permissions, limits, SQL-like inputs, approval, bounded tools, causal attention, gradients, classifier API, time splits, evaluation |
| Offline reference commands | **16 passed**, including actual CNN/tiny-LM training and a real PEFT adapter update |
| Spark project | **1,000,000 rows**, 50 groups, total **4,999,500,000 cents**, matching an independent Python sum; Parquet outputs written |
| Docker Compose | Configuration passed using installed `docker-compose config --quiet` |
| Python sources | Compiled successfully |
| Local navigation | Checked with `tools/check_links.py`; no missing local targets at delivery |

Notebook results are archived in [validation/notebooks.json](validation/notebooks.json); reference command results in [validation/projects.json](validation/projects.json). Executed notebook copies, raw project outputs, Spark Parquet files, and logs are under ignored `work/`. Re-run checks after changing code or dependencies.

## Observed model results

These are instructional measurements on the supplied data, not performance promises:

- Ticket classifier: logistic regression selected on validation; 1.0 test accuracy on **six authored test tickets**. The tiny, simple fixture does not demonstrate real-world quality.
- Digits CNN: approximately **96.11%** accuracy on 360 held-out digit examples after validation checkpoint selection.
- Tiny transformer: training loss decreased from approximately **3.466** to **1.245**; sampled validation loss approximately **1.188**. The corpus repeats short authored sentences, so this does not demonstrate general language ability.
- Offline LoRA smoke test: real adapter gradient/update on a random tiny BERT, loss approximately **1.099**, 307 trainable parameters. This was **not** a downloaded pretrained model evaluation.

## Environment details and issues fixed

Key installed versions: NumPy 2.5.3, Pandas 2.3.3, scikit-learn 1.9.1, PyTorch 2.14.0, FastAPI 0.141.1, Pydantic 2.13.5, LangGraph 1.2.12, Transformers 4.57.6, PEFT 0.21.0, PySpark 4.0.4. The complete observed environment is in [requirements/validated-macos-py312.txt](../requirements/validated-macos-py312.txt). It is a macOS validation snapshot, not a cross-platform hashed release lock; use the named requirement groups for a new platform and revalidate.

The original system interpreter was Python 3.9.6. A separate Python 3.12 environment was created for the course; the system Python was not replaced. The local runtime now lives under `.runtime/` and dependencies under `.venv/`, both excluded from source control and Docker builds.

The active Android Studio Java 21 runtime lacked `jdk.incubator.vector`. Spark passed using a separate complete temporary Temurin JDK 21.0.12.1. Your global Java configuration was not changed. For future Spark sessions, install/select a complete supported JDK and set JAVA_HOME for that session. The temporary validation JDK path may be removed by system cleanup; it is not a permanent installation.

Spark also initially selected system Python 3.9 for workers while the notebook used Python 3.12. The local examples now set worker Python to `sys.executable`. Jupyter and Spark required local sockets unavailable in the restricted sandbox; real-kernel checks ran with that local access enabled.

## Not run here

- Docker image build/container startup and PostgreSQL-backed service execution: the Docker engine was not running. The standalone Compose configuration was validated.
- Live pgvector/learned-embedding/reranker integration: no running PostgreSQL service or downloaded embedding model was configured.
- Downloaded pretrained transformer fine-tuning: only the separate no-download adapter smoke path was run.
- Ollama/vLLM requests, GPU inference, QLoRA, streaming/concurrent serving benchmarks: no configured server/model/GPU target.
- Coolify deployment, HTTPS, external identity provider, production monitoring, durable distributed limits, backup/restore, or a multi-machine Spark cluster.
- The larger independent evaluation corpus and real-world portfolio evidence: these are learner deliverables. The automated retrieval command used the development smoke fixtures; it is not a capstone-scale evaluation.

These are explicitly pending integration/operational milestones, with commands and acceptance evidence in [INTEGRATIONS.md](INTEGRATIONS.md), [the runbook](../projects/stage10/RUNBOOK.md), and [CAPSTONE.md](CAPSTONE.md).

## Reproduce the checks

```bash
source .venv/bin/activate
python -m pip install -r requirements/test.txt
python -m pytest -q
python tools/check_course.py --kernel --groups stdlib,data,deep,agents
python tools/check_projects.py
python tools/check_links.py
```

For Spark, install its requirements and a complete supported JDK, then run the commands in INTEGRATIONS.md. The checker reports excluded groups as not run. A successful offline test cannot replace a required live integration.
