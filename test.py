"""Run tests on dulp.py"""
from math import inf, nan
import unittest
import sys

from dulp import dulp, val, dif, bits

f64max = sys.float_info.max
f64min = sys.float_info.min
u64max = (1 << 64) - 1


class TestDulp(unittest.TestCase):
    def test_type(self):
        self.assertIsInstance(dulp(.5, .7), float)

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


class TestVal(unittest.TestCase):
    def test_type(self):
        self.assertIsInstance(val(0.7), int)

    def test_order(self):
        self.assertLess(val(.5), val(.7))
        self.assertLess(val(-.3), val(.3))
        self.assertLess(val(0.), val(5e-324))
        self.assertLess(val(-inf), val(inf))


class TestDif(unittest.TestCase):
    def test_type(self):
        self.assertIsInstance(dif(1, 2), float)

    def test_dif(self):
        self.assertEqual(dif(0, 1), 1.)
        self.assertEqual(dif(0, u64max), float(u64max))
        self.assertEqual(dif(u64max, 0), -float(u64max))


class TestBits(unittest.TestCase):
    def test_type(self):
        self.assertIsInstance(bits(2.7), float)

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
