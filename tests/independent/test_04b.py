import math

def test_labeled_new_examples(assignment):
    rows=assignment.novel_tickets()
    assert len(rows)>=20 and len({r['id'] for r in rows})==len(rows)
    assert len({r['text'] for r in rows})==len(rows)
    assert {r['label'] for r in rows}=={'access','billing','technical'}
    assert all(r['provenance'] for r in rows)

def test_error_review_keeps_correct_controls(assignment):
    rows=assignment.ticket_errors()
    assert len(rows)>=20
    for row in rows:
        assert row['correct']==(row['label']==row['predicted'])
        assert row['review_category']

def test_clustering_covers_both_shapes(assignment,tmp_path):
    report=assignment.clustering(tmp_path)
    assert {(r['dataset'],r['model']) for r in report['comparisons']}=={(d,m) for d in ['blobs','moons'] for m in ['kmeans','dbscan']}
    assert all(math.isfinite(r['ari_external_diagnostic']) for r in report['comparisons'])
    assert (tmp_path/'clusters.png').stat().st_size>100
