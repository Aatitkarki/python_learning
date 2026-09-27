# AI Mastery Roadmap — From Beginner to AI Engineer

> **The hands-on course is ready:** start with [START_HERE.md](START_HERE.md).
> It includes a [1,200-hour learning plan](curriculum/PLAN.md), 36 practice notebooks with
> separate worked answers, 16 project stages, and [mastery assessments](curriculum/assessments/MASTERY.md).
> The original roadmap and checklist below are preserved.

## Goal

Become capable of independently:

* Writing production-quality Python
* Working with data, SQL, APIs, and backend systems
* Understanding mathematics used in AI
* Training and evaluating machine learning models
* Building neural networks with PyTorch
* Understanding transformers and LLMs
* Building RAG systems
* Building AI agents and agentic workflows
* Running LLMs locally and on private infrastructure
* Deploying AI applications with Docker
* Evaluating AI systems properly
* Building secure production AI systems
* Working with big-data tools such as Spark
* Designing complete AI architectures
* Debugging AI systems instead of blindly using frameworks

---

# Overall Learning Path

```text
Programming
    ↓
Python
    ↓
Mathematics
    ↓
Data + SQL
    ↓
Machine Learning
    ↓
Deep Learning
    ↓
Transformers + LLMs
    ↓
RAG
    ↓
AI Agents
    ↓
Self-Hosted AI
    ↓
Production AI Engineering
    ↓
Advanced Specialization
```

---

# Estimated Study Commitment

The roadmap is approximately:

**1,000 focused learning hours**

This includes:

* studying
* coding
* exercises
* debugging
* projects
* reading documentation
* experimentation
* revision

Example timelines:

| Weekly Study  | Approximate Duration |
| ------------- | -------------------: |
| 10 hours/week |           ~23 months |
| 15 hours/week |        ~15–16 months |
| 20 hours/week |           ~12 months |
| 25 hours/week |         ~9–10 months |

Do not advance because a certain number of weeks passed.

Advance when you can complete the stage checkpoint independently.

---

# Stage 0 — Orientation and Development Setup

## Goal

Understand what AI engineering involves and prepare your development environment.

## Learn the difference between

* Artificial Intelligence
* Machine Learning
* Deep Learning
* Natural Language Processing
* Computer Vision
* Reinforcement Learning
* Generative AI
* Large Language Models
* AI Agents
* AI Engineering
* Machine Learning Engineering
* Data Science

## Install and configure

* [ ] Python
* [ ] VS Code
* [ ] Git
* [ ] GitHub
* [ ] Python virtual environments
* [ ] Jupyter Notebook
* [ ] Docker
* [ ] Terminal basics

## Learn basic Git

```bash
git init
git status
git add .
git commit -m "Initial commit"
git branch
git checkout
git pull
git push
```

## Create a learning repository

Suggested structure:

```text
ai-mastery/
│
├── notes/
├── exercises/
├── python/
├── mathematics/
├── machine-learning/
├── deep-learning/
├── llms/
├── rag/
├── agents/
├── infrastructure/
├── projects/
│
├── progress.md
└── README.md
```

## Checkpoint

You should be able to:

* create a Python project
* create a virtual environment
* install dependencies
* run Python files
* commit code using Git
* push code to GitHub

---

# Stage 1 — Python Programming

## Goal

Become comfortable programming without depending on AI-generated solutions.

## Topics

### Python fundamentals

* [ ] Variables
* [ ] Integers
* [ ] Floats
* [ ] Strings
* [ ] Booleans
* [ ] Operators
* [ ] Conditions
* [ ] Loops
* [ ] Functions
* [ ] Parameters
* [ ] Return values

---

## Data Structures

Learn:

* [ ] Lists
* [ ] Tuples
* [ ] Dictionaries
* [ ] Sets
* [ ] List comprehensions
* [ ] Dictionary comprehensions

Understand when to use each one.

---

## Functions

Learn:

```python
def calculate_profit(buy_price, sell_price, shares):
    return (sell_price - buy_price) * shares
```

Understand:

* parameters
* arguments
* return values
* scope
* default arguments
* keyword arguments

---

## Files

Learn to work with:

* [ ] TXT
* [ ] CSV
* [ ] JSON

Example:

```python
import json

with open("data.json") as file:
    data = json.load(file)
```

---

## Error Handling

Learn:

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")
```

Learn:

* Exceptions
* Custom exceptions
* Validation
* Defensive programming

---

## Object-Oriented Programming

Learn:

* Classes
* Objects
* Constructors
* Methods
* Properties
* Inheritance
* Composition
* Encapsulation

Example:

```python
class Stock:
    def __init__(self, ticker, price):
        self.ticker = ticker
        self.price = price
```

---

## Python Modules and Packages

Understand:

```text
project/
│
├── main.py
├── services/
│   ├── __init__.py
│   └── stock_service.py
│
└── utils/
    └── calculations.py
```

---

## Testing

Learn:

* pytest
* assertions
* unit tests
* integration tests
* mocks

Example:

```python
def test_profit():
    assert calculate_profit(100, 110, 10) == 100
