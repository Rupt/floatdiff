"""

python -m timeit -vv -s "from dulp_numpy import perf" "perf()"


"""
import numpy

from numpy import asanyarray
from numpy import float32, float64
from numpy import int32, int64
from numpy import uint32, uint64

# TODO documentation
# TODO tests

def dulp(x, y):
    x = asanyarray(x)
    y = asanyarray(y)

    if x.dtype is not y.dtype:
        raise TypeError("%s is not %s" % (x.dtype, y.dtype))

    if x.dtype.type is float64:
        r = _dulp(x, y)
    elif x.dtype.type is float32:
        r = _dulpf(x, y)
    else:
        raise TypeError("%s not in (float64, float32)" % x.dtype)

    return _un0d(r)


def val(x):
    x = asanyarray(x)

    if x.dtype.type is float64:
        r = _val(x)
    elif x.dtype.type is float32:
        r = _valf(x)
    else:
        raise TypeError("%s not in (float64, float32)" % x.dtype)

    return _un0d(r)


def dif(vx, vy):
    vx = asanyarray(vx)
    vy = asanyarray(vy)

    if vx.dtype is not vy.dtype:
        raise TypeError("%s is not %s" % (vx.dtype, vy.dtype))

    if vx.dtype.type is uint64:
        r = _dif(vx, vy)
    elif vx.dtype.type is uint32:
        r = _diff(vx, vy)
    else:
        raise TypeError("%s not in (uint64, uint32)" % vx.dtype)

    return _un0d(r)


def _dulp(x, y):
    vx = _val(x)
    vy = _val(y)
    return _dif(vx, vy)


def _val(x):
    shift = int64(63)
    u = x.view(int64)
    r = (u >> shift)
    r |= (int64(1) << shift)
    r ^= u
    return r.view(uint64)


def _dif(vx, vy):
    one = uint64(1)
    hi = (vy >> one).view(int64)
    hi -= (vx >> one).view(int64)
    hi = hi.astype(float32)
    lo = (vy & one).astype(int32)
    lo -= (vx & one).view(int64)
    lo = lo.astype(float32)
    return float32(2)*hi + lo


def _dulpf(x, y):
    vx = _valf(x)
    vy = _valf(y)
    return _diff(vx, vy)


def _valf(x):
    shift = int32(31)
    u = x.view(int32)
    r = (u >> shift)
    r |= (int32(1) << shift)
    r ^= u
    return r.view(uint32)


def _diff(vx, vy):
    r = vx.astype(int64)
    r -= vy.astype(int64)
    return r.astype(float32)


def _un0d(x):
    if x.ndim == 0:
        x = x.dtype.type(x)
    return x
