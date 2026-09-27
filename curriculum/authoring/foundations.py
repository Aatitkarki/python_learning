from schema import lesson, exercise as E

lesson('00a', 'Your first reproducible experiment', 'stdlib',
['Run cells in order and restart the kernel', 'Distinguish source code, runtime state, and saved output', 'Make and explain a small reproducible experiment'],
'''A program is a sequence of instructions executed by an interpreter. A notebook stores text and code cells; its kernel holds variables in memory. A cell can appear correct only because an earlier experiment left a variable behind. Restart the kernel and run all cells to test reproducibility.

`name = value` binds a name. `print(value)` displays it. A function accepts inputs and returns a result. Python uses indentation to group instructions. An assertion checks a claim and raises an error when it is false. Errors are feedback: read the last line first, then follow the traceback to your code.

AI is the broad field of systems performing tasks associated with intelligence. ML learns patterns from examples; deep learning uses layered neural networks. NLP processes language; vision processes images; reinforcement learning optimizes actions using rewards. LLMs predict language tokens. An agent combines a model with tools and a control loop. AI engineering includes data, software, evaluation, and operation, not just calling a model.''',
'''message = "Hello, AI engineering"
print(message)
print(3 * 5)
assert 3 * 5 == 15''', [
E('Study budget', 'Return total hours for nonnegative weeks and hours_per_week; reject negative inputs.', 'def study_hours(weeks, hours_per_week):\n    raise NotImplementedError', '''def study_hours(weeks, hours_per_week):
    if weeks < 0 or hours_per_week < 0:
        raise ValueError("Time cannot be negative")
    return weeks * hours_per_week''', '''assert study_hours(80, 15) == 1200
assert study_hours(0, 15) == 0
expect_error(ValueError, lambda: study_hours(-1, 15))''', 'Validate before multiplying.', 'The unit is weeks × hours/week = hours. Validation makes your contract explicit.'),
E('Experiment manifest', 'Return a dictionary containing seed and Python version (under keys seed, python). Import sys inside your function.', 'def manifest(seed):\n    raise NotImplementedError', '''def manifest(seed):
    import sys
    return {"seed": seed, "python": sys.version.split()[0]}''', '''assert manifest(42)["seed"] == 42
assert len(manifest(42)["python"].split(".")) == 3''', 'sys.version contains a version and extra build text.', 'A seed alone is not full reproducibility: record dependencies, data hashes, hardware, and code revision too.'),
E('Reproducible randomness', 'Return n integer die rolls using a private random.Random(seed).', 'def rolls(n, seed):\n    raise NotImplementedError', '''def rolls(n, seed):
    import random
    rng = random.Random(seed)
    return [rng.randint(1, 6) for _ in range(n)]''', '''assert rolls(20, 7) == rolls(20, 7)
assert len(rolls(20, 7)) == 20
assert all(1 <= x <= 6 for x in rolls(20, 7))''', 'Keep generator state local.', 'A private generator prevents unrelated code from changing your experiment.')],
'Create work/hello.py, run it from the terminal, then reproduce it in a fresh notebook. Make a Git commit in your own learning repository and explain the diff.',
[('Why restart a kernel?', 'To expose missing dependencies on hidden in-memory state.'), ('Is a notebook a deployed service?', 'No. It is an interactive development artifact; a service needs a defined entry point, validation, lifecycle, and operational controls.')],
['https://docs.python.org/3/tutorial/'])

