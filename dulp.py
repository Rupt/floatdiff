"""dulp measures order distances between floats"""
from ctypes import Union, c_double, c_ulonglong
from math import log2

class Word64(Union):
    _fields_ = [
        ("f8", c_double),
        ("u8", c_ulonglong),
    ]


def dulp(x, y):
    """Return the  order difference from x to y."""
    vx = val(x)
    vy = val(y)
    return float(vy - vx)


def val(x):
    """Return an integer valuation of float x."""
    if not isinstance(x, float):
        raise TypeError("must be float, not %s" % type(x))
    
    u = Word64(f8=x).u8
    sign = 1 << 63
    if u < sign:
        value = sign + u
    else:
        value = 2*sign - 1 - u
    
    return value
