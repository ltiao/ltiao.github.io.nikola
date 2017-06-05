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

    If you fully understand these issues and their implications, then proceed.

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

    >>> Config template written to <starcluster-project>/starcluster.cfg
    >>> Please customize the config template

Note that without the ``-c`` argument, the configuration file would have been
initialized in the default location, which is ``~/.starcluster/config``. Since
we may want to version control this configuration, we initialize and store 
this file in an alternate location, namely, ``<starcluster-project>/starcluster.cfg``.

Now that this file has been created, we can execute the previous command without
errors:

..  code:: console

    $ starcluster -c <starcluster-project>/starcluster.cfg help
    StarCluster - (http://star.mit.edu/cluster) (v. 0.95.6)
    Software Tools for Academics and Researchers (STAR)
    Please submit bug reports to starcluster@mit.edu

    Usage: StarCluster Command Line Interface:

    starcluster [global-opts] action [action-opts] [<action-args> ...]

    Available Commands:
    -------------------
    NOTE: Pass --help to any command for a list of its options and detailed usage information

    - start: Start a new cluster
    - stop: Stop a running EBS-backed cluster
    - terminate: Terminate a running or stopped cluster
    [...]

We can set the ``STARCLUSTER_CONFIG`` environment variable so we don't have to
provide the full path to the config file everytime we execute a ``starcluster``
subcommand:

..  code:: console

    $ export STARCLUSTER_CONFIG="<starcluster-project>/starcluster.cfg"

Now we can simply run ``starcluster help`` and get the same output as before.

For further information, see `Creating the configuration file`_

AWS Credentials and Connection Settings
---------------------------------------

Next fill in your AWS credentials and connection settings under the ``[aws info]``
section. 

You can (kind of) generate this with the `AWS Command Line Interface`_, by 
creating a named profile with the name ``aws info``:

..  code:: console

    $ aws configure --profile='aws info'
    AWS Access Key ID [None]: ###
    AWS Secret Access Key [None]: ###
    Default region name [None]: 
    Default output format [None]: 
    $ cat ~/.aws/credentials
    [aws info]
    aws_access_key_id = ###
    aws_secret_access_key = ###

You just need to include these credentials in the global config file (``starcluster.cfg`` 
in this tutorial):

..  code:: ini

    [global]
    include = ~/.aws/credentials

The full list of Regions and Endpoints can be found at 
http://docs.aws.amazon.com/general/latest/gr/rande.html#ec2_region, and 
information on how to determine your Account ID can be found at
http://docs.aws.amazon.com/general/latest/gr/acct-identifiers.html.

For further information, see `Amazon Web Services Credentials`_.

Amazon EC2 Keypairs
-------------------

The next step is to fill in your keypair information. If you don’t already 
have a keypair you can create one directly with StarCluster:

..  code:: console

    $ starcluster -c ./starcluster.cfg createkey starcluster -o ~/.ssh/starcluster.rsa

You should be able to see the keypair you just created, and any other existing
ones on Amazon EC2:

..  code:: console

    $ starcluster -c ./starcluster.cfg listkeypairs

You must define this key the the location of the private key in the config (``starcluster.cfg``):

..  code:: ini

    [key starcluster]
    KEY_LOCATION=~/.ssh/starcluster.rsa

For more information, see `Amazon EC2 Keypairs`_.

Defining Cluster Templates
--------------------------

Now you just need to define your cluster templates. The default settings are
quite reasonable. You can find a description of every setting at 
http://star.mit.edu/cluster/docs/latest/manual/configuration.html#cluster-settings.

The only change you are required to make is to specifying the keypair we just created
to be used by the cluster.

..  code:: console

    [cluster smallcluster]
    # change this to the name of one of the keypair sections defined above
    KEYNAME = starcluster

Depending on the AWS region you specified, you may need to modify the AMI Image
ID, as not all AMIs are available in all across all regions. You can use the 
``listpublic`` subcommand to see the list of available AMIs. Here we list all
available AMIs for the ``ap-southeast-2`` region:

..  code:: console

    $ starcluster listpublic
    StarCluster - (http://star.mit.edu/cluster) (v. 0.95.6)
    Software Tools for Academics and Researchers (STAR)
    Please submit bug reports to starcluster@mit.edu

    >>> Listing all public StarCluster images...

    32bit Images:
    -------------
    [0] ami-d58719ef ap-southeast-2 starcluster-base-ubuntu-13.04-x86 (EBS)
    [1] ami-1adf4f20 ap-southeast-2 starcluster-base-ubuntu-12.04-x86 (EBS)

    64bit Images:
    --------------
    [0] ami-cd841af7 ap-southeast-2 starcluster-base-ubuntu-13.04-x86_64-hvm (HVM-EBS)
    [1] ami-e3841ad9 ap-southeast-2 starcluster-base-ubuntu-13.04-x86_64 (EBS)
    [2] ami-18df4f22 ap-southeast-2 starcluster-base-ubuntu-12.04-x86_64 (EBS)

    total images: 5

Note that you can have multiple cluster templates, and are able to inherit 
settings existing templates. For more information, see `Defining Multiple Cluster Templates`_.

Enable the IPython Cluster Plugin
---------------------------------

Finally, you must define settings for the built-in ``ipcluster`` plugin:

..  code:: ini

    # The IPCluster plugin configures a parallel IPython cluster with optional
    # web notebook support. This allows you to run Python code in parallel with low
    # latency message passing via ZeroMQ.
    [plugin ipcluster]
    SETUP_CLASS = starcluster.plugins.ipcluster.IPCluster
    # Set a custom packer. Must be one of 'json', 'pickle', or 'msgpack'
    # This is optional.
    PACKER = json

We don't enable the IPython Notebook here, although this is quite straight-forward,
and instructions can be found at http://star.mit.edu/cluster/docs/latest/plugins/ipython.html#using-the-ipython-html-notebook.

Lastly, you need to add ``ipcluster`` to the list of plugins to be loaded after 
StarCluster's default setup routines

..  code:: diff

    [cluster smallcluster]
    plugins = ipcluster

Starting the Cluster
--------------------

Now we are finally ready to start the cluster:

..  code:: console

    $ starcluster start mycluster

This will take about 5-10 minutes. Once the cluster has successfully started, 
you should first SSH into the master node as the ``CLUSTER_USER`` (by default 
this is ``sgeadmin``). This is important as this will add the master node to
the list of know hosts, which is required for the subsequent commands to work.

..  code:: console

    $ starcluster sshmaster mycluster -u sgeadmin
    $ ipython # now you should be able to create a parallel client
    [~]> from IPython.parallel import Client
    [~]> rc = Client()
    [~]> view = rc[:]
    [~]> results = view.map_async(lambda x: x**30, range(8))
    [~]> print results.get()
    [0,
     1,
     1073741824,
     205891132094649L,
     1152921504606846976L,
     931322574615478515625L,
     221073919720733357899776L,
     22539340290692258087863249L]

You can now create a parallel client on your local machine that connects to and
leverages the remote cluster. When you run ``starcluster start mycluster``, it
generates and stores a JSON file containing the client's connection information
in ``~/.starcluster/ipcluster/``, with the name ``<cluster>-<region>.json'``

..  code:: console

    $ ipython
    [~]> from IPython.parallel import Client
    [~]> rc = Client('~/.starcluster/ipcluster/<cluster>-<region>.json'
                     sshkey='~/.ssh/starcluster.rsa')

See https://ipython.org/ipython-doc/2/parallel/parallel_intro.html for an 
introduction to using IPython Parallel.

You should also be able to use the IPython Parallel cluster with the 
``--ipcluster`` option:

..  code:: console

    $ starcluster shell --ipcluster=mycluster

The expected behavior is described below (taken from http://star.mit.edu/cluster/docs/latest/plugins/ipython.html#connecting-from-your-local-ipython-installation): 

    This will start StarCluster’s development shell and configure a remote parallel 
    session for you automatically. StarCluster will create a parallel client in a 
    variable named ipclient and a corresponding view of the entire cluster in a 
    variable named ipview which you can use to run parallel tasks on the remote cluster:

    ..  code:: console

        $ starcluster shell --ipcluster=mycluster
        [~]> ipclient.ids
        [0, 1, 2, 3]
        [~]> res = ipview.map_async(lambda x: x**30, range(8))
        [~]> print res.get()
        [0,
         1,
         1073741824,
         205891132094649L,
         1152921504606846976L,
         931322574615478515625L,
         221073919720733357899776L,
         22539340290692258087863249L]

However, at the time of writing, this feature appears to be broken.

Tearing Down the Cluster
------------------------

Once you are done with the cluster, remember to tear it down so you don't incur
unnecessary costs:

..  code:: console
    
    $ starcluster terminate mycluster

For help or further information, refer to the `official StarCluster documentation`_.

Best of Luck!

.. _official StarCluster documentation: http://star.mit.edu/cluster/docs/latest/index.html
.. _StarCluster: http://star.mit.edu/cluster/
.. _54a61fd: https://github.com/jtriley/StarCluster/commit/54a61fd0add8802e61a8c035944389fe2939be23
.. _open issue: https://github.com/jtriley/StarCluster/issues/514
.. _ipyparallel: http://ipyparallel.readthedocs.io/en/latest/
.. _version 1.1.0: http://ipython.org/ipython-doc/1/index.html
.. _Client: http://ipyparallel.readthedocs.io/en/latest/api/ipyparallel.html#ipyparallel.Client
.. _AWS Command Line Interface: https://aws.amazon.com/cli/
.. _Amazon Web Services Credentials: http://star.mit.edu/cluster/docs/latest/manual/configuration.html#amazon-web-services-credentials
.. _Creating the configuration file: http://star.mit.edu/cluster/docs/latest/manual/configuration.html#creating-the-configuration-file
.. _Amazon EC2 Keypairs: http://star.mit.edu/cluster/docs/latest/manual/configuration.html#amazon-ec2-keypairs
.. _Defining Multiple Cluster Templates: http://star.mit.edu/cluster/docs/latest/manual/configuration.html#defining-multiple-cluster-templates