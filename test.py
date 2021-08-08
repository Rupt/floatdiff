""" Run tests on floatdiff.py """
from math import inf, nan
import unittest
import sys

from floatdiff import floatdiff, rank, diff, bits


f64max = sys.float_info.max
f64min = sys.float_info.min
i64max = (1 << 63) - 1
i64min = -(1 << 63)


class TestBits(unittest.TestCase):
    def test_type(self):
        self.assertIsInstance(bits(5.), float)

    def test_bits(self):
        self.assertEqual(bits(0.), 0.)
        self.assertEqual(bits(1.), 1.)
        self.assertEqual(bits(7), 3.)
        self.assertLess(bits(8), 4.)
        self.assertGreater(bits(8), 3.)
        self.assertLess(bits(floatdiff(-inf, inf)), 64.)

    def test_absolute(self):
        self.assertEqual(bits(floatdiff(.5, .7)), bits(floatdiff(.7, .5)))


class TestDulp(unittest.TestCase):
    def test_type(self):
        self.assertIsInstance(floatdiff(.5, .7), float)

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


class TestRank(unittest.TestCase):
    def test_type(self):
        self.assertIsInstance(rank(0.7), int)

    def test_order(self):
        self.assertLess(rank(.5), rank(.7))
        self.assertLess(rank(-.3), rank(.3))
        self.assertLess(rank(0.), rank(5e-324))
        self.assertLess(rank(-inf), rank(inf))


class TestDiff(unittest.TestCase):
    def test_type(self):
        self.assertIsInstance(diff(1, 2), float)

    def test_diff(self):
        self.assertEqual(diff(0, 1), 1.)
        self.assertEqual(diff(0, i64max), float(i64max))
        self.assertEqual(diff(i64max, 0), -float(i64max))
        self.assertEqual(diff(0, i64min), float(i64min))
        self.assertEqual(diff(i64min, 0), -float(i64min))


class TestReadme(unittest.TestCase):
    def test_readme(self):
        self.assertEqual(floatdiff(1., 1. + 2**-52), 1.)
        self.assertEqual(floatdiff((1 + 5**0.5)/2, 1.6180339887), -224707.)
        self.assertEqual(floatdiff(-0., 0.), 1.)


if __name__ == "__main__":
    unittest.main()
