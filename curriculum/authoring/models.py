from schema import lesson, exercise as E

lesson('04a', 'Supervised learning without leakage', 'data',
['Build baselines and pipelines', 'Compare regression and classification models', 'Separate training, validation, and final testing'],
'''A feature is an input available at prediction time; a label is the target. Regression predicts a number; classification predicts a category. Training fits parameters. Validation chooses modeling decisions. The test set estimates performance after those choices are frozen. Never fit preprocessing on the test set.

Start with a baseline: mean prediction for regression or majority class for classification. Linear regression fits additive relationships; logistic regression maps a linear score to class probabilities. Trees partition feature space; random forests average trees; gradient boosting adds models that correct residual errors. k-nearest neighbors uses nearby examples; SVMs maximize a separating margin. Their inductive biases differ, so compare on the same evaluation protocol.

A pipeline fits preprocessing inside each cross-validation fold. Group related users/templates/documents together when splitting, and split by time when predicting the future. Duplicates across splits can make a weak model look excellent. Hyperparameter tuning must not repeatedly consult the final test set.''',
'''from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
pipeline = make_pipeline(StandardScaler(), LogisticRegression(max_iter=500))
print(pipeline)''', [
E('Regression baseline', 'Predict the training-label mean for every test item. Reject empty training labels.', 'def mean_baseline(train_y, n):\n    raise NotImplementedError', '''def mean_baseline(train_y, n):
    if len(train_y) == 0: raise ValueError("Empty training labels")
    return [sum(train_y)/len(train_y)]*n''', '''assert mean_baseline([2, 4, 6], 2) == [4, 4]''', 'Do not inspect test labels.', 'Even a baseline can leak if its mean comes from the test set.'),
E('Text pipeline', 'Return an unfitted TF-IDF + LogisticRegression pipeline with max_iter=500, random_state=42.', 'def text_pipeline():\n    raise NotImplementedError', '''def text_pipeline():
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    return make_pipeline(TfidfVectorizer(ngram_range=(1, 2)), LogisticRegression(max_iter=500, random_state=42))''', '''model = text_pipeline().fit(["login password", "account login", "refund invoice", "billing invoice"], [0, 0, 1, 1])
assert model.predict(["password login", "invoice refund"]).tolist() == [0, 1]''', 'Vectorization belongs inside the pipeline.', 'Vocabulary and IDF weights are learned transformations and must see training data only.'),
E('Group separation', 'Given rows with group and split keys, return True only if no group appears in multiple splits.', 'def groups_are_separate(rows):\n    raise NotImplementedError', '''def groups_are_separate(rows):
    seen = {}
    for row in rows:
        group, split = row["group"], row["split"]
        if group in seen and seen[group] != split: return False
        seen[group] = split
    return True''', '''assert groups_are_separate([{"group": "a", "split": "train"}, {"group": "b", "split": "test"}])
assert not groups_are_separate([{"group": "a", "split": "train"}, {"group": "a", "split": "test"}])''', 'Remember the first split assigned to a group.', 'Grouping by a shared source tests generalization beyond near-duplicate examples.')],
'Train the support-ticket project with DummyClassifier, logistic regression, random forest, and gradient boosting. Fit a separate synthetic demand regression task with linear, tree, forest, and boosting models. Record MAE, RMSE, R² and classification macro-F1.',
[('What is leakage?', 'Use of information unavailable at prediction time, including test-derived preprocessing or future labels.'), ('Why can a simple model win?', 'Limited data, strong linear signal, lower variance, and fewer tuning opportunities may favor it.')], ['https://scikit-learn.org/stable/common_pitfalls.html'])