lesson('01a', 'Variables, decisions, and functions', 'stdlib',
['Trace variables and return values', 'Use conditions and exceptions', 'Write reusable functions'],
'''Integers count things, floats approximate real numbers, strings hold text, and booleans represent true/false. Operators combine values; comparisons produce booleans. `if/elif/else` selects one branch. `return` gives a caller a value; `print` only displays it. Prefer a function that returns a result because it is easier to reuse and test.

Parameters are names in a definition; arguments are values supplied by the caller. Local variables belong to one invocation. A default argument supplies a value when the caller omits it; avoid mutable defaults such as `items=[]`. Write the input contract before the implementation: valid types, units, invalid cases, and expected output. When an input cannot represent a valid request, raise a specific exception.''',
'''def celsius_to_fahrenheit(celsius):
    return celsius * 9 / 5 + 32

print(celsius_to_fahrenheit(20))
assert celsius_to_fahrenheit(0) == 32''', [
E('Profit function', 'Return (sell-buy)*shares. Require shares > 0 and prices >= 0.', 'def profit(buy, sell, shares):\n    raise NotImplementedError', '''def profit(buy, sell, shares):
    if shares <= 0 or min(buy, sell) < 0:
        raise ValueError("Invalid price or quantity")
    return (sell - buy) * shares''', '''assert profit(100, 110, 10) == 100
assert profit(10, 8, 2) == -4
expect_error(ValueError, lambda: profit(1, 2, 0))''', 'A loss is a valid output; a negative price is not.', 'Separate invalid inputs from valid but undesirable business outcomes.'),
E('Calculator', 'Support +, -, *, /. Reject unknown operators with ValueError and division by zero with ZeroDivisionError.', 'def calculate(a, op, b):\n    raise NotImplementedError', '''def calculate(a, op, b):
    if op == "+": return a + b
    if op == "-": return a - b
    if op == "*": return a * b
    if op == "/": return a / b
    raise ValueError("Unknown operator")''', '''assert calculate(6, "/", 2) == 3
assert calculate(6, "-", 9) == -3
expect_error(ZeroDivisionError, lambda: calculate(2, "/", 0))
expect_error(ValueError, lambda: calculate(2, "**", 4))''', 'Use explicit branches; do not evaluate arbitrary strings.', 'An allowlist keeps the behavior small, readable, and testable.'),
E('Tiered shipping', 'Orders >= 100 ship free; smaller nonnegative orders cost 5. A negative total raises ValueError.', 'def shipping(total):\n    raise NotImplementedError', '''def shipping(total):
    if total < 0: raise ValueError("Negative total")
    return 0 if total >= 100 else 5''', '''assert [shipping(x) for x in (0, 99, 100)] == [5, 5, 0]
expect_error(ValueError, lambda: shipping(-1))''', 'Test just below and exactly at the boundary.', 'Boundary examples find off-by-one and incorrect comparison operators.')],
'Build a terminal calculator and temperature converter with a loop. Handle invalid numeric input without hiding programming errors. Add five tests per function.',
[('Why return instead of print?', 'The caller can use or test a returned value; printed text is only a display side effect.'), ('What is scope?', 'The region in which a name can be resolved; function-local names do not automatically exist outside the call.')], ['https://docs.python.org/3/tutorial/controlflow.html'])

lesson('01b', 'Collections, loops, and text', 'stdlib',
['Select lists, tuples, sets, and dictionaries', 'Aggregate records with loops', 'Normalize text consistently'],
'''A list preserves order and allows changes. A tuple is useful for a fixed record or immutable key. A set stores unique values and supports membership and set operations. A dictionary maps unique keys to values; it is useful for counting and indexing.

A loop processes one element at a time. An accumulator collects partial results. A comprehension builds a collection from a simple expression; use a normal loop when validation or several steps would make a comprehension hard to read. Normalize data once at a boundary. For text counting, lowercase and punctuation rules must be explicit because “AI” and “ai” may otherwise become separate words. Do not modify a collection while iterating over it unless the behavior is deliberate.''',
'''totals = {}
for category, amount in [("food", 10), ("bus", 5), ("food", 8)]:
    totals[category] = totals.get(category, 0) + amount
print(totals)''', [
E('Word frequencies', 'Count lowercase words matching [a-z]+; return a dictionary. Empty text returns {}.', 'def word_counts(text):\n    raise NotImplementedError', '''def word_counts(text):
    import re
    counts = {}
    for word in re.findall(r"[a-z]+", text.lower()):
        counts[word] = counts.get(word, 0) + 1
    return counts''', '''assert word_counts("AI, ai! Data.") == {"ai": 2, "data": 1}
assert word_counts("") == {}''', 'Use dict.get(word, 0).', 'This tokenizer is deliberately ASCII-only; multilingual text needs a different policy.'),
E('Stable deduplication', 'Return the first occurrence of each hashable item, preserving input order.', 'def unique(items):\n    raise NotImplementedError', '''def unique(items):
    seen, result = set(), []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result''', '''assert unique([3, 1, 3, 2, 1]) == [3, 1, 2]
assert unique([]) == []''', 'A set tracks membership; a list tracks order.', 'Expected O(n) time uses O(n) extra memory; a nested membership scan can be quadratic.'),
E('Inventory update', 'Return a new dictionary with deltas applied. Reject a resulting negative count. Do not change the original.', 'def update_stock(stock, deltas):\n    raise NotImplementedError', '''def update_stock(stock, deltas):
    result = dict(stock)
    for item, delta in deltas.items():
        result[item] = result.get(item, 0) + delta
        if result[item] < 0: raise ValueError("Insufficient stock")
    return result''', '''original = {"pen": 3}
assert update_stock(original, {"pen": -2, "book": 1}) == {"pen": 1, "book": 1}
assert original == {"pen": 3}
expect_error(ValueError, lambda: update_stock(original, {"pen": -4}))''', 'Copy before updating.', 'Returning a new result avoids partial mutations when validation fails.')],
'Build a contact book with add, search, update, delete, and duplicate handling. Add a text analyzer that reports characters, word count, unique words, and deterministic top words.',
[('When is a set unsuitable?', 'When duplicates or positional order are meaningful.'), ('Why copy an input dictionary?', 'To keep the caller’s state unchanged and avoid partial updates on failure.')], ['https://docs.python.org/3/tutorial/datastructures.html'])

