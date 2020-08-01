"""dulp measures order distances between floats"""
from ctypes import Union, c_double, c_longlong
from math import log2


class Word64(Union):
    _fields_ = [
        ("f64", c_double),
        ("i64", c_longlong),
    ]


def dulp(x, y):
    """Return the order difference from x to y."""
    valx = val(x)
    valy = val(y)
    return dif(valx, valy)


def dif(valx, valy):
    """Return the difference of valuations valx and valy.

    Trivial, but included for consistency with other modules.
    """
    return float(valy - valx)


def val(x):
    """Return an integer valuation of float x."""
    value = Word64(f64=x).i64

    if value < 0:
        value = -(1 << 63) + ~value

    return value


def bits(delta):
    """Return a bits-equivalent of dulp distance delta.

    The form log2(|delta| + 1) satisfies
        bits(0) == 0
        bits(1) == 1
        bits(0b111) == 3               (0b111 == 7)
    with interpolation such that
        3 < bits(0b1000) < 4          (0b1000 == 8)
    and so on.
    """
    delta = float(delta)
    distance = abs(delta)
    return log2(distance + 1.)