lesson('04b', 'Metrics, clustering, and error analysis', 'data',
['Compute precision, recall, and F1', 'Choose metrics for the cost of errors', 'Explore PCA and clustering without inventing labels'],
'''Accuracy is the fraction correct and can hide failure on a rare class. Precision asks what fraction of predicted positives are correct; recall asks what fraction of true positives were found. F1 is their harmonic mean. Macro averaging weights classes equally; micro averaging pools decisions. Inspect the confusion matrix and actual errors.

ROC varies a classification threshold and plots true-positive against false-positive rate; ROC-AUC measures ranking, not calibration. Precision-recall curves often expose rare-class performance more directly. Tune thresholds on validation data using business costs. A model score is not automatically a calibrated probability.

Unsupervised learning has no supplied labels. K-means minimizes squared within-cluster distances and prefers roughly spherical groups. DBSCAN groups dense regions and marks noise. PCA finds orthogonal directions of greatest variance; it can compress features but does not identify causal factors. Scaling changes distances and therefore clusters.''',
'''from sklearn.metrics import confusion_matrix
print(confusion_matrix([1, 1, 0, 0], [1, 0, 1, 0]))''', [
E('Binary metrics', 'Return precision, recall, f1 for 0/1 truth and predictions of equal length. Zero denominators yield zero.', 'def binary_metrics(y, pred):\n    raise NotImplementedError', '''def binary_metrics(y, pred):
    if len(y) != len(pred): raise ValueError("Length mismatch")
    tp = sum(a == b == 1 for a, b in zip(y, pred))
    fp = sum(a == 0 and b == 1 for a, b in zip(y, pred))
    fn = sum(a == 1 and b == 0 for a, b in zip(y, pred))
    p = tp/(tp+fp) if tp+fp else 0
    r = tp/(tp+fn) if tp+fn else 0
    return p, r, 2*p*r/(p+r) if p+r else 0''', '''assert binary_metrics([1, 1, 0], [1, 0, 1]) == (.5, .5, .5)
assert binary_metrics([0], [0]) == (0, 0, 0)''', 'Count TP, FP, and FN first.', 'Defining zero-denominator behavior avoids accidental NaNs in reports.'),
E('Cost-sensitive threshold', 'Return total cost with false negatives costing 5 and false positives 1; score >= threshold predicts 1.', 'def decision_cost(y, scores, threshold):\n    raise NotImplementedError', '''def decision_cost(y, scores, threshold):
    return sum(5 if actual == 1 and score < threshold else 1 if actual == 0 and score >= threshold else 0 for actual, score in zip(y, scores))''', '''assert decision_cost([1, 0], [.4, .6], .5) == 6
assert decision_cost([1, 0], [.4, .6], .3) == 1''', 'The same scores can produce different operating costs.', 'The lowest validation cost may sacrifice accuracy; report that tradeoff.'),
E('PCA pipeline', 'Fit StandardScaler then PCA(n_components=1) on X and return transformed data plus pipeline.', 'def reduce_dimension(x):\n    raise NotImplementedError', '''def reduce_dimension(x):
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.decomposition import PCA
    pipe = make_pipeline(StandardScaler(), PCA(n_components=1))
    return pipe.fit_transform(x), pipe''', '''z, pipe = reduce_dimension([[1, 2], [2, 4], [3, 6]])
assert z.shape == (3, 1)
assert pipe[-1].explained_variance_ratio_[0] > .999''', 'Scale first because units affect variance.', 'PCA direction signs may flip across implementations; test explained variance, not the sign.')],
'Compare KMeans and DBSCAN on two-moons and blob datasets. Explain failure shapes, outliers, and scale sensitivity. Write a ticket error taxonomy with at least 20 independently labeled new examples.',
[('Can AUC select a deployment threshold?', 'No. AUC summarizes ranking across thresholds; deployment needs a specific operating point.'), ('Are clusters ground-truth categories?', 'No. They depend on representation, distance, and algorithm assumptions.')], ['https://scikit-learn.org/stable/modules/model_evaluation.html'])

