.. highlight:: rst

.. role:: python(code)
    :language: python

Floating point differences: dulp
================================

`dulp`_ puts floating-point numbers in order, then measures differences
by counting the steps between them.

.. code-block:: python

    from dulp import dulp
    dulp(1., 1. + 2.**-52) # 1.
    dulp(1., 1. - 2.**-50) # -8.
    dulp(1.6180339887, (1 + 5**0.5)/2) # 224707.
    dulp(-0., 0.) # 1.

This distance was proposed by an anonymous reviewer of
*"On the definition of ulp (x)"* (JM Muller 2005).

Detail
------

.. code-block:: python

    # Paraphrasing Muller
    # define an integer valuation
    val(x)
    # such that
    val(0.) == 0
    # and, if y is the next representable number after x, then
    val(y) == val(x) + 1

    # the distance then has
    dulp(x, y) == val(y) - val(x)
    # and is more conveniently represented as a float.


.. _`dulp`: https://github.com/Rupt/dulp
