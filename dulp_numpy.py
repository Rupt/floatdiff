"""

python -m timeit -vv -s "from dulp_numpy import perf" "perf()"


"""
import numpy
from numpy import (
    uint64, int64, uint32, int32,
    float64, float32,
)

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
        raise TypeError("must be float64 or float32, not %s" % x.dtype)

    if x.ndim == 0:
        x = ftype(x)

    u = x.view(utype)
    u = -(u >> shift) ^ (u | utype(1) << shift)

    return u


def dif(vx, vy):
    vx = numpy.asanyarray(vx)
    vy = numpy.asanyarray(vy)
    
    if vx.shape != vy.shape:
        shapes = (vx.shape, vy.shape)
        raise ValueError("vy vy have different shapes %s %s" % shapes)
    
    if vx.dtype is not vy.dtype:
        types = (vx.dtype, vy.dtype)
        raise TypeError("vx vy have different types %s %s" % types)
    
    utype = vx.dtype.type
    if utype is uint64:
        itype = int64
    elif utype is uint32:
        itype = int32
    else:
        raise TypeError("must be uint64 or uint32, not %s" % vx.dtype)
    
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
    return dif(val(x), val(y))
    
    



ntest = 1000*1000
numpy.random.seed(1234)
testx = numpy.random.rand(ntest) - 0.5
testy = numpy.random.rand(ntest) - 0.5

def perf():
    return dulp(testx, testy)


if __name__ == "__main__":
    x = numpy.array([1., numpy.nan, 1.])
    y = numpy.array([1. + 2**-52, numpy.nan, 1.5])
    vx = val(x)
    vy = val(y)
    print(vx)
    print(vy)
    d = dif(vx, vy)
    print(d)
    print(dulp(1., 2.))
    print(dulp([[1.],[4.]], [[2.],[3.]]))
    #print(dif(uint32(1), uint64(2)))
    