lesson('01c', 'Files, validation, and money', 'stdlib',
['Read CSV and JSON safely', 'Validate malformed records', 'Aggregate dates and exact decimal values'],
'''A file stores bytes; an encoding maps bytes to text. Use UTF-8 explicitly for portable text. `with open(...)` closes the resource even when an exception occurs. CSV is a table format whose quoting rules belong to a parser, not `split(',')`. JSON stores nested values, but dates and Decimal values need an explicit representation.

Money should not silently accumulate binary floating-point rounding. Decimal constructed from a string preserves the supplied decimal value. Validate at ingestion: required columns, parseable dates, finite nonnegative amounts, and blank categories. Choose a failure policy—reject the whole batch or quarantine bad rows—and explain it. An empty input should have a documented result. Avoid catching all exceptions because that hides defects unrelated to bad data.''',
'''from decimal import Decimal
print(Decimal("0.1") + Decimal("0.2"))
from pathlib import Path
print((ROOT / "datasets" / "expenses.csv").exists())''', [
E('Amount parser', 'Parse a string as a finite, nonnegative Decimal; raise ValueError on invalid inputs including NaN.', 'def parse_amount(value):\n    raise NotImplementedError', '''def parse_amount(value):
    from decimal import Decimal, InvalidOperation
    try:
        amount = Decimal(value)
    except (InvalidOperation, TypeError):
        raise ValueError("Invalid amount") from None
    if not amount.is_finite() or amount < 0:
        raise ValueError("Invalid amount")
    return amount''', '''from decimal import Decimal
assert parse_amount("12.50") == Decimal("12.50")
for bad in ("NaN", "-1", "oops", "Infinity"):
    expect_error(ValueError, lambda bad=bad: parse_amount(bad))''', 'Check is_finite before comparing to zero.', 'NaN and infinity can poison aggregates without obvious parsing failures.'),
E('CSV summary', 'For CSV text with date,category,amount, return total Decimal and by_category dict. Validate ISO dates and nonblank categories; use parse_amount.', 'def summarize_csv(text):\n    raise NotImplementedError', '''def summarize_csv(text):
    import csv, io
    from datetime import date
    from decimal import Decimal
    total, groups = Decimal("0"), {}
    for row in csv.DictReader(io.StringIO(text)):
        date.fromisoformat(row["date"])
        category = row["category"].strip()
        if not category: raise ValueError("Blank category")
        amount = parse_amount(row["amount"])
        total += amount
        groups[category] = groups.get(category, Decimal("0")) + amount
    return total, groups''', '''sample = "date,category,amount\\n2026-01-01,Food,0.10\\n2026-01-02,Food,0.20\\n"
total, groups = summarize_csv(sample)
assert str(total) == "0.30" and groups == {"Food": total}
assert summarize_csv("date,category,amount\\n")[0] == 0''', 'DictReader yields one dictionary per record.', 'Parsing belongs at the boundary; downstream calculations can assume valid typed values.'),
E('JSON contract', 'Serialize a total Decimal and currency into JSON strings, using keys total and currency. Preserve the decimal text.', 'def report_json(total, currency="USD"):\n    raise NotImplementedError', '''def report_json(total, currency="USD"):
    import json
    return json.dumps({"total": str(total), "currency": currency}, sort_keys=True)''', '''import json
assert json.loads(report_json(Decimal("0.30"))) == {"total": "0.30", "currency": "USD"}''', 'Convert Decimal explicitly to str.', 'A JSON string prevents a consumer from assuming exact decimal arithmetic from a binary float.')],
'Build the expense CLI in Stage 01: total, category/month summaries, mean, maximum, and bad-row diagnostics. Use a temporary directory for file tests.',
[('Why not split CSV manually?', 'Commas and newlines may occur inside quoted fields.'), ('What is a useful error message?', 'One that identifies the record and invalid field without exposing unrelated sensitive data.')], ['https://docs.python.org/3/library/csv.html'])