lesson('05a', 'A neural network from scratch', 'data',
['Implement forward and backward passes', 'Track matrix dimensions', 'Verify gradients before training'],
'''A neuron computes a weighted sum plus bias, followed by an activation. Layers compose these transformations. Without nonlinear activations, stacked linear layers collapse into one linear transformation. ReLU keeps positive values, sigmoid maps to (0,1), tanh to (-1,1), and softmax normalizes class scores.

For a batch X of shape (n,d), a weight matrix W of shape (d,h) gives hidden activations (n,h). A loss measures prediction error. Backpropagation applies the chain rule to compute parameter gradients. The optimizer updates parameters; it does not compute the forward loss itself.

MSE is common for regression. Binary cross entropy suits a binary target; multiclass cross entropy uses one target class per example. Stable implementations operate on logits to avoid logarithms of rounded probabilities. Verify individual gradients numerically before trusting a loss curve. Here a one-layer regression network isolates the mechanics; the project extends it to two layers and XOR.''',
'''import numpy as np
x = np.array([[1., 2.], [3., 4.]])
w = np.array([[.2], [.3]])
print((x @ w).shape)''', [
E('Stable sigmoid', 'Return a sigmoid for NumPy input without overflowing exp on large magnitudes.', 'def sigmoid(x):\n    raise NotImplementedError', '''def sigmoid(x):
    import numpy as np
    x = np.asarray(x, dtype=float)
    z = np.exp(-np.abs(x))
    return np.where(x >= 0, 1/(1+z), z/(1+z))''', '''assert np.allclose(sigmoid([-1000, 0, 1000]), [0, .5, 1])''', 'Exponentiate negative absolute values only.', 'Numerical stability is part of correctness, not a cosmetic optimization.'),
E('Linear backward pass', 'For X(n,d), y(n,1), w(d,1), scalar b, return MSE, dw, db.', 'def backward(x, y, w, b):\n    raise NotImplementedError', '''def backward(x, y, w, b):
    residual = x @ w + b - y
    loss = float((residual**2).mean())
    return loss, 2*x.T@residual/len(x), float(2*residual.mean())''', '''x = np.array([[1.], [2.]])
y = 2*x
w = np.zeros((1, 1))
loss, dw, db = backward(x, y, w, 0)
assert loss == 10 and np.allclose(dw, [[-10]]) and db == -6''', 'The transpose maps example gradients back to feature weights.', 'Batch averaging must be applied consistently to loss and gradients.'),
E('Training loop', 'Use backward to fit w,b from zeros with 500 updates and lr=.05. Return w,b,loss history.', 'def train_linear(x, y, steps=500, lr=.05):\n    raise NotImplementedError', '''def train_linear(x, y, steps=500, lr=.05):
    import numpy as np
    w, b, history = np.zeros((x.shape[1], 1)), 0., []
    for _ in range(steps):
        loss, dw, db = backward(x, y, w, b)
        history.append(loss)
        w -= lr*dw
        b -= lr*db
    return w, b, history''', '''w, b, history = train_linear(np.array([[-1.], [0.], [1.]]), np.array([[-1.], [1.], [3.]]))
assert history[-1] < 1e-8 and np.allclose(w, [[2]], atol=1e-3)''', 'Update only after computing all gradients.', 'Mixing updated and old parameters within one backward pass produces incorrect gradients.')],
'Implement a NumPy two-layer tanh network for XOR. Check 10 random gradient entries, overfit four examples, then compare SGD and momentum. Plot loss versus epoch.',
[('Why an activation?', 'It enables nonlinear functions; otherwise multiple affine layers remain affine.'), ('What is backpropagation?', 'Efficient reverse accumulation of derivatives through a computation graph.')], ['https://d2l.ai/chapter_multilayer-perceptrons/backprop.html'])

