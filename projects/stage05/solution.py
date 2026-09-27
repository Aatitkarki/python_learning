"""Real CPU CNN on bundled sklearn digits, with checkpoint selected on validation only."""
import copy
import json
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

def run(epochs=12):
    torch.manual_seed(42)
    torch.set_num_threads(1)
    data = load_digits()
    x = torch.tensor(data.images[:,None]/16., dtype=torch.float32)
    y = torch.tensor(data.target, dtype=torch.long)
    train, test = train_test_split(range(len(y)), test_size=.2, stratify=y, random_state=42)
    train, val = train_test_split(train, test_size=.2, stratify=y[train], random_state=42)
    loader = DataLoader(TensorDataset(x[train],y[train]), batch_size=64, shuffle=True,
                        generator=torch.Generator().manual_seed(42))
    model = nn.Sequential(nn.Conv2d(1,8,3,padding=1), nn.ReLU(), nn.MaxPool2d(2), nn.Flatten(), nn.Linear(8*4*4,10))
    optimizer = torch.optim.AdamW(model.parameters(), lr=.01)
    history, best, state = [], float('inf'), None
    for epoch in range(epochs):
        model.train(); total = 0.
        for xb,yb in loader:
            optimizer.zero_grad()
            loss = nn.functional.cross_entropy(model(xb),yb)
            loss.backward(); optimizer.step()
            total += loss.item()*len(yb)
        model.eval()
        with torch.no_grad():
            val_loss = nn.functional.cross_entropy(model(x[val]),y[val]).item()
        history.append({'epoch': epoch+1, 'train_loss': total/len(train), 'validation_loss': val_loss})
        if val_loss < best: best, state = val_loss, copy.deepcopy(model.state_dict())
    model.load_state_dict(state)
    model.eval()
    with torch.no_grad(): prediction = model(x[test]).argmax(1)
    return {'history': history, 'test_accuracy': (prediction == y[test]).float().mean().item(),
            'test_count': len(test), 'split_seed': 42}

if __name__ == '__main__': print(json.dumps(run(), indent=2))
