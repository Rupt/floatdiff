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


def dif(vx, vy):
    """Return the (broadcasted) difference of valuations vx and vy.

    Inputs vx and vy must be int32 or int64, as returned by val(x).
    """
    vx = asanyarray(vx)
    vy = asanyarray(vy)

    if vx.dtype is not vy.dtype:
        raise TypeError("%s is not %s" % (vx.dtype, vy.dtype))

    if vx.dtype.type is int64:
        delta = _dif(vx, vy)
    elif vx.dtype.type is int32:
        delta = _diff(vx, vy)
    else:
        raise TypeError("%s not in (int64, int32)" % vx.dtype)

    return delta


def bits(delta):
    """Return a bits-like transform of difference (array) d.

    The form log2(|delta| + 1) satisfies
        bits(0) == 0
        bits(1) == 1
        bits(0b111) == 3               (0b111 == 7)
    with interpolation such that
        3 < bits(0b1000) < 4          (0b1000 == 8)
    and so on.
    """
    delta = asanyarray(delta)
    dist = absolute(delta)
    return log2(dist + 1.)


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


def _dif(vx, vy):
    "Return the valuation difference from int64 vx to int64 vy"
    shift = int64(32)
    mask = int64(0xffffffff)
    scale = float64(mask + 1)
    hi = vy >> shift
    hi -= vx >> shift
    lo = vy & mask
    lo -= vx & mask
    return scale*hi + lo


def _diff(vx, vy):
    "Return the valuation difference from int32 vx to int32 vy"
    delta = vy.astype(int64) - vx
    return delta.astype(float64)
