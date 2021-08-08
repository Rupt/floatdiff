"""WIP benchmark for numpy version

python -m timeit -vv -s "from bench_numpy import bench" "bench()"

python -m timeit -vv -s "from bench_numpy import benchf" "benchf()"


"""
import numpy
from dulp_numpy import dulp


def init():
    ntest = 1000*1000
    numpy.random.seed(1234)
    x = numpy.random.rand(ntest) - 0.5
    y = numpy.random.rand(ntest) - 0.5
    return x, y


def initf():
    x, y = init()
    x = x.astype(numpy.float32)
    y = y.astype(numpy.float32)
    return x, y
