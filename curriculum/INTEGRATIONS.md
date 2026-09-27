# Live integration labs

These labs are part of the advanced completion gates. Offline unit tests are useful preparation; they do not count as having run a server, downloaded a pretrained model, or operated a cluster. Keep unrun integrations marked pending in progress.md.

## PostgreSQL and the API — Stages 03 and 10

Install and start Docker with Compose, then follow [the runbook](../projects/stage10/RUNBOOK.md). Create a local `.env` using `python tools/create_local_env.py`. The API reads `DATABASE_URL` and uses the same parameterized repository interface for SQLite or PostgreSQL. Compose configures PostgreSQL automatically; local Python uses SQLite by default.

After `docker compose up --build -d`, verify `/ready`, POST records, restart only the API, and verify totals. Record database/image versions and actual queries. Run the SQL worksheet in EXTRA_LABS.md against PostgreSQL, inspect `EXPLAIN ANALYZE`, and demonstrate a rolled-back transaction. A working SQLite demo does not pass this gate.

## Pretrained transformers and PEFT — Stage 06

Install `requirements/deep.txt`. First run the no-download adapter check:

```bash
python -m projects.stage06.pretrained --offline-smoke
```

Then choose a compatible sequence-classification architecture, review its model card/license and memory requirements, and pin an immutable model revision. Example command shape:

```bash
python -m projects.stage06.pretrained --model distilbert/distilbert-base-uncased --revision MODEL_COMMIT --epochs 3
```

Replace `MODEL_COMMIT` with the actual commit hash from the chosen model repository. The script downloads the weights and tokenizer, adds LoRA, trains on course tickets, selects an epoch on validation, and evaluates test once. It starts with an untrained task head when using a base model; that is not a strong pretrained classifier baseline. Compare against a separately task-trained model if appropriate.

Record model ID/revision, tokenizer, license, trainable/total parameters, runtime, memory, validation/test scores, and failed examples. QLoRA is an additional hardware-dependent extension: use a supported quantization backend and measure actual memory and quality. A numerical INT8 simulation is not equivalent to that run.

## Learned embeddings + pgvector — Stage 07

Install `requirements/integration.txt` and start the database. In the activated terminal, load your generated `.env` and set the localhost DSN:

```bash
set -a
source .env
set +a
export DATABASE_URL="postgresql://learner:${POSTGRES_PASSWORD}@127.0.0.1:15432/learning"
python -m projects.stage07.integration --model sentence-transformers/all-MiniLM-L6-v2 --revision MODEL_COMMIT --tenant A --query "Aurora 2025 revenue"
```

Use a real immutable revision. This command downloads the selected embedding model. Optionally add `--reranker CROSS_ENCODER_ID --reranker-revision COMMIT` after reviewing that model. Add `--ollama INSTALLED_MODEL` for a local generated draft.

The script scopes records before retrieval, stores model versions with vectors, uses exact cosine search and PostgreSQL lexical ranking, combines rankings with RRF, and optionally reranks. It uses a small exact index for clarity; add a dimension-specific ANN index only after measuring recall and filter behavior. Its `ts_rank_cd` lexical scorer is not BM25. The draft is explicitly unverified until you assess claim support and citations.

Use `parse_document` from the same module to inspect PDF/HTML/DOCX/Markdown/JSON parsing. It does not provide OCR, layout-aware table reconstruction, or page-level citations for every format. For your project, retain page/section boundaries and inspect every numeric table. Never treat a successful parse call as proof of correct extraction.

## Ollama and vLLM — Stage 09

Install a server appropriate for your machine using its current official documentation. Choose and download a model deliberately; no server or model download happens automatically in the course checks. Confirm the model ID with your server’s model-list command.

```bash
python -m projects.stage09.serve --model INSTALLED_MODEL --runs 30
```

This defaults to Ollama at `http://127.0.0.1:11434`. For a vLLM server on a supported host, select `--backend vllm --url http://127.0.0.1:8000 --model SERVED_MODEL`. The learning API also defaults to port 8000, so run the servers on different ports or hosts and pass the right URL.

Record first-load timing separately. The supplied client measures non-streaming elapsed time; extend it for streaming TTFT, inter-token latency, cancellation, and concurrent throughput. Keep inference endpoints private or behind authenticated access. The provided client is designed for your private/local lab; adapt authentication before using an endpoint that requires it.

## Spark — Stage 11

Install `requirements/spark.txt` and a Java version supported by the pinned Spark release (the course validation uses Java 21). Check `java -version` and set `JAVA_HOME` if your installation requires it. Use a full supported JDK: the Android Studio runtime found during validation lacked `jdk.incubator.vector`, despite reporting Java 21. The local notebook/job sets `PYSPARK_PYTHON` to its active Python interpreter so workers do not accidentally use system Python 3.9.

```bash
python tools/check_course.py --kernel --groups spark --only 11b
python -m projects.stage11.solution --rows 1000000 --output work/spark-million
```

Use a new output directory for each run. If the driver cannot resolve its own host in a local lab, `SPARK_LOCAL_IP=127.0.0.1` can help; do not blindly apply localhost settings to a multi-host cluster. Local Spark exercises the real engine but does not demonstrate executor deployment, remote storage, or production cluster operations.

## Required integration evidence

For each lab save: setup commands with secrets redacted, service/model/library versions, input/data hashes, actual outputs, one induced failure, recovery behavior, and a short interpretation. “Not available on my machine” is a valid pending status; never replace it with a fabricated benchmark or a passed checkbox.
