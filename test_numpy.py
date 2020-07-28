"""Run tests on dulp_numpy.py"""
import unittest

import numpy
from numpy import inf, nan
from numpy import float32, float64
from numpy import uint32, uint64

from dulp_numpy import dulp, val, dif, bits

f64max = numpy.finfo(float64).max
f64min = numpy.finfo(float64).tiny
f32max = numpy.finfo(float32).max
f32min = numpy.finfo(float32).tiny
u64max = uint64(numpy.iinfo(uint64).max)
u32max = uint32(numpy.iinfo(uint32).max)


class TestDulp(unittest.TestCase):
    def test_type(self):
        self.assertIs(dulp(.5, .7).dtype.type, float64)
        self.assertIsInstance(dulp([.5], [.7]), numpy.ndarray)
        self.assertIs(dulp(float32(.5), float32(.7)).dtype.type, float64)
        self.assertIsInstance(dulp([float32(.5)], [float32(.7)]), numpy.ndarray)
        with self.assertRaises(TypeError):
            dulp(float32(1), float64(0.5))
        with self.assertRaises(TypeError):
            dulp(1j, 1j)
        with self.assertRaises(TypeError):
            dulp(0, 5e-324)

    def test_increment(self):
        self.assertEqual(dulp(1. - 2**-53, 1.), 1.)
        self.assertEqual(dulp(1.5, 1.5 + 2**-52), 1.)
        self.assertEqual(dulp(0., 5e-324), 1.)
        self.assertEqual(dulp(5e-324, 1e-323), 1.)
        self.assertEqual(dulp(f64min - 5e-324, f64min), 1.)
        self.assertEqual(dulp(f64max, inf), 1.)
        self.assertEqual(dulp(-0., 0.), 1.)

    def test_jump(self):
        self.assertEqual(dulp(1., 1.5), 2**51.)

    def test_asym(self):
        self.assertEqual(dulp(.5, .7), -dulp(.7, .5))
        self.assertEqual(dulp(.5, .7), -dulp(-.5, -.7))

    def test_nan(self):
        self.assertEqual(dulp(nan, nan), 0.)

    def test_broadcast(self):
        vec = dulp(.5, [.7]*2)
        mat = dulp(.5, .5*numpy.ones((1, 2, 3)))
        self.assertEqual(vec.shape, (2,))
        self.assertEqual(mat.shape, (1, 2, 3))
        self.assertEqual(vec[0], dulp(.5, .7))
        self.assertEqual(mat[0, 0, 0], 0.)
        with self.assertRaises(ValueError):
            dulp(vec, mat)

    def test_incrementf(self):
        self.assertEqual(dulp(float32(1. - 2**-24), float32(1.)), 1.)
        self.assertEqual(dulp(float32(1.5), float32(1.5 + 2**-23)), 1.)
        self.assertEqual(dulp(float32(0.), float32(1e-45)), 1.)
        self.assertEqual(dulp(float32(1e-45), float32(3e-45)), 1.)
        self.assertEqual(dulp(f32min - float32(1e-45), f32min), 1.)
        self.assertEqual(dulp(f32max, float32(inf)), 1.)
        self.assertEqual(dulp(-float32(0.), float32(0.)), 1.)

    def test_jumpf(self):
        self.assertEqual(dulp(float32(1.), float32(1.5)), 2**22.)

    def test_asymf(self):
        self.assertEqual(dulp(float32(.5), float32(.7)),
                         -dulp(float32(.7), float32(.5)))
        self.assertEqual(dulp(float32(.5), float32(.7)),
                         -dulp(-float32(.5), -float32(.7)))

    def test_nanf(self):
        self.assertEqual(dulp(float32(nan), float32(nan)), 0.)

    def test_broadcastf(self):
        vec = dulp(.5, [.7]*2)
        mat = dulp(.5, .5*numpy.ones((1, 2, 3)))
        self.assertEqual(vec.shape, (2,))
        self.assertEqual(mat.shape, (1, 2, 3))
        self.assertEqual(vec[0], dulp(.5, .7))
        with self.assertRaises(ValueError):
            dulp(vec, mat)


class TestVal(unittest.TestCase):
    def test_type(self):
        self.assertIs(val(.7).dtype.type, uint64)
        self.assertIsInstance(val([.7]), numpy.ndarray)
        self.assertIs(val(float32(.7)).dtype.type, uint32)
        self.assertIsInstance(val([float32(.7)]), numpy.ndarray)

    def test_order(self):
        self.assertLess(val(.5), val(.7))
        self.assertLess(val(-.3), val(.3))
        self.assertLess(val(0.), val(1e-323))
        self.assertLess(val(-inf), val(inf))

    def test_orderf(self):
        self.assertLess(val(float32(.5)), val(float32(.7)))
        self.assertLess(val(-float32(.3)), val(float32(.3)))
        self.assertLess(val(0.), val(1e-45))
        self.assertLess(val(-float32(inf)), val(float32(inf)))


class TestDif(unittest.TestCase):
    def test_type(self):
        self.assertIs(dif(uint32(1), uint32(2)).dtype.type, float64)
        self.assertIs(dif(uint64(1), uint64(2)).dtype.type, float64)
        with self.assertRaises(TypeError):
            dif(uint32(1), uint64(1))

    def test_dif(self):
        self.assertEqual(dif(uint64(0), uint64(1)), 1.)
        self.assertEqual(dif(uint64(0), u64max), float64(u64max))
        self.assertEqual(dif(u64max, uint64(0)), -float64(u64max))

    def test_diff(self):
        self.assertEqual(dif(uint32(0), uint32(1)), 1)
        self.assertEqual(dif(uint32(0), u32max), float64(u32max))
        self.assertEqual(dif(u32max, uint32(0)), -float64(u32max))


class TestBits(unittest.TestCase):
    def test_type(self):
        self.assertIs(bits(2.7).dtype.type, float64)
        self.assertIsInstance(bits([2.7]), numpy.ndarray)

    def test_bits(self):
        self.assertEqual(bits(0.), 0.)
        self.assertEqual(bits(1.), 1.)
        self.assertEqual(bits(7), 3.)
        self.assertLess(bits(8), 4.)
        self.assertGreater(bits(8), 3.)
        self.assertLess(bits(dulp(-inf, inf)), 64.)

    def test_absolute(self):
        self.assertEqual(bits(dulp(.5, .7)), bits(dulp(.7, .5)))


if __name__ == "__main__":
    unittest.main()
