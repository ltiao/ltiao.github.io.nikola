.. title: Installing NLopt with Python support on Mac OS X (10.10)
.. slug: installing-nlopt-with-python-support-on-mac-os-x-1010
.. date: 2015-07-17 15:39:17 UTC+10:00
.. tags: NLopt, python, python3, optimization, homebrew, virtualenv
.. category: coding
.. link: 
.. description: 
.. type: text

`NLopt`_ is a popular open-source library for nonlinear optimization. It can be 
somewhat tricky to install it with Python support on Mac OS X, especially 
isolated under a virtual environment. This article outlines the different ways 
of making NLopt play nicely with your Python development environment, whatever 
that may be.

Homebrew
========

As usual, the easiest way of installing any package on a Mac is using the 
popular third-party package manager, `Homebrew`_. This option is perfectly
fine if you only need to bind NLopt to your default Python installation, i.e.
not an alternative version of Python that in a virtual environment.

.. code:: console

   $ brew install nlopt --with-python

If the version of Python you are currently running was installed with Homebrew 
(i.e. according to http://docs.python-guide.org/en/latest/starting/install/osx/), 
you should find the Python bindings for NLopt created in the ``site-packages``
directory (looks something like ``/usr/local/lib/python2.7/site-packages/nlopt.py``.)

At this point, you should be able to just import NLopt with no problems.

.. code:: console

   $ python -c 'import nlopt'
   $

Inside a virtual environment
============================

If you've gotten up to this section of this post, I probably don't need to 
explain the benefits of installing NLOpt inside a virtual environment.

First, I assume you have created a virtual environment, say ``my_env`` with 
Python 3.4 as the Python interpreter [#]_. I am using the excellent 
`virtualenvwrapper`_ extension here by Doug Hellmann, though this is not 
strictly required (but highly recommended!)

.. code:: console

   $ mkvirtualenv --python=`which python3` my_env

Before moving on, we need to first install ``numpy``

.. code:: console

   (my_env)$ pip install numpy
   
Next, `download NLOpt`_ and extract it. At the time of writing, the latest 
stable version is 2.4.2. Now we can configure and install it to our virtual
environment:

.. code:: console

   $ ./configure PYTHON=$WORKON_HOME/my_env/bin/python --prefix=$WORKON_HOME/my_env --enable-shared
   $ make
   $ make install

Note that ``WORKON_HOME`` is an environment variable required to be set by 
``virtualenvwrapper``, usually to something like ``$HOME/.virtualenvs``. If 
you're not using ``virtualenvwrapper``, simply replace ``$WORKON_HOME`` above 
with the path to the directory containing your virtual environment directory.

For further information on what these additional flags are, and why they are 
required, please see `NLOpt installation`_.

Now you should be able to import NLOpt within the ``my_env`` virtual 
environment, which was installed locally to ``$WORKON_HOME/my_env``, rather 
than to ``/usr/local``.

.. code:: console

   (my_env)$ python -c 'import nlopt'
   (my_env)$

.. [#] The steps outlined below doesn't seem to work for virtual environments 
   with Python 2.7 as the Python interpreter. If you have managed to get to to 
   work for Python 2.7, I'd love to learn how you did it!

.. _download NLOpt: http://ab-initio.mit.edu/wiki/index.php/NLopt#Download_and_installation
.. _NLOpt installation: http://ab-initio.mit.edu/wiki/index.php/NLopt_Installation
.. _virtualenvwrapper: https://virtualenvwrapper.readthedocs.org/en/latest/
.. _NLopt: http://ab-initio.mit.edu/wiki/index.php/NLopt
.. _Homebrew: http://brew.sh
