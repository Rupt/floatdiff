"""WIP tests for numpy version

python test_numpy.py

"""
import unittest
import sys
import numpy
import dulp_numpy

from numpy import ndarray
from numpy import float32, float64
from numpy import uint32, uint64
from numpy import inf, nan, log2
from dulp_numpy import dulp, val, dif

f64max = numpy.finfo(float64).max
f64min = numpy.finfo(float64).tiny
f32max = numpy.finfo(float32).max
f32min = numpy.finfo(float32).tiny


class testdulp(unittest.TestCase):
    def test_increment(self):
        self.assertEqual(dulp(1., 1. + 2**-52), 1.)
        self.assertEqual(dulp(1.5, 1.5 + 2**-52), 1.)

    def test_jump(self):
        self.assertEqual(dulp(1., 1.5), 2**51.)

    def test_antisym(self):
        self.assertEqual(dulp(.5, .7), -dulp(.7, .5))
        self.assertEqual(dulp(.5, .7), -dulp(-.5, -.7))

    def test_zero(self):
        self.assertEqual(dulp(-0., 0.), 1.)

    def test_incrementf(self):
        self.assertEqual(dulp(float32(1.), float32(1. + 2**-23)), 1.)
        self.assertEqual(dulp(float32(1.5), float32(1.5 + 2**-23)), 1.)

    def test_denormal(self):
        self.assertEqual(dulp(0., 5e-324), 1.)
        self.assertEqual(dulp(5e-324, 1e-323), 1.)
        fmin = numpy.finfo(float64).tiny
        self.assertEqual(dulp(fmin - 5e-324, fmin), 1.)

    def test_naninf(self):
        self.assertEqual(dulp(nan, nan), 0.)
        self.assertEqual(dulp(inf, inf), 0.)
        fmax = numpy.finfo(float64).max
        self.assertEqual(dulp(fmax, inf), 1.)

    def test_type(self):
        self.assertIsInstance(dulp(.5, .7), float32)
        self.assertIsInstance(dulp([.5], [.7]), ndarray)
    
    def test_arg(self):
        with self.assertRaises(TypeError):
            dulp(float32(1), float64(0.5))
        with self.assertRaises(TypeError):
            dulp(1j, 1j)
        with self.assertRaises(TypeError):
            dulp(0, 5e-324)

    def test_broadcast(self):
        fvec = dulp(.5, [.7]*2)
        fmat = dulp(.5*numpy.ones((1, 2, 3)), .5)
        self.assertEqual(fvec.shape, (2,))
        self.assertEqual(fmat.shape, (1,2,3))
        self.assertEqual(fvec[0], dulp(.5, .7))
        self.assertEqual(fmat[0, 0, 0], 0.)
        with self.assertRaises(ValueError):
            dulp(numpy.ones(2), numpy.ones(3))


class testdulpf(unittest.TestCase):
    def test_jump(self):
        self.assertEqual(dulp(float32(1.), float32(1.5)), 2**22.)

    def test_antisym(self):
        f5, f7 = float32(.5), float32(.7)
        self.assertEqual(dulp(f5, f7), -dulp(f7, f5))
        self.assertEqual(dulp(f5, f7), -dulp(-f5, -f7))

    def test_zero(self):
        self.assertEqual(dulp(-float32(0.), float32(0.)), 1.)

    def test_denormal(self):
        self.assertEqual(dulp(float32(0.), float32(1e-45)), 1.)
        self.assertEqual(dulp(float32(1e-45), float32(3e-45)), 1.)
        fmin = numpy.finfo(float32).tiny
        self.assertEqual(dulp(fmin - float32(1e-45), fmin), 1.)

    def test_naninf(self):
        self.assertEqual(dulp(float32(nan), float32(nan)), 0.)
        self.assertEqual(dulp(float32(inf), float32(inf)), 0.)
        fmax = numpy.finfo(float32).max
        self.assertEqual(dulp(fmax, float32(inf)), 1.)

    def test_type(self):
        self.assertIsInstance(dulp(float32(.5), float32(.7)), float32)
        self.assertIsInstance(dulp([float32(.5)], [float32(.7)]), ndarray)

# TODO testdif

class testval(unittest.TestCase):
    # TODO update, include float
    def test_order(self):
        self.assertLess(val(.5), val(.7))
        self.assertLess(val(-.3), val(.3))
        self.assertLess(val(0.), val(1e-323))
        self.assertLess(val(-inf), val(inf))

    def test_cast(self):
        with self.assertRaises(TypeError):
            val(-0)

    def test_type(self):
        self.assertIsInstance(val(.7), uint64)

    def test_error(self):
        with self.assertRaises(TypeError):
            val(None)
        with self.assertRaises(TypeError):
            val(1j)


if __name__ == "__main__":
    unittest.main()