```

---

## Debugging

Learn:

* reading stack traces
* breakpoints
* logging
* inspecting variables
* reproducing bugs

---

## Algorithms Basics

Learn:

* searching
* sorting
* recursion
* Big O notation

Understand roughly:

```text
O(1)
O(log n)
O(n)
O(n log n)
O(n²)
```

---

## Recommended Course

### Harvard CS50P

Complete:

**CS50's Introduction to Programming with Python**

Website:

```text
https://cs50.harvard.edu/python/
```

Do the exercises.

Do not only watch the videos.

---

# Stage 1 Projects

Build these without copying entire solutions.

## Project 1

Calculator

Features:

* addition
* subtraction
* multiplication
* division
* error handling

---

## Project 2

Text Analyzer

Input:

```text
A long paragraph
```

Output:

```text
Words: 153
Characters: 892
Most common word: AI
Unique words: 94
```

---

## Project 3

CSV Expense Analyzer

Example:

```csv
date,category,amount
2026-01-01,Food,15
2026-01-02,Transport,10
```

Calculate:

* total expenses
* expenses by category
* average expense
* highest expense
* monthly totals

Add tests.

---

# Stage 1 Checkpoint

Do not continue until you can:

* write functions independently
* work with dictionaries and lists
* read CSV and JSON
* split code across multiple modules
* debug errors
* write basic tests
* understand classes
* use Git comfortably

---

# Stage 2 — Mathematics for AI

## Goal

Understand the mathematics behind machine learning instead of memorizing formulas.

---

# 2.1 Algebra

Learn:

* variables
* equations
* functions
* graphs
* exponents
* logarithms
* summation notation

Understand:

```text
y = mx + b
```

and functions such as:

```text
f(x) = x²
```

---

# 2.2 Linear Algebra

Extremely important.

Learn:

* Scalars
* Vectors
* Matrices
* Tensors
* Vector addition
* Dot product
* Matrix multiplication
* Transpose
* Identity matrix
* Norm
* Distance
* Cosine similarity
* Eigenvalues
* Eigenvectors

Understand:

```text
Vector

[2, 5, 8]

Matrix

[1 2 3]
[4 5 6]
```

---

## Important AI concept

Embeddings are essentially vectors.

Example:

```text
"king"

[0.21, -0.82, 0.34, ...]
```

This makes linear algebra extremely important later.

---

# 2.3 Calculus

Learn:

* Functions
* Limits
* Derivatives
* Partial derivatives
* Gradients
* Chain rule

Understand:

```text
Loss
 ↓
Gradient
 ↓
Update weights
 ↓
Lower loss
```

---

# 2.4 Probability

Learn:

* probability basics
* conditional probability
* independence
* Bayes theorem
* random variables
* probability distributions

Learn distributions such as:

* Normal
* Bernoulli
* Binomial

---

# 2.5 Statistics

Learn:

* mean
* median
* mode
* variance
* standard deviation
* percentiles
* correlation
* covariance
* sampling
* confidence intervals
* hypothesis testing

---

# 2.6 Optimization

Learn:

* objective function
* loss function
* gradient descent
* learning rate
* local minima
* regularization

Understand:

```text
Weights
   ↓
Prediction
   ↓
Loss
   ↓
Gradient
   ↓
Update weights
   ↓
Repeat
```

---

# Recommended Math Resources

## 3Blue1Brown

Watch:

**Essence of Linear Algebra**

```text
https://www.3blue1brown.com/topics/linear-algebra
```

---

## Dive Into Deep Learning

```text
https://d2l.ai/
```

Use its mathematics sections for practical ML-oriented mathematics.

---

# Stage 2 Projects

Create a notebook:

```text
mathematics_for_ai.ipynb
```

Implement:

* vector addition
* dot product
* cosine similarity
* matrix multiplication
* mean
* variance
* standard deviation
* probability simulations
* gradient descent

Try implementing operations manually before using NumPy.

---

# Stage 2 Checkpoint

Explain without searching:

* What is a vector?
* What is a matrix?
* What is a dot product?
* What is cosine similarity?
* What is a derivative?
* What is a gradient?
* What does gradient descent do?
* What is variance?
* What is standard deviation?
* What is conditional probability?

---

# Stage 3 — NumPy, Pandas, SQL and Data Engineering Basics

## Goal

Learn how data is stored, processed, cleaned and queried.

---

# NumPy

Learn:

* arrays
* shapes
* dimensions
* indexing
* slicing
* broadcasting
* vectorized operations
* matrix operations

Example:

```python
import numpy as np

prices = np.array([100, 110, 120])
returns = prices[1:] / prices[:-1] - 1
```

---

# Pandas

Learn:

* DataFrame
* Series
* reading CSV
* reading JSON
* filtering
* sorting
* grouping
* joining
* merging
* missing values
* duplicates
* date/time
* rolling calculations

Example:

```python
import pandas as pd

df = pd.read_csv("stocks.csv")
```

---

# SQL

Learn:

```sql
SELECT
WHERE
ORDER BY
GROUP BY
HAVING
JOIN
LEFT JOIN
INNER JOIN
UNION
CTE
WINDOW FUNCTIONS
SUBQUERIES
```

Then learn:

* indexes
* primary keys
* foreign keys
* transactions
* normalization

---

## Recommended SQL Course

Harvard CS50 SQL:

```text
https://cs50.harvard.edu/sql/
```

---

# Databases

Learn PostgreSQL.

Understand:

```text
Application
    ↓
PostgreSQL
    ↓
Tables
    ↓
Rows
```

Learn:

* schemas
* migrations
* indexes
* transactions

---

# APIs

Learn:

* HTTP
* GET
* POST
* PUT
* PATCH
* DELETE
* headers
* JSON
* authentication
* HTTP status codes

Understand:

```text
Frontend
   ↓ HTTP
Backend API
   ↓
Database
```

---

# FastAPI

Learn:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/stocks")
def stocks():
    return {"stocks": []}
```

