"""dulp measures order distances between floats"""
from ctypes import Union, c_double, c_ulonglong

class w64(Union):
    _fields_ = [
        ("f", c_double),
        ("u", c_ulonglong),
    ]


def dulp(x, y):
    """Return the order distance from x to y"""
    vx = val(x)
    vy = val(y)
    return float(vy - vx)


def val(x):
    """Return an integer valuation of float x"""
    if not isinstance(x, float):
        raise TypeError("must be float, not %s" % type(x))
    
    u = w64(f=x).u
    sign = 1 << 63
    if u < sign:
        r = sign + u
    else:
        r = 2*sign - 1 - u
    
    return r
