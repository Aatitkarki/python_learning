# Primary resources and how to use them

The local course provides the learning sequence, exercises, and answers. Use these primary references to deepen a topic and check changing APIs. Access was checked for the main course/framework pages during authoring on 2026-09-27; exact software versions can change. Prefer the documentation for the version in your environment.

| Stage | Resource | Assigned use |
|---|---|---|
| 00–01 | [CS50P](https://cs50.harvard.edu/python/) | Functions/variables, conditionals, loops, exceptions, libraries, unit tests, file I/O, regex, OOP. Attempt course exercises yourself; this repository does not supply answers to third-party graded work. |
| 00–01 | [Python tutorial](https://docs.python.org/3/tutorial/) | Revisit control flow, data structures, modules, errors, and classes after the local beginner explanations. |
| 02, 05 | [Dive into Deep Learning](https://d2l.ai/) | Preliminaries: linear algebra, calculus, probability; then linear networks, MLPs, optimization, convolution, and attention. Read equations with a pencil and reproduce small cases. |
| 03 | [NumPy broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html), [Pandas guide](https://pandas.pydata.org/docs/user_guide/) | Predict shapes and join results before running examples. |
| 03 | [CS50 SQL](https://cs50.harvard.edu/sql/), [PostgreSQL tutorial](https://www.postgresql.org/docs/current/tutorial.html) | Querying, relating, designing, writing, viewing, optimizing, scaling; repeat local SQLite queries in PostgreSQL. |
| 03, 10 | [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/) | Request models, errors, dependencies, security, middleware, SQL databases, and tests. |
| 04 | [Scikit-learn pitfalls](https://scikit-learn.org/stable/common_pitfalls.html), [evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html) | Audit preprocessing and splits; choose metrics before tuning. |
| 05 | [PyTorch basics](https://docs.pytorch.org/tutorials/beginner/basics/intro.html) | Tensors, loaders, models, autograd, optimization, save/load. |
| 06 | [Hugging Face LLM course](https://huggingface.co/learn/llm-course/chapter1/1), [Attention Is All You Need](https://arxiv.org/abs/1706.03762) | Tokenizers, transformer models, fine-tuning, and attention equations. |
| 06 | [PEFT LoRA guide](https://huggingface.co/docs/peft/en/conceptual_guides/lora) | Shapes, rank, scaling, target modules, and adapter/base distinction. |
| 07 | [pgvector](https://github.com/pgvector/pgvector) | Distance operators, indexes, filtering, and recall/performance tradeoffs. |
| 08 | [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview), [interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) | State, edges, persistence, resumable human review. |
| 09 | [Ollama chat API](https://docs.ollama.com/api/chat), [vLLM documentation](https://docs.vllm.ai/en/latest/) | Current request contracts, supported hardware, serving and benchmarking. |
| 10 | [Docker introduction](https://docs.docker.com/get-started/), [Compose](https://docs.docker.com/compose/) | Build, volumes, networking, health, and service configuration. |
| 11 | [PySpark installation](https://spark.apache.org/docs/latest/api/python/getting_started/install.html), [PySpark API](https://spark.apache.org/docs/latest/api/python/) | Match Python/Java requirements to your chosen Spark version; inspect DataFrame and window behavior. |
| 12 | [OWASP GenAI risks](https://genai.owasp.org/llm-top-10/) | Map each risk to a local threat, code-level control, and regression test. |
| 14 | [SEC financial-statement guide](https://www.sec.gov/about/reports-publications/investorpubsbegfinstmtguide), [Investor.gov products](https://www.investor.gov/introduction-investing/investing-basics/investment-products) | Statement relationships, terminology, instrument differences; use fictional data for the exercises. |

Do not spend the whole study budget reading. For every source, write one explanation, reproduce one example, change one assumption, and record one limitation. Model families, optional vector databases, and alternative agent frameworks are comparison topics; you do not need to install them all to understand the design choices.
