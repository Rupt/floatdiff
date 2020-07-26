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
    def test_arg(self):
        with self.assertRaises(TypeError):
            dulp(float32(1), float64(0.5))
        with self.assertRaises(TypeError):
            dulp(1j, 1j)
        with self.assertRaises(TypeError):
            dulp(0, 5e-324)


class testdulp64(unittest.TestCase):
    def test_increment(self):
        self.assertEqual(dulp(1. - 2**-53, 1.), 1.)
        self.assertEqual(dulp(1.5, 1.5 + 2**-52), 1.)
        self.assertEqual(dulp(0., 5e-324), 1.)
        self.assertEqual(dulp(5e-324, 1e-323), 1.)
        self.assertEqual(dulp(f64min - 5e-324, f64min), 1.)
        self.assertEqual(dulp(-0., 0.), 1.)

    def test_jump(self):
        self.assertEqual(dulp(1., 1.5), 2**51.)

    def test_antisym(self):
        self.assertEqual(dulp(.5, .7), -dulp(.7, .5))
        self.assertEqual(dulp(.5, .7), -dulp(-.5, -.7))

    def test_naninf(self):
        self.assertEqual(dulp(nan, nan), 0.)
        self.assertEqual(dulp(inf, inf), 0.)
        self.assertEqual(dulp(f64max, inf), 1.)

    def test_type(self):
        self.assertIs(dulp(.5, .7).dtype.type, float32)
        self.assertIsInstance(dulp([.5], [.7]), ndarray)

    def test_broadcast(self):
        vec = dulp(.5, [.7]*2)
        mat = dulp(.5, .5*numpy.ones((1, 2, 3)))
        self.assertEqual(vec.shape, (2,))
        self.assertEqual(mat.shape, (1,2,3))
        self.assertEqual(vec[0], dulp(.5, .7))
        self.assertEqual(mat[0, 0, 0], 0.)
        with self.assertRaises(ValueError):
            dulp(vec, mat)


class testdulp32(unittest.TestCase):
    def test_increment(self):
        self.assertEqual(dulp(float32(1. - 2**-24), float32(1.)), 1.)
        self.assertEqual(dulp(float32(1.5), float32(1.5 + 2**-23)), 1.)
        self.assertEqual(dulp(float32(0.), float32(1e-45)), 1.)
        self.assertEqual(dulp(float32(1e-45), float32(3e-45)), 1.)
        self.assertEqual(dulp(f32min - float32(1e-45), f32min), 1.)
        self.assertEqual(dulp(-float32(0.), float32(0.)), 1.)
        
    def test_jump(self):
        self.assertEqual(dulp(float32(1.), float32(1.5)), 2**22.)

    def test_antisym(self):
        f5, f7 = float32(.5), float32(.7)
        self.assertEqual(dulp(f5, f7), -dulp(f7, f5))
        self.assertEqual(dulp(f5, f7), -dulp(-f5, -f7))

    def test_naninf(self):
        self.assertEqual(dulp(float32(nan), float32(nan)), 0.)
        self.assertEqual(dulp(float32(inf), float32(inf)), 0.)
        self.assertEqual(dulp(f32max, float32(inf)), 1.)

    def test_type(self):
        f5, f7 = float32(.5), float32(.7)
        self.assertIs(dulp(f5, f7).dtype.type, float32)
        self.assertIsInstance(dulp([f5], [f7]), ndarray)

    def test_broadcast(self):
        vec = dulp(.5, [.7]*2)
        mat = dulp(.5, .5*numpy.ones((1, 2, 3)))
        self.assertEqual(vec.shape, (2,))
        self.assertEqual(mat.shape, (1,2,3))
        self.assertEqual(vec[0], dulp(.5, .7))
        self.assertEqual(mat[0, 0, 0], 0.)
        with self.assertRaises(ValueError):
            dulp(vec, mat)
            

class testval(unittest.TestCase):
    def test_arg(self):
        with self.assertRaises(TypeError):
            val(-0)

    
class testval64(unittest.TestCase):
    def test_order(self):
        self.assertLess(val(.5), val(.7))
        self.assertLess(val(-.3), val(.3))
        self.assertLess(val(0.), val(1e-323))
        self.assertLess(val(-inf), val(inf))

    def test_type(self):
        self.assertIs(val(.7).dtype.type, uint64)
        self.assertIsInstance(val([.7]), ndarray)

    
class testval32(unittest.TestCase):
    def test_order(self):
        self.assertLess(val(float32(.5)), val(float32(.7)))
        self.assertLess(val(-float32(.3)), val(float32(.3)))
        self.assertLess(val(0.), val(1e-45))
        self.assertLess(val(-float32(inf)), val(float32(inf)))

    def test_type(self):
        self.assertIs(val(float32(.7)).dtype.type, uint32)
        self.assertIsInstance(val([float32(.7)]), ndarray)
        
        

# TODO testdif
class testdif(unittest.TestCase):
    def test_arg(self):
        with self.assertRaises(TypeError):
            dif(uint32(1), uint64(1))
        with self.assertRaises(TypeError):
            dif(1j, 1j) # TODO
        with self.assertRaises(TypeError):
            dif(0, 5e-324)


if __name__ == "__main__":
    unittest.main()
