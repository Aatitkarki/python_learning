"""The missing-answer bug must fail validation when a question or file is lost."""
import copy
import json
import pytest
from tools.check_answers import ROOT, check

def records():
    return json.loads((ROOT/'curriculum/answer_manifest.json').read_text())

def test_all_current_questions_have_specific_worked_answers():
    result=check()
    assert result['counts']==dict(exercise=108,oral=72,transfer=36,project=72,gate=16)

def test_missing_answer_is_rejected():
    with pytest.raises(ValueError,match='Coverage mismatch'):check(records()[1:])

def test_stale_question_and_missing_implementation_are_rejected():
    changed=copy.deepcopy(records());changed[0]['question']='A new question without an updated answer'
    changed[0]['implementations']=['projects/answer-that-does-not-exist.py']
    with pytest.raises(ValueError,match='stale question'):check(changed)

def test_wrong_anchor_is_rejected():
    changed=records();changed[0]['answer']=changed[0]['answer'].split('#')[0]+'#wrong-anchor'
    with pytest.raises(ValueError,match='missing explicit anchor'):check(changed)