lesson('01d', 'Objects, algorithms, and debugging', 'stdlib',
['Encapsulate state with a class', 'Reason about algorithm cost', 'Test a bug before fixing it'],
'''A class groups state and related behavior. A constructor creates an instance; methods operate on that instance. Composition places one object inside another and often keeps dependencies clearer than deep inheritance. A property can expose controlled access to state. Type hints document intent but do not enforce runtime validation.

Big O describes how work grows with input size, not elapsed milliseconds. Scanning a list is O(n); binary search on sorted data is O(log n); comparison sorting is typically O(n log n). Recursion solves a smaller version of the same problem and needs a base case. Python recursion depth is limited.

Debugging starts with a reproducible failing example. Read the traceback, inspect inputs and intermediate values, form a hypothesis, change one thing, rerun. Unit tests isolate one component; integration tests exercise collaboration. Mock an external boundary, not the logic you are trying to verify.''',
'''from dataclasses import dataclass
@dataclass(frozen=True)
class Ticket:
    id: int
    category: str
print(Ticket(1, "access"))''', [
E('Inventory object', 'Implement Inventory with fresh per-instance items and add(name, quantity); quantity must be positive.', 'class Inventory:\n    def __init__(self):\n        raise NotImplementedError\n    def add(self, name, quantity):\n        raise NotImplementedError', '''class Inventory:
    def __init__(self):
        self.items = {}
    def add(self, name, quantity):
        if quantity <= 0: raise ValueError("Positive quantity required")
        self.items[name] = self.items.get(name, 0) + quantity''', '''a, b = Inventory(), Inventory()
a.add("book", 2)
assert a.items == {"book": 2} and b.items == {}
expect_error(ValueError, lambda: a.add("book", 0))''', 'Do not put mutable instance state on the class.', 'A shared class dictionary would contaminate every inventory.'),
E('Binary search', 'For sorted ascending values, return an index of target, else -1. Use an iterative halving algorithm.', 'def binary_search(values, target):\n    raise NotImplementedError', '''def binary_search(values, target):
    lo, hi = 0, len(values) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if values[mid] == target: return mid
        if values[mid] < target: lo = mid + 1
        else: hi = mid - 1
    return -1''', '''assert binary_search([1, 3, 5, 7], 5) == 2
assert binary_search([], 1) == -1
assert binary_search([1, 3], 2) == -1''', 'Exclude mid after comparing or the loop may never shrink.', 'Each comparison halves the remaining search space. Sorting first costs more than one linear lookup.'),
E('Regression fix', 'Return the arithmetic mean of values. Empty input raises ValueError; do not divide by len(values)-1.', 'def average(values):\n    raise NotImplementedError', '''def average(values):
    if not values: raise ValueError("Empty sample")
    return sum(values) / len(values)''', '''assert average([2, 4]) == 3
assert average([9]) == 9
expect_error(ValueError, lambda: average([]))''', 'A one-element sample is an especially useful regression case.', 'The denominator n-1 belongs to sample variance, not the mean.')],
'Refactor the expense analyzer into parser, domain, and CLI modules. Add pytest tests, one mock for a file failure, logging, a recursive directory-size exercise, and a measured linear-versus-binary search experiment.',
[('Why prefer composition here?', 'You can replace a storage object without making the analyzer a subtype of storage.'), ('What must a recursive function have?', 'A terminating base case and a step that moves toward it.')], ['https://docs.python.org/3/tutorial/classes.html'])

lesson('02a', 'Vectors, matrices, and algebra', 'stdlib',
['Track dimensions and units', 'Implement dot products and cosine similarity', 'Explain matrix multiplication and eigenvectors'],
'''A scalar is one number, a vector an ordered collection, and a matrix a rectangular collection. A tensor generalizes dimensions. A dot product sums pairwise products and requires equal lengths. A matrix A of shape (m,n) can multiply B of shape (n,p), producing (m,p). Each output is a row-column dot product.

The Euclidean norm measures length. Cosine similarity divides a dot product by both vector norms, measuring direction rather than magnitude; it is undefined for a zero vector. A transpose swaps axes. An identity matrix leaves vectors unchanged. An eigenvector keeps its direction under a matrix transformation: Av = λv. Embeddings are learned vectors, so geometry helps explain retrieval.

Algebra expresses relationships with functions: y=mx+b, powers, logarithms, and summations. Logarithms turn products into sums and appear in likelihoods. Always check the domain: log requires positive real inputs.''',
'''import math
v = [3, 4]
print(math.sqrt(sum(x*x for x in v)))
print(math.log(math.e))''', [
E('Dot product', 'Return sum(a_i*b_i); reject unequal lengths.', 'def dot(a, b):\n    raise NotImplementedError', '''def dot(a, b):
    if len(a) != len(b): raise ValueError("Shape mismatch")
    return sum(x*y for x, y in zip(a, b))''', '''assert dot([1, 2], [3, 4]) == 11
expect_error(ValueError, lambda: dot([1], [2, 3]))''', 'zip alone silently truncates.', 'A dimension error must be visible rather than becoming a plausible wrong result.'),
E('Cosine similarity', 'Use dot to return cosine similarity; reject a zero vector.', 'def cosine(a, b):\n    raise NotImplementedError', '''def cosine(a, b):
    import math
    numerator = dot(a, b)
    denominator = math.sqrt(dot(a, a) * dot(b, b))
    if denominator == 0: raise ValueError("Zero vector")
    return numerator / denominator''', '''assert abs(cosine([1, 0], [0, 1])) < 1e-12
assert abs(cosine([2, 2], [1, 1])-1) < 1e-12
expect_error(ValueError, lambda: cosine([0, 0], [1, 2]))''', 'Magnitude cancels for parallel vectors.', 'Two differently scaled embeddings can have the same direction.'),
E('Matrix multiplication', 'Multiply nonempty rectangular nested lists. Validate rectangularity and inner dimensions.', 'def matmul(a, b):\n    raise NotImplementedError', '''def matmul(a, b):
    if not a or not b or not a[0] or not b[0]: raise ValueError("Empty matrix")
    if any(len(row) != len(a[0]) for row in a) or any(len(row) != len(b[0]) for row in b):
        raise ValueError("Ragged matrix")
    if len(a[0]) != len(b): raise ValueError("Shape mismatch")
    return [[dot(row, col) for col in zip(*b)] for row in a]''', '''assert matmul([[1, 2]], [[3], [4]]) == [[11]]
assert matmul([[2, 3]], [[1, 0], [0, 1]]) == [[2, 3]]
expect_error(ValueError, lambda: matmul([[1, 2]], [[1, 2]]))''', 'zip(*b) exposes columns.', 'Matrix multiplication is not elementwise multiplication; shape reasoning catches many neural-network bugs.')],
'Implement vector addition, transpose, norms, distances, and a 2D rotation. Draw original/transformed vectors. Check an eigenvector for diagonal matrix diag(2,3). Repeat using NumPy in Stage 03.',
[('What does a dot product measure?', 'A sum of pairwise products; geometrically it combines length and directional alignment.'), ('Why does shape matter?', 'It defines which operations are valid and the meaning of each axis.')], ['https://d2l.ai/chapter_preliminaries/linear-algebra.html'])

