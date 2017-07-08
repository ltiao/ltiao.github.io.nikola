.. title: NumPy mgrid vs. meshgrid
.. slug: numpy-mgrid-vs-meshgrid
.. date: 2015-10-30 16:00:19 UTC+11:00
.. tags: python, numpy
.. category: 
.. link: 
.. description: 
.. type: text

The `meshgrid`_ function is useful for creating coordinate arrays to 
vectorize function evaluations over a grid. Experienced NumPy users will have 
noticed some discrepancy between ``meshgrid`` and the `mgrid`_, a function 
that is used just as often, for exactly the same purpose. What is the 
discrepancy, and why does a discrepancy even exist when *"there should be one 
- and preferably only one - obvious way to do it."* [#]_

First, recall that ``meshgrid`` behaves as follows:

.. code:: pycon

   >>> import numpy as np
   >>> x1, y1 = np.meshgrid(np.arange(1, 11, 2), np.arange(-12, -3, 3))
   >>> x1
   array([[1, 3, 5, 7, 9],
          [1, 3, 5, 7, 9],
          [1, 3, 5, 7, 9]])
   >>> y1
   array([[-12, -12, -12, -12, -12],
          [ -9,  -9,  -9,  -9,  -9],
          [ -6,  -6,  -6,  -6,  -6]])

.. TEASER_END

If you have used NumPy for a while or are familiar enough with how 
`Broadcasting`_ works, you will have realized that ``meshgrid`` is actually 
superfluous for NumPy arrays, and that it is actually just an implementation 
of `MATLAB's meshgrid`_, probably to cater to users coming from a MATLAB 
background. 

Observe the behavior of ``mgrid``, which essentially returns the transpose of 
``meshgrid``:

.. code:: pycon

   >>> x2, y2 = np.mgrid[1:11:2, -12:-3:3]
   >>> x2
   array([[1, 1, 1],
          [3, 3, 3],
          [5, 5, 5],
          [7, 7, 7],
          [9, 9, 9]])
   >>> y2
   array([[-12,  -9,  -6],
          [-12,  -9,  -6],
          [-12,  -9,  -6],
          [-12,  -9,  -6],
          [-12,  -9,  -6]])
   >>> np.all(x1 == x2.T)
   True
   >>> np.all(y2 == y2.T)
   True

Note this this order is actually more natural, since ``mgrid`` just fleshes 
out the open (not fleshed out) grids given by `ogrid`_ by broadcasting them to 
form dense grids, i.e.

.. code:: pycon

   >>> a, b = np.ogrid[1:11:2, -12:-3:3]
   >>> a
   array([[1],
          [3],
          [5],
          [7],
          [9]])
   >>> b
   array([[-12,  -9,  -6]])

and the *5x1* array ``a`` is broadcasted with the *1x3* array ``b`` to form 
two *5x3* arrays

.. code:: pycon

   >>> x2, y2 = np.broadcast_arrays(a, b)
   >>> x2
   array([[1, 1, 1],
          [3, 3, 3],
          [5, 5, 5],
          [7, 7, 7],
          [9, 9, 9]])
   >>> y2
   array([[-12,  -9,  -6],
          [-12,  -9,  -6],
          [-12,  -9,  -6],
          [-12,  -9,  -6],
          [-12,  -9,  -6]])

which behaves exactly the same way as ``mgrid``. Note that you seldom have to 
broadcast arrays explicitly, let alone use functions like ``mgrid`` or 
``meshgrid``, since all arithmetic operations on NumPy arrays already perform 
broadcasting implicitly. E.g.

.. code:: pycon
   
   >>> x2 + y2
   array([[-11,  -8,  -5],
          [ -9,  -6,  -3],
          [ -7,  -4,  -1],
          [ -5,  -2,   1],
          [ -3,   0,   3]])
   >>> a + b
   array([[-11,  -8,  -5],
          [ -9,  -6,  -3],
          [ -7,  -4,  -1],
          [ -5,  -2,   1],
          [ -3,   0,   3]])

Finally, if for some reason you must have output like that of  ``meshgrid``, 
just use ``mgrid`` with the  arguments and unpacking targets reversed.

.. code:: pycon

   >>> y3, x3 = np.mgrid[-12:-3:3, 1:11:2]
   >>> x3
   array([[1, 3, 5, 7, 9],
          [1, 3, 5, 7, 9],
          [1, 3, 5, 7, 9]])
   >>> y3
   array([[-12, -12, -12, -12, -12],
          [ -9,  -9,  -9,  -9,  -9],
          [ -6,  -6,  -6,  -6,  -6]])
   >>> np.all(x1 == x3)
   True
   >>> np.all(y1 == y3)
   True

Of course, if you are using ``np.linspace`` instead of ``np.arange``, then
you're better off sticking with ``np.meshgrid``.

.. _meshgrid: http://docs.scipy.org/doc/numpy/reference/generated/numpy.meshgrid.html
.. _mgrid: http://docs.scipy.org/doc/numpy/reference/generated/numpy.mgrid.html
.. _ogrid: http://docs.scipy.org/doc/numpy/reference/generated/numpy.ogrid.html
.. _`MATLAB's meshgrid`: http://au.mathworks.com/help/matlab/ref/meshgrid.html
.. _Broadcasting: http://docs.scipy.org/doc/numpy/user/basics.broadcasting.html

.. [#] PEP20 - The Zen of Python (https://www.python.org/dev/peps/pep-0020/)

Further Reading
---------------

- http://stackoverflow.com/questions/12402045/mesh-grid-functions-in-python-meshgrid-mgrid-ogrid-ndgrid
