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

def val(x):
    x = numpy.asanyarray(x)

    ftype = x.dtype.type
    if ftype is float64:
        utype = uint64
        shift = utype(63)
    elif ftype is float32:
        utype = uint32
        shift = utype(31)
    else:
        raise TypeError("%s not in (float64, float32)" % x.dtype)

    if x.ndim == 0:
        x = ftype(x)

    u = x.view(utype)
    return -(u >> shift) ^ (u | utype(1) << shift)


def dif(vx, vy):
    vx = numpy.asanyarray(vx)
    vy = numpy.asanyarray(vy)

    if vx.dtype is not vy.dtype:
        raise TypeError("%s is not %s" % (vx.dtype, vy.dtype))

    utype = vx.dtype.type
    if utype is uint64:
        itype = int64
    elif utype is uint32:
        itype = int32
    else:
        raise TypeError("%s not in (uint64, uint32)" % vx.dtype)

    if vx.ndim == 0:
        vx = utype(vx)
        vy = utype(vy)

    one = utype(1)
    hi = (vy >> one).view(itype)
    hi -= (vx >> one).view(itype)
    hi = hi.astype(float32)
    lo = (vy & one).astype(int32)
    lo -= (vx & one).astype(int32)
    lo = lo.astype(float32)
    return lo + 2.*hi


def dulp(x, y):
    vx = val(x)
    vy = val(y)
    return dif(vx, vy)
