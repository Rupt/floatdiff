"""
Floating point differences

Measure directed differences between floating point numbers by enumerating the
discrete spaces between them.

This distance was proposed by an anonymous reviewer to
*"On the definition of ulp(x)"* (JM Muller 2005).

>>> from floatdiff import floatdiff
>>>
>>> floatdiff(1., 1. + 2.**-52) # 1.
>>> floatdiff((1. + 5**0.5)/2, 1.6180339887) # -224707.
>>> floatdiff(-0., 0.) # 1.

Each float gets an integer valuation rank(x) which satisfies:

>>> rank(0.) == 0 # True

>>> rank(nextafter(x)) == rank(x) + 1 # True .

Floats almost have this naturally when reinterpreted as integers,
but are reversed for negative numbers.

We just reverse negative numbers' order.

The floatdiff(x, y) directed distance from x to y equals rank(y) - rank(x),
as a float for coverage of small and large distances.

A bits-precision equivalent conversion is given by bits(...).

Assumes IEEE 754 binary64 for float.
"""
from ctypes import Union, c_double, c_longlong
from math import log2


class Word64(Union):
    _fields_ = [
        ("f64", c_double),
        ("i64", c_longlong),
    ]


def bits(delta):
    """ Return a bits-equivalent of difference delta.

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


def floatdiff(x, y):
    """ Return the order difference from x to y. """
    return diff(rank(x), rank(y))


def diff(rankx, ranky):
    """ Return the difference of valuations rankx and ranky.

        Trivial, but included for consistency with other modules.
    """
    return float(ranky - rankx)


def rank(x):
    """ Return an integer valuation of float x. """
    i64 = Word64(f64=x).i64

    if i64 < 0:
        value = -(1 << 63) - i64 - 1
    else:
        value = i64

    return value
