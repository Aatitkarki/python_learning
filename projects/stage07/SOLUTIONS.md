# Stage 07: question-by-question solutions

[All-stage answer index](../../curriculum/ANSWER_INDEX.md) · [Project brief](README.md)

`solution.py` is the main project reference. It does not contain every answer. Use the exact question IDs below to find the smaller exercises and extra programs.

**Suggested workflow:** notebook → independent assignment in your own `.py` files → stage project → closed-book gate. Compare answers only after an attempt; then close them and rebuild with changed input.

## Notebook questions and independent assignments

### 07a: Retrieval from first principles

[Test your independent assignment](../../curriculum/assignments/07a.md)

| ID | Question | Answer |
|---|---|---|
| 07a-E1 | Return word chunks with size>0 and 0<=overlap<size. Avoid an extra final chunk made only of overlap. | [Worked solution](../../curriculum/answers/07a.md#07a-e1) |
| 07a-E2 | For dicts with id,text, rank documents by number of shared unique lowercase alphanumeric terms; omit zero scores, break ties by id. | [Worked solution](../../curriculum/answers/07a.md#07a-e2) |
| 07a-E3 | Combine ranked ID lists using sum(1/(c+rank)), rank starting at 1. Count an ID at most once per list; tie-break by ID. | [Worked solution](../../curriculum/answers/07a.md#07a-e3) |
| 07a-O1 | Why keep source offsets? | [Worked solution](../../curriculum/answers/07a.md#07a-o1) |
| 07a-O2 | What can reranking fix? | [Worked solution](../../curriculum/answers/07a.md#07a-o2) |
| 07a-T | Build a private document index with chunk IDs, source offsets, parser version, and content hashes. Compare keyword, embedding, hybrid, and reranked recall on the same labeled questions. | [Worked solution](../../curriculum/answers/07a.md#07a-t) |

### 07b: Grounding, permissions, and vector search

[Test your independent assignment](../../curriculum/assignments/07b.md)

| ID | Question | Answer |
|---|---|---|
| 07b-E1 | Return public documents or documents with tenant equal to the authenticated tenant. Do not infer identity from the query text. | [Worked solution](../../curriculum/answers/07b.md#07b-e1) |
| 07b-E2 | Using TF-IDF, rank authorized nonzero-scoring documents. Return (id,score) pairs, sorted descending then id. Empty input returns []. | [Worked solution](../../curriculum/answers/07b.md#07b-e2) |
| 07b-E3 | Return status=unsupported with empty citations when no hits; else status=evidence with exact quotes and IDs. Do not synthesize a claim. | [Worked solution](../../curriculum/answers/07b.md#07b-e3) |
| 07b-O1 | Can a citation be valid but misleading? | [Worked solution](../../curriculum/answers/07b.md#07b-o1) |
| 07b-O2 | Why filter before model access? | [Worked solution](../../curriculum/answers/07b.md#07b-o2) |
| 07b-T | Run the pgvector lab, ingest Markdown plus one PDF, and answer through Ollama. Evaluate access isolation, paraphrases, exact numbers, unsupported questions, and malicious retrieved instructions. | [Worked solution](../../curriculum/answers/07b.md#07b-t) |

## Project tasks, in brief order

<a id="07-p1"></a>
### 07-P1

**Question:** Build the lexical baseline and label relevant source chunks for questions before tuning.

**Answer:** [07a worked implementation and explanation](../../curriculum/answers/07a.md#07a-t)

<a id="07-p2"></a>
### 07-P2

**Question:** Ingest at least three formats, inspect extracted tables, and retain source/version/page or offset metadata.

**Answer:** [07b worked implementation and explanation](../../curriculum/answers/07b.md#07b-t)

<a id="07-p3"></a>
### 07-P3

**Question:** Run learned embeddings and pgvector integration; compare keyword, dense, RRF hybrid, and cross-encoder reranking.

**Answer:** [07a worked implementation and explanation](../../curriculum/answers/07a.md#07a-t) · [07b worked implementation and explanation](../../curriculum/answers/07b.md#07b-t)

<a id="07-p4"></a>
### 07-P4

**Question:** Add a local generator and claim-level citation review; distinguish unsupported answers from empty retrieval.

**Answer:** [07b worked implementation and explanation](../../curriculum/answers/07b.md#07b-t)

<a id="07-p5"></a>
### 07-P5

**Question:** Test two tenants, public documents, permission changes, stale indexes, and malicious document instructions.

**Answer:** [07b worked implementation and explanation](../../curriculum/answers/07b.md#07b-t) · [12b worked implementation and explanation](../../curriculum/answers/12b.md#12b-t)

<a id="07-g"></a>
## Mastery gate: 07-G

**Task:** Diagnose one failure each from parsing, chunking, embedding, ranking, reranking, and generation. Prove no cross-tenant evidence reaches the model.

**Expected reasoning and invariant outputs:** The baseline returns source quotes only and explicitly does not synthesize an answer. integration.py performs actual model embeddings and pgvector exact cosine search, PostgreSQL text ranking, optional cross-encoder reranking, and optional Ollama drafting. PostgreSQL ts_rank_cd is not BM25; implement or choose a genuine BM25 scorer for that comparison. Candidate presence is not evidence support. Compare against labeled questions and return unknown when sources do not support an answer.

Use the question-specific implementations above and [the reviewer answers](../../curriculum/assessments/ANSWERS.md). For deployment or model experiments, use [the worked operational procedures](../../curriculum/answers/OPERATIONS.md).

**Pass criteria:** 80/100 across correctness/reasoning (40), independent implementation (25), tests/debugging (20), and explanation/reproducibility (15). No permission leak, future-data leakage, invented evidence, or unreproducible core result. Live requirements remain pending until actually run. Running the answer files does not establish your independent mastery.

**If the gate fails:** Return to exact keyword matching and source inspection if embedding results are mysterious; keep the same evaluation set when changing one retrieval component.
