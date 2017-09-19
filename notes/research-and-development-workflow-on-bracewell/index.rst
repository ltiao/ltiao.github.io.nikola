.. title: Research and Development Workflow on Bracewell
.. slug: research-and-development-workflow-on-bracewell
.. date: 2017-09-12 16:07:09 UTC+10:00
.. tags: 
.. category: 
.. link: 
.. description: 
.. type: text

.. youtube:: HTHi_pHI734
   :align: center

- `CSIRO Confluence Landing Page for Bracewell <https://confluence.csiro.au/display/SC/CSIRO+Accelerator+Cluster+-+Bracewell>`_
- `Gizmodo article <https://www.gizmodo.com.au/2017/07/meet-dell-and-csiros-large-scale-artificial-intelligence-computer/>`_

Connecting to Bracewell
-----------------------

CSIRO VPN
#########

Request VPN access. Easily done on-site but can also be done off-site 
(https://security.csiro.au/offsite.php)

You will most likely be redirected to https://vpn.csiro.au/. When you log in, it will attempt to install the "Cisco AnyConnect Secure Mobility Client", and fail.
While you can install this manually, I find the best thing is to install the
open-source alternative, `openconnect <https://wiki.archlinux.org/index.php/OpenConnect>`_:

.. code:: console

    $ pacin openconnect networkmanager-openconnect

You can now initiate VPN connections in the command line console with 
``openconnect``:

.. code:: console

    $ sudo openconnect vpn.csiro.au

The Network Manager package makes it really nice and easy to work with

.. code:: console

    $ pacin networkmanager-openconnect

(you may need to logout and log back in)

SSH
###

.. code:: console

   $ ssh -X ident@bracewell.hpc.csiro.au

You can also use the ``-Y`` flag instead.

- https://confluence.csiro.au/display/SC/Using+SSH+and+hpn-ssh+on+our+Linux+systems

Might be a good idea to set up password-less SSH with public key cryptography.

- https://confluence.csiro.au/display/SC/Passwordless+SSH+and+keys
- https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys--2

Interactive node
################

Use an interactive node for persistence, moderate computing and a well integrated experience. The interactive node for Bracewell is:

    bracewell-i1.hpc.csiro.au

Module environment
------------------

.. code:: console

   $ module avail

.. code:: console

   $ module list
   Currently Loaded Modulefiles:
     1) SC                    3) cuda-driver/current   5) intel-fc/16.0.4.258
     2) slurm/16.05.8         4) intel-cc/16.0.4.258

.. code:: console

   $ module show tensorflow/1.3.0-py35-gpu
   -------------------------------------------------------------------
   /var/apps_bracewell/modules/modulefiles/tensorflow/1.3.0-py35-gpu:   

   prepend-path     PATH /apps/tensorflow/1.3.0-py35-gpu/bin 
   prepend-path     CPATH /apps/tensorflow/1.3.0-py35-gpu/include 
   prepend-path     PKG_CONFIG_PATH /apps/tensorflow/1.3.0-py35-gpu/lib/pkgconfig 
   prepend-path     LD_RUN_PATH /apps/tensorflow/1.3.0-py35-gpu/lib 
   prepend-path     PYTHONPATH /apps/tensorflow/1.3.0-py35-gpu/lib/python3.5/site-packages 
   setenv       TENSORFLOW_HOME /apps/tensorflow/1.3.0-py35-gpu    

   load-module  python/3.6.1
   load-module  cuda/8.0.61
   load-module  cudnn/v6
   -------------------------------------------------------------------

.. code:: console

   $ module load tensorflow/1.3.0-py35-gpu

.. code:: console

   $ module list
   Currently Loaded Modulefiles:
     1) SC                          5) intel-fc/16.0.4.258         9) cudnn/v6
     2) slurm/16.05.8               6) intel-mkl/2017.2.174       10) tensorflow/1.3.0-py35-gpu
     3) cuda-driver/current         7) python/3.6.1
     4) intel-cc/16.0.4.258         8) cuda/8.0.61


Customizing your shell
----------------------

.. code:: console

   $ cd ~
   $ git clone https://github.com/ltiao/dotfiles.git
   $ source bootstrap.sh
   $ rm ~/.hushlogin # I don't want to disable the Bracewell ASCII art login screen

