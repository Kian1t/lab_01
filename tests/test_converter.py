import pytest

from toolkit import errors
from toolkit.converter import *


def test_conv_1():
    assert convert(100, "m", "km") == 0.1

def test_conv_2():
    assert convert(1000, "mm", "m") == 1

def test_conv_3():
    assert convert(-273.15, "c", "k") == 0

def test_conv_4():
    assert convert(1000, "g", "kg") == 1

def test_conv_5():
    with pytest.raises(errors.BelowAbsoluteZeroError):
        convert(-500, "c", "k")

def test_conv_6():
    with pytest.raises(errors.IncompatibleUnitsError):
        convert(100, "c", "kg")

def test_conv_7():
    with pytest.raises(errors.UnknownUnitError):
        convert(100, "dol", "kg")


import subprocess


def test_cli_conv():
    result = subprocess.run(
        ["python", "-m", "toolkit", "convert", "100", "--from", "g", "--to", "kg"],
        capture_output=True, text=True, check=False
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "0.1"