lesson('02b', 'Derivatives and optimization', 'stdlib',
['Approximate and derive gradients', 'Implement gradient descent', 'Diagnose learning-rate failures'],
'''A derivative is a local rate of change, defined as the limit of a difference quotient. A partial derivative changes one input while holding others fixed. A gradient collects partial derivatives. The chain rule propagates derivatives through composed functions, which makes backpropagation possible.

For mean squared error L(w)=mean((wx-y)^2), dL/dw=mean(2x(wx-y)). Gradient descent updates w ← w-η∇L. The minus sign moves downhill locally, and η is the learning rate. Too large a rate can diverge; too small a rate can stall. A finite-difference check compares your analytical gradient to (L(w+h)-L(w-h))/(2h). Very tiny h suffers cancellation.

Regularization adds a preference to the objective: L2 adds λw² and gradient 2λw. Nonconvex objectives may have local minima and saddle points; a decreasing training loss alone says nothing about generalization.''',
'''def loss(w):
    return (w - 3) ** 2
w = 0.0
for _ in range(5):
    w -= 0.1 * 2 * (w - 3)
    print(round(w, 4), round(loss(w), 4))''', [
E('Numerical derivative', 'Approximate f prime at x using a central difference with h > 0.', 'def derivative(f, x, h=1e-5):\n    raise NotImplementedError', '''def derivative(f, x, h=1e-5):
    if h <= 0: raise ValueError("Positive step required")
    return (f(x+h)-f(x-h))/(2*h)''', '''assert abs(derivative(lambda x: x*x, 3)-6) < 1e-6
expect_error(ValueError, lambda: derivative(lambda x: x, 0, 0))''', 'Evaluate on both sides of x.', 'Central differences balance first-order truncation errors.'),
E('Linear gradient', 'Return the MSE gradient for scalar w on equally sized nonempty xs, ys.', 'def mse_gradient(w, xs, ys):\n    raise NotImplementedError', '''def mse_gradient(w, xs, ys):
    if not xs or len(xs) != len(ys): raise ValueError("Invalid data")
    return sum(2*x*(w*x-y) for x, y in zip(xs, ys))/len(xs)''', '''xs, ys = [1, 2, 3], [2, 4, 6]
f = lambda w: sum((w*x-y)**2 for x,y in zip(xs,ys))/len(xs)
assert abs(mse_gradient(1, xs, ys)-derivative(f, 1)) < 1e-6''', 'Differentiate each residual squared, then average.', 'Gradient checks detect signs, missing factors, and incorrect reductions.'),
E('Fit one weight', 'Start at w=0, apply steps gradient updates, and return w. Defaults should fit y=2x.', 'def fit_weight(xs, ys, lr=0.05, steps=100):\n    raise NotImplementedError', '''def fit_weight(xs, ys, lr=0.05, steps=100):
    w = 0.0
    for _ in range(steps):
        w -= lr * mse_gradient(w, xs, ys)
    return w''', '''assert abs(fit_weight([1, 2, 3], [2, 4, 6])-2) < 1e-6''', 'Recompute the gradient after every update.', 'This is optimization of a known objective, not a general guarantee that learning works.')],
'Add an intercept, L2 regularization, and loss history. Compare rates 0.001, 0.05, and 1.0. Explain divergence from the update equation; save a loss plot.',
[('What does the chain rule do?', 'It multiplies local derivatives along a computation path and sums contributions from multiple paths.'), ('Does low training loss imply good predictions?', 'No; evaluation on unseen data is needed.')], ['https://d2l.ai/chapter_preliminaries/calculus.html'])

