.. title: Creating a Nikola theme with Sass-compiled Bootstrap
.. slug: creating-a-nikola-theme-with-sass-compiled-bootstrap
.. date: 2015-09-28 22:59:54 UTC+10:00
.. tags: sass, bootstrap, nikola
.. category: coding
.. link: 
.. description: 
.. type: text

Initializing the Theme
----------------------

First, create a new Nikola theme. I prefer to do this by creating a
`new repository on Github`_ so that it can be initialized with a README, 
LICENSE, ``.gitignore``, etc. Once that's done, clone the newly created repo 
into ``<site-root>/themes``.

The bare minimum requirement for a Nikola theme is that it include a 
``parent`` file. Since our theme just uses our own extended and customized 
version of Bootstrap, it makes sense to inherit from ``bootstrap3`` or its 
`Jinja2`_ port, ``bootstrap3-jinja``. I much prefer Jinja2 over `Mako`_, so we
shall opt for the latter. It goes without saying that everything outlined 
below can trivially be made to work for Mako.

.. code:: console

   $ cd <site-root>/themes/<repo-root>
   $ echo "bootstrap3-jinja" > parent

The following is not strictly required, but is good practice (explicit is 
better than implicit). We specify Jinja2 as the template engine.

.. code:: console

   $ echo "jinja" > engine

Note that our theme is going to be very similar to `bootstrap3-gradients-jinja`_, 
which is a theme that uses ``bootstrap-theme.css``, an optional Bootstrap 
stylesheet that includes gradients and is touted by the Bootstrap developers 
as "providing a visually enhanced experience".

Not surprisingly, it is almost identical to the ``bootstrap3-jinja`` theme. 
The key difference is that is requires an additional stylesheet, so the 
webassets bundle and ``html_stylesheets()`` macro in ``base_helper.tmpl`` are 
updated to reflect that. Our theme is going to be similar in that we use our 
own customized Boostrap stylesheet, compiled from Sass. We will take care of 
this later. For now, let's just get our Sass workflow up and running so we can
get Nikola to use Sass to compile our customized stylesheet.

.. TEASER_END

Sass workflow in Nikola
-----------------------

Create the ``sass`` directory inside the root of the repo

.. code:: console

   $ cd <site-root>/themes/<repo-root>
   $ mkdir sass

Next, obtain the Sass sources for Bootstrap. There are several ways to do this, 
e.g. through Compass, Bower, directly from source, etc. I do this through Bower:

If you don't already have Bower, you can install it with `npm`_, which is most 
easily done by installing `Node.js`_. Then you can just install `Bower`_ 
globally:

.. code:: console

   $ npm install -g bower

Now we can install ``boostrap-sass`` inside the ``sass`` directory:

.. code:: console

   $ cd <site-root>/themes/<repo-root>/sass
   $ bower install bootstrap-sass

You should now see all components installed in the ``bower_components`` 
directory:

.. code:: console

   $ ls bower_components
   bootstrap-sass   jquery

Now we create a SCSS file, call it say, ``bootstrap-custom.scss``, which is the 
primary file that we will be compiling to CSS. It will be the main entrypoint 
that imports the Bootstrap sources, as well as any other customizations we 
make. We also create a file ``_variables-custom.scss`` to isolate all the 
modifications we make to Bootstrap variables. 

.. code:: console

   $ touch bootstrap-custom.scss
   $ touch _variables-custom.scss

