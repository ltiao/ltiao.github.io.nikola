.. title: Installing NLopt with Python bindings inside a virtualenv on Travis CI
.. slug: installing-nlopt-with-python-bindings-inside-a-virtualenv-on-travis-ci
.. date: 2015-12-17 10:52:05 UTC+11:00
.. tags: travis ci, python, nlopt, ubuntu, virtualenv
.. category: coding
.. link: 
.. description: 
.. type: text

In a previous post, I discussed ways of :doc:`installing-nlopt-with-python-support-on-mac-os-x-1010`.
Recently, I have been incorporating `Travis CI`_ in all of my projects, and 
have encountered a similar problem with installing NLopt in a Travis CI build.

For Python builds, `Travis uses separate virtualenv instances`_ for each Python 
version:

    CI Environment uses separate virtualenv instances for each Python version. 
    System Python is not used and should not be relied on. If you need to 
    install Python packages, do it via ``pip`` and not ``apt``.

    If you decide to use apt anyway, note that Python system packages only 
    include Python 2.7 libraries on Ubuntu 12.04 LTS. This means that the 
    packages installed from the repositories are not available in other 
    virtualenvs even if you use the ``–system-site-packages`` option.

.. TEASER_END

Therefore, installing NLopt (and its dependencies) with ``apt`` is very 
problematic. First of all, it will only work for Python 2.7. Second, the 
packages ``libnlopt0`` and ``python-nlopt`` are only available/whitelisted on
Ubuntu 14.04 Trusty. Finally, ``python-numpy`` is a dependency of 
``python-nlopt`` and will automatically be installed.

On all versions except ``pypy`` and ``pypy3`` have ``numpy`` as well.
https://docs.travis-ci.com/user/ci-environment/#Preinstalled-pip-packages

The most straightforward solution is to manually install NLopt inside the
``virtualenv``

https://github.com/travis-ci/travis-ci/issues/4260

.. code:: yaml

   language: python

   python:
     - "2.7"
     - "3.4"   

   before_install:
     - wget http://ab-initio.mit.edu/nlopt/nlopt-2.4.2.tar.gz
     - tar -xvf nlopt-2.4.2.tar.gz
     - cd nlopt-2.4.2   

   install:
     - PYTHON=$(which python) ./configure --prefix=$(dirname $(dirname $(which python))) --enable-shared
     - make
     - make install   

   script:
     - python -c 'import nlopt'   

.. _Travis CI: https://travis-ci.org/
.. _Travis uses separate virtualenv instances: https://docs.travis-ci.com/user/languages/python#Travis-CI-Uses-Isolated-virtualenvs