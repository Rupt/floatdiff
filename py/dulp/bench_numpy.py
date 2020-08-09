"""WIP benchmark for numpy version

python -m timeit -vv -s "from bench_numpy import bench" "bench()"

python -m timeit -vv -s "from bench_numpy import benchf" "benchf()"


"""
import numpy
from np import dulp

ntest = 1000*1000
numpy.random.seed(1234)
testx = numpy.random.rand(ntest) - 0.5
testy = numpy.random.rand(ntest) - 0.5
testxf = testx.astype(numpy.float32)
testyf = testy.astype(numpy.float32)

def bench():
    return dulp(testx, testy)

def benchf():
    return dulp(testxf, testyf)
