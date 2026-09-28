import pytest

def test_contact_crud_and_duplicate_policy(assignment):
    book=assignment.ContactBook();book.add(' ADA@example.test ','Ada','123')
    with pytest.raises(ValueError):book.add('ada@EXAMPLE.test','Other')
    book.update('ada@example.test',phone='456')
    assert book.search('456')[0]['name']=='Ada'
    assert book.delete('ada@example.test') is True
    assert book.delete('ada@example.test') is False
    with pytest.raises(KeyError):book.update('missing@example.test',name='Unknown')

def test_search_copy_and_persistence(assignment,tmp_path):
    book=assignment.ContactBook();book.add('s@test.example','Suresh','555')
    book.search('suresh')[0]['name']='Changed'
    assert book.search('suresh')[0]['name']=='Suresh'
    path=tmp_path/'book.json';book.save(path)
    assert assignment.ContactBook.load(path).search('555')==book.search('555')
    path.write_text('');
    with pytest.raises(ValueError):assignment.ContactBook.load(path)

@pytest.mark.parametrize('text,words,unique,top',[('B a b A!',4,2,[('a',2),('b',2)]),('',0,0,[]),('...',0,0,[]),('Cat dog cat',3,2,[('cat',2),('dog',1)])])
def test_text_policy(assignment,text,words,unique,top):
    result=assignment.analyze(text)
    assert result['characters']==len(text) and result['words']==words and result['unique_words']==unique
    assert result['top_words']==top
    assert result['most_common']==(top[0][0] if top else None)