lesson('05b', 'PyTorch training and image classification', 'deep',
['Use tensors, autograd, modules, and loaders', 'Separate train and evaluation modes', 'Train a small CPU image classifier'],
'''PyTorch tensors can track operations for automatic differentiation. `loss.backward()` accumulates gradients; clear them before the next update unless accumulation is intentional. `model.train()` enables training behavior such as dropout; `model.eval()` switches to evaluation behavior. `torch.no_grad()` avoids building gradient graphs during validation. These are separate controls.

An epoch visits the training set; a batch is a subset used for one update. DataLoader handles batches and shuffling. SGD, momentum, Adam, and AdamW use gradients differently; AdamW decouples weight decay. Learning rate and regularization affect fit. Normalize inputs using training statistics. Monitor train and validation loss to detect overfitting.

A CNN slides learned kernels across spatial dimensions, reusing weights. Pooling reduces spatial resolution. Images conventionally use (batch,channels,height,width). RNNs process sequences through recurring state; LSTM/GRU gates address long-range gradient problems. They provide historical context for attention.''',
'''import torch
from torch import nn
torch.manual_seed(42)
torch.set_num_threads(1)
x = torch.tensor(3., requires_grad=True)
(x*x).backward()
print(x.grad)''', [
E('Gradient with autograd', 'Return derivative of sum(x²) as a tensor; create a fresh float tensor with gradients enabled.', 'def squared_gradient(values):\n    raise NotImplementedError', '''def squared_gradient(values):
    x = torch.tensor(values, dtype=torch.float32, requires_grad=True)
    (x*x).sum().backward()
    return x.grad''', '''assert torch.allclose(squared_gradient([1, -2]), torch.tensor([2., -4.]))''', 'backward needs a scalar loss.', 'Autograd reproduces the analytical gradient while handling larger computation graphs.'),
E('CNN shape', 'Return a network mapping (N,1,8,8) to (N,10): Conv2d(1,4,3,padding=1), ReLU, Flatten, Linear(256,10).', 'def make_cnn():\n    raise NotImplementedError', '''def make_cnn():
    return nn.Sequential(nn.Conv2d(1, 4, 3, padding=1), nn.ReLU(), nn.Flatten(), nn.Linear(4*8*8, 10))''', '''assert make_cnn()(torch.zeros(2, 1, 8, 8)).shape == (2, 10)''', 'Padding preserves the 8×8 spatial dimensions.', 'Return logits: CrossEntropyLoss already performs a stable log-softmax internally.'),
E('One update', 'Set training mode, zero gradients, compute cross entropy, backpropagate, step optimizer; return float loss.', 'def train_step(model, optimizer, x, y):\n    raise NotImplementedError', '''def train_step(model, optimizer, x, y):
    model.train()
    optimizer.zero_grad()
    loss = nn.functional.cross_entropy(model(x), y)
    loss.backward()
    optimizer.step()
    return loss.item()''', '''model = make_cnn()
optimizer = torch.optim.AdamW(model.parameters(), lr=.01)
x, y = torch.randn(4, 1, 8, 8), torch.tensor([0, 1, 2, 3])
before = model[-1].weight.detach().clone()
assert train_step(model, optimizer, x, y) > 0
assert not torch.equal(before, model[-1].weight)''', 'Call optimizer.zero_grad before backward.', 'A parameter-change check catches an omitted optimizer step; a learning curve is still needed to establish useful training.')],
'Run the digits CNN project with train/validation/test splits, DataLoader, loss curves, best-checkpoint restore, per-class errors, and a model card. Compare an MLP and CNN using the same split.',
[('Why both eval and no_grad?', 'eval changes module behavior; no_grad disables gradient recording.'), ('Why can gradients explode?', 'Repeated transformations can amplify derivatives; inspect norms and consider clipping, normalization, or architecture changes.')], ['https://docs.pytorch.org/tutorials/beginner/basics/intro.html'])

