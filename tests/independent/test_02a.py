import math
import pytest

def test_hand_calculated_vectors(assignment):
    assert assignment.add([1,-2],[3,5])==[4,3]
    assert assignment.dot([2,1],[3,4])==10
    assert assignment.norm([3,4])==5
    assert assignment.distance([1,1],[4,5])==5
    assert assignment.cosine([1,0],[0,1])==0

def test_transpose_and_rectangular_product(assignment):
    assert assignment.transpose([[1,2,3],[4,5,6]])==[[1,4],[2,5],[3,6]]
    assert assignment.matmul([[1,2,3]],[[1,0],[0,1],[1,1]])==[[4,5]]

def test_rotation_and_eigenvector(assignment):
    rotated=assignment.rotate([3,4],math.pi/2)
    assert rotated==pytest.approx([-4,3])
    assert assignment.norm(rotated)==pytest.approx(5)
    assert assignment.matmul([[2,0],[0,3]],[[1],[0]])==[[2],[0]]

def test_shape_and_zero_direction_errors(assignment):
    for name,args in [('add',([1],[1,2])),('dot',([1],[1,2])),('transpose',([[1],[2,3]],)),('matmul',([[1,2]],[[3]],)),('cosine',([0,0],[1,1]))]:
        with pytest.raises(ValueError):getattr(assignment,name)(*args)
