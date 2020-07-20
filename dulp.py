"""dulp measures order distances between floats"""
import ctypes
from ctypes import Union, c_double, c_ulonglong

class fu64(Union):
    _fields_ = [
        ("f64", c_double),
        ("u64", c_ulonglong),
    ]


def val(x):
    """Return an integer valuation of float x"""
    u = fu64(f64=x).u64
    sign = (1 << 63)
    if u < sign:
        return sign + u
    else:
        return 2*sign - 1 - u


def dulp(x, y):
    """Return the order distance from x to y"""
    return float(val(y) - val(x))
