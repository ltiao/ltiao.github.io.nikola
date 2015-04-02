.. title: Generating PDFs from Pelican Articles
.. slug: generating-pdfs-from-pelican-articles
.. date: 2015-04-02 00:37:26 UTC+11:00
.. tags: python, pelican, pdf, synopsis
.. category: coding
.. link: 
.. description: 
.. type: text

As of mid-2013, Pelican still advertised PDF generation of articles/pages 
as one of its `features`_. However, the `change log`_ indicates that this 
is no longer a core feature and has since become a Pelican plugin as of 
version 3.3.0 (2013-09-24), see `issue`_ for further discussion. Therefore, it was 
rather confounding to find the setting ``PDF_GENERATOR`` to be listed in the 
`examples settings`_ of version 3.5.0, and of course, to no one's surprise, 
adding the setting ``PDF_GENERATOR=True`` isn't going to do anything.

If you have used `Pelican plugins`_ before, then the solution should be obvious.
Simply install the ``pdf`` plugin from `Pelican plugins`_. I personally
prefer to keep all plugins (and themes) in the ``<pelican_site_root>`` directory,
on the same level as the ``pelicanconf.py`` settings file:

.. code-block:: console

   $ cd <pelican_site_root>
   $ mkdir plugins
   $ git clone https://github.com/getpelican/pelican-plugins.git plugins

Optionally, you can also add the repository as a submodule:

.. code-block:: console

   $ git submodule add https://github.com/getpelican/pelican-plugins.git plugins

or clone it anywhere else you like for that matter. 

Lastly, you simply need to add ``plugins`` to ``PLUGIN_PATHS`` and ``pdf`` 
to ``PLUGINS``. The former will temporarily add ``PLUGIN_PATHS`` to your 
system path so that the latter is importable:

.. code-block:: python

   PLUGIN_PATHS = ['plugins']
   PLUGINS = ['pdf']

When you run ``pelican`` (or ``make html``), the generated PDFs of your articles
will appear in the ``pdf`` directory of the output directory, named according
to the article slug with the ``.pdf`` extension.

In my opinion, the generated PDFs aren't exactly terrific, and the plugin could
do with a little bit more work.

.. note:: If you happen to be using the ``notmyidea`` theme, a link *get the pdf*
          will appear by simply adding ``PDF_PROCESSOR=True`` to your settings
          (as of `commit a7ca52`_).

.. _features: https://github.com/getpelican/pelican/blob/
		          8be7c0dbae5bd094379d74fd47acb41a56f18afd/docs/
              index.rst#features
.. _change log: http://docs.getpelican.com/en/3.5.0/changelog.html#id3
.. _examples settings: http://docs.getpelican.com/en/3.5.0/settings.html
                       #example-settings
.. _Pelican plugins: http://docs.getpelican.com/en/3.5.0/plugins.html
.. _commit a7ca52: https://github.com/getpelican/pelican/blob/
                   a7ca52dee05819be269b95556da01f965d107a50/pelican/
                   themes/notmyidea/templates/taglist.html
.. _issue: https://github.com/getpelican/pelican/issues/1009
