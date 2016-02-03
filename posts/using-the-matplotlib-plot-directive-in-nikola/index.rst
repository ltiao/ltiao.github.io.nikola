.. title: Using the Matplotlib plot directive in Nikola
.. slug: using-the-matplotlib-plot-directive-in-nikola
.. date: 2016-02-02 22:58:11 UTC+11:00
.. tags: nikola, matplotlib
.. category: coding
.. link: 
.. description: 
.. type: text

Matplotlib's `plot directive`_ is an immensely useful `Sphinx extension`_ for 
easily embedding plots within your documentation. It allows you to include 
source code for generating a matplotlib plot, either inline or by providing 
the path to a source file. By default, the HTML documentation that is 
generated will display a PNG of the plot, and also provide links to the source
code for generating the plot, a high-resolution PNG, and also a vector graphic
(PDF).

In this article, we try out the Nikola plugin pyplots_, which is a (lite) 
implementation of the matplotlib's ``plot`` directive. 

First, we install the plugin:

.. code:: console

   $ nikola plugin --install pyplots

This will also install matplotlib and any dependencies. Now let's try out
a `3D surface plot example`_:

..  code:: python

    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm
    from matplotlib.ticker import LinearLocator, FormatStrFormatter

    import matplotlib.pyplot as plt
    import numpy as np

    fig = plt.figure()
    ax = plt.axes(projection='3d')

    X = np.arange(-5, 5, 0.25)
    Y = np.arange(-5, 5, 0.25)
    X, Y = np.meshgrid(X, Y)
    R = np.sqrt(X**2 + Y**2)
    Z = np.sin(R)
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)
    ax.set_zlim(-1.01, 1.01)

    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    fig.colorbar(surf, shrink=0.5, aspect=5)

..  plot::

    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm
    from matplotlib.ticker import LinearLocator, FormatStrFormatter
    
    import matplotlib.pyplot as plt
    import numpy as np

    fig = plt.figure()
    ax = plt.axes(projection='3d')

    X = np.arange(-5, 5, 0.25)
    Y = np.arange(-5, 5, 0.25)
    X, Y = np.meshgrid(X, Y)
    R = np.sqrt(X**2 + Y**2)
    Z = np.sin(R)
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)
    ax.set_zlim(-1.01, 1.01)

    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    fig.colorbar(surf, shrink=0.5, aspect=5)

.. warning::
   
   While the SVG is generated with no issues with ``nikola build`` and with
   ``nikola auto``, it appears that the ``nikola github_deploy`` command 
   actually deletes the generated SVG from the output directory before 
   committing and pushing. I supposed this is pretty useless if only I can see 
   the plot with ``nikola serve`` or ``nikola auto``...

Unlike the `plot directive`_, which is highly flexible, this plugin does not
support any configuration options whatsoever. This means that useful options 
such as ``include-source``, which displays the source inline, is not supported. 
Furthermore, the plugin offers no alternative solution for providing this 
functionality.

Another difference, which could argued to be a strength rather than a 
shortcoming, is that it only outputs SVG. Compared to the multitude of output 
formats that the matplotlib Sphinx extension provides, it does leave 
much to be desired. While this is not a deal-breaker, it certainly highlights 
important differences between the behavior of this plugin and the matplotlib 
Sphinx extension it is supposed to implement.

.. _plot directive: http://matplotlib.org/1.5.1/devel/documenting_mpl.html?highlight=directive#module-matplotlib.sphinxext.plot_directive
.. _Sphinx extension: http://www.sphinx-doc.org/en/stable/extensions.html
.. _pyplots: https://plugins.getnikola.com/#pyplots
.. _3D surface plot example: http://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html#surface-plots