Note that Sass/SCSS files with leading underscores are `partials`, which lets 
Sass know that it is only a partial file and should not be compiled 
(see http://sass-lang.com/guide). This doesn't really matter with Nikola since 
we have to explicitly tell Nikola which files to pass on to the Sass compiler
anyways.

Now we modify ``bootstrap-custom.scss`` to import our custom variables and the 
Bootstrap sources

.. code:: scss

   @import "variables-custom";
   @import "bower_components/bootstrap-sass/assets/stylesheets/bootstrap";

and create the ``targets`` file, which lets Nikola know which files to pass on
to the Sass compiler (see https://getnikola.com/theming.html#less-and-sass).

.. code:: console

   $ echo "bootstrap-custom.scss" > sass/targets
       
Now, install the Nikola plugin for Sass.

.. code:: console

   $ nikola plugin --install=sass

If this plugin is not installed, Nikola will just silently ignore anything 
in the ``sass`` directory of your theme. 

Once the plugin has been installed successfully, you will be reminded to 
`install Sass`_. If you haven't already done so, you can do so easily with 
``gem``:

.. code:: console

   $ gem install sass

At this point, when you execute ``nikola build``, you will see the Bootstrap
Sass source files being processed by the ``prepare_sass_sources`` task and the 
final ``output/assets/css/bootstrap-custom.css`` built by the ``build_sass`` 
task:

.. code:: console

   $ nikola build
   .  prepare_sass_sources:cache/sass/_variables-custom.scss
   .  prepare_sass_sources:cache/sass/bootstrap-custom.scss
   .  prepare_sass_sources:cache/sass/targets
   .  prepare_sass_sources:cache/sass/bower_components/bootstrap-sass/.bower.json
   .  prepare_sass_sources:cache/sass/bower_components/bootstrap-sass/bower.json
   .  prepare_sass_sources:cache/sass/bower_components/bootstrap-sass/CHANGELOG.md
   .  prepare_sass_sources:cache/sass/bower_components/bootstrap-sass/composer.json
   .  prepare_sass_sources:cache/sass/bower_components/bootstrap-sass/CONTRIBUTING.md
   .  prepare_sass_sources:cache/sass/bower_components/bootstrap-sass/LICENSE
   .  prepare_sass_sources:cache/sass/bower_components/bootstrap-sass/package.json
   .  prepare_sass_sources:cache/sass/bower_components/bootstrap-sass/README.md
   .  prepare_sass_sources:cache/sass/bower_components/bootstrap-sass/sache.json
       ...
   .  build_sass:output/assets/css/bootstrap-custom.css
       ...

A quick sanity check to confirm 
``<site-root>/themes/<repo-root>/sass/bootstrap-custom.scss`` was compiled to
``<site-root>/output/assets/css/bootstrap-custom.css`` as expected.

.. code:: console

   $ head -15 output/assets/css/bootstrap-custom.css 
   @charset "UTF-8";
   /*!
    * Bootstrap v3.3.5 (http://getbootstrap.com)
    * Copyright 2011-2015 Twitter, Inc.
    * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
    */
   /*! normalize.css v3.0.3 | MIT License | github.com/necolas/normalize.css */
   html {
     font-family: sans-serif;
     -ms-text-size-adjust: 100%;
     -webkit-text-size-adjust: 100%; }   

   body {
     margin: 0; }

Update templates to use Sass-compiled CSS
-----------------------------------------

Now all that's left to do is to override the ``base_helper.tmpl`` template and 
the webassets bundle to use our customized Bootstrap stylesheet. As mentioned 
earlier, our modifications are going to closely resemble those of the 
``bootstrap3-gradients-jinja`` theme. Let us locate and install this theme to 
use as a reference:

.. code:: console

   $ nikola install_theme -l | grep bootstrap
   [2015-10-01T05:34:12Z] INFO: requests.packages.urllib3.connectionpool: Starting new HTTPS connection (1): themes.getnikola.com
   bootstrap
   bootstrap-jinja
   bootstrap3-gradients
   bootstrap3-gradients-jinja
   $ nikola install_theme bootstrap3-gradients-jinja
   [2015-10-01T05:35:16Z] INFO: requests.packages.urllib3.connectionpool: Starting new HTTPS connection (1): themes.getnikola.com
   [2015-10-01T05:35:17Z] INFO: install_theme: Downloading 'https://themes.getnikola.com/v7/bootstrap3-gradients-jinja.zip'
   [2015-10-01T05:35:17Z] INFO: requests.packages.urllib3.connectionpool: Starting new HTTPS connection (1): themes.getnikola.com
   [2015-10-01T05:35:17Z] INFO: install_theme: Extracting 'bootstrap3-gradients-jinja' into themes/
   [2015-10-01T05:35:17Z] NOTICE: install_theme: Remember to set THEME="bootstrap3-gradients-jinja" in conf.py to use this theme.

We can inspect the modifications that have been made by comparing the 
differences between the relevant files in ``bootstrap3-jinja`` and 
``bootstrap3-gradients-jinja``. First, let us get the location of the 
``bootstrap3-jinja`` theme which was shipped with Nikola:

.. code:: console

   $ nikola install_theme --get-path bootstrap3-jinja
   <env>/lib/python2.7/site-packages/nikola/data/themes/bootstrap3-jinja

.. code:: console

   $ diff -u <env>/lib/python2.7/site-packages/nikola/data/themes/bootstrap3-jinja/bundles themes/bootstrap3-gradients-jinja/bundles 
   
.. code:: diff

   --- <env>/lib/python2.7/site-packages/nikola/data/themes/bootstrap3-jinja/bundles  2015-10-01 15:33:47.000000000 +1000
   +++ <site-root>/themes/themes/bootstrap3-gradients-jinja/bundles 2015-10-01 15:35:17.000000000 +1000
   @@ -1,4 +1,4 @@
   -assets/css/all-nocdn.css=bootstrap.css,rst.css,code.css,colorbox.css,theme.css,custom.css
   +assets/css/all-nocdn.css=bootstrap.css,bootstrap-theme.css,rst.css,code.css,colorbox.css,theme.css,custom.css
    assets/css/all.css=rst.css,code.css,colorbox.css,theme.css,custom.css
    assets/js/all-nocdn.js=jquery.min.js,bootstrap.min.js,jquery.colorbox-min.js,moment-with-locales.min.js,fancydates.js
    assets/js/all.js=jquery.colorbox-min.js,moment-with-locales.min.js,fancydates.js

.. code:: console

   $ diff -u <env>/lib/python2.7/site-packages/nikola/data/themes/bootstrap3-jinja/templates/base_helper.tmpl themes/bootstrap3-gradients-jinja/templates/base_helper.tmpl 

.. code:: diff

   --- <env>/lib/python2.7/site-packages/nikola/data/themes/bootstrap3-jinja/templates/base_helper.tmpl 2015-10-01 15:33:47.000000000 +1000
   +++ <site-root>/themes/themes/bootstrap3-gradients-jinja/templates/base_helper.tmpl  2015-10-01 15:35:17.000000000 +1000
   @@ -103,6 +103,7 @@
        {% if use_bundles %}
            {% if use_cdn %}
                <link href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css" rel="stylesheet">
   +            <link href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap-theme.min.css" rel="stylesheet">
                <link href="/assets/css/all.css" rel="stylesheet" type="text/css">
            {% else %}
                <link href="/assets/css/all-nocdn.css" rel="stylesheet" type="text/css">
   @@ -110,8 +111,10 @@
        {% else %}
            {% if use_cdn %}
                <link href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css" rel="stylesheet">
   +            <link href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap-theme.min.css" rel="stylesheet">
            {% else %}
                <link href="/assets/css/bootstrap.min.css" rel="stylesheet" type="text/css">
   +            <link href="/assets/css/bootstrap-theme.min.css" rel="stylesheet" type="text/css">
            {% endif %}
            <link href="/assets/css/rst.css" rel="stylesheet" type="text/css">
            <link href="/assets/css/code.css" rel="stylesheet" type="text/css">

We see the only difference is that ``bootstrap3-gradients-jinja`` includes the 
additional ``bootstrap-theme.css`` stylesheet after the standard 
``bootstrap.css`` stylesheet. While we could simply replicate this with our 
own theme, it would become problematic if we introduce things like ``@import``
statements in our Sass sources (which we would definitely need to if we 
decided to use, for example `Google Fonts`_) as ``@imports`` must come before 
all other content and our compiled ``bootstrap-custom.css`` stylesheet would
come after the standard ``bootstrap.min.css`` stylesheet. 

Since we build all of Bootstrap from source anyways, the most straightforward 
solution is to get rid of the ``bootstrap.min.css`` stylesheet altogether and 
only use our own compiled ``bootstrap-custom.css`` stylesheet.

Our custom Bootstrap is compiled at the time we run ``nikola build``, so 
obviously it would not be available on any CDN. Therefore, we would not need to
make the distinction between using and not using a CDN by having separate 
webassets bundle files ``all.css`` and ``all-nocdn.css``. We can just bundle 
everything into the ``all.css`` file. Additionally, the ``use_cdn`` variable is
effectively ignored since we need to include our compiled stylesheets no 
matter what; it is not available from anywhere else.

To summarize, for ``bundles``, we have:

.. code::

   assets/css/all.css=bootstrap-custom.css,rst.css,code.css,colorbox.css,theme.css,custom.css
   assets/js/all-nocdn.js=jquery.min.js,bootstrap.min.js,jquery.colorbox-min.js,moment-with-locales.min.js,fancydates.js
   assets/js/all.js=jquery.colorbox-min.js,moment-with-locales.min.js,fancydates.js

and for the relevant section of ``base_helper.tmpl``, we have:

.. code:: html

   {% if use_bundles %}
       <link href="/assets/css/all.css" rel="stylesheet" type="text/css">
   {% else %}
       <link href="/assets/css/bootstrap-custom.css" rel="stylesheet" type="text/css">
       <link href="/assets/css/rst.css" rel="stylesheet" type="text/css">
       <link href="/assets/css/code.css" rel="stylesheet" type="text/css">
       <link href="/assets/css/colorbox.css" rel="stylesheet" type="text/css">
       <link href="/assets/css/theme.css" rel="stylesheet" type="text/css">
       {% if has_custom_css %}
           <link href="/assets/css/custom.css" rel="stylesheet" type="text/css">
       {% endif %}
   {% endif %}

TODO
  * Sass compress, and why Nikola can't
  * Bootswatch (optional)
  * Include Sass Bootstrap workflow references

.. _`Mako`: http://www.makotemplates.org/
.. _`Jinja2`: http://jinja.pocoo.org/
.. _`new repository on Github`: https://github.com/new
.. _`bootstrap3-gradients-jinja`: https://themes.getnikola.com/#bootstrap3-gradients-jinja
.. _`Node.js`: https://nodejs.org/
.. _`npm`: http://blog.npmjs.org/post/85484771375/how-to-install-npm
.. _`Bower`: http://bower.io/#install-bower
.. _`bootstrap-sass`: https://github.com/twbs/bootstrap-sass#c-bower
.. _`install Sass`: http://sass-lang.com/install
.. _`Google Fonts`: https://www.google.com/fonts