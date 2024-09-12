from Q1 import Calculator
import pytest

@pytest.fixture
def calc():
    return Calculator()

def test_add(calc):
    assert calc.add(1, 2) == 3
    assert calc.add(-1, -1) == -2
    assert calc.add(-1, 1) == 0
    assert calc.add(0, 0) == 0

def sub_add(calc):
    assert calc.subtract(1,2) == -1
    assert calc.subtract(3,2) == 1

def test_multiply(calc):
    assert calc.multiply(2, 3) == 6
    assert calc.multiply(-1, -1) == 1

def test_divide(calc):
    assert calc.divide(6, 3) == 2
    assert calc.divide(-6, -3) == 2
    assert calc.divide(-6, 3) == -2

    with pytest.raises(ValueError):
        calc.divide(1, 0)   