.. title: Using the Matplotlib plot directive in Nikola
.. slug: using-the-matplotlib-plot-directive-in-nikola
.. date: 2016-02-02 22:58:11 UTC+11:00
.. tags: nikola, matplotlib
.. category: coding
.. link: 
.. description: 
.. type: text

.. code:: console

   $ nikola plugin --install pyplots

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


- http://matplotlib.org/1.5.1/devel/documenting_mpl.html?highlight=directive#module-matplotlib.sphinxext.plot_directive
- https://plugins.getnikola.com/#pyplots
