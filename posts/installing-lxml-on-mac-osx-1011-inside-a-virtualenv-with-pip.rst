.. title: Installing lxml on Mac OSX (10.11) inside a virtualenv with pip
.. slug: installing-lxml-on-mac-osx-1011-inside-a-virtualenv-with-pip
.. date: 2015-12-01 14:04:57 UTC+11:00
.. tags: osx, lxml, python, virtualenv, pip
.. category: coding
.. link: 
.. description: 
.. type: text

The ``lxml`` library is a dependency for many popular Python projects such as 
Scrapy and Nikola. If you are a Mac OSX user, it's highly likely that you have
encountered the following error when trying to install ``lxml`` or its 
dependants with ``pip``:

.. code:: console

   In file included from src/lxml/lxml.etree.c:346:
   $WORKON_HOME/venv_name/build/lxml/src/lxml/includes/etree_defs.h:9:10: fatal error: 'libxml/xmlversion.h' file not found
   #include "libxml/xmlversion.h"
            ^
   1 error generated.
   error: command 'clang' failed with exit status 1

.. TEASER_END

For a long time, the easy fix for this was to simply set the env var 

.. code::

   STATIC_DEPS=true

which makes the ``setup.py`` for ``lxml`` download and build the latest 
versions of ``libxml2`` and ``libxslt`` instead of using the system version, 
as suggested by the official `installation instructions`_ and this 
`StackOverflow answer`_:

.. code:: console

   $ STATIC_DEPS=true pip install lxml 

This was all fine until 20 Nov 2015, when version 2.9.3 of ``libxml2`` was 
`released`_. When installing with the above command, you will encounter an 
exception similar to this:

.. code:: console

   Exception: Command "make -j6" returned code 512

with the compilation error somewhere above in the traceback message:

.. code:: console

   xmlIO.c:1450:52: error: use of undeclared identifier 'LZMA_OK'
       ret =  (__libxml2_xzclose((xzFile) context) == LZMA_OK ) ? 0 : -1;
                                                      ^
     CC       uri.lo
   1 error generated.
   make[2]: *** [xmlIO.lo] Error 1 

This seems to be an error introduced in version 2.9.3. For now, a reasonable
workaround is to install ``lxml`` as before, but explicitly specify the version 
of ``lxml`` to use (version 2.9.2). In `another StackOverflow answer`_, they
manually download ``lxml`` and run ``setup.py`` with flags ``--static-deps``, 
``--libxml2-version`` and ``libxslt-version``. 

Note that we can still use ``pip`` (only version >= 7.0) and 
`propagate the options`_ to ``setup.py`` with ``--install-option``:

.. code:: console

   $ pip install lxml --install-option="--static-deps=true" \
                      --install-option="--libxml2-version=2.9.2"

Alternatively, if you must us an older version of ``pip`` that does not support
passing options, the ``setup.py`` for ``lxml`` is implemented to support 
passing command line options as environment variables (see `setupinfo.py`_). 
This is why we were able to simply set ``STATIC_DEPS=true`` before. 

In the same manner, we can just set ``LIBXML2_VERSION=2.9.2``:

.. code:: console

   $ STATIC_DEPS=true LIBXML2_VERSION=2.9.2 pip install lxml
   Collecting lxml
     Using cached lxml-3.5.0.tar.gz
   Building wheels for collected packages: lxml
     Running setup.py bdist_wheel for lxml
     Stored in directory: [...]
   Successfully built lxml
   Installing collected packages: lxml
   Successfully installed lxml-3.5.0

Now ``lxml`` should be successfully installed:

.. code:: console

   $ python -c 'import lxml'
   $ python -c 'from lxml import etree'

Good luck!

.. _propagate the options: http://pip.readthedocs.org/en/stable/reference/pip_install/#per-requirement-overrides
.. _StackOverflow answer: http://stackoverflow.com/a/19550278/1924843
.. _another StackOverflow answer: http://stackoverflow.com/a/1277421/1924843
.. _installation instructions: http://lxml.de/installation.html#installation
.. _released: http://www.xmlsoft.org/news.html
.. _setupinfo.py: https://github.com/lxml/lxml/blob/42bbfdca8956d607c7bfceed1cc55b9bca48faf8/setupinfo.py#L410
