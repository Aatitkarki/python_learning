import sys

def test_greeting_interpreter_and_budget(assignment,capsys):
    assignment.main();text=capsys.readouterr().out
    assert 'Hello' in text, 'Print a greeting'
    assert sys.executable in text, 'Show the actual interpreter, not a copied path'
    assert '1200' in text, '80 weeks times 15 hours should be 1200'

def test_fresh_call_has_same_output(assignment,capsys):
    assignment.main();first=capsys.readouterr().out
    assignment.main();assert capsys.readouterr().out==first
