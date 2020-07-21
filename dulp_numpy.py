"""

python -m timeit -vv -s "from dulp_numpy import perf" "perf()"


"""
import numpy
from numpy import uint64, int64, uint32, int32, float32

# TODO normal numpy behavior
# TODO preamble and exceptions
# TODO separate file

def val(x):
    u = x.view(uint64)
    return -(u >> 63) ^ (u | 1 << 63)


def dif(vx, vy):
    hi = (vy >> 1).view(int64)
    hi -= (vx >> 1).view(int64)
    hi = hi.astype(float32)
    lo = (vy & 1).astype(int32)
    lo -= (vx & 1).astype(int32)
    lo = lo.astype(float32)
    return lo + 2.*hi


ntest = 1000*1000
numpy.random.seed(1234)
testx = numpy.random.rand(ntest) - 0.5
testy = numpy.random.rand(ntest) - 0.5

def perf():
    return dif(val(testx), val(testy))


if __name__ == "__main__":
    import numpy
    x = numpy.array([1., numpy.nan, 1.])
    y = numpy.array([1. + 2**-52, numpy.nan, 1.5])
    vx = val(x)
    vy = val(y)
    print(vx)
    print(vy)
    d = dif(vx, vy)
    print(d)
    print(numpy.log2(d + 0.5) + 1) 
