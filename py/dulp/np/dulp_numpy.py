"""Floating point differences --- dulp (numpy module)

dulp measures directed differences between floating point numbers by
counting the discrete spaces between them.

This distance was proposed by an anonymous reviewer to
*"On the definition of ulp(x)"* (JM Muller 2005).

>>> from dulp.np import dulp
>>> from numpy import float32
>>>
>>> dulp(1., [1. + 2.**-52, 1. + 2.**-50]) # array([1., 4.])
>>> dulp(float32((1 + 5**0.5)/2), float32(1.6180339887)) # 0.
>>> dulp(-0., float32(0.)) # TypeError


Each float gets an integer valuation val(x) which satisfies

>>> val(0.) == 0 # True

>>> val(x + eps) == val(x) + 1 # True

where x + eps is the next floating point number after x.
Floats almost have this naturally in their binary, but are reversed for
negative numbers; we just reverse negative numbers' order.


The dulp(x, y) directed distance from x to y equals val(y) - val(x),
casted to float for convenience with small and large distances.

A bits-precision equivalent conversion is given by dulpbits.


This optional module uses numpy types and broadcasting features.


Assumes IEEE 764 binary64 and binary32 for float64s and float32s.
"""
from numpy import asanyarray
from numpy import absolute, log2
from numpy import float32, float64
from numpy import int32, int64


def bits(delta):
    """Return a (broadcasted) bits-equivalent of dulp distance delta.

    The form log2(|delta| + 1) satisfies
        bits(0) == 0
        bits(1) == 1
        bits(0b111) == 3               (0b111 == 7)
    with interpolation such that
        3 < bits(0b1000) < 4          (0b1000 == 8)
    and so on.
    """
    delta = asanyarray(delta)
    distance = absolute(delta)
    return log2(distance + 1.)


def dulp(x, y):
    """Return the (broadcasted) order difference from x to y.

    Inputs x and y must be both float32 or both float64.
    """
    x = asanyarray(x)
    y = asanyarray(y)

    if x.dtype is not y.dtype:
        raise TypeError("%s is not %s" % (x.dtype, y.dtype))

    if x.dtype.type is float64:
        delta = _dulp(x, y)
    elif x.dtype.type is float32:
        delta = _dulpf(x, y)
    else:
        raise TypeError("%s not in (float64, float32)" % x.dtype)

    return delta


def val(x):
    """Return an integer (broadcasted) valuation of x.

    Input x must be float32 or float64.
    """
    x = asanyarray(x)

    if x.dtype.type is float64:
        value = _val(x)
    elif x.dtype.type is float32:
        value = _valf(x)
    else:
        raise TypeError("%s not in (float64, float32)" % x.dtype)

    return value


def dif(valx, valy):
    """Return the (broadcasted) difference from valx to valy.

    Inputs valx and valy must be int32 or int64, as returned by val(x).
    """
    valx = asanyarray(valx)
    valy = asanyarray(valy)

    if valx.dtype is not valy.dtype:
        raise TypeError("%s is not %s" % (valx.dtype, valy.dtype))

    if valx.dtype.type is int64:
        delta = _dif(valx, valy)
    elif valx.dtype.type is int32:
        delta = _diff(valx, valy)
    else:
        raise TypeError("%s not in (int64, int32)" % valx.dtype)

    return delta


def _dulp(x, y):
    "Return the order distance from float64 x to float64 y"
    valx = _val(x)
    valy = _val(y)
    return _dif(valx, valy)


def _dulpf(x, y):
    "Return the order distance from float32 x to float32 y"
    valx = _valf(x)
    valy = _valf(y)
    return _diff(valx, valy)


def _val(x):
    "Return an integer valuation of float64 x"
    shift = int64(63)
    mask = int64((1 << 63) - 1)
    i64 = x.view(int64)
    value = i64 >> shift
    value &= mask
    value ^= i64
    return value


def _valf(x):
    "Return an integer valuation of float32 x"
    shift = int32(31)
    mask = int32((1 << 31) - 1)
    i32 = x.view(int32)
    value = i32 >> shift
    value &= mask
    value ^= i32
    return value


def _dif(valx, valy):
    "Return the valuation difference from int64 valx to int64 valy"
    shift = int64(32)
    mask = int64((1 << 32) - 1)
    scale = float64(mask + 1)
    hi = valy >> shift
    hi -= valx >> shift
    lo = valy & mask
    lo -= valx & mask
    return scale*hi + lo


def _diff(valx, valy):
    "Return the valuation difference from int32 valx to int32 valy"
    delta = valy.astype(int64) - valx
    return delta.astype(float64)
