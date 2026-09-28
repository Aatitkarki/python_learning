import torch
import pytest

@pytest.mark.parametrize('blocks',[1,2])
def test_cached_logits_positions_and_layer_count(assignment,blocks):
    torch.set_num_threads(1);torch.manual_seed(7)
    model=assignment.CachedLM(12,blocks=blocks,context=8).eval();ids=torch.tensor([[1,2,3,4]])
    with torch.no_grad():
        full,_=model(ids);cache=None;pieces=[]
        for i in range(4):
            logits,cache=model(ids[:,i:i+1],cache);pieces.append(logits)
            assert len(cache)==blocks
            assert all(pair[0].shape[2]==i+1 for pair in cache)
    assert torch.allclose(full,torch.cat(pieces,dim=1),atol=1e-5)

def test_causality_and_context_limit(assignment):
    torch.set_num_threads(1);model=assignment.CachedLM(12,context=4).eval()
    original=torch.tensor([[1,2,3,4]]);changed=torch.tensor([[1,2,3,9]])
    assert torch.allclose(model(original)[0][:,:3],model(changed)[0][:,:3],atol=1e-6)
    with pytest.raises(ValueError):model(torch.tensor([[1,2,3,4,5]]))
