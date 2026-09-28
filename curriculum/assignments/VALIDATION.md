# Assignment tests and notebook enrichment validation

Validated 2026-09-28. [Machine-readable report](../validation/learning-expansion.json).

- 36 assignment test packs, each with a blank starter, explicit interface, reference adapter, and additional completion-evidence checklist.
- **143 offline acceptance cases passed** against the references; one live Spark case was skipped by default.
- The separate `11b --reference --live-spark` run passed both its reference precheck and actual Spark partition/skew/broadcast integration case. This validates all 144 distinct acceptance cases in the configured local environment.
- **84 regression tests passed**, including a valid learner implementation that passes, an invalid learner implementation that fails, and a missing file that never silently falls back to the reference.
- Ordinary `pytest` deliberately skips the 144 independent cases when no learner/reference target is selected. Run the explicit command below to exercise them.
- All 72 updated notebooks validate. Their 360 supplementary local links resolve. Original cells, answers, outputs, and metadata were retained from the pre-enrichment backups; 38 other existing learner files stayed byte-identical.
- The enrichment tool is idempotent, refuses to overwrite edited supplementary text, and detects a file changed while an update is being prepared. Notebook backups are under `work/backups/notebook-enrichment/`.
- The future notebook generator was validated in memory for 72 templates; existing notebooks were not regenerated.

```bash
python tools/test_assignment.py --all --reference
python tools/check_learning_materials.py
python tools/check_links.py
python -m pytest -q
```

For your own work, use `python tools/test_assignment.py 01a --solution work/assignments/01a.py`. A reference pass does not assess that file. `--case calculator` selects only matching test names; remove it for the full pack.

With the supported JDK, PySpark, and loopback sockets, the actual local Spark check is:

```bash
python tools/test_assignment.py 11b --reference --live-spark
```

No live PostgreSQL/model-serving/deployment/remote-cluster outcome, human review, independent mastery gate, or peer reproduction is inferred from offline tests. Each assignment guide names its remaining evidence requirements.