lesson('06a', 'Tokens, attention, and decoding', 'data',
['Implement a tokenizer baseline', 'Compute masked scaled dot-product attention', 'Explain context, sampling, and model families'],
'''A tokenizer maps text to IDs. Character tokenizers are simple but inefficient; subword tokenizers balance vocabulary size and sequence length. Token IDs are indices, not meaningful numerical magnitudes. An embedding table maps IDs to learned vectors. Positional information lets a transformer distinguish order.

Attention computes scores QKᵀ/√d, normalizes each query row with softmax, and combines value vectors. A causal mask prevents attending to future positions. Multiple heads learn different projections; residual connections and normalization stabilize deep stacks. Encoders such as BERT use bidirectional context; decoder families such as GPT and many Llama/Qwen/Mistral models generate autoregressively; T5 uses encoder-decoder structure. Family names do not specify every variant.

Greedy decoding selects the highest score. Temperature rescales logits; top-k restricts to k choices; top-p retains a probability-mass prefix. Beam search tracks multiple sequences. A context window limits tokens the model can consider. A KV cache reuses past attention keys and values, trading memory for less recomputation.''',
'''import numpy as np
scores = np.array([1., 2., 3.])
p = np.exp(scores-scores.max())
print(p/p.sum())''', [
E('Character tokenizer', 'Build sorted unique-character vocabulary. Return ids, encode mapping, and decoded text for the given nonempty string.', 'def tokenize(text):\n    raise NotImplementedError', '''def tokenize(text):
    vocabulary = sorted(set(text))
    encode = {char: i for i, char in enumerate(vocabulary)}
    ids = [encode[char] for char in text]
    return ids, encode, "".join(vocabulary[i] for i in ids)''', '''ids, vocab, decoded = tokenize("banana")
assert decoded == "banana" and len(vocab) == 3''', 'Use one consistent mapping for encoding and decoding.', 'Real tokenizers also need handling for unknown text, normalization, and special tokens.'),
E('Causal attention', 'Return output and attention weights for equal-length 2D Q,K,V. Mask all future positions before stable row softmax.', 'def attention(q, k, v):\n    raise NotImplementedError', '''def attention(q, k, v):
    scores = q@k.T/np.sqrt(q.shape[-1])
    scores = np.where(np.triu(np.ones(scores.shape), 1).astype(bool), -np.inf, scores)
    weights = np.exp(scores-scores.max(axis=-1, keepdims=True))
    weights /= weights.sum(axis=-1, keepdims=True)
    return weights@v, weights''', '''out, weights = attention(np.eye(3), np.eye(3), np.eye(3))
assert np.allclose(weights.sum(axis=1), 1)
assert np.allclose(np.triu(weights, 1), 0)
assert np.allclose(out[0], [1, 0, 0])''', 'Softmax each row after masking.', 'A causal mask is a training-data boundary: future tokens would leak the answer.'),
E('Temperature distribution', 'Return stable softmax(logits/temperature). Reject nonpositive temperature.', 'def distribution(logits, temperature=1.):\n    raise NotImplementedError', '''def distribution(logits, temperature=1.):
    if temperature <= 0: raise ValueError("Temperature must be positive")
    values = np.asarray(logits)/temperature
    p = np.exp(values-values.max())
    return p/p.sum()''', '''assert distribution([0, 1], .1)[1] > distribution([0, 1], 2)[1]
expect_error(ValueError, lambda: distribution([1, 2], 0))''', 'Subtract the maximum after dividing.', 'Lower temperature sharpens a distribution; it does not guarantee factual correctness.')],
'Visualize attention weights and prove changing a future value cannot affect an earlier output. Implement top-k/top-p and compare entropy. Read a subword tokenizer vocabulary and explain special tokens.',
[('Why divide by square root of d?', 'It moderates dot-product scale as dimension grows, helping avoid saturated softmax.'), ('Does attention prove explanation?', 'No. Attention weights alone do not establish a causal explanation of a model’s decision.')], ['https://huggingface.co/learn/llm-course/chapter1/1', 'https://arxiv.org/abs/1706.03762'])