lesson('02c', 'Probability, statistics, and uncertainty', 'stdlib',
['Compute sample statistics', 'Apply conditional probability and Bayes rule', 'Estimate uncertainty with reproducible bootstrap samples'],
'''A random variable maps outcomes to numbers. Bernoulli models one binary trial; binomial counts successes across independent trials; a normal distribution is continuous and symmetric. Independence means observing one variable does not change the distribution of another. Conditional probability P(A|B) restricts attention to B. Bayes rule reverses conditioning using a base rate.

The mean is the arithmetic center; median resists extreme outliers; mode is the most frequent value. Variance measures squared deviations; standard deviation restores the original units. Sample variance uses n-1 when estimating population variance from an IID sample. Covariance tracks joint variation; correlation normalizes it and does not establish causation.

A confidence interval is a property of a repeated-sampling procedure, not the probability that a fixed parameter lies in this one observed interval. Bootstrap intervals resample observed data and inherit its biases. A p-value is the probability, under a specified null model, of a statistic at least as extreme as observed; it is not the probability the null is true.''',
'''import statistics
sample = [2, 4, 4, 6]
print(statistics.mean(sample), statistics.median(sample), statistics.variance(sample))''', [
E('Sample variance', 'Compute unbiased sample variance for n >= 2; reject smaller samples.', 'def variance(xs):\n    raise NotImplementedError', '''def variance(xs):
    if len(xs) < 2: raise ValueError("Need two observations")
    mean = sum(xs)/len(xs)
    return sum((x-mean)**2 for x in xs)/(len(xs)-1)''', '''assert variance([1, 2, 3]) == 1
expect_error(ValueError, lambda: variance([1]))''', 'Compute the mean first.', 'The n-1 adjustment compensates for estimating the mean from the same sample.'),
E('Bayesian alert', 'Return P(event|positive) from prevalence, sensitivity, and false_positive_rate in [0,1]. Reject an impossible positive event.', 'def posterior(prevalence, sensitivity, false_positive_rate):\n    raise NotImplementedError', '''def posterior(prevalence, sensitivity, false_positive_rate):
    if any(not 0 <= p <= 1 for p in (prevalence, sensitivity, false_positive_rate)):
        raise ValueError("Invalid probability")
    true = prevalence*sensitivity
    positive = true + (1-prevalence)*false_positive_rate
    if positive == 0: raise ValueError("Impossible conditioning event")
    return true/positive''', '''assert abs(posterior(.01, .9, .1)-(.009/.108)) < 1e-12
expect_error(ValueError, lambda: posterior(0, 1, 0))''', 'Count true positives and false positives in an imagined population.', 'Rare events can yield many false alarms even with high sensitivity.'),
E('Bootstrap mean interval', 'Return the 2.5th and 97.5th percentile order statistics of 1000 bootstrap means using seed=42. Require nonempty data.', 'def bootstrap_ci(xs, repeats=1000, seed=42):\n    raise NotImplementedError', '''def bootstrap_ci(xs, repeats=1000, seed=42):
    import random
    if not xs or repeats < 40: raise ValueError("Insufficient data or repeats")
    rng = random.Random(seed)
    means = sorted(sum(rng.choices(xs, k=len(xs)))/len(xs) for _ in range(repeats))
    return means[int(.025*repeats)], means[int(.975*repeats)]''', '''lo, hi = bootstrap_ci([1, 2, 3, 4, 5])
assert lo <= 3 <= hi
assert bootstrap_ci([2]*10) == (2, 2)''', 'Resample with replacement, keeping sample size fixed.', 'This simple percentile interval assumes representative independent observations; time series need block-aware methods.')],
'Simulate 10,000 Bernoulli trials, plot a binomial count histogram, calculate percentiles/covariance/correlation, and run a permutation test of a mean difference. Explain sampling bias and multiple testing.',
[('What is a base-rate error?', 'Ignoring prevalence when converting a test result to a posterior probability.'), ('Why is correlation insufficient for causation?', 'Confounding, selection, or reverse causality can produce association.')], ['https://d2l.ai/chapter_preliminaries/probability.html'])

