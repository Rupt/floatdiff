"""
Floating point differences --- dulp

dulp measures directed differences between floating point numbers by
counting the discrete spaces between them.

This distance was proposed by an anonymous reviewer to
*"On the definition of ulp(x)"* (JM Muller 2005).

>>> from dulp import dulp
>>>
>>> dulp(1., 1. + 2.**-52) # 1.
>>> dulp((1. + 5**0.5)/2, 1.6180339887) # -224707.
>>> dulp(-0., 0.) # 1.

Each float gets an integer valuation val(x) which satisfies:

>>> val(0.) == 0 # True

>>> val(nextafter(x)) == val(x) + 1 # True

Floats almost have this naturally when reinterpreted as integers,
but are reversed for negative numbers.
We just reverse negative numbers' order.

The dulp(x, y) directed distance from x to y equals val(y) - val(x),
casted to float for convenience with small and large distances.

A bits-precision equivalent conversion is given by dulpbits.

Assumes IEEE 764 binary64 for floats.
"""
from ctypes import Union, c_double, c_longlong
from math import log2


class Word64(Union):
    _fields_ = [
        ("f64", c_double),
        ("i64", c_longlong),
    ]


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
    i64 = Word64(f64=x).i64

    if i64 < 0:
        value = -(1 << 63) - i64 - 1
    else:
        value = i64

    return value
