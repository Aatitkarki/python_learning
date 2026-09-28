# Stage 00: question-by-question solutions

[All-stage answer index](../../curriculum/ANSWER_INDEX.md) · [Project brief](README.md)

`solution.py` is the main project reference. It does not contain every answer. Use the exact question IDs below to find the smaller exercises and extra programs.

**Suggested workflow:** notebook → independent assignment in your own `.py` files → stage project → closed-book gate. Compare answers only after an attempt; then close them and rebuild with changed input.

## Notebook questions and independent assignments

### 00a: Your first reproducible experiment

[Test your independent assignment](../../curriculum/assignments/00a.md)

| ID | Question | Answer |
|---|---|---|
| 00a-E1 | Return total hours for nonnegative weeks and hours_per_week; reject negative inputs. | [Worked solution](../../curriculum/answers/00a.md#00a-e1) |
| 00a-E2 | Return a dictionary containing seed and Python version (under keys seed, python). Import sys inside your function. | [Worked solution](../../curriculum/answers/00a.md#00a-e2) |
| 00a-E3 | Return n integer die rolls using a private random.Random(seed). | [Worked solution](../../curriculum/answers/00a.md#00a-e3) |
| 00a-O1 | Why restart a kernel? | [Worked solution](../../curriculum/answers/00a.md#00a-o1) |
| 00a-O2 | Is a notebook a deployed service? | [Worked solution](../../curriculum/answers/00a.md#00a-o2) |
| 00a-T | Create work/hello.py, run it from the terminal, then reproduce it in a fresh notebook. Make a Git commit in your own learning repository and explain the diff. | [Worked solution](../../curriculum/answers/00a.md#00a-t) |

## Project tasks, in brief order

<a id="00-p1"></a>
### 00-P1

**Question:** Create your own notes/, work/, tests/, and project folders; keep secrets and environments out of Git.

**Answer:** [00a worked implementation and explanation](../../curriculum/answers/00a.md#00a-t)

<a id="00-p2"></a>
### 00-P2

**Question:** Run hello.py from terminal and notebook. Record the interpreter path and explain any differences.

**Answer:** [00a worked implementation and explanation](../../curriculum/answers/00a.md#00a-t)

<a id="00-p3"></a>
### 00-P3

**Question:** Create a branch, make two commits, inspect a diff, resolve a small practice conflict, and push to your own GitHub repository.

**Answer:** [00a worked implementation and explanation](../../curriculum/answers/00a.md#00a-t)

<a id="00-g"></a>
## Mastery gate: 00-G

**Task:** On a fresh terminal, create an environment, run a script, recover from an intentional NameError, and show a commit. Explain AI, ML, DL, NLP, CV, RL, LLMs, agents, data science, and engineering in your own words.

**Expected reasoning and invariant outputs:** The manifest must contain Python version, seed 42, and the actual SHA-256 of expenses.csv. A changed byte changes the hash. Use git status/diff/log to explain exactly what a commit contains. Do not commit .venv, .env, or generated local databases.

Use the question-specific implementations above and [the reviewer answers](../../curriculum/assessments/ANSWERS.md). For deployment or model experiments, use [the worked operational procedures](../../curriculum/answers/OPERATIONS.md).

**Pass criteria:** 80/100 across correctness/reasoning (40), independent implementation (25), tests/debugging (20), and explanation/reproducibility (15). No permission leak, future-data leakage, invented evidence, or unreproducible core result. Live requirements remain pending until actually run. Running the answer files does not establish your independent mastery.

**If the gate fails:** If interpreter/kernel confusion remains, repeat the same three-line program in terminal and notebook and print sys.executable in each.
