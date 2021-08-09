Floating point differences
===================================

`floatdiff`_ measures directed differences between floating point numbers by
counting the spaces between them.


This distance was proposed by an anonymous reviewer to
*"On the definition of ulp(x)"* (JM Muller 2005).


Various implementations included.

**python**

.. code-block:: python

    from floatdiff import floatdiff

    floatdiff(1., 1. + 2.**-52) # 1.
    floatdiff((1. + 5**0.5)/2, 1.6180339887) # -224707.
    floatdiff(-0., 0.) # 1.


**numpy**

.. code-block:: python

    from floatdiff_numpy import floatdiff
    from numpy import float32

    floatdiff(1., [1. + 2.**-52, 1. + 2.**-50]) # array([1., 4.])
    floatdiff(float32((1 + 5**0.5)/2), float32(1.6180339887)) # 0.
    floatdiff(-0., float32(0.)) # TypeError


**c**

.. code-block:: c

    #include <stdint.h>
    #include "floatdiff.c"

    floatdiff(1., 1. + pow(2, -52)); /* 1. */
    floatdiff((1. + sqrt(5))/2, 1.6180339887); /* -224707. */
    floatdifff(-0., 0.) /* 1. */


**go**

.. code-block:: go

    floatdiff.Floatdiff(1, 1 + math.Pow(2, -52)) // 1.
    floatdiff.Floatdiff((1 + math.Sqrt(5))/2, 1.6180339887) // -224707.
    zero := float32(0)
    floatdiff.Floatdiff32(-zero, 0) // 1.


Details
-------

Each float or double gets an integer valuation ``rank(x)`` satisfying

.. code-block:: python

    rank(0.) == 0 # True

and

.. code-block:: python

    rank(nextafter(x)) == rank(x) + 1 # True .

Floats almost have this naturally when reinterpreted as integers,
but are reversed for negative numbers.

We just reverse negative numbers' order.

Then

.. code-block:: python

    floatdiff(x, y) == float(rank(y) - rank(x)) # True

uses floating point for coverage of small and large distances.

A bits-precision equivalent conversion is given by ``bits``.


.. _`floatdiff`: https://github.com/Rupt/floatdiff
