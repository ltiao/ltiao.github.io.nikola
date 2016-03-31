.. title: Installing Cartopy on Mac OSX (10.11)
.. slug: installing-cartopy-on-mac-osx-1011
.. date: 2016-03-31 23:33:50 UTC+11:00
.. tags: cartopy, cython, numpy, geos, proj.4,  
.. category: coding
.. link: 
.. description: 
.. type: text

So you develop on Mac OS X (10.11) and have installed the external 
dependencies (geos_ 3.5.0, proj_ 4.9.2) of Cartopy_ with Homebrew_:

..  code:: console

    $ brew install geos
    $ brew install proj

.. TEASER_END

Moreover, you have created a ``virtualenv`` and installed the Python 
dependencies (Cython, NumPy):

..  code:: console

    $ mkvirtualenv cartopy_venv
    (cartopy_venv)$ pip install cython
    (cartopy_venv)$ pip install numpy

Yet, when you finally go install Cartopy, you still encounter the following 
seemingly inexplicable error: 

..  code:: console

    (cartopy_venv)$ pip install cartopy
    [...]
    clang -fno-strict-aliasing -fno-common -dynamic -isysroot /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.11.sdk -I/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.11.sdk/System/Library/Frameworks/Tk.framework/Versions/8.5/Headers -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -I/usr/local/Cellar/python/2.7.11/Frameworks/Python.framework/Versions/2.7/include -I./lib/cartopy -I-I/usr/local/Cellar/proj/4.9.2/include -I/usr/local/Cellar/geos/3.5.0/include -I/usr/local/Cellar/python/2.7.11/Frameworks/Python.framework/Versions/2.7/include/python2.7 -c lib/cartopy/trace.cpp -o build/temp.macosx-10.11-x86_64-2.7/lib/cartopy/trace.o
    lib/cartopy/trace.cpp:249:10: fatal error: 'proj_api.h' file not found
    #include "proj_api.h"
             ^
    1 error generated.
    error: command 'clang' failed with exit status 1

    ----------------------------------------

despite the fact that ``proj_api.h`` does in fact exist:

..  code:: console

    $ ls /usr/local/Cellar/proj/4.9.2/include | grep proj_api.h
    proj_api.h

It turns out this is a bug in the ``setup.py`` script for Cartopy that 
prepends an extraneous ``-I`` to the include directory containing 
``proj_api.h`` (in the error message above one can see that the call to 
``clang`` has ``-I-I/usr/local/Cellar/proj/4.9.2/include`` as one of its flags)
so ``clang`` ends up not being able to see it at all. 

This bug is discussed at length and fixed in my `pull request`_, which has since
been merged. 

The Workaround
--------------

Until the next release, the temporary workaround is to use the bleeding-edge 
version (*not recommended*):

..  code:: console

    (cartopy_venv)$ pip install git+https://github.com/SciTools/cartopy.git@master#egg=cartopy
    Collecting cartopy from git+https://github.com/SciTools/cartopy.git@master#egg=cartopy
        [...]
    Installing collected packages: cartopy
      Running setup.py install for cartopy ... done
    Successfully installed cartopy-0.14.0

Or alternatively, pass the ``build_ext`` subcommand and its options to 
``setup.py`` via the `--global-option flag`_ in ``pip`` (*highly recommended*):

..  code:: console

    (cartopy_venv)$ pip install --global-option=build_ext --global-option=$(pkg-config --cflags proj) cartopy
    [...]
    Installing collected packages: cartopy
      Running setup.py install for cartopy ... done
    Successfully installed cartopy-0.13.0

And that's pretty much it :)

.. _Homebrew: http://brew.sh/
.. _Cartopy: http://scitools.org.uk/cartopy/
.. _geos: https://trac.osgeo.org/geos/
.. _proj: https://trac.osgeo.org/proj/
.. _pull request: https://github.com/SciTools/cartopy/pull/747
.. _`--global-option flag`: https://pip.pypa.io/en/stable/reference/pip_install/#cmdoption--global-option