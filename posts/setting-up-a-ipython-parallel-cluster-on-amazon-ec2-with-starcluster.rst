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

AWS Credentials and Connection Settings
---------------------------------------

..  code:: console

    $ starcluster -c ./starcluster.cfg createkey starcluster -o ~/.ssh/starcluster.rsa
    $ starcluster -c ./starcluster.cfg listkeypairs

..  code:: diff

    --- default.cfg 2016-05-04 15:16:18.000000000 +1000
    +++ starcluster.cfg 2016-05-02 19:29:47.000000000 +1000
    @@ -22,15 +22,15 @@
     # This is the AWS credentials section (required).
     # These settings apply to all clusters
     # replace these with your AWS keys
    -AWS_ACCESS_KEY_ID = #your_aws_access_key_id
    -AWS_SECRET_ACCESS_KEY = #your_secret_access_key
    +AWS_ACCESS_KEY_ID = #your_aws_access_key_id
    +AWS_SECRET_ACCESS_KEY = #your_secret_access_key
     # replace this with your account number
    -AWS_USER_ID= #your userid
    +AWS_USER_ID= #your userid
     # Uncomment to specify a different Amazon AWS region  (OPTIONAL)
     # (defaults to us-east-1 if not specified)
     # NOTE: AMIs have to be migrated!
    -#AWS_REGION_NAME = eu-west-1
    -#AWS_REGION_HOST = ec2.eu-west-1.amazonaws.com
    +AWS_REGION_NAME = ap-southeast-2
    +AWS_REGION_HOST = ec2.ap-southeast-2.amazonaws.com
     # Uncomment these settings when creating an instance-store (S3) AMI (OPTIONAL)
     #EC2_CERT = /path/to/your/cert-asdf0as9df092039asdfi02089.pem
     #EC2_PRIVATE_KEY = /path/to/your/pk-asdfasd890f200909.pem
    @@ -46,8 +46,8 @@
     # Sections starting with "key" define your keypairs. See "starcluster createkey
     # --help" for instructions on how to create a new keypair. Section name should
     # match your key name e.g.:
    -[key mykey]
    -KEY_LOCATION=~/.ssh/mykey.rsa
    +[key starcluster]
    +KEY_LOCATION=~/.ssh/starcluster.rsa

     # You can of course have multiple keypair sections
     # [key myotherkey]
    @@ -72,9 +72,9 @@

     [cluster smallcluster]
     # change this to the name of one of the keypair sections defined above
    -KEYNAME = mykey
    +KEYNAME = starcluster
     # number of ec2 instances to launch
    -CLUSTER_SIZE = 2
    +CLUSTER_SIZE = 5
     # create the following user on the cluster
     CLUSTER_USER = sgeadmin
     # optionally specify shell (defaults to bash)
    @@ -90,7 +90,7 @@
     # The base i386 StarCluster AMI is ami-9bf9c9f2
     # The base x86_64 StarCluster AMI is ami-3393a45a
     # The base HVM StarCluster AMI is ami-6b211202
    -NODE_IMAGE_ID = ami-3393a45a
    +NODE_IMAGE_ID = ami-e3841ad9
     # instance type for all cluster nodes
     # (options: m3.large, c3.8xlarge, i2.8xlarge, t2.micro, hs1.8xlarge, c1.xlarge, r3.4xlarge, g2.2xlarge, m1.small, c1.medium, m3.2xlarge, c3.2xlarge, m2.xlarge, m2.2xlarge, t2.small, r3.2xlarge, t1.micro, cr1.8xlarge, r3.8xlarge, cc1.4xlarge, m1.medium, r3.large, c3.xlarge, i2.xlarge, m3.medium, cc2.8xlarge, m1.large, cg1.4xlarge, i2.2xlarge, c3.large, i2.4xlarge, c3.4xlarge, r3.xlarge, t2.medium, hi1.4xlarge, m2.4xlarge, m1.xlarge, m3.xlarge)
     NODE_INSTANCE_TYPE = m1.small
    @@ -122,7 +122,7 @@
     #VOLUMES = oceandata, biodata
     # list of plugins to load after StarCluster's default setup routines (OPTIONAL)
     # see "Configuring StarCluster Plugins" below on how to define plugin sections
    -#PLUGINS = myplugin, myplugin2
    +PLUGINS = ipcluster
     # list of permissions (or firewall rules) to apply to the cluster's security
     # group (OPTIONAL).
     #PERMISSIONS = ssh, http
    @@ -285,8 +285,8 @@
     # The IPCluster plugin configures a parallel IPython cluster with optional
     # web notebook support. This allows you to run Python code in parallel with low
     # latency message passing via ZeroMQ.
    -# [plugin ipcluster]
    -# SETUP_CLASS = starcluster.plugins.ipcluster.IPCluster
    +[plugin ipcluster]
    +SETUP_CLASS = starcluster.plugins.ipcluster.IPCluster
     # # Enable the IPython notebook server (optional)
     # ENABLE_NOTEBOOK = True
     # # Set a password for the notebook for increased security
    @@ -294,9 +294,9 @@
     # NOTEBOOK_PASSWD = a-secret-password
     # # Set a custom directory for storing/loading notebooks (optional)
     # NOTEBOOK_DIRECTORY = /path/to/notebook/dir
    -# # Set a custom packer. Must be one of 'json', 'pickle', or 'msgpack'
    -# # This is optional.
    -# PACKER = pickle
    +# Set a custom packer. Must be one of 'json', 'pickle', or 'msgpack'
    +# This is optional.
    +PACKER = json
     #
     # Use this plugin to create a cluster SSH "dashboard" using tmux. The plugin
     # creates a tmux session on the master node that automatically connects to all


.. _StarCluster: http://star.mit.edu/cluster/
.. _54a61fd: https://github.com/jtriley/StarCluster/commit/54a61fd0add8802e61a8c035944389fe2939be23
.. _open issue: https://github.com/jtriley/StarCluster/issues/514
.. _ipyparallel: http://ipyparallel.readthedocs.io/en/latest/
.. _version 1.1.0: http://ipython.org/ipython-doc/1/index.html
.. _Client: http://ipyparallel.readthedocs.io/en/latest/api/ipyparallel.html#ipyparallel.Client