.. title: Adding __name__ and __doc__ attributes to functools.partial objects
.. slug: adding-__name__-and-__doc__-attributes-to-functoolspartial-objects
.. date: 2016-02-08 14:42:56 UTC+11:00
.. tags: python, functools, partial function application, functional programming, autograd, regression
.. category: coding 
.. link: 
.. description: 
.. type: text

The partial_ function from the functools_ library is useful for performing
partial function application in Python. There are plenty of guides and 
resources on functional programming in Python and this post assumes a reasonable
degree of proficiency with both.

.. TEASER_END

The Problem
-----------

Consider the sum squared residuals function defined below:

..  code:: python

    def sse(X, y, w):
        """Sum squared error function"""  
        z = X.dot(w) - y
        return .5 * z.T.dot(z)

In actual regression problems, we would minimize with respect to weights ``w`` 
and keep ``X`` and ``y`` fixed. For example, consider the following synthetic
regression problem:

..  code:: pycon
    
    >>> import numpy as np
    >>> f = lambda x, y, z: 2.*x + .5*y - 1.2*z # true weights [2., .5, -1.2]
    >>> X = np.random.randn(10, 3) # 10 samples, 3 features
    >>> y = f(*X.T) + .25 * np.random.randn(10) # Gaussian noise, scale 0.25
    >>> sse(X, y, np.ones(3)) # try weights [1., 1., 1.]
    12.013621162428603

We could partially apply ``X`` and ``y`` to the function ``sse``, and obtain
a function of only the weights ``w``, and pass that to an optimizer, for example.

..  code:: pycon

    >>> from functools import partial
    >>> sse_w = partial(sse, X, y)
    >>> sse_w(np.ones(3)) # try weights [1., 1., 1.]
    12.013621162428603

Now ``sse_w`` is a `partial object`_ which is *callable* and takes a single 
weights parameter. The only potential issue is that the ``__name__`` and 
``__doc__`` attributes are not created automatically, i.e. for function ``sse``
defined earlier, we have

..  code:: pycon

    >>> sse.__name__
    'sse'
    >>> sse.__doc__
    'Sum squared error function'

whereas for the partially applied function ``sse_w``, we get

..  code:: pycon

    >>> sse_w.__name__
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: 'functools.partial' object has no attribute '__name__'
    >>> sse_w.__doc__
    'partial(func, *args, **keywords) - new function with partial application\n    of the given arguments and keywords.\n'

If we don't intend on using ``sse`` by itself later down the track, and don't
need to do anything special with the ``__name__`` and ``__doc__`` of the 
partially applied version, we can simply propagate these properties from the 
original, using the `update_wrapper`_ function.

..  code:: python

    from functools import partial, update_wrapper

    def wrapped_partial(func, *args, **kwargs):
        partial_func = partial(func, *args, **kwargs)
        update_wrapper(partial_func, func)
        return partial_func

Now we get

..  code:: pycon

    >>> sse_w = wrapped_partial(sse, X, y)
    >>> sse_w.__name__
    'sse'
    >>> sse_w.__doc__
    'Sum squared error function'

so that the partially applied function looks more like the original function, 
since it has the metadata of the original, rather than the metadata of 
``partial`` itself, which is less than helpful.

Case Study
----------

An actual example where missing a ``__name__`` is a major issue is when working
with libraries with interfaces that require it. For example, consider 
`autograd`_ - an excellent library for efficiently performing automatic 
differentiation.

We differentiate the ``sse`` function with respect to the weights, the 2nd 
parameter (counting from 0), and get:

..  code:: pycon

    >>> from autograd import grad
    >>> grad(sse, argnum=2)(X, y, np.ones(3))
    array([-3.83312179,  9.40730972,  7.11817447])

Note that we cannot differentiate ``partial(sse, X, y)`` but can differentiate 
``wrapped_partial(sse, X, y)`` with no problem:

..  code:: pycon

    >>> grad(partial(sse, X, y))(np.ones(3))
    Traceback (most recent call last):
        ...
    AttributeError: 'functools.partial' object has no attribute '__name__'
    >>> grad(wrapped_partial(sse, X, y))(np.ones(3))
    array([-3.83312179,  9.40730972,  7.11817447])

In this case, ``autograd`` obviously makes use of the ``__name__`` attribute of
a given function to attach a name and docstring of its own:

..  code:: pycon

    >>> grad(sse, argnum=2).__name__
    'gradient_sse_wrt_argnum_2'
    >>> grad(wrapped_partial(sse, X, y)).__name__
    'gradient_sse_wrt_argnum_0'
    >>> grad(sse, argnum=2).__doc__
    'Gradient of function sse with respect to argument number 2. Has the same arguments as sse but the return value has type ofargument 2'
    >>> grad(wrapped_partial(sse, X, y)).__doc__
    'Gradient of function sse with respect to argument number 0. Has the same arguments as sse but the return value has type ofargument 0'

Finally, we can use a gradient-based optimization method to minimize the ``sse``
with respect to weights ``w``. We use the `L-BFGS-B` method from ``scipy.optimize``
with ``w = [1., 1., 1.]`` as the starting point. We get:

..  code:: pycon
    
    >>> from scipy.optimize import minimize
    >>> res = minimize(sse_w, x0=np.ones(3), method='L-BFGS-B', jac=grad(sse_w))
    >>> res.success
    True
    >>> res.nit
    7
    >>> res.fun
    0.20607947299232429
    >>> res.x
    array([ 2.10921327,  0.37558212, -1.20400518])

We see that the optimization converged successfully in 7 iterations to 
``[ 2.10921327,  0.37558212, -1.20400518]``, which is close to the true weights
``[2., .5, -1.2]``.

Conclusion
----------

By default, partial functions created from ``functools.partial`` do not inherit
the ``__name__`` and ``__doc__`` attributes automatically. If these are 
required for some reason, we can either define them manually, or use the 
``wrapped_partial`` we defined above to propagate these attributes from the 
original function.

Useful Resources
----------------

- https://pymotw.com/2/functools/
- https://docs.python.org/2/library/functools.html

.. _partial: https://docs.python.org/2/library/functools.html#functools.partial
.. _partial object: https://docs.python.org/2/library/functools.html#partial-objects
.. _update_wrapper: https://docs.python.org/2/library/functools.html#functools.update_wrapper
.. _functools: https://docs.python.org/2/library/functools.html
.. _autograd: https://github.com/HIPS/autograd