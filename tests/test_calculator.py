import pytest

from toolkit import errors
from toolkit.calculator import calculation, tokenize


def test_calc_1():
    assert calculation(tokenize("2 + 3")) == 5

def test_calc_2():
    assert calculation(tokenize("---8*24/5")) == -38.4

def test_calc_3():
    assert calculation(tokenize("0*7+5  *4 + 2 - 1 - 1 -----0 + 1")) == 21

def test_calc_4():
    assert calculation(tokenize("17/2/4 + 7 + 1000000000 - 0 - 100000 +++++++27")) == 999900036.125

def test_calc_5():
    assert calculation(tokenize("0")) == 0

def test_calc_6():
    with pytest.raises(errors.DivisionByZeroError):
        calculation(tokenize("2/0"))

def test_calc_7():
    with pytest.raises(errors.MissingOperatorError):
        calculation(tokenize("2 3"))

def test_calc_8():
    with pytest.raises(errors.MissingOperandError):
        calculation(tokenize("2*/8"))

def test_calc_9():
    with pytest.raises(errors.EmptyExpressionError):
        calculation(tokenize(""))

def test_calc_10():
    with pytest.raises(errors.InvalidCharacterError):
        calculation(tokenize("2 $ 5"))

import subprocess


def test_cli_calc_error():
    result = subprocess.run(
        ["python", "-m", "toolkit", "calc", "2+"],
        capture_output=True, text=True, check=False
    )
    assert result.returncode == 2
    assert result.stderr.strip() != ""