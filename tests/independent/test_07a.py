import hashlib
import pytest

def doc(id,text,tenant='A',public=False):return dict(id=id,text=text,tenant=tenant,public=public,source=id)

def test_offsets_hashes_and_overlap(assignment):
    original=doc('x','red  blue\ngreen yellow orange')
    chunks=assignment.chunks(original,size=3,overlap=1)
    assert len(chunks)==2
    assert all(original['text'][c['start']:c['end']]==c['text'] for c in chunks)
    assert all(c['sha256']==hashlib.sha256(original['text'].encode()).hexdigest() for c in chunks)
    assert all(c['parser_version'] for c in chunks)
    assert assignment.chunks(doc('x',''),size=3,overlap=1)==[]
    with pytest.raises(ValueError):assignment.chunks(original,size=3,overlap=3)

def test_real_term_scores_and_permission_filter(assignment):
    docs=[doc('a','apple banana'),doc('b','secret apple','B'),doc('p','apple public','B',True)]
    scores=assignment.bm25('banana',docs)
    assert scores[0]>0 and scores[1]==0 and scores[2]==0
    ranks=assignment.rankings('apple',docs,'A')
    assert set(ranks)=={'keyword','vector','hybrid','reranked'}
    assert all({d['id'] for d in hits}<={'a','p'} for hits in ranks.values())
    assert all(hits for hits in ranks.values()), 'Do not pass access isolation by returning no allowed results'
