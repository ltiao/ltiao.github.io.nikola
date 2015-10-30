.. title: NumPy mgrid vs. meshgrid
.. slug: numpy-mgrid-vs-meshgrid
.. date: 2015-10-30 16:00:19 UTC+11:00
.. tags: python, numpy
.. category: 
.. link: 
.. description: 
.. type: text

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