Documentation:

```text
https://fastapi.tiangolo.com/
```

Learn:

* routing
* validation
* Pydantic
* dependency injection
* authentication
* middleware
* error handling

---

# Stage 3 Project

Build:

# Data Analysis API

Architecture:

```text
CSV
 ↓
Python ingestion
 ↓
PostgreSQL
 ↓
FastAPI
 ↓
REST API
```

Endpoints:

```text
GET /records
GET /summary
GET /statistics
POST /records
```

Add:

* validation
* tests
* logging

---

# Stage 3 Checkpoint

You should be comfortable with:

* NumPy
* Pandas
* PostgreSQL
* SQL joins
* FastAPI
* REST APIs
* validation
* tests

---

# Stage 4 — Machine Learning

## Goal

Learn how machines learn patterns from data.

---

# Fundamental Concepts

Learn:

* Dataset
* Feature
* Label
* Model
* Training
* Validation
* Testing
* Inference

Understand:

```text
Data
 ↓
Features
 ↓
Model
 ↓
Prediction
```

---

# Supervised Learning

Learn:

## Regression

Used for predicting numbers.

Examples:

```text
House price
Revenue
Temperature
Demand
```

Algorithms:

* Linear Regression
* Decision Tree Regression
* Random Forest Regression
* Gradient Boosting

---

## Classification

Used for predicting categories.

Examples:

```text
Spam / Not Spam
Fraud / Normal
Positive / Negative
```

Learn:

* Logistic Regression
* Decision Trees
* Random Forest
* Gradient Boosting
* k-Nearest Neighbors
* Support Vector Machines

---

# Unsupervised Learning

Learn:

* clustering
* dimensionality reduction

Algorithms:

* K-Means
* DBSCAN
* PCA

---

# Evaluation

For classification learn:

* Accuracy
* Precision
* Recall
* F1 score
* Confusion matrix
* ROC
* AUC

For regression:

* MAE
* MSE
* RMSE
* R²

---

# Critical Concepts

Learn deeply:

* overfitting
* underfitting
* bias
* variance
* cross-validation
* feature engineering
* data leakage
* class imbalance
* baselines

---

# Scikit-Learn

Learn:

```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
```

Understand pipelines:

```text
Raw Data
   ↓
Preprocessing
   ↓
Feature engineering
   ↓
Model
   ↓
Evaluation
```

---

# Recommended Course

Machine Learning Specialization:

```text
DeepLearning.AI
Andrew Ng
```

or

Google Machine Learning Crash Course.

Choose one first.

---

# Stage 4 Project

Build a:

# Support Ticket Classifier

Input:

```text
"I cannot login to my account."
```

Output:

```text
Category: Account Access
Confidence: 91%
```

Compare:

* Logistic Regression
* Random Forest
* Gradient Boosting

Record:

* accuracy
* precision
* recall
* F1

Analyze errors.

---

# Stage 4 Checkpoint

You should be able to answer:

* Why split train/test data?
* What is overfitting?
* What is data leakage?
* Accuracy vs precision?
* Precision vs recall?
* What is cross-validation?
* Why use a baseline?
* Why might a simple model beat a complicated model?

---

# Stage 5 — Deep Learning

## Goal

Understand neural networks.

---

# Neural Network Fundamentals

Learn:

* neuron
* weights
* bias
* activation function
* layers
* forward propagation
* loss
* backpropagation

Architecture:

```text
Input
 ↓
Layer
 ↓
Activation
 ↓
Layer
 ↓
Output
 ↓
Loss
 ↓
Backpropagation
```

---

# Activation Functions

Learn:

* ReLU
* Sigmoid
* Tanh
* Softmax

---

# Loss Functions

Learn:

* Mean Squared Error
* Binary Cross Entropy
* Cross Entropy

---

# Optimizers

Learn:

* SGD
* Momentum
* Adam
* AdamW

---

# Important Concepts

Learn:

* batch
* epoch
* learning rate
* regularization
* dropout
* normalization
* gradient explosion
* vanishing gradient

---

# PyTorch

Learn:

```python
import torch
```

Learn:

* Tensor
* Dataset
* DataLoader
* nn.Module
* optimizer
* loss function
* autograd
* training loop
* validation loop

---

# Example Training Loop

Understand this deeply:

```python
for batch in dataloader:

    optimizer.zero_grad()

    prediction = model(batch)

    loss = loss_fn(prediction, target)

    loss.backward()

    optimizer.step()
```

---

# Computer Vision Basics

Learn:

* images as tensors
* CNN
* kernels
* convolution
* pooling

---

# Sequence Models

Understand historically:

* RNN
* LSTM
* GRU

You do not need to specialize deeply in them before transformers.

---

# Recommended Resources

PyTorch:

```text
https://pytorch.org/tutorials/
```

Dive Into Deep Learning:

```text
https://d2l.ai/
```

---

# Stage 5 Projects

Build:

## Image Classifier

Example:

```text
Cat
Dog
Car
Plane
```

Track:

* training loss
* validation loss
* accuracy

---

## Tiny Neural Network From Scratch

Implement a small network using NumPy.

Purpose:

Understand:

* matrix multiplication
* activation
* loss
* gradient updates

---

# Stage 5 Checkpoint

Be able to explain:

* neural network
* neuron
* activation
* loss
* gradient
* backpropagation
* optimizer
* epoch
* batch
* learning rate

And write a basic PyTorch training loop.

---

# Stage 6 — Transformers and Large Language Models

## Goal

Understand what modern LLMs are doing.

