# Assessment answers and reviewer guide

The tasks use changed data, so evaluate invariants and reasoning rather than memorized outputs. Each item below describes what a strong answer must show.

| Stage | Expected answer / evidence | Common failure |
|---|---|---|
| 00 | Print sys.executable, show isolated dependencies, execute from a fresh kernel/process, explain the changed lines in Git | Relying on hidden notebook state |
| 01 | Parse with csv, validate date/quantity/finite money, aggregate typed values, return clear errors, test quoted/empty/malformed input | split(',') and float-money totals without a policy |
| 02 | For MSE: dw=2 mean(x(wx+b−y)), db=2 mean(wx+b−y); converge near w=3,b=−2; posterior accounts for false positives and prevalence | Wrong derivative sign, n−1 mean denominator, ignored base rate |
| 03 | Left join retains customers without orders, COALESCE gives zero; running sum uses explicit ordering/frame; transaction rolls back all writes | Join multiplication, interpolated SQL, trusting caller tenant |
| 04 | Remove future/resolution-only feature, split related examples correctly, fit transforms within training folds, choose on validation, test once | Reporting a tuned-on-test score as generalization |
| 05 | zero_grad before backward, optimizer.step after backward, train/eval correctly, no_grad validation, checkpoint selected on validation | Fixing loss display without fixing gradient accumulation |
| 06 | Causal mask blocks future keys; shifted targets predict next token; changed future input leaves earlier logits unchanged; LoRA uses r(in+out) parameters | Shape-only tests that miss semantic leakage |
| 07 | Verify extraction and source offsets, inspect relevant candidate presence, separate ranking from generated claim support, enforce permissions before context | Blaming all errors on the LLM or checking citation existence only |
| 08 | Strict tool registry and args, verified principal outside model state, per-call timeouts, global budgets, structured failure, approval bound to exact request | Generic approved=True or invented successful tool output |
| 09 | Record model/hardware/context/concurrency, cold and warm distributions, token counts, p50/p95, timeout behavior; distinguish TTFT from total time | Quoting theoretical weight memory as actual peak use |
| 10 | Reproducible container configuration, private network/secrets, ready check, restored counts/totals, compatible rollback/migration plan | A backup file without a restore check |
| 11 | Sum partial sums/counts, explicit schema, inspect Exchange/shuffle, detect hot keys, avoid collecting large data, verify Parquet round trip | Unweighted average of partition averages |
| 12 | Allowed control succeeds, unauthorized one fails at data/tool boundary, malicious document cannot change identity, logs/caches/state remain scoped | Passing by denying everything or relying only on prompt wording |
| 13 | Paired cases and group-aware uncertainty, denominators and slices, predefined gates, no safety failure averaged away | A single unqualified overall accuracy |
| 14 | Normalize statement/price/share units, use proper denominator definitions, preserve undefined ratios, join by known-at time, chronological folds | Joining a fiscal-year report before publication |
| 15 | Trace one request end to end, identify component responsibilities, demonstrate unfamiliar change, reproduce deployment and a failure/restore drill | A memorized architecture diagram without working evidence |

For the financial comparison, Aurora 2025 revenue is 144 million USD, margin 36/144=25%, and FCF 32−8=24 million. Beacon 2025 revenue is 108, margin 15/108≈13.89%, and FCF 18−6=12. A correct answer cites the matching source rows and publication dates and does not infer investment merit from these numbers alone.

Reviewers should ask “What evidence would change your conclusion?”, “Which input would break this assumption?”, “What can this test not prove?”, and “How would you localize a failure?” Award reasoning and observable evidence, not confidence of presentation. Reassess fragile skills after a delay.
