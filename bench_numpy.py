"""WIP benchmark for numpy version

python -m timeit -vv -s "from bench_numpy import bench" "bench()"


"""
import numpy
import dulp_numpy

ntest = 1000*1000
numpy.random.seed(1234)
testx = numpy.random.rand(ntest) - 0.5
testy = numpy.random.rand(ntest) - 0.5

def bench():
    return dulp_numpy.dulp(testx, testy)