---

# Start With Tokenization

Understand:

```text
"Artificial intelligence is amazing"

        ↓

Tokens

        ↓

[1532, 9421, 374, 8056]
```

Learn:

* token
* vocabulary
* tokenizer
* subword tokenization
* token IDs

---

# Embeddings

Understand:

```text
Token
 ↓
Embedding
 ↓
Vector
```

Example:

```text
"cat"

[0.18, -0.92, 0.41, ...]
```

---

# Attention

Learn deeply:

* Query
* Key
* Value
* Self-attention
* Attention scores
* Multi-head attention

Understand conceptually:

```text
Q = Query
K = Key
V = Value

Attention(Q, K, V)
```

Eventually understand:

```text
softmax(QKᵀ / √d)V
```

---

# Transformer Architecture

Learn:

```text
Tokens
 ↓
Embeddings
 ↓
Positional Information
 ↓
Attention
 ↓
Feed Forward Network
 ↓
Attention
 ↓
Feed Forward Network
 ↓
Output probabilities
```

---

# Understand

* encoder
* decoder
* encoder-decoder
* autoregressive model
* next-token prediction
* context window

---

# Learn Major Model Families

Understand at a high level:

* GPT
* BERT
* T5
* Llama
* Qwen
* Mistral
* DeepSeek

Do not attempt to memorize every model.

Understand architectural differences.

---

# Inference Concepts

Learn:

* Temperature
* Top-K
* Top-P
* Greedy decoding
* Beam search
* Context length
* KV cache

---

# Fine-Tuning

Understand:

```text
Base Model
 ↓
Fine-tuning
 ↓
Specialized Model
```

Learn:

* full fine-tuning
* supervised fine-tuning
* LoRA
* QLoRA
* PEFT

---

# Quantization

Learn:

* FP32
* FP16
* BF16
* INT8
* INT4

Understand tradeoff:

```text
Lower precision

→ less memory
→ faster inference
→ possible quality reduction
```

---

# Recommended Course

Hugging Face LLM Course:

```text
https://huggingface.co/learn/llm-course
```

---

# Stage 6 Projects

## Project 1

Text classification with a pretrained transformer.

---

## Project 2

Structured extraction.

Input:

```text
Apple reported revenue of $100 billion.
```

Output:

```json
{
  "company": "Apple",
  "revenue": 100000000000
}
```

Validate the output.

---

## Project 3

Train a tiny language model.

Not to build ChatGPT.

The purpose is to understand:

```text
data
→ tokens
→ batches
→ transformer
→ loss
→ training
→ inference
```

---

# Stage 6 Checkpoint

Explain:

* tokenizer
* embeddings
* attention
* transformer
* context window
* temperature
* fine-tuning
* LoRA
* quantization
* KV cache

---

# Stage 7 — RAG

## Goal

Build AI that can answer using your own data.

---

# RAG Architecture

Understand:

```text
Documents
    ↓
Parsing
    ↓
Chunking
    ↓
Embeddings
    ↓
Vector Database
    ↓
Retriever

User Question
    ↓
Question Embedding
    ↓
Vector Search
    ↓
Relevant Chunks
    ↓
LLM
    ↓
Answer
```

---

# Learn

## Document Processing

* PDF
* Markdown
* HTML
* DOCX
* JSON
* database records

---

# Chunking

Learn:

* fixed token chunking
* paragraph chunking
* semantic chunking
* overlapping chunks

Understand why chunk size matters.

---

# Embedding Models

Learn:

```text
Text
 ↓
Embedding Model
 ↓
Vector
```

Understand:

* dimensionality
* similarity
* semantic search

---

# Vector Databases

Start with:

## PostgreSQL + pgvector

Later explore:

* Qdrant
* Weaviate
* Milvus
* Pinecone

Do not learn all at once.

---

# Retrieval

Learn:

* semantic retrieval
* keyword search
* BM25
* hybrid search
* metadata filtering

---

# Reranking

Architecture:

```text
1000 documents
 ↓
Retriever
 ↓
20 candidates
 ↓
Reranker
 ↓
5 best documents
 ↓
LLM
```

---

# RAG Evaluation

Separate:

## Retrieval Quality

Did the system retrieve the right information?

## Generation Quality

Did the model correctly use the retrieved information?

---

# Learn

* Recall@K
* Precision@K
* MRR
* answer correctness
* groundedness
* citation accuracy

---

# Stage 7 Project

Build:

# Private Knowledge Assistant

Data:

```text
PDFs
Markdown
Documentation
Policies
```

Features:

* upload document
* chunk document
* generate embeddings
* store in pgvector
* search
* answer questions
* show citations
* reject unsupported questions

---

# Add Authentication

Users should only retrieve documents they are allowed to access.

Example:

```text
User A
 ↓
Documents A

User B
 ↓
Documents B
```

User A must never retrieve User B's documents.

---

# Stage 7 Checkpoint

You should be able to identify whether a wrong answer came from:

* bad parsing
* bad chunking
* bad embedding
* bad retrieval
* bad reranking
* insufficient context
* model hallucination

---

# Stage 8 — AI Agents

## Goal

Build systems where LLMs can use tools and perform controlled workflows.

---

# Understand Tool Calling

Example:

```text
User:
"What is NVDA's P/E ratio?"

LLM
 ↓
Needs financial data
 ↓
Calls financial API
 ↓
Receives result
 ↓
Explains result
```

---

# Learn

* tools
* function calling
* structured output
* routing
* state
* memory
* retries
* timeouts
* tool errors
* human approval

