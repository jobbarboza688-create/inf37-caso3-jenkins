import pytest
from xyzapp import sumar


@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5), (-2, 2, 0), (0, 0, 0), (1.5, 2.5, 4)])
def test_suma(a, b, expected):
    assert sumar(a, b) == expected


@pytest.mark.parametrize("value", [True, "2", None, [], {}])
def test_rechazo(value):
    with pytest.raises(ValueError):
        sumar(value, 1)
