"""dulp measures order distances between floats"""
import ctypes

class word64(ctypes.Union):
    _fields_ = [
        ("f", ctypes.c_double),
        ("u", ctypes.c_ulonglong),
    ]


def val(x):
    """Return an integer valuation of float x"""
    u = word64(f=x).u
    sign = 1 << 63
    if u < sign:
        return sign + u
    else:
        return 2*sign - 1 - u


def dulp(x, y):
    """Return the order distance from x to y"""
    return float(val(y) - val(x))