---

# Agent Architecture

Example:

```text
User
 ↓
Agent
 ↓
Decide Action
 ↓
Tool
 ↓
Observation
 ↓
Reason
 ↓
Next Action
 ↓
Final Answer
```

---

# LangChain

Learn enough to understand:

* models
* prompts
* tools
* retrievers
* structured outputs

Do not depend entirely on abstractions.

---

# LangGraph

Study more deeply.

Architecture:

```text
START
 ↓
Analyze Request
 ↓
Route
 ├── Search
 ├── Database
 └── Calculator
 ↓
Combine Results
 ↓
END
```

Learn:

* state
* nodes
* edges
* conditional edges
* persistence
* checkpoints
* human-in-the-loop

---

# Multi-Agent Systems

Only learn this after building good single-agent systems.

Example:

```text
Supervisor
     │
 ┌───┼───────────┐
 ↓   ↓           ↓
Research      Database
Agent         Agent
               │
             SQL
     ↓
Analysis Agent
     ↓
Final Answer
```

---

# Important Rule

Do not build multiple agents simply because it looks impressive.

Use multiple agents only when:

```text
Multiple agents
```

perform measurably better than:

```text
One controlled workflow
```

---

# Agent Security

Learn:

* prompt injection
* indirect prompt injection
* tool abuse
* excessive permissions
* secrets leakage
* malicious documents
* data exfiltration

---

# Stage 8 Project

Extend your RAG project.

Build:

# AI Research Agent

Tools:

```text
Document Search
SQL
Calculator
Public Data API
```

Agent can:

1. understand the question
2. choose a tool
3. retrieve information
4. perform calculations
5. cite evidence
6. generate a report

---

# Add Limits

For example:

```text
Maximum tool calls: 10
Maximum execution time: 60 seconds
Maximum retries: 2
```

Add human approval before destructive actions.

---

# Stage 8 Checkpoint

Your agent should:

* choose correct tools
* validate arguments
* handle tool failures
* stop correctly
* never fake tool results
* respect permissions
* avoid uncontrolled loops

---

# Stage 9 — Local and Self-Hosted AI

## Goal

Learn to run AI models privately.

---

# Ollama

Learn:

```bash
ollama run llama
```

Understand:

```text
Application
 ↓
Ollama
 ↓
Local LLM
 ↓
CPU/GPU
```

Learn its API.

---

# vLLM

Later learn:

```text
Application
 ↓
OpenAI-compatible API
 ↓
vLLM
 ↓
GPU
 ↓
LLM
```

Understand why vLLM is useful for higher-throughput model serving.

---

# Hardware Concepts

Learn:

* CPU
* GPU
* VRAM
* RAM
* CUDA
* tensor cores
* bandwidth

---

# Model Memory

Understand approximately:

```text
Model Size
×
Precision
=
Memory Requirement
```

Learn why:

```text
FP16
INT8
INT4
```

change memory requirements.

---

# Serving Concepts

Learn:

* requests per second
* tokens per second
* latency
* throughput
* batching
* continuous batching
* KV cache
* concurrent users

---

# Stage 9 Project

Run your RAG assistant using a self-hosted model.

Architecture:

```text
Browser
 ↓
FastAPI
 ↓
Agent
 ↓
Retriever
 ↓
PostgreSQL + pgvector
 ↓
vLLM / Ollama
 ↓
Local Model
```

---

# Stage 10 — Docker and Production AI

## Goal

Turn your project into something deployable.

---

# Docker

Learn:

* Dockerfile
* image
* container
* volume
* port
* network
* Docker Compose

Example:

```text
docker-compose.yml

api
database
vector database
model server
monitoring
```

---

# Networking

Learn:

* localhost
* ports
* DNS
* reverse proxies
* HTTP
* HTTPS
* TLS

---

# Secrets

Never store:

```text
API_KEY=secret
```

inside Git.

Learn environment variables and secret-management systems.

---

# Authentication

Learn:

* sessions
* JWT
* OAuth
* API keys

Understand:

```text
Authentication

Who are you?
```

vs

```text
Authorization

What are you allowed to do?
```

---

# Observability

Learn:

* logs
* metrics
* traces

Measure:

```text
Request count
Latency
Failures
Model latency
Tokens
Retrieval time
Database latency
```

---

# Production Concepts

Learn:

* health checks
* backups
* rate limits
* retry policies
* timeouts
* rollback
* versioning
* migrations

---

# AI-Specific Monitoring

Monitor:

* hallucination rate
* RAG retrieval quality
* token consumption
* model failures
* tool-call failures
* latency
* prompt changes
* model versions

---

# CI/CD

Learn:

```text
GitHub
 ↓
Tests
 ↓
Build Docker Image
 ↓
Deploy
 ↓
Health Check
```

Since you already use Coolify, use it for practical deployments after you understand the underlying Docker concepts.

---

# Stage 10 Project

Productionize your AI assistant.

Requirements:

* Docker
* authentication
* PostgreSQL
* vector search
* model server
* logs
* tests
* backups
* monitoring
* automated deployment

---

# Failure Testing

Intentionally break things.

Test:

* database unavailable
* model unavailable
* malformed input
* missing document
* timeout
* invalid authentication
* insufficient permission
* corrupted document
* huge prompt

Your application should fail safely.

---

# Stage 11 — Big Data and Spark

## Goal

Learn distributed data processing.

This is especially useful for enterprise AI roles.

---

# Learn

Apache Spark:

