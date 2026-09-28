import json
import pytest

def test_three_format_parsing_and_provenance(assignment,tmp_path):
    paths=[tmp_path/'report.md',tmp_path/'report.html',tmp_path/'report.json']
    paths[0].write_text('# Revenue\nAurora 144 million')
    paths[1].write_text('<h1>Revenue</h1><p>Aurora 144 million</p><script>evil()</script>')
    paths[2].write_text(json.dumps({'company':'Aurora','revenue':144}))
    docs=assignment.documents_from_paths(paths,'A')
    assert len(docs)==3 and len({d['id'] for d in docs})==3
    assert all('144' in d['text'] and d['tenant']=='A' and not d['public'] and d['source'] for d in docs)
    assert 'evil()' not in assignment.parse_document(paths[1])

def test_empty_or_unsupported_file_is_visible(assignment,tmp_path):
    empty=tmp_path/'empty.md';empty.write_text('')
    with pytest.raises(ValueError):assignment.documents_from_paths([empty],'A')
    unknown=tmp_path/'unknown.bin';unknown.write_bytes(b'bytes')
    with pytest.raises(ValueError):assignment.parse_document(unknown)

def test_changed_source_changes_identity(assignment,tmp_path):
    p=tmp_path/'report.md';p.write_text('Revenue 10');first=assignment.documents_from_paths([p],'A')[0]
    p.write_text('Revenue 20');second=assignment.documents_from_paths([p],'A')[0]
    assert first['id']!=second['id']
