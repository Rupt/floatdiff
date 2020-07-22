"""WIP tests for numpy version

python test_numpy.py

"""
import numpy
import dulp_numpy

from numpy import uint64, uint32
from dulp_numpy import val, dif, dulp

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
try:
    print(dif(uint32(1), uint64(2)))
except TypeError:
    pass

     
