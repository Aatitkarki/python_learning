# Answer update validation — 2026-09-28

[Answer index](../ANSWER_INDEX.md) · [Machine-readable results](../validation/answers.json)

- **304 question records checked:** 108 exercises, 72 oral questions, 36 independent assignments, 72 project tasks, 16 mastery gates. The checker compares exact authored question text, implementation paths, answer anchors, and exported exercise code/checks.
- **79 tests passed**, including regression checks for missing/stale answer mappings and the new implementations.
- **All 36 exported exercise scripts passed** in fresh Python processes, including the Spark script with a full Java 21 JDK.
- **15 extra lab entry points passed** using local/default modes; the saved classifier artifact also round-tripped through HTTP with identical predictions.
- **Local Spark:** one million rows, 50 aggregates, exact total 4,999,500,000 cents at 2/8/32 partitions; salted aggregates reconciled and broadcast join retained one million rows. Recorded timings include warmup/order effects and are not a universal performance ranking.
- **Security:** 50 endpoint/principal matrix checks plus adversarial, resource-scope, and cache/revocation checks passed. See [observed checks](../validation/answer-security.json).
- **Preservation:** SHA-256 comparison verified 36 practice notebooks, 36 existing work notebooks, and progress.md unchanged (73 files).
- **Generator:** rerunning the answer-only builder produced identical reference files. All local Markdown targets were checked.

Run these from the repository root with the course dependencies installed:

```bash
python tools/check_answers.py
python tools/check_links.py
python -m pytest -q
python projects/stage01/notebook_solutions/01a.py
python -m projects.stage01.expense_app.cli datasets/expenses.csv
```

For the advanced checks:

```bash
python -m projects.stage04.persistence
python -m projects.stage12.security_lab
python -m projects.stage13.evaluation_lab
python -m projects.stage11.partition_lab --spark --rows 1000000
```

The last command requires the supported Java/PySpark setup. The full exercise exports require the environment group listed in their lesson answers. New reports normally write beneath work/reference_answers/; existing notebook files are not rewritten.

**Not executed in this update:** live PostgreSQL/pgvector; downloaded pretrained/embedding/reranker models; CUDA QLoRA; Ollama/vLLM serving; Docker/Coolify deployment and PostgreSQL restore; a remote Spark cluster. These have actual implementation files and [worked operational procedures](OPERATIONS.md), with required observations clearly distinguished from local validation. No independent learner assessment or peer reproduction is claimed.