lesson('06b', 'A tiny causal transformer', 'deep',
['Shift language-model targets correctly', 'Train a causal attention block', 'Measure held-out loss and generate tokens'],
'''Next-token training pairs a sequence x₀…xₜ with targets x₁…xₜ₊₁. If targets are not shifted, a model can learn to copy the current token. Split the text before creating overlapping windows so neighboring chunks cannot leak across evaluation boundaries.

A small causal language model needs token embeddings, positions, masked self-attention, a feed-forward layer, residual paths, normalization, and a vocabulary output projection. Cross entropy compares the logits at each position with the next token. Perplexity is exp(mean cross entropy) under natural logs and a fixed tokenizer; comparing different tokenizers by perplexity can mislead.

Tiny models trained for minutes teach mechanics, not useful general intelligence. Inspect shape invariants, gradient flow, training loss, validation loss, and generation. The project contains a full CPU training script with no downloaded model. Increase scale only after confirming the causal mask and target alignment.''',
'''import torch
from torch import nn
torch.manual_seed(42)
torch.set_num_threads(1)
sequence = torch.tensor([1, 2, 3, 4])
print(sequence[:-1], sequence[1:])''', [
E('Shifted examples', 'Return sequence[:-1] and sequence[1:] for a 1D tensor of at least two tokens.', 'def shifted(sequence):\n    raise NotImplementedError', '''def shifted(sequence):
    if sequence.ndim != 1 or len(sequence) < 2: raise ValueError("Need a token sequence")
    return sequence[:-1], sequence[1:]''', '''x, y = shifted(torch.tensor([3, 1, 4]))
assert x.tolist() == [3, 1] and y.tolist() == [1, 4]''', 'Every target is one position ahead.', 'Correct alignment prevents the identity-copying shortcut.'),
E('Future mask', 'Return an n×n boolean mask where True blocks future keys; diagonal stays False.', 'def causal_mask(n):\n    raise NotImplementedError', '''def causal_mask(n):
    return torch.triu(torch.ones(n, n, dtype=torch.bool), diagonal=1)''', '''mask = causal_mask(3)
assert mask.tolist() == [[False, True, True], [False, False, True], [False, False, False]]''', 'Boolean mask semantics depend on the API; this is MultiheadAttention’s convention.', 'Check your library’s mask convention rather than assuming True always means keep.'),
E('Transformer block', 'Implement TinyBlock with batch_first MultiheadAttention(d,2), LayerNorm, and residual connection. Forward accepts (N,T,d), uses causal_mask, returns same shape.', 'class TinyBlock(nn.Module):\n    def __init__(self, d=8):\n        super().__init__()\n        raise NotImplementedError\n    def forward(self, x):\n        raise NotImplementedError', '''class TinyBlock(nn.Module):
    def __init__(self, d=8):
        super().__init__()
        self.attn = nn.MultiheadAttention(d, 2, batch_first=True)
        self.norm = nn.LayerNorm(d)
    def forward(self, x):
        out, _ = self.attn(x, x, x, attn_mask=causal_mask(x.shape[1]).to(x.device), need_weights=False)
        return self.norm(x+out)''', '''block = TinyBlock().eval()
x = torch.randn(1, 4, 8)
changed = x.clone(); changed[:, 3] += 10
assert block(x).shape == x.shape
assert torch.allclose(block(x)[:, :3], block(changed)[:, :3], atol=1e-6)''', 'Add the original input before normalization.', 'A future-token perturbation is a meaningful causal-mask test, beyond just checking shape.')],
'Train projects/stage06/tiny_lm.py, add a second block, compare held-out loss and generation, then implement cached inference as an extension. Explain why train loss alone is insufficient.',
[('Why split text before windowing?', 'Overlapping windows otherwise share tokens across train and test.'), ('Why a residual path?', 'It preserves a direct path for information and gradients through depth.')], ['https://docs.pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html'])

