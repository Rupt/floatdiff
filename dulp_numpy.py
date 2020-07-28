"""
TODO documentation

python -m timeit -vv -s "from dulp_numpy import perf" "perf()"


"""
from numpy import asanyarray
from numpy import abs as fabs
from numpy import log2
from numpy import float32, float64
from numpy import int32, int64
from numpy import uint32, uint64


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


def dif(vx, vy):
    """Return the (broadcasted) difference of valuations vx and vy.

    Inputs vx and vy must be uint32 or uint64, as returned by val(x).
    """
    vx = asanyarray(vx)
    vy = asanyarray(vy)

    if vx.dtype is not vy.dtype:
        raise TypeError("%s is not %s" % (vx.dtype, vy.dtype))

    if vx.dtype.type is uint64:
        delta = _dif(vx, vy)
    elif vx.dtype.type is uint32:
        delta = _diff(vx, vy)
    else:
        raise TypeError("%s not in (uint64, uint32)" % vx.dtype)

    return delta

def bits(d):
    """Return a bits-like transform of difference (array) d."""
    d = asanyarray(d)
    return log2(fabs(d) + 1.)


def _dulp(x, y):
    "Return the order distance from float64 x to float64 y"
    vx = _val(x)
    vy = _val(y)
    return _dif(vx, vy)


def _dulpf(x, y):
    "Return the order distance from float32 x to float32 y"
    vx = _valf(x)
    vy = _valf(y)
    return _diff(vx, vy)


def _val(x):
    "Return an integer valuation of float64 x"
    shift = int64(63)
    u = x.view(int64)
    value = u >> shift
    value |= int64(1) << shift
    value ^= u
    return value.view(uint64)


def _valf(x):
    "Return an integer valuation of float32 x"
    shift = int32(31)
    u = x.view(int32)
    value = u >> shift
    value |= int32(1) << shift
    value ^= u
    return value.view(uint32)


def _dif(vx, vy):
    "Return the valuation difference from uint64 vx to uint64 vy"
    shift = uint64(32)
    mask = (uint64(1) << shift) - uint64(1)
    scale = float64(mask + 1)
    hi = (vy >> shift).view(int64)
    hi -= (vx >> shift).view(int64)
    lo = (vy & mask).view(int64)
    lo -= (vx & mask).view(int64)
    return scale*hi + lo


def _diff(vx, vy):
    "Return the valuation difference from uint32 vx to uint32 vy"
    delta = vy.astype(int64) - vx
    return delta.astype(float64)
