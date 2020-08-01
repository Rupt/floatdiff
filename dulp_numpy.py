"""
TODO documentation

python -m timeit -vv -s "from dulp_numpy import perf" "perf()"


"""
from numpy import asanyarray
from numpy import absolute
from numpy import log2
from numpy import float32, float64
from numpy import int32, int64


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
    mask = int64(0x7fffffffffffffff)
    i64 = x.view(int64)
    value = i64 >> shift
    value &= mask
    value ^= i64
    return value


def _valf(x):
    "Return an integer valuation of float32 x"
    shift = int32(31)
    mask = int32(0x7fffffff)
    i32 = x.view(int32)
    value = i32 >> shift
    value &= mask
    value ^= i32
    return value


def _dif(valx, valy):
    "Return the valuation difference from int64 valx to int64 valy"
    shift = int64(32)
    mask = int64(0xffffffff)
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
