.. title: Installing NLopt with Python support on Mac OS X (10.10)
.. slug: installing-nlopt-with-python-support-on-mac-os-x-1010
.. date: 2015-07-17 15:39:17 UTC+10:00
.. tags: NLopt, python, python3, optimization, homebrew, draft
.. category: coding
.. link: 
.. description: 
.. type: text

`NLopt`_ is a popular open-source library for nonlinear optimization. It can
be somewhat tricky to install it Python support on Mac OS X, especially with
``virtualenv`` and Python 3. This article outlines the different ways of making
NLopt play nicely with your Python development environment, whatever that may
be.

The path of least resistence: Homebrew
======================================

As usual, the easiest way of installing any package on a Mac is using the 
popular third-party package manager, `Homebrew`_. This option is perfectly
fine if you only need to bind NLopt to your default Python installation, i.e.
not an alternative version of Python that lives inside a ``virtualenv``.

.. code:: console

   $ brew install nlopt --with-python

If the version of Python you are currently running was installed with Homebrew 
(i.e. according to http://docs.python-guide.org/en/latest/starting/install/osx/), 
you should find the Python bindings for NLopt created in the ``site-packages``
directory (looks something like ``/usr/local/lib/python2.7/site-packages/``.)

At this point, you should be able to just import NLopt with no problems.

.. code:: console

   $ python -c 'import nlopt'
   $

Inside a virtual environment
============================

.. code:: console

   $ mkvirtualenv --python=`which python3` test
   $ pip install numpy
   
   $ ./configure PYTHON=$WORKON_HOME/test/bin/python --prefix=$WORKON_HOME/test --enable-shared
   $ make
   $ make install
   $ python -c 'import nlopt'
   $

.. _NLopt: http://ab-initio.mit.edu/wiki/index.php/NLopt
.. _Homebrew: http://brew.sh
