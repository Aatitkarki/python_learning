# Independent mastery assessments

Take each assessment after its stage project. Close solved notebooks and reference code. Documentation is allowed for library syntax after you explain the intended approach; do not use AI to generate the implementation during the timed independent portion. Ask another person to change inputs or choose a comparable unseen task when possible.

A visible exercise test checks correctness on known cases. These assessments check transfer, explanation, and debugging. Record what you could do without help, then study the answer rubric and repeat after 7 and 30 days.

| Stage | Independent task | Time | Critical evidence |
|---|---|---:|---|
| 00 | Recreate an environment, run code, debug a name error, make a commit | 45m | Correct interpreter, fresh execution, explained diff |
| 01 | Inventory CSV summarizer with quantity/price validation and tests | 90m | Correct totals, empty/bad input handling, clean interfaces |
| 02 | Fit y=3x−2 manually; derive/check gradients; explain a Bayesian alert | 90m | Shape reasoning, gradient agreement, base-rate reasoning |
| 03 | Persistent orders API plus customer left join and running sum | 120m | Transactions, parameter binding, validation, access boundaries |
| 04 | Train a new ticket/demand model with a deliberately leaky feature present | 120m | Remove unavailable feature, honest split, baseline, error analysis |
| 05 | Repair a neural training loop with accumulated gradients and eval-mode errors | 90m | Reproduction, correct fix, loss/gradient evidence |
| 06 | Detect a future-token leak and explain a low-rank adapter | 120m | Perturbation test, shifted targets, rank/shape calculation |
| 07 | Add a new document format and diagnose a wrong sourced answer | 120m | Parsed source inspection, retrieval metrics, claim support |
| 08 | Build a bounded three-tool workflow and reject changed approval arguments | 120m | Correct calls/results, no invented output, safe termination |
| 09 | Explain a real model-serving benchmark and a timeout | 90m | Actual runtime/memory/latency data and limits |
| 10 | Reproduce deployment, break a dependency, restore into a new database | 180m | Controlled failure, verified restore, repeatable runbook |
| 11 | Reconcile a skewed Spark aggregation and explain its physical plan | 120m | Real job output, correct sum/count, shuffle explanation |
| 12 | Attack your own app with an unseen cross-tenant and indirect-injection case | 90m | Positive/negative access tests, scope enforced in code |
| 13 | Audit a misleading evaluation and decide whether a candidate can ship | 120m | Case pairing, slices, uncertainty, hard-gate reasoning |
| 14 | Correct a financial report with unit and publication-time errors | 90m | Corrected values, source timestamps, valid comparison |
| 15 | Add an unseen feature and defend the complete system | 90m + defense | Independent code, operational evidence, architecture explanation |

## Scoring

- **40 points: correctness and reasoning.** Results satisfy the contract; mathematical/data assumptions and units are explicit.
- **25 points: independence and transfer.** You produce a working solution without reading the reference, including changed inputs.
- **20 points: tests and debugging.** You choose meaningful normal/boundary/error tests, reproduce a failure, and explain the fix.
- **15 points: explanation and reproducibility.** Another person can run your work; you can explain each component and limitation.

Pass at **80/100**, with no critical failure. Critical failures include test leakage, unauthorized disclosure, fabricated tool/evidence results, unsafe unbounded execution, or an essential result that cannot be reproduced. An unrun live service/cluster requirement stays pending. A score from your own review is provisional; use peer review for final defense when available.

## Failure and reassessment

Identify the earliest concept responsible, return to its notebook, and solve a smaller example. Reassess with different data at least 48 hours later. Record help received honestly. Passing after copying a solution is a practice success, not an independent pass.

[Answer and reviewer guide](ANSWERS.md)
