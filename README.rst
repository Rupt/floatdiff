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
    dulp(1., 1. - 2.**-50) # -8.
    dulp(1.6180339887, (1 + 5**0.5)/2) # 224707.
    dulp(-0., 0.) # 1.

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
