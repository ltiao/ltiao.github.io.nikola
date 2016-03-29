.. title: Workflow for keeping Nikola config file updated
.. slug: workflow-for-keeping-nikola-config-file-updated
.. date: 2016-03-29 11:13:12 UTC+11:00
.. tags: nikola, python, meld, pip
.. category: coding 
.. link: 
.. description: 
.. type: text

For most, keeping Nikola up-to-date is usually a simple matter of running 
something like:

.. code:: console

   $ pip install --upgrade nikola

The same goes for its dependencies. However, one important thing that can get 
overlooked is the Nikola configuration file for your site (the ``conf.py`` file
sitting at the root of your Nikola site directory), which is almost always 
updated with each major Nikola release.

.. TEASER_END

There is no sound way to keep this updated automatically, since what you're
trying to do is a essentially "rebase_" your version of ``conf.py`` onto the 
version that is generated for new Nikola sites with the latest version of 
Nikola.

The way I address this is:

1. Update Nikola to the latest version (command above)
2. Initialize a new Nikola site:

   .. code:: console

      $ mkdir temp_site
      $ nikola init

3. Merge updates from the newly generated ``conf.py`` with your favourite merge
   tool. I usually use meld_

   .. code:: console

      $ meld temp_site/conf.py real_site/conf.py

4. Remove new temporary Nikola site

   .. code:: console

      $ rm -r temp_site

And that's pretty much all there is to it.

.. _rebase: https://git-scm.com/book/en/v2/Git-Branching-Rebasing
.. _meld: http://meldmerge.org/