lesson('03a', 'NumPy and Pandas data contracts', 'data',
['Inspect shapes and broadcasting', 'Clean, join, and summarize tabular data', 'Preserve provenance and missingness'],
'''NumPy arrays hold regular typed data. Broadcasting aligns axes from the right: dimensions must match or one must equal 1. A (n,1) column minus a (d,) row produces (n,d); accidentally subtracting (n,) from (n,1) produces (n,n). Inspect shape before trusting a result.

Pandas labels rows and columns. Its joins align keys, not row positions. Duplicate keys on both sides can multiply rows, so use merge validation. Missing values represent absent information; zero is an observed value and should not be substituted automatically. Parse dates explicitly, sort before rolling calculations, and document duplicate policy.

A data contract defines fields, types, units, valid ranges, uniqueness, and freshness. Keep rejected records with a reason. Fit statistical imputers only on training data; cleaning based on fixed domain rules is different from learning a transformation from observations.''',
'''import numpy as np
import pandas as pd
x = np.array([[1., 2.], [3., 4.]])
print(x.shape, x.mean(axis=0))
print(pd.read_csv(ROOT / "datasets" / "expenses.csv").head())''', [
E('Column standardization', 'Standardize each column using population std. Constant columns become zeros. Return a NumPy array.', 'def standardize(x):\n    raise NotImplementedError', '''def standardize(x):
    import numpy as np
    x = np.asarray(x, dtype=float)
    std = x.std(axis=0)
    return (x-x.mean(axis=0))/np.where(std == 0, 1, std)''', '''z = standardize([[1, 7], [3, 7]])
assert np.allclose(z, [[-1, 0], [1, 0]])''', 'Replace zero denominators, not output NaNs.', 'In ML, save training mean/std and reuse them on validation and test data.'),
E('Monthly spending', 'Parse dates and amounts, group by calendar month string YYYY-MM, return a sorted Series. Use a copied frame.', 'def monthly_spending(frame):\n    raise NotImplementedError', '''def monthly_spending(frame):
    import pandas as pd
    frame = frame.copy()
    frame["date"] = pd.to_datetime(frame["date"], errors="raise")
    frame["amount"] = pd.to_numeric(frame["amount"], errors="raise")
    return frame.groupby(frame["date"].dt.strftime("%Y-%m"))["amount"].sum().sort_index()''', '''frame = pd.DataFrame({"date": ["2026-02-01", "2026-01-01", "2026-01-03"], "amount": [4, 2, 3]})
assert monthly_spending(frame).to_dict() == {"2026-01": 5, "2026-02": 4}''', 'dt.strftime creates the monthly grouping key.', 'This float-based exploration is fine for visualization; exact ledger arithmetic should retain decimal or integer cents.'),
E('Safe join', 'Left-join orders and customers on customer_id; enforce many-to-one and preserve row count.', 'def enrich(orders, customers):\n    raise NotImplementedError', '''def enrich(orders, customers):
    return orders.merge(customers, on="customer_id", how="left", validate="many_to_one")''', '''orders = pd.DataFrame({"customer_id": [1, 1, 2], "amount": [1, 2, 3]})
customers = pd.DataFrame({"customer_id": [1, 2], "name": ["A", "B"]})
assert len(enrich(orders, customers)) == 3
expect_error(pd.errors.MergeError, lambda: enrich(orders, pd.concat([customers, customers])))''', 'Use the validate parameter.', 'Join explosions can silently distort totals and training distributions.')],
'Profile missing values, duplicates, date ranges, and outliers in expenses.csv. Write a cleaning report and a three-day rolling mean. Explain every exclusion.',
[('What is broadcasting?', 'Expansion of compatible singleton dimensions during array operations without explicitly copying all values.'), ('Why validate a join?', 'It detects key cardinality violations that can duplicate or lose records.')], ['https://numpy.org/doc/stable/user/basics.broadcasting.html', 'https://pandas.pydata.org/docs/user_guide/'])

lesson('03b', 'SQL, transactions, and schema design', 'stdlib',
['Write joins, CTEs, and window queries', 'Parameterize user values', 'Use transactions and constraints'],
'''SQL describes desired results over tables. WHERE filters rows before grouping; HAVING filters groups. INNER JOIN requires a match; LEFT JOIN preserves unmatched left rows. UNION removes duplicates; UNION ALL preserves them. A CTE names an intermediate query; a subquery embeds a query inside another. Window functions compute across related rows without collapsing them.

Primary keys identify rows. Foreign keys enforce relationships. Normalization separates facts so updates do not produce contradictions. Indexes trade write/storage cost for faster access paths; inspect a query plan. A transaction groups operations atomically. Never construct SQL by interpolating user values; bind parameters instead. Schema migrations are versioned changes with a tested rollout strategy.

These exercises use SQLite for an offline first step. The project repeats them in PostgreSQL, where concurrency, types, query plans, and migration behavior need direct testing.''',
'''import sqlite3
conn = sqlite3.connect(":memory:")
conn.executescript("CREATE TABLE orders(id INTEGER PRIMARY KEY, customer TEXT, amount INTEGER); INSERT INTO orders VALUES(1,'A',10),(2,'A',20),(3,'B',7);")
print(conn.execute("SELECT customer, SUM(amount) FROM orders GROUP BY customer").fetchall())''', [
E('Bound filter', 'Return (id,amount) rows for a customer ordered by id, using SQL parameters.', 'def customer_orders(conn, customer):\n    raise NotImplementedError', '''def customer_orders(conn, customer):
    return conn.execute("SELECT id, amount FROM orders WHERE customer = ? ORDER BY id", (customer,)).fetchall()''', '''assert customer_orders(conn, "A") == [(1, 10), (2, 20)]
assert customer_orders(conn, "' OR 1=1 --") == []''', 'The SQL structure stays constant.', 'Parameter binding treats the entire input as data, including quotes and SQL-like text.'),
E('Running totals', 'Return (id,running_amount) per customer, ordered by id. Use SUM OVER with an explicit ROWS frame.', 'def running_totals(conn):\n    raise NotImplementedError', '''def running_totals(conn):
    return conn.execute("SELECT id, SUM(amount) OVER (PARTITION BY customer ORDER BY id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) FROM orders ORDER BY id").fetchall()''', '''assert running_totals(conn) == [(1, 10), (2, 30), (3, 7)]''', 'Partition by customer, order by id.', 'An explicit frame removes ambiguity about equal sort keys.'),
E('Atomic batch', 'Insert rows inside a transaction; any duplicate key rolls back the entire batch.', 'def insert_batch(conn, rows):\n    raise NotImplementedError', '''def insert_batch(conn, rows):
    with conn:
        conn.executemany("INSERT INTO orders VALUES (?, ?, ?)", rows)''', '''expect_error(sqlite3.IntegrityError, lambda: insert_batch(conn, [(4, "C", 4), (1, "D", 5)]))
assert conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 3''', 'The connection context manager rolls back on an exception.', 'Partial ingestion can create inconsistent reports; atomicity keeps the batch all-or-nothing.')],
'Design customers, records, and categories tables with keys; write INNER/LEFT joins, CTE, HAVING, UNION, and correlated subquery examples. Use PostgreSQL EXPLAIN before/after an index and demonstrate rollback.',
[('Why a LEFT JOIN?', 'To retain a row even when no related row exists, such as a customer with no orders.'), ('Are indexes free?', 'No. They consume storage and must be maintained on writes.')], ['https://www.postgresql.org/docs/current/tutorial.html'])

