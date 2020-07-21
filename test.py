import unittest
import sys
import math
import dulp

from math import nan, inf, log2
from dulp import val, dulp

fmax = sys.float_info.max
fmin = sys.float_info.min


class testval(unittest.TestCase):
    def test_order(self):
        self.assertLess(val(0.5), val(0.7))
        self.assertLess(val(-0.3), val(0.3))
        self.assertLess(val(0.), val(1e-323))
        self.assertLess(val(-inf), val(inf))

    def test_cast(self):
        self.assertEqual(val(0), val(0.))
        self.assertEqual(val(1), val(1.))
        self.assertEqual(val(-3), val(-3.))
        self.assertEqual(val(10**300), val(1e300))
        self.assertNotEqual(val(-0), val(-0.))

    def test_type(self):
        self.assertIsInstance(val(0.7), int)


class testdulp(unittest.TestCase):
    def test_increment(self):
        self.assertEqual(dulp(1., 1. + 2.**-52), 1.)
        self.assertEqual(dulp(1.5, 1.5 + 2.**-52), 1.)
        
    def test_jump(self):
        self.assertEqual(log2(dulp(1., 1.5)), 51.)

    def test_antisym(self):
        self.assertEqual(dulp(.5, .7), -dulp(.7, .5))
        self.assertEqual(dulp(.5, .7), -dulp(-.5, -.7))

    def test_zero(self):
        self.assertEqual(dulp(-0., 0.), 1.)

    def test_denormal(self):
        self.assertEqual(dulp(0., 5e-324), 1.)
        self.assertEqual(dulp(5e-324, 1e-323), 1.)
        self.assertEqual(dulp(fmin - 5e-324, fmin), 1.)

    def test_naninf(self):
        self.assertEqual(dulp(nan, nan), 0.)
        self.assertEqual(dulp(inf, inf), 0.)
        self.assertEqual(dulp(fmax, inf), 1.)

    def test_type(self):
        self.assertIsInstance(dulp(0.5, .7), float)


if __name__ == "__main__":
    unittest.main()
