# Course data

All fixtures are authored or deterministically generated for this course. They contain no real customer records, confidential filings, or live market data. Regenerate with `python tools/make_datasets.py`; doing so replaces these fixtures, so keep your own data under work/.

| File | Contents | Useful expectations |
|---|---|---|
| expenses.csv | Six valid expense rows | Total 100.00; each month 50.00; Food 55.00, Transport 15.00, Books 30.00 |
| financials.csv | Aurora and Beacon, 2023–2025 | Currency USD; statement amounts and shares in millions; stock prices per share |
| documents.json / reports/ | Nine short documents | Six financial summaries, public expense policy, B-only private document, A-only injection fixture |
| tickets.csv | 36 independently worded but authored tickets | Three classes, fixed 24/6/6 train/validation/test rows, explicit template groups |
| prices.csv | 240 synthetic daily observations | Includes calendar days, not an exchange trading calendar; no predictive edge claimed |
| tiny_corpus.txt | Repeated short instructional text | Suitable for testing a tiny LM’s mechanics, not language generalization |
| evals.jsonl | Nine smoke cases with dev/holdout labels | Seed examples for an evaluation process, not the capstone’s final 100–500 cases |

Financial conventions: capex is a positive cash outflow; FCF = operating cash flow − capex. Period year and publication date are distinct. The simplified fictional net income is 75% of operating income. Statements are not a full accounting model. Never substitute these fixtures for a real financial analysis.

The digits project uses the bundled `sklearn.datasets.load_digits` dataset; consult its dataset documentation for provenance when preparing a public portfolio. No dataset download is needed for that project.

Seed: 42 for prices and model examples. Record software versions and data hashes because a seed alone does not guarantee identical results across platforms.
