""" Run tests on floatdiff_numpy.py """
import unittest

import numpy
from numpy import inf, nan
from numpy import float32, float64
from numpy import int32, int64

from floatdiff_numpy import floatdiff, rank, diff, bits


f64max = numpy.finfo(float64).max
f64min = numpy.finfo(float64).tiny
f32max = numpy.finfo(float32).max
f32min = numpy.finfo(float32).tiny
i64max = int64(numpy.iinfo(int64).max)
i64min = int64(numpy.iinfo(int64).min)
i32max = int32(numpy.iinfo(int32).max)
i32min = int32(numpy.iinfo(int32).min)


class TestDulp(unittest.TestCase):
    def test_type(self):
        self.assertIs(floatdiff(.5, .7).dtype.type, float64)
        self.assertIsInstance(floatdiff([.5], [.7]), numpy.ndarray)
        self.assertIs(floatdiff(float32(.5), float32(.7)).dtype.type, float64)
        self.assertIsInstance(floatdiff([float32(.5)], [float32(.7)]), numpy.ndarray)
        with self.assertRaises(TypeError):
            floatdiff(float32(1), float64(0.5))
        with self.assertRaises(TypeError):
            floatdiff(1j, 1j)
        with self.assertRaises(TypeError):
            floatdiff(0, 5e-324)

    def test_increment(self):
        self.assertEqual(floatdiff(1. - 2**-53, 1.), 1.)
        self.assertEqual(floatdiff(1.5, 1.5 + 2**-52), 1.)
        self.assertEqual(floatdiff(0., 5e-324), 1.)
        self.assertEqual(floatdiff(5e-324, 1e-323), 1.)
        self.assertEqual(floatdiff(f64min - 5e-324, f64min), 1.)
        self.assertEqual(floatdiff(f64max, inf), 1.)
        self.assertEqual(floatdiff(-0., 0.), 1.)

    def test_jump(self):
        self.assertEqual(floatdiff(1., 1.5), 2**51.)

    def test_asym(self):
        self.assertEqual(floatdiff(.5, .7), -floatdiff(.7, .5))
        self.assertEqual(floatdiff(.5, .7), -floatdiff(-.5, -.7))

    def test_nan(self):
        self.assertEqual(floatdiff(nan, nan), 0.)

    def test_broadcast(self):
        vec = floatdiff(.5, [.7]*2)
        mat = floatdiff(.5, .5*numpy.ones((1, 2, 3)))
        self.assertEqual(vec.shape, (2,))
        self.assertEqual(mat.shape, (1, 2, 3))
        self.assertEqual(vec[0], floatdiff(.5, .7))
        self.assertEqual(mat[0, 0, 0], 0.)
        with self.assertRaises(ValueError):
            floatdiff(vec, mat)

    def test_incrementf(self):
        self.assertEqual(floatdiff(float32(1. - 2**-24), float32(1.)), 1.)
        self.assertEqual(floatdiff(float32(1.5), float32(1.5 + 2**-23)), 1.)
        self.assertEqual(floatdiff(float32(0.), float32(1e-45)), 1.)
        self.assertEqual(floatdiff(float32(1e-45), float32(3e-45)), 1.)
        self.assertEqual(floatdiff(f32min - float32(1e-45), f32min), 1.)
        self.assertEqual(floatdiff(f32max, float32(inf)), 1.)
        self.assertEqual(floatdiff(-float32(0.), float32(0.)), 1.)

    def test_jumpf(self):
        self.assertEqual(floatdiff(float32(1.), float32(1.5)), 2**22.)

    def test_asymf(self):
        self.assertEqual(floatdiff(float32(.5), float32(.7)),
                         -floatdiff(float32(.7), float32(.5)))
        self.assertEqual(floatdiff(float32(.5), float32(.7)),
                         -floatdiff(-float32(.5), -float32(.7)))

    def test_nanf(self):
        self.assertEqual(floatdiff(float32(nan), float32(nan)), 0.)

    def test_broadcastf(self):
        vec = floatdiff(.5, [.7]*2)
        mat = floatdiff(.5, .5*numpy.ones((1, 2, 3)))
        self.assertEqual(vec.shape, (2,))
        self.assertEqual(mat.shape, (1, 2, 3))
        self.assertEqual(vec[0], floatdiff(.5, .7))
        with self.assertRaises(ValueError):
            floatdiff(vec, mat)


class TestVal(unittest.TestCase):
    def test_type(self):
        self.assertIs(rank(.7).dtype.type, int64)
        self.assertIsInstance(rank([.7]), numpy.ndarray)
        self.assertIs(rank(float32(.7)).dtype.type, int32)
        self.assertIsInstance(rank([float32(.7)]), numpy.ndarray)

    def test_order(self):
        self.assertLess(rank(.5), rank(.7))
        self.assertLess(rank(-.3), rank(.3))
        self.assertLess(rank(0.), rank(1e-323))
        self.assertLess(rank(-inf), rank(inf))

    def test_orderf(self):
        self.assertLess(rank(float32(.5)), rank(float32(.7)))
        self.assertLess(rank(-float32(.3)), rank(float32(.3)))
        self.assertLess(rank(0.), rank(1e-45))
        self.assertLess(rank(-float32(inf)), rank(float32(inf)))


class TestDif(unittest.TestCase):
    def test_type(self):
        self.assertIs(diff(int32(1), int32(2)).dtype.type, float64)
        self.assertIs(diff(int64(1), int64(2)).dtype.type, float64)
        with self.assertRaises(TypeError):
            diff(int32(1), int64(1))

    def test_diff(self):
        self.assertEqual(diff(int64(0), int64(1)), 1.)
        self.assertEqual(diff(int64(0), i64max), float64(i64max))
        self.assertEqual(diff(i64max, int64(0)), -float64(i64max))
        self.assertEqual(diff(int64(0), i64min), float64(i64min))
        self.assertEqual(diff(i64min, int64(0)), -float64(i64min))

    def test_diff(self):
        self.assertEqual(diff(int32(0), int32(1)), 1)
        self.assertEqual(diff(int32(0), i32max), float64(i32max))
        self.assertEqual(diff(i32max, int32(0)), -float64(i32max))
        self.assertEqual(diff(int32(0), i32min), float64(i32min))
        self.assertEqual(diff(i32min, int32(0)), -float64(i32min))


class TestBits(unittest.TestCase):
    def test_type(self):
        self.assertIs(bits(5.).dtype.type, float64)
        self.assertIsInstance(bits([5., 8.]), numpy.ndarray)

    def test_bits(self):
        self.assertEqual(bits(0.), 0.)
        self.assertEqual(bits(1.), 1.)
        self.assertEqual(bits(7), 3.)
        self.assertLess(bits(8), 4.)
        self.assertGreater(bits(8), 3.)
        self.assertLess(bits(floatdiff(-inf, inf)), 64.)

    def test_absolute(self):
        self.assertEqual(bits(floatdiff(.5, .7)), bits(floatdiff(.7, .5)))


class TestREADME(unittest.TestCase):
    def test_readme(self):
        vec = floatdiff(1., [1. + 2.**-52, 1. + 2.**-50])
        self.assertEqual(vec.shape, (2,))
        self.assertEqual(list(vec), [1., 4.])
        self.assertEqual(floatdiff(float32((1 + 5**0.5)/2),
                              float32(1.6180339887)), 0.)
        with self.assertRaises(TypeError):
            floatdiff(-0., float32(0.))


if __name__ == "__main__":
    unittest.main()
