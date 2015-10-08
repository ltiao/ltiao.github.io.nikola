.. title: Hosting Sphinx documentation on Github Pages
.. slug: hosting-sphinx-documentation-on-github-pages
.. date: 2015-10-08 15:08:19 UTC+11:00
.. tags: github, github pages, sphinx, python, documentation, draft
.. category: python
.. link: 
.. description: 
.. type: text


.. code:: makefile

   # You can set these variables from the command line.
   html:
       $(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
       @echo
       @echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

.. code:: makefile

   SPHINXOPTS    =
   SPHINXBUILD   = sphinx-build
   PAPER         =
   BUILDDIR      = _build

Install `ghp-import`_.

.. code:: console

   $ pip install ghp-import
   $ ghp-import --help
   Usage: ghp-import [OPTIONS] DIRECTORY
   Options:
     -n          Include a .nojekyll file in the branch.
     -m MESG     The commit message to use on the target branch.
     -p          Push the branch to origin/{branch} after committing.
     -r REMOTE   The name of the remote to push to. [origin]
     -b BRANCH   Name of the branch to write to. [gh-pages]
     -h, --help  show this help message and exit

Push after commiting
--------------------

*TODO*

Static files (leading underscores)
----------------------------------

By default, static files are outputted to directories with leading underscores,
e.g. ``_static``. This can be problematic with Github Pages where directories 
with leading underscores are ignored. 

While we could modify Sphinx's default
configuration (e.g. ``html_static_path``), a more straightforward solution is 
to bypass preprocessing on Github Pages to support Sphinx HTML output properly,
as outlined in `Bypassing Jekyll on GitHub Pages`_.

This is made even simpler by the fact that ``ghp-import`` has a ``-n`` flag, 
which will automatically include the necessary file (``.nojekyll``) for us.

.. code:: console

   $ ghp-import -n -p $(BUILDDIR)/html

Updating the Makefile (Optional)
--------------------------------

*TODO*

Resources
---------

- http://sphinx-doc.org/faq.html#using-sphinx-with
- https://help.github.com/articles/creating-project-pages-manually/
- https://daler.github.io/sphinxdoc-test/includeme.html
- http://blog.nikhilism.com/2012/08/automatic-github-pages-generation-from.html


.. _`ghp-import`: https://github.com/davisp/ghp-import
.. _`Bypassing Jekyll on GitHub Pages`: 
   https://github.com/blog/572-bypassing-jekyll-on-github-pages