lesson('06c', 'Adaptation, extraction, and quantization', 'data',
['Validate structured model outputs', 'Explain and calculate low-rank updates', 'Measure quantization error'],
'''Pretraining learns broad patterns; supervised fine-tuning adjusts weights on task examples. Full fine-tuning updates all parameters. LoRA learns low-rank matrices A and B and adds a scaled BA update to a frozen weight matrix. This reduces trainable parameters but does not remove the base model’s inference cost. PEFT implements parameter-efficient approaches. QLoRA combines adapters with a quantized frozen base and requires compatible kernels/hardware.

Structured extraction requires a schema, numeric units, evidence spans, and failure handling. JSON syntax alone does not prove that a value is supported by the source. Validate both structure and semantics; keep an unknown result when evidence is absent.

Quantization maps weights to a smaller representation. FP32/FP16/BF16 differ in precision and range; INT8/INT4 use integer codes and scaling metadata. Weight storage reduction does not guarantee proportional speedup because kernels, activation memory, and KV cache also matter. Measure quality on held-out examples after adaptation or quantization.''',
'''import numpy as np
from pydantic import BaseModel, Field
print("A 1000×1000 matrix has", 1000*1000, "parameters")
print("Rank-8 adapters have", 8*(1000+1000), "parameters")''', [
E('Validated extraction', 'Parse JSON with company (nonempty str) and revenue (finite float >=0), forbid extra keys. Return a validated model_dump dictionary.', 'def validate_extraction(text):\n    raise NotImplementedError', '''def validate_extraction(text):
    from pydantic import BaseModel, Field, ConfigDict
    class Report(BaseModel):
        model_config = ConfigDict(extra="forbid")
        company: str = Field(min_length=1)
        revenue: float = Field(ge=0, allow_inf_nan=False)
    return Report.model_validate_json(text).model_dump()''', '''assert validate_extraction('{"company":"Example","revenue":100000000000}')["revenue"] == 1e11
from pydantic import ValidationError
expect_error(ValidationError, lambda: validate_extraction('{"company":"","revenue":-1}'))''', 'Use model_validate_json.', 'The schema rejects malformed output; verifying the source and units is a separate check.'),
E('LoRA update', 'For W(out,in), A(rank,in), B(out,rank), return W+(alpha/rank)*(B@A).', 'def lora_weight(w, a, b, alpha):\n    raise NotImplementedError', '''def lora_weight(w, a, b, alpha):
    return w + (alpha/a.shape[0])*(b@a)''', '''w = np.zeros((3, 4)); a = np.ones((2, 4)); b = np.ones((3, 2))
assert np.allclose(lora_weight(w, a, b, 2), np.full((3, 4), 2))''', 'Write down shapes before multiplying.', 'For low rank r, r(in+out) parameters can be much fewer than in×out.'),
E('Symmetric INT8 simulation', 'Return int8 codes, scale, and dequantized weights using max(abs(w))/127; all-zero arrays use scale=1.', 'def quantize(w):\n    raise NotImplementedError', '''def quantize(w):
    w = np.asarray(w, dtype=float)
    scale = float(np.max(np.abs(w)))/127 or 1.
    codes = np.clip(np.round(w/scale), -127, 127).astype(np.int8)
    return codes, scale, codes.astype(float)*scale''', '''codes, scale, restored = quantize([-.7, .1, 1.])
assert codes.dtype == np.int8
assert np.max(np.abs(restored-[-.7, .1, 1.])) <= scale/2+1e-12
assert np.allclose(quantize([0, 0])[2], 0)''', 'Store the scale along with integer codes.', 'This is a numerical simulation, not a fast quantized matrix-multiplication kernel.')],
'Run the pretrained text-classification and PEFT lab in projects/stage06/pretrained.py after selecting/downloading a model. Compare frozen baseline versus fine-tuning on validation examples; record revision, license, cost, and test metrics. Audit extraction against source spans.',
[('Does valid JSON imply truth?', 'No. A valid schema can contain unsupported values.'), ('What does LoRA change?', 'It learns a low-rank weight update while keeping the original base weights frozen.')], ['https://huggingface.co/docs/peft/en/conceptual_guides/lora'])
