import pytest
from my_script import add, subtract

def test_add():
    assert add(2, 3) == 5, "Addition should be correct"

def test_subtract():
    assert subtract(5, 2) == 3, "Subtraction should be correct"