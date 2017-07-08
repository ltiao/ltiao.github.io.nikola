.. title: A Better Approach For Initializing New Nikola Themes (since v7.7.5)
.. slug: a-better-approach-for-initializing-new-nikola-themes-since-v775
.. date: 2016-05-18 12:20:24 UTC+10:00
.. tags: nikola, python
.. category: 
.. link: 
.. description: 
.. type: text

A few months ago, I wrote a post on :doc:`creating-a-nikola-theme-with-sass-compiled-bootstrap`.
Since then, `Nikola 7.7.5`_ has added several new features which makes it less
tedious to get started with your custom theme.

Initializing the Theme
----------------------

First, I initialize a theme named ``tiao``, which automatically creates the 
necessary directories and files for me.

..  code:: console

    $ nikola theme --new=tiao --engine=jinja --parent=bootstrap3-jinja
    [2016-05-18T02:29:49Z] INFO: theme: Creating theme tiao with parent bootstrap3-jinja and engine jinja in themes/tiao
    [2016-05-18T02:29:49Z] INFO: theme: Created directory themes/tiao
    [2016-05-18T02:29:49Z] INFO: theme: Created file themes/tiao/parent
    [2016-05-18T02:29:49Z] INFO: theme: Created file themes/tiao/engine
    [2016-05-18T02:29:49Z] INFO: theme: Theme themes/tiao created successfully.
    [2016-05-18T02:29:49Z] NOTICE: theme: Remember to set THEME="tiao" in conf.py to use this theme.

    $ tree themes/tiao
    themes/tiao
    ├── engine
    └── parent

    0 directories, 2 files

.. TEASER_END

We are reminded to set the ``THEME`` setting in ``conf.py``. Now we can use the
``--copy-template`` option to copy the named template file from the parent to 
a local theme or to ``templates/`` [#]_:

..  code:: console

    $ nikola theme --copy-template=base.tmpl
    [2016-05-18T04:50:20Z] INFO: theme: Copied template from /Users/ltiao/.virtualenvs/blog/lib/python3.5/site-packages/nikola/data/themes/bootstrap3-jinja/templates/base.tmpl to themes/tiao/templates/base.tmpl
    
    $ tree themes/tiao
    themes/tiao
    ├── engine
    ├── parent
    └── templates
        └── base.tmpl

    1 directory, 3 files

If you are unsure which templates are available, you can path to the contents
of the parent theme with:

..  code:: console

    $ cat themes/tiao/parent | xargs nikola theme --get-path
    /Users/ltiao/.virtualenvs/blog/lib/python3.5/site-packages/nikola/data/themes/bootstrap3-jinja

Now you can list the available templates:

..  code:: console

    $ ls /Users/ltiao/.virtualenvs/blog/lib/python3.5/site-packages/nikola/data/themes/bootstrap3-jinja/templates
    authors.tmpl     base_helper.tmpl listing.tmpl     slides.tmpl
    base.tmpl        gallery.tmpl     post.tmpl        tags.tmpl

(If you have ``tree`` installed, here is a slicker alternative)

..  code:: console

    $ cat themes/tiao/parent | xargs nikola theme -g | xargs tree -L 2
    /Users/ltiao/.virtualenvs/blog/lib/python3.5/site-packages/nikola/data/themes/bootstrap3-jinja
    ├── AUTHORS.txt
    ├── README.md
    ├── assets
    │   ├── css
    │   ├── fonts
    │   └── js
    ├── bundles
    ├── engine
    ├── parent
    └── templates
        ├── authors.tmpl
        ├── base.tmpl
        ├── base_helper.tmpl
        ├── gallery.tmpl
        ├── listing.tmpl
        ├── post.tmpl
        ├── slides.tmpl
        └── tags.tmpl

    5 directories, 13 files

Now you are ready to make customizations to your theme.

.. [#] https://github.com/getnikola/nikola/blob/d9609e37d96a14189d3d54cea213030d47d0a8b3/nikola/plugins/command/theme.py#L262

.. _Nikola 7.7.5: https://getnikola.com/changes.html#new-in-v7-7-5
