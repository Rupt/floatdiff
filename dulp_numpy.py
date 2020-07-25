"""

python -m timeit -vv -s "from dulp_numpy import perf" "perf()"


"""
import numpy
from numpy import (
    uint64, int64, uint32, int32,
    float64, float32,
)

# TODO documentation
# TODO tests

def dulp(x, y):
    x = numpy.asanyarray(x)
    y = numpy.asanyarray(y)

    if x.dtype is not y.dtype:
        raise TypeError("%s is not %s" % (x.dtype, y.dtype))

    if x.dtype.type is float64:
        cdulp = _dulp
    elif x.dtype.type is float32:
        cdulp = _dulpf
    else:
        raise TypeError("%s not in (float64, float32)" % x.dtype)

    return _un0d(cdulp(x, y))


def val(x):
    x = numpy.asanyarray(x)

    if x.dtype.type is float64:
        cval = _val
    elif x.dtype.type is float32:
        cval = _valf
    else:
        raise TypeError("%s not in (float64, float32)" % x.dtype)

    return _un0d(cval(x))


def dif(vx, vy):
    vx = numpy.asanyarray(vx)
    vy = numpy.asanyarray(vy)

    if vx.dtype is not vy.dtype:
        raise TypeError("%s is not %s" % (vx.dtype, vy.dtype))

    if vx.dtype.type is uint64:
        cdif = _dif
    elif vx.dtype.type is uint32:
        cdif = _diff
    else:
        raise TypeError("%s not in (uint64, uint32)" % vx.dtype)

    return _un0d(cdif(vx, vy))



def _dulp(x, y):
    vx = _val(x)
    vy = _val(y)
    return _dif(vx, vy)


def _val(x):
    u = x.view(int64)
    shift = int64(63)
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
    lo -= (vx & one).astype(int32)
    lo = lo.astype(float32)
    return float32(2)*hi + lo


def _dulpf(x, y):
    vx = _valf(x)
    vy = _valf(y)
    return _diff(vx, vy)


def _valf(x):
    u = x.view(int32)
    shift = int32(31)
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
