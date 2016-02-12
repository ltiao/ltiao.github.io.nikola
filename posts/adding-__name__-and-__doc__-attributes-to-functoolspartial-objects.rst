.. title: Adding __name__ and __doc__ attributes to functools.partial objects
.. slug: adding-__name__-and-__doc__-attributes-to-functoolspartial-objects
.. date: 2016-02-08 14:42:56 UTC+11:00
.. tags: 
.. category: 
.. link: 
.. description: 
.. type: text

..  code:: python

    def sse(X, y, w):
        """Sum squared error function"""  
        z = X.dot(w) - y
        return .5 * z.T.dot(z)

..  code:: python

    from functools import partial, update_wrapper

    def wrapped_partial(func, *args, **kwargs):
        partial_func = partial(func, *args, **kwargs)
        update_wrapper(partial_func, func)
        return partial_func

- https://pymotw.com/2/functools/
- https://docs.python.org/2/library/functools.html