* Spark architecture
* driver
* executor
* DataFrame
* transformations
* actions
* lazy execution
* partitioning
* shuffle
* joins

---

# PySpark

Example:

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

df = spark.read.csv("data.csv")
```

---

# Learn Data Formats

Understand:

* CSV
* JSON
* Parquet
* Avro

Learn why Parquet is common for analytical data.

---

# Project

Generate a large synthetic transaction dataset.

Process using PySpark.

Calculate:

* aggregates
* trends
* anomalies
* rolling statistics
* grouped statistics

---

# Stage 12 — AI Security

## Goal

Build systems that do not become security liabilities.

---

# Learn OWASP GenAI Risks

Understand:

* Prompt Injection
* Sensitive Information Disclosure
* Supply Chain Risks
* Data Poisoning
* Improper Output Handling
* Excessive Agency
* System Prompt Leakage
* Vector and Embedding Weaknesses
* Misinformation
* Unbounded Consumption

---

# Test Your Own Systems

Try malicious prompts such as:

```text
Ignore previous instructions...
```

Or malicious retrieved documents containing instructions to the model.

Check whether tools can access resources beyond the user's permissions.

---

# Stage 13 — Evaluation Engineering

## Goal

Learn to prove whether an AI system actually works.

This is one of the most important advanced skills.

---

# Create Evaluation Datasets

Example:

```json
{
  "question": "What was revenue?",
  "expected_source": "report.pdf",
  "expected_answer": "..."
}
```

Build hundreds of test cases over time.

---

# Evaluate

## LLM

* correctness
* relevance
* format compliance

## RAG

* retrieval recall
* citation correctness
* groundedness

## Agent

* tool selection
* arguments
* number of steps
* final answer
* safe termination

---

# Regression Testing

Whenever you change:

```text
Prompt
Model
Embedding model
Chunk size
Retriever
Reranker
Agent logic
```

rerun your evaluation set.

Do not assume the new version is better.

---

# Stage 14 — Financial AI Specialization

After completing the foundations, specialize based on your interests.

---

# Learn Financial Fundamentals

Study:

* Income Statement
* Balance Sheet
* Cash Flow Statement
* EPS
* Revenue
* Net Income
* Free Cash Flow
* Debt
* Assets
* Liabilities
* Equity

---

# Financial Ratios

Learn:

* P/E
* PEG
* P/S
* P/B
* ROE
* ROA
* Debt-to-Equity
* Gross Margin
* Operating Margin
* Net Margin
* FCF Yield

---

# Markets

Learn:

* stocks
* ETFs
* indexes
* bonds
* options
* futures
* market orders
* limit orders
* bid
* ask
* spread
* liquidity
* volatility

---

# Time Series

Learn:

* lag
* returns
* rolling statistics
* moving averages
* autocorrelation
* stationarity
* time-series cross-validation

---

# Critical Financial ML Rule

Never randomly shuffle time-series data when future information could leak into the past.

Use:

```text
Past
 ↓
Training

Future
 ↓
Validation/Test
```

---

# Stage 15 — Final Capstone

Build:

# Private Financial Research AI Platform

Architecture:

```text
                       ┌───────────────────┐
                       │      Frontend     │
                       └─────────┬─────────┘
                                 ↓
                       ┌───────────────────┐
                       │      FastAPI      │
                       └─────────┬─────────┘
                                 ↓
                     ┌─────────────────────┐
                     │    AI Orchestrator  │
                     └──────────┬──────────┘
                                │
           ┌────────────────────┼────────────────────┐
           ↓                    ↓                    ↓
     RAG Retriever          SQL Tool          Calculator
           ↓                    ↓
     PostgreSQL             PostgreSQL
     + pgvector
           │
           └────────────────────┬────────────────────┘
                                ↓
                         Local Model
                                ↓
                              vLLM
                                ↓
                              GPU
```

---

# Capstone Features

## Authentication

* users
* roles
* permissions

---

## Document System

Support:

* PDF
* Markdown
* financial reports
* earnings reports

---

## Retrieval

Implement:

* embeddings
* vector search
* keyword search
* hybrid search
* metadata filters
* reranking

---

## Financial Tools

Create:

```text
calculate_pe()
calculate_eps_growth()
calculate_revenue_growth()
calculate_margin()
calculate_return()
```

---

# AI Agent

Tools:

```text
Financial database
Document search
Calculator
Public market-data API
```

---

# Example Question

```text
Compare the last three years of revenue,
operating margin and free cash flow for
Company A and Company B.
```

System:

```text
Question
 ↓
Plan
 ↓
Retrieve filings
 ↓
Query database
 ↓
Calculate metrics
 ↓
Verify numbers
 ↓
Generate answer
 ↓
Cite sources
```

---

# Self-Hosted AI

Run using:

```text
Ollama
or
vLLM
```

---

# Production

Deploy with:

* Docker
* GitHub
* Coolify
* PostgreSQL
* monitoring
* backups

---

# Security

Implement:

* authentication
* authorization
* document permissions
* tool restrictions
* prompt injection protection
* rate limiting

---

# Evaluation

Build at least:

```text
100–500 evaluation questions
```

over time.

Test:

* retrieval
* citations
* calculations
* hallucinations
* agent tools
* permissions

---

# Portfolio Projects

By the time you are comfortable applying for AI engineering roles, aim for approximately four strong projects.

---

## Project 1 — Classical Machine Learning

Example:

```text
Support Ticket Classifier
```

Demonstrate:

* preprocessing
* model training
* evaluation
* API deployment

---

## Project 2 — Deep Learning

Example:

```text
Image Classification System
```

Demonstrate:

* PyTorch
* training
* validation
* experiment tracking

---

## Project 3 — RAG

Example:

```text
Private Document Assistant
```

Demonstrate:

* parsing
* embeddings
* vector DB
* retrieval
* reranking
* citations
* evaluation

---

## Project 4 — Production Agent System

Example:

```text
Financial Research Agent
```

Demonstrate:

* tools
* LangGraph
* databases
* RAG
* local LLM
* Docker
* authentication
* evaluation
* monitoring

---

# Weekly Learning Schedule

Example for 15 hours/week:

| Activity          | Hours |
| ----------------- | ----: |
| Lessons / Reading |     4 |
| Coding            |     6 |
| Projects          |     2 |
| Mathematics       |     2 |
| Review            |     1 |

---

# Daily Study Pattern

Use this loop:

```text
Learn
 ↓
