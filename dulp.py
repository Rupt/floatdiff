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
    vx = val(x)
    vy = val(y)
    return dif(vx, vy)


def dif(vx, vy):
    """Return the difference of valuations vx and vy.

    Trivial, but included for consistency with other modules.
    """
    return float(vy - vx)


def val(x):
    """Return an integer valuation of float x."""
    i = Word64(f64=x).i64

    if i < 0:
        return -(1 << 63) - i - 1

    return i


def bits(delta):
    """Return a bits-like transform of difference d.

    The form log2(|delta| + 1) satisfies
        bits(0) == 0
        bits(1) == 1
        bits(0b111) == 3               (0b111 == 7)
    with interpolation such that
        3 < bits(0b1000) < 4          (0b1000 == 8)
    and so on.
    """
    delta = float(delta)
    dist = abs(delta)
    return log2(dist + 1.)
