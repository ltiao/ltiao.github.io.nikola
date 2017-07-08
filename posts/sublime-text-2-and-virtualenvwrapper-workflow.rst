.. title: Sublime Text 2 and Virtualenvwrapper Workflow
.. slug: sublime-text-2-and-virtualenvwrapper-workflow
.. date: 2015-03-27 16:33:03 UTC+11:00
.. tags: sublime text 2, virtualenv, virtualenvwrapper, python, bash, draft
.. category: coding
.. link: 
.. description: 
.. type: text

``Project > Save Project As...``

Add the root of the virtualenv directory to the ``folders`` list

.. code-block:: json

   {
     "path": "$WORKON_HOME/<venv_name>/"
   }

.. code-block:: bash

   export PROJECT_ROOT=/Users/tiao/Dropbox/Projects/ltiao.github.io 

   echo "Changing current working directory to [$PROJECT_ROOT]..."
   cd $PROJECT_ROOT 

   # Start up sublime text project
   echo "Starting up Sublime Text project..."
   subl --project site.sublime-project

   unset PROJECT_ROOT


