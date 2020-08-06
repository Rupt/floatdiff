.. highlight:: rst

.. role:: python(code)
    :language: python

Floating point differences: dulp
================================

`dulp`_ measures differences between floating point numbers by 
putting them in order, then counting steps.

.. code-block:: python

    from dulp import dulp
    
    dulp(1., 1. + 2.**-52) # 1.
    dulp(1.6180339887, (1 + 5**0.5)/2) # 224707.
    dulp(-0., 0.) # 1.

    
.. raw:: html

   <details>
   <summary><b>numpy</b></summary>

.. code-block:: python

    from dulp.numpy import dulp
    from numpy import float32
    
    dulp(1., [1. + 2.**-52, 1. + 2.**-50]) # array([1., 4.])
    dulp(float32(1.6180339887), float32((1 + 5**0.5)/2)) # 0.
    dulp(-0., float32(0.)) # TypeError

.. raw:: html

   </details>
   
.. raw:: html

   <details>
   <summary><b>C</b></summary>

.. code-block:: C

    #include <stdint.h>
    #include "dulp.c"
    
    dulp(1., 1. + pow(2, -52)); # 1.
    dulp(1.6180339887, (1 + sqrt(5))/2); # 224707.
    dulpf(-0., 0.) # 1.f

.. raw:: html

   </details>

This distance was proposed by an anonymous reviewer of
*"On the definition of ulp (x)"* (JM Muller 2005).


WIP project

Detail
------

We first construct a valuation which assigns integers to floats
while preserving numerical order.

.. code-block:: python

    val(0.618) < val(1.618) # True
    
Following Muller's definition, we also have

.. code-block:: python

    val(0.) == 0 # True
    
and

.. code-block:: python

    val(x + eps) == val(x) + 1 # True

whenever ``x + eps`` is the smallest float larger than ``x``.

The dulp distance is then simply the valuation difference

.. code-block:: python

    dulp(x, y) == float(val(y) - val(x)) # True

converted to float for convenience with large differences.


.. _`dulp`: https://github.com/Rupt/dulp