Explain
 ↓
Implement
 ↓
Break
 ↓
Debug
 ↓
Improve
 ↓
Teach it back
```

---

# Learning Rule

For every topic ask yourself:

## 1. What is it?

Explain it simply.

## 2. Why does it exist?

What problem does it solve?

## 3. How does it work?

Understand the mechanics.

## 4. Can I implement a simplified version?

Do it.

## 5. Can I use the production version?

Learn the library/framework.

## 6. Can I debug it?

Break it intentionally.

## 7. Can I explain its limitations?

This is extremely important.

---

# How to Use AI While Learning

Use AI as a teacher, not as your replacement.

---

## Good

Ask:

```text
Explain why this error occurs.
```

```text
Give me a hint, not the solution.
```

```text
Review my implementation.
```

```text
Give me five exercises on Python dictionaries.
```

```text
Ask me interview questions on gradient descent.
```

---

## Bad

Do not constantly ask:

```text
Build this entire project for me.
```

then copy it without understanding.

---

# Tutor Prompt

Use:

```text
Act as my AI engineering tutor.

I am learning this topic from scratch.

Do not immediately give me complete solutions.

First ask me how I think the problem should be solved.

If I get stuck, provide increasingly detailed hints.

After I solve the problem, review my solution and ask
follow-up questions to verify that I understand it.

If code is involved, make me explain important sections
before moving forward.
```

---

# Monthly Review

At the end of every month answer:

```text
What did I learn?

What can I build now that I couldn't build last month?

Which concepts are still unclear?

What did I build independently?

Where am I depending too much on AI?

What mistakes did I repeatedly make?

What should I focus on next month?
```

Add answers to:

```text
progress.md
```

---

# First 30 Days

Do not start with LLM agents.

Start with programming.

---

# Week 1

Learn:

* Python setup
* variables
* strings
* numbers
* Boolean values
* input/output
* functions
* conditions

Build:

```text
Calculator
BMI calculator
Simple profit calculator
Temperature converter
```

---

# Week 2

Learn:

* loops
* lists
* dictionaries
* tuples
* sets

Build:

```text
Word Counter
Contact Book
Simple Inventory
```

---

# Week 3

Learn:

* files
* CSV
* JSON
* modules
* exceptions

Build:

```text
CSV Expense Analyzer
```

---

# Week 4

Learn:

* testing
* debugging
* Git
* OOP
* refactoring

Improve the expense analyzer.

Add:

```text
Tests
Classes
README
Git history
Validation
```

---

# First-Month Checkpoint

At the end of the first month, you should be able to create something similar to:

```python
def calculate_profit(buy_price, sell_price, shares):
    if shares <= 0:
        raise ValueError("Shares must be positive")

    return (sell_price - buy_price) * shares
```

and explain every line.

You should understand:

```text
Why use a function?
Why validate input?
What exception is raised?
What is returned?
How would you test it?
```

---

# Do Not Rush Into These Yet

Avoid starting your learning journey directly with:

* LangChain
* LangGraph
* CrewAI
* AutoGen
* vector databases
* fine-tuning
* CUDA
* Kubernetes
* massive LLMs

They become much easier once you understand the foundations.

---

# Final Skill Tree

```text
AI ENGINEER
│
├── Programming
│   ├── Python
│   ├── OOP
│   ├── Algorithms
│   ├── Testing
│   └── Git
│
├── Mathematics
│   ├── Algebra
│   ├── Linear Algebra
│   ├── Calculus
│   ├── Probability
│   └── Statistics
│
├── Data
│   ├── NumPy
│   ├── Pandas
│   ├── SQL
│   ├── PostgreSQL
│   └── Spark
│
├── Machine Learning
│   ├── Regression
│   ├── Classification
│   ├── Clustering
│   ├── Evaluation
│   └── Feature Engineering
│
├── Deep Learning
│   ├── Neural Networks
│   ├── PyTorch
│   ├── CNN
│   ├── Embeddings
│   └── Optimization
│
├── LLMs
│   ├── Tokenization
│   ├── Transformers
│   ├── Attention
│   ├── Fine-Tuning
│   ├── LoRA
│   └── Quantization
│
├── RAG
│   ├── Chunking
│   ├── Embeddings
│   ├── Vector Search
│   ├── Hybrid Search
│   ├── Reranking
│   └── Evaluation
│
├── Agents
│   ├── Tool Calling
│   ├── State
│   ├── LangGraph
│   ├── Workflows
│   ├── Multi-Agent
│   └── Human Approval
│
├── Infrastructure
│   ├── Docker
│   ├── APIs
│   ├── Networking
│   ├── Authentication
│   ├── Monitoring
│   └── CI/CD
│
├── Self-Hosted AI
│   ├── Ollama
│   ├── vLLM
│   ├── GPUs
│   ├── Quantization
│   ├── Batching
│   └── Model Serving
│
└── Production AI
    ├── Evaluation
    ├── Security
    ├── Observability
    ├── Permissions
    ├── Reliability
    └── Scaling
