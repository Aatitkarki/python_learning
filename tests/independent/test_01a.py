import pytest

@pytest.mark.parametrize('a,op,b,result',[(2,'+',3,5),(2,'-',3,-1),(-2,'*',3,-6),(7,'/',2,3.5),(0,'+',0,0)])
def test_calculator_five_cases(assignment,a,op,b,result):assert assignment.calculate(a,op,b)==pytest.approx(result)
@pytest.mark.parametrize('v,s,t,result',[(0,'C','F',32),(100,'C','F',212),(32,'F','C',0),(-40,'F','C',-40),(18,'C','C',18)])
def test_converter_five_cases(assignment,v,s,t,result):assert assignment.temperature(v,s,t)==pytest.approx(result)
@pytest.mark.parametrize('values,result',[((5,7,2),4),((7,5,2),-4),((0,2,3),6),((2,2,1),0),((2,3,.5),.5)])
def test_profit_five_cases(assignment,values,result):assert assignment.profit(*values)==pytest.approx(result)
@pytest.mark.parametrize('mass,height,result',[(80,2,20),(45,1.5,20),(100,2,25),(18,1,18),(50,2,12.5)])
def test_bmi_arithmetic_five_cases(assignment,mass,height,result):assert assignment.bmi(mass,height)==pytest.approx(result)
@pytest.mark.parametrize('args,error',[(('bad','+',2),ValueError),((1,'/',0),ZeroDivisionError),((1,'**',2),ValueError),((float('nan'),'+',1),ValueError)])
def test_invalid_calculations(assignment,args,error):
    with pytest.raises(error):assignment.calculate(*args)

def test_loop_recovers_and_quits(assignment):
    commands=iter(['calc bad + 1','calc 8 / 2','temp 0 C F','quit']);out=[]
    assignment.main(lambda prompt:next(commands),lambda value:out.append(str(value)))
    assert any('4' in x for x in out) and any('32' in x for x in out)
    assert any('error' in x.lower() for x in out), 'Explain invalid input and continue the loop'

def test_programmer_error_is_visible(assignment):
    def broken_read(prompt):raise RuntimeError('deliberate bug')
    with pytest.raises(RuntimeError):assignment.main(broken_read,lambda text:None)