While you're here, you might like to set-up your ``virtualenvwrapper``. Add 
something like the following to your ``bash_profile``:

.. code:: bash 

   module load python/3.6.1
   export WORKON_HOME=$HOME/.virtualenvs
   source $(which virtualenvwrapper_lazy.sh)

Now you can create Python ``virtualenv`` s as usual with 

.. code:: console

   $ mkvirtualenv --system-site-packages <virtual-env-name>


.. note:: Some work still needs to be done to determine how system-wide 
   installed packages are affected when they are upgraded in a ``virtualenv``. 
   For example, I noticed ``Keras==2.0.3`` was install in the system site 
   packages. When I execute ``pip install Keras==2.0.8`` does the ``virtualenv``
   installed version then take precedence and override the system-wide version? 
   I assume this is the case.

- https://confluence.csiro.au/display/SC/virtualenv+and+customising+your+python

Some dependencies for ``zsh`` are missing so you're stuck with Bash.

.. note:: In batch jobs that use bash (i.e. ``sinteractive``) or if the script 
   you run with ``sbatch`` begins with ``#!/bin/bash``, your ``~/.bash_profile`` 
   will be invoked.

Slurm batch system
------------------

Time limits:

  A time limit of zero requests that no time limit be imposed. Acceptable time formats include "minutes", "minutes:seconds", "hours:minutes:seconds", "days-hours", "days-hours:minutes" and "days-hours:minutes:seconds".


Interactive batch shell
#######################

- https://confluence.csiro.au/display/SC/Running+jobs+in+an+interactive+batch+shell

Batch job scripts
#################

- https://confluence.csiro.au/display/SC/Where+can+I+find+some+job+script+examples

.. code:: console

   $ sinteractive -h
   Usage: sinteractive [-n] [-t] [-p] [-J] [-w] [-g]
   Optional arguments:   

       -n: Number of tasks to request (default: 1)
           Consider the number of processes you need to run.   

       -c: Number of CPUs per task to request (default: 1)
           Consider the number of threads each process requires. A combination of
           number of tasks and CPUs per task are typically required for hybrid
           codes (multi-processes and multi-threads).
           Note that MATLAB's parallel processing requires this to be set. e.g.
           -n 1 -c 4 will allow MATLAB's "local" cluster profile to use 4 workers.   

       -t: Wall time to request (default: 2:00:00)   

       -m: Memory to request (no default)   

       -p: Partition to run job in (no default)   

       -J: Job name (default: interactive)   

       -w: Node name (no default)   

       -g: Request a generic resource e.g. gpu:2   

   NB: The command that is actually run is printed first so you can copy it
       and run fancier versions with more salloc and srun options if necessary.   

   e.g.
     sinteractive -n 2 -t 1:00:00 -m 2gb
   
.. code:: console

   tia00c at bracewell-i1 in ~
   $ sinteractive -n 1 -c 1 -m 50mb -g gpu:1 -t 00:00:30
   running: salloc --ntasks-per-node 1 --cpus-per-task=1 --mem 50mb -J interactive -t 00:00:30 --gres gpu:1 srun --pty /bin/bash -l
   salloc: Granted job allocation 8186661
   srun: Job step created   

   tia00c at b043 in ~
   $ 

- https://confluence.csiro.au/display/SC/Requesting+resources+in+Slurm
- https://confluence.csiro.au/display/SC/Accessing+Accelerator+resources+on+the+Bracewell+cluster

Storage and persistence
-----------------------

Bracewell landing page

- https://confluence.csiro.au/display/SC/SC+filesystem+conventions
- https://confluence.csiro.au/display/SC/Data+Handling

Transferring and synchonizing files
-----------------------------------

Nautilus

- https://confluence.csiro.au/display/SC/File+Transfer
- https://confluence.csiro.au/display/SC/rsync

GUI Applications
----------------



- https://confluence.csiro.au/display/SC/Using+a+GUI+display+in+a+batch+job

Jupyter Notebooks 
-----------------

- https://confluence.csiro.au/display/SC/Using+IPython+Notebooks
- https://confluence.csiro.au/display/SC/Using+the+SC+Launcher
