"""dulp measures order distances between floats"""
from ctypes import Union, c_double, c_ulonglong
from math import log2


class Word64(Union):
    _fields_ = [
        ("f8", c_double),
        ("u8", c_ulonglong),
    ]


def dulp(x, y):
    """Return the order difference from x to y."""
    vx = val(x)
    vy = val(y)
    delta = dif(vx, vy)
    return delta


def dif(vx, vy):
    """Return the difference of valuations vx and vy.

    Trivial, but included for internal consistency.
    """
    return float(vy - vx)


def val(x):
    """Return an integer valuation of float x."""
    u = Word64(f8=x).u8

    sign = 1 << 63
    if u < sign:
        value = sign + u
    else:
        value = 2*sign - 1 - u

    return value


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
    return log2(abs(delta) + 1.)
