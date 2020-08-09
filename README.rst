
Floating point differences --- dulp
================================

`dulp`_ measures directed differences between floating point numbers by
counting the discrete spaces between them.


This distance was proposed by an anonymous reviewer to
*"On the definition of ulp(x)"* (JM Muller 2005).


.. code-block:: python

    from dulp import dulp

    dulp(1., 1. + 2.**-52) # 1.
    dulp((1. + 5**0.5)/2, 1.6180339887) # -224707.
    dulp(-0., 0.) # 1.


.. raw:: html

   <details>
   <summary><b>numpy</b></summary>

.. code-block:: python

    from dulp.np import dulp
    from numpy import float32

    dulp(1., [1. + 2.**-52, 1. + 2.**-50]) # array([1., 4.])
    dulp(float32((1 + 5**0.5)/2), float32(1.6180339887)) # 0.
    dulp(-0., float32(0.)) # TypeError

.. raw:: html

   </details>

.. raw:: html

   <details>
   <summary><b>C</b></summary>

.. code-block:: C

    #include <stdint.h>
    #include "dulp.c"

    dulp(1., 1. + pow(2, -52)); /* 1. */
    dulp((1. + sqrt(5))/2, 1.6180339887); /* -224707. */
    dulpf(-0., 0.) /* 1.f */

.. raw:: html

   </details>


Each float or double gets an integer valuation val(x) which satisfies

.. code-block:: python

    val(0.) == 0 # True

and

.. code-block:: python

    val(x + eps) == val(x) + 1 # True

where x + eps is the next floating point number after x.
Floats almost have this naturally in their binary, but are reversed for
negative numbers; we just reverse negative numbers' order.

Then

.. code-block:: python

    dulp(x, y) == float(val(y) - val(x)) # True

casted to floating point for convenience with small and large distances.

A bits-precision equivalent conversion is given by ``dulpbits``.


.. _`dulp`: https://github.com/Rupt/dulp
