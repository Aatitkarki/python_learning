# Start here — your AI engineering course

This course turns [your original README](readme.md) into a beginner-to-advanced learning path with **36 practice notebooks, 36 worked-answer notebooks, 108 checked exercises, and 16 practical project stages**. It follows your choice to start from Python basics.

Budget **1,200 hours**, or about **80 weeks at 15 hours/week**. Move forward when you can build, debug, and explain the stage independently. Completing files by copying answers will not establish mastery; use the assessments and delayed reviews to check your understanding.

## Your first session

1. Set up Python and Jupyter below.
2. Open [00a — Your first reproducible experiment](curriculum/notebooks/00a_your_first_reproducible_experiment.ipynb).
3. Read the lesson, predict and run the example, then solve the three exercises. `NotImplementedError` in a practice cell is intentional until you implement it.
4. Save your copy under work/. Try before reading [the answer notebook](curriculum/solutions/00a_your_first_reproducible_experiment.ipynb).
5. Record the session in [progress.md](progress.md), then follow [the first 30 days](curriculum/FIRST_30_DAYS.md).

## Setup

Use **Python 3.12** for the supported course environment. Your original system Python was 3.9; leave it alone. A workspace `.venv` has been prepared and tested. Its Python interpreter is stored locally under ignored `.runtime/`, so it does not depend on a temporary directory. On this Mac you can start now with `source .venv/bin/activate` followed by `python -m jupyter lab`. If you move the course to another machine, recreate the environment below.

With an installed Python 3.12, from this folder:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements/core.txt
python -m jupyter lab
```

If you use `uv`, a durable alternative is `uv venv --python 3.12 .venv`, followed by `uv pip install --python .venv/bin/python -r requirements/core.txt` and `.venv/bin/python -m jupyter lab`. On Windows, use `.venv\Scripts\Activate.ps1` instead of `source`; invoke installed Python 3.12 with `py -3.12` when appropriate.

Choose the notebook kernel from this environment. If imports fail, run `import sys; print(sys.executable)` in the notebook and compare it with your terminal. Restart the kernel and run all cells after changes. Foundations use only Python’s standard library; Jupyter provides the interface.

Install additional groups only when you reach them:

| Stage | Install | Other needs |
|---|---|---|
| 00–04 and most later exercises | `requirements/core.txt` | Laptop CPU; no paid API |
| 05–06 | `requirements/deep.txt` | CPU works for supplied tiny models; pretrained lab downloads a selected model |
| 08 | `requirements/agents.txt` | No API key for deterministic graph labs |
| 07 integrations | `requirements/integration.txt` | PostgreSQL/pgvector and a selected embedding model |
| 09 | Server-specific setup | An installed Ollama model; vLLM needs a compatible host |
| 10 | Docker + Compose | Running daemon and local `.env` |
| 11 | `requirements/spark.txt` | Compatible Java runtime; local Spark is not a cluster |

Do not install every model or framework immediately. [Integration instructions](curriculum/INTEGRATIONS.md) identify exactly what each live lab needs. Package ranges support learning; [the validation report](curriculum/VALIDATION.md) records the environment actually checked. API and dependency versions evolve; review the linked primary docs when upgrading.

## Navigate the course

- [Full plan and 80-week schedule](curriculum/PLAN.md)
- [First 30 days, session by session](curriculum/FIRST_30_DAYS.md)
- [Roadmap coverage and evidence](curriculum/COVERAGE.md)
- [Stage guides](curriculum/stages/00.md), linking every notebook, answer, and project
- [Supplementary explanations and lab answers](curriculum/EXTRA_LABS.md)
- [Primary learning resources](curriculum/RESOURCES.md)
- [Starting diagnostic](curriculum/assessments/DIAGNOSTIC.md)
- [Mastery assessment](curriculum/assessments/MASTERY.md) and [answer/rubric guide](curriculum/assessments/ANSWERS.md)
- [Final capstone requirements](curriculum/CAPSTONE.md)
- [Dataset descriptions and expected values](datasets/README.md)
- [Progress log](progress.md)

## Run and verify reference work

Activate the environment first. To run the complete offline verification suite, install `requirements/test.txt`; individual projects need only their listed group. These commands run offline examples without paid services:

```bash
python -m projects.stage01.solution
python -m projects.stage03.solution
python -m projects.stage04.solution
python -m projects.stage05.solution
python -m projects.stage06.tiny_lm
python -m projects.stage07.solution
python -m projects.stage08.solution
python -m projects.stage12.solution
python -m projects.stage13.solution --split dev
python -m projects.stage14.solution
python -m projects.stage15.solution
python -m pytest -q
python tools/check_projects.py
python tools/check_course.py --kernel --groups stdlib,data,deep,agents
```

The notebook checker validates both template sets and executes **solutions**, not unfinished practice cells. It saves executed copies and a report under work/. Add `spark` to the group list after setting up Java/Spark. Groups excluded from a run are explicitly reported as not run. `python tools/check_course.py` executes cells in fresh Python processes if a Jupyter kernel cannot start.

For the API, generate a local environment file with `python tools/create_local_env.py`, load it as described in the runbook, and run `python -m uvicorn projects.api:app --host 127.0.0.1 --port 8000`. The API has no usable default credential. Keep the generated `.env` private.

## What is included, and what you must still demonstrate

The checked notebooks and reference applications give you concrete answers. Live model serving, downloaded pretrained models, database/vector integrations, deployments, cluster operations, and a larger independently labeled evaluation set require your own observed evidence. The included financial data is fictional. The local research API returns source quotes and deterministic calculations; the separate integration lab adds learned embeddings and optional model drafting. Its generated draft still needs support evaluation.

Use the code as a reference implementation after your attempt. The larger projects intentionally require decisions, measurement, and debugging that a single canned answer cannot substitute for. The course’s graduation standard is independent performance on new tasks, not a promise of automatic expertise after a fixed number of hours.
