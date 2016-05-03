.. title: Setting up a IPython Parallel Cluster on Amazon EC2 with StarCluster
.. slug: setting-up-a-ipython-parallel-cluster-on-amazon-ec2-with-starcluster
.. date: 2016-05-03 22:55:55 UTC+10:00
.. tags: python, ipython, starcluster, distributed computing, amazon aws, amazon ec2, virtualenv, pip
.. category: coding
.. link: 
.. description: 
.. type: text

StarCluster_ is an open source cluster-computing toolkit for Amazon’s Elastic 
Compute Cloud (EC2) that is designed to automate and simplify the process of 
building, configuring, and managing clusters of virtual machines on Amazon’s
EC2 cloud. StarCluster makes it easy to create a cluster computing environment
in the cloud for distributed and parallel computing applications.

.. TEASER_END

..  attention:: Before you venture any further, be aware of the following:

    - At the time of writing (3 May 2016), the last commit (54a61fd_) was made
      on Nov 13 2015, which is *long* time ago in the FOSS world.
    - There is no official Python 3 support, and this is an `open issue`_ from
      Mar 21 2015 - again, a *long* time ago.
    - The version of IPython used to create and manipulate the ``IPython.parallel`` 
      Client_ only works with version 1.1.0 of IPython (from before September 
      23, 2015). At the time of writing, the latest stable version of IPython 
      is 4.2.0. Furthermore ``IPython.parallel`` has since become its own 
      project, ipyparallel_.

    If you are able to circumvent the ramifications of these issues then we
    are ready to proceed.

Getting Started
---------------

First we initialize a ``virtualenv`` for our project with Python 2.7 and install
StarCluster with ``pip``:

..  code:: console

    $ mkvirtualenv starcluster --python=`which python2`
    $ python -V
    Python 2.7.11
    $ pip install starcluster

Create a directory to contain the various configuration files:

..  code:: console

    $ mkdir <starcluster-project>
    $ cd <starcluster-project>

Initialize the StarCluster configuration file:

..  code:: console

    $ starcluster -c <starcluster-project>/starcluster.cfg help
    StarCluster - (http://star.mit.edu/cluster) (v. 0.95.6)
    Software Tools for Academics and Researchers (STAR)
    Please submit bug reports to starcluster@mit.edu

    !!! ERROR - config file <starcluster-project>/starcluster.cfg does not exist

    Options:
    --------
    [1] Show the StarCluster config template
    [2] Write config template to <starcluster-project>/starcluster.cfg
    [q] Quit

    Please enter your selection: 2

Note that without the ``-c`` argument, the configuration file would have been
initialized in the default location, which is ``~/.starcluster/config``. Since
we may want to version control this configuration, we initialize and store 
this file in an alternate location, namely, ``<starcluster-project>/starcluster.cfg``.

We can set the ``STARCLUSTER_CONFIG`` environment variable so we don't have to
provide the full path to the config file everytime we execute a ``starcluster``
subcommand:

..  code:: console

    $ export STARCLUSTER_CONFIG="<starcluster-project>/starcluster.cfg"



.. _StarCluster: http://star.mit.edu/cluster/
.. _54a61fd: https://github.com/jtriley/StarCluster/commit/54a61fd0add8802e61a8c035944389fe2939be23
.. _open issue: https://github.com/jtriley/StarCluster/issues/514
.. _ipyparallel: http://ipyparallel.readthedocs.io/en/latest/
.. _version 1.1.0: http://ipython.org/ipython-doc/1/index.html
.. _Client: http://ipyparallel.readthedocs.io/en/latest/api/ipyparallel.html#ipyparallel.Client