```

---

# Progress Checklist

## Foundations

* [ ] Python fundamentals
* [ ] Functions
* [ ] OOP
* [ ] Files
* [ ] Testing
* [ ] Git
* [ ] Algorithms
* [ ] Linear algebra
* [ ] Calculus
* [ ] Probability
* [x] Statistics

## Data

* [ ] NumPy
* [ ] Pandas
* [ ] SQL
* [ ] PostgreSQL
* [ ] FastAPI

## Machine Learning

* [ ] Regression
* [ ] Classification
* [ ] Clustering
* [ ] Model evaluation
* [ ] Cross-validation
* [ ] Feature engineering
* [ ] Data leakage
* [ ] Scikit-learn

## Deep Learning

* [ ] Neural networks
* [ ] Backpropagation
* [ ] PyTorch
* [ ] Optimizers
* [ ] CNN
* [ ] Embeddings

## LLM

* [ ] Tokens
* [ ] Tokenization
* [ ] Embeddings
* [ ] Attention
* [ ] Transformers
* [ ] Context windows
* [ ] Decoding
* [ ] Fine-tuning
* [ ] LoRA
* [ ] Quantization

## RAG

* [ ] Parsing
* [ ] Chunking
* [ ] Embeddings
* [ ] pgvector
* [ ] Semantic search
* [ ] Hybrid search
* [ ] Reranking
* [ ] Citations
* [ ] RAG evaluation

## Agents

* [ ] Tool calling
* [ ] Structured output
* [ ] Routing
* [ ] State
* [ ] LangChain basics
* [ ] LangGraph
* [ ] Persistence
* [ ] Human approval
* [ ] Multi-agent systems
* [ ] Agent evaluation

## Infrastructure

* [ ] Docker
* [ ] Docker Compose
* [ ] Networking
* [ ] HTTPS
* [ ] Authentication
* [ ] Authorization
* [ ] Logging
* [ ] Monitoring
* [ ] Backups
* [ ] CI/CD

## Self-hosted AI

* [ ] Ollama
* [ ] GPU fundamentals
* [ ] VRAM
* [ ] CUDA basics
* [ ] Quantization
* [ ] vLLM
* [ ] Batching
* [ ] KV cache
* [ ] Performance testing

## Advanced

* [ ] Spark
* [ ] AI security
* [ ] Evaluation engineering
* [ ] Distributed systems basics
* [ ] Financial AI specialization

---

# Main Resources

## Python

```text
https://cs50.harvard.edu/python/
```

## SQL

```text
https://cs50.harvard.edu/sql/
```

## General AI

```text
https://cs50.harvard.edu/ai/
```

## Mathematics / Deep Learning

```text
https://d2l.ai/
```

## PyTorch

```text
https://pytorch.org/tutorials/
```

## LLMs

```text
https://huggingface.co/learn/llm-course
```

## FastAPI

```text
https://fastapi.tiangolo.com/
```

## LangChain

```text
https://docs.langchain.com/
```

## LangGraph

```text
https://docs.langchain.com/oss/python/langgraph/
```

## Ollama

```text
https://docs.ollama.com/
```

## vLLM

```text
https://docs.vllm.ai/
```

## PySpark

```text
https://spark.apache.org/docs/latest/api/python/
```

## AI Security

```text
https://genai.owasp.org/
```

---

# Golden Rules

## Rule 1

Do not learn frameworks before understanding the concepts they abstract.

## Rule 2

Do not measure progress by the number of videos watched.

Measure progress by what you can build.

## Rule 3

Do not trust model accuracy without understanding the evaluation setup.

## Rule 4

Never mix train and test information.

## Rule 5

Do not call something production-ready simply because it runs locally.

## Rule 6

Always build evaluation into AI applications.

## Rule 7

Learn to debug.

Debugging ability is one of the biggest differences between someone who can use AI tools and an AI engineer.

## Rule 8

Understand security before giving an agent powerful tools.

## Rule 9

Start simple.

```text
Function
→ Script
→ API
→ ML
→ LLM
→ RAG
→ Agent
→ Production
```

Do not jump directly to the end.

## Rule 10

Always ask:

> Can I explain why this works?

If not, you are not finished learning it.

---

# Long-Term Target

The eventual goal is to be capable of designing something like:

```text
                    USERS
                      │
                      ↓
                WEB APPLICATION
                      │
                      ↓
                   API
                      │
          ┌───────────┴────────────┐
          │                        │
          ↓                        ↓
   AUTHORIZATION              AI SYSTEM
                                   │
                    ┌──────────────┼──────────────┐
                    ↓              ↓              ↓
                  RAG          AI AGENT         TOOLS
                    │              │              │
               VECTOR DB        STATE        DATABASE
                    │              │              │
                    └──────────────┼──────────────┘
                                   ↓
                             MODEL SERVER
                                   │
                              Ollama/vLLM
                                   │
                                  GPU
                                   │
                           SELF-HOSTED LLM
```

And you should be able to explain:

* why every component exists
* how information moves through the system
* how it is evaluated
* how it can fail
* how it is secured
* how it is monitored
* how it is deployed
* how it is scaled
* how you would improve it

That is the level to work toward.