lesson('03c', 'HTTP, validation, and FastAPI', 'data',
['Model request and response contracts', 'Test HTTP errors without a live server', 'Separate authentication and authorization'],
'''HTTP requests have a method, path, headers, and optional body. GET reads; POST creates or triggers work; PUT usually replaces; PATCH partially updates; DELETE removes. Status codes communicate outcomes: 2xx success, 4xx client/request failures, 5xx server failures. A JSON response still needs a schema.

FastAPI maps functions to routes and Pydantic validates input. Dependency injection supplies shared resources such as database sessions and the authenticated principal. Middleware can record request duration or attach a request ID. Authentication establishes identity; authorization decides what that identity may access. Derive tenant scope on the server from verified identity, never from a caller-supplied tenant field.

Use tests at the HTTP boundary to verify status codes, bodies, malformed inputs, and permissions. An in-memory list is useful for this first exercise but loses data on restart and is not safe shared storage for multiple workers.''',
'''from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field
app = FastAPI()
@app.get("/health")
def health():
    return {"status": "ok"}
assert TestClient(app).get("/health").json() == {"status": "ok"}''', [
E('Request schema', 'Define Record(BaseModel) with category length 1..50 and amount finite >=0.', 'class Record(BaseModel):\n    pass', '''from pydantic import BaseModel, Field
class Record(BaseModel):
    category: str = Field(min_length=1, max_length=50)
    amount: float = Field(ge=0, allow_inf_nan=False)''', '''assert Record(category="Food", amount=2).amount == 2
from pydantic import ValidationError
expect_error(ValidationError, lambda: Record(category="", amount=-1))''', 'Import BaseModel and Field before defining your class.', 'Validation expresses constraints centrally and generates an API schema.'),
E('Create endpoint', 'Write make_app() with POST /records returning the validated record with status 201.', 'def make_app():\n    raise NotImplementedError', '''def make_app():
    app = FastAPI()
    @app.post("/records", status_code=201)
    def create(record: Record):
        return record
    return app''', '''client = TestClient(make_app())
assert client.post("/records", json={"category": "Food", "amount": 2}).status_code == 201
assert client.post("/records", json={"category": "", "amount": -1}).status_code == 422''', 'Annotate the body with your Pydantic model.', 'HTTP tests prove invalid input is rejected at the boundary, not just inside a helper.'),
E('Pagination contract', 'Return a slice for offset>=0 and 1<=limit<=100; reject other bounds.', 'def paginate(rows, offset=0, limit=20):\n    raise NotImplementedError', '''def paginate(rows, offset=0, limit=20):
    if offset < 0 or not 1 <= limit <= 100: raise ValueError("Invalid pagination")
    return rows[offset:offset+limit]''', '''assert paginate(list(range(10)), 3, 2) == [3, 4]
expect_error(ValueError, lambda: paginate([], 0, 1000))''', 'Bound resource usage at the API boundary.', 'A production database uses stable ordering and LIMIT/OFFSET or cursor pagination rather than loading all rows.')],
'Build Stage 03’s persistent API with GET /records, /summary, /statistics and POST /records. Add auth, request IDs, tests, and PostgreSQL ingestion. Restart it and prove persistence.',
[('What does 422 mean here?', 'The request body fails the declared validation contract.'), ('Why inject a database session?', 'It makes resource lifetime explicit and allows test substitution.')], ['https://fastapi.tiangolo.com/tutorial/'])
