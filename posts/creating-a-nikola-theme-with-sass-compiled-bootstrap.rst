.. title: Creating a Nikola theme with Sass-compiled Bootstrap
.. slug: creating-a-nikola-theme-with-sass-compiled-bootstrap
.. date: 2015-09-28 22:59:54 UTC+10:00
.. tags: sass, bootstrap, nikola, draft
.. category: coding
.. link: 
.. description: 
.. type: text

First, create a new Nikola theme. The way I like to do this is by creating a 
`new repository on Github`_ so that it can be initialized with a README, 
LICENSE, ``.gitignore``, etc. Next, clone the newly created repo into 
``<site-root>/themes``.

The bare minimum requirement for a Nikola theme is that it include a 
``parent`` file. Since we are extending and customizing Bootstrap, it makes
sense to inherit from ``bootstrap3`` or its `Jinja2`_ port, 
``bootstrap3-jinja``. I much prefer Jinja2 over `Mako`_, so we shall opt for 
the latter. It goes without saying that everything outlined below can 
trivially be made to work for Mako.

.. code:: console

   $ cd <site-root>/themes/<rep-root>
   $ echo "bootstrap3-jinja" > parent

The following is not strictly required, but is good practice (explicit is 
better than implicit). We specify Jinja2 as the template engine.

.. code:: console

   $ echo "jinja" > engine

Note that our theme is going to be very similar to 
`bootstrap3-gradients-jinja`_, which is a theme that uses 
``bootstrap-theme.css``, an optional Bootstrap stylesheet that includes 
gradients and is touted by the Bootstrap developers as providing a visually 
enhanced experience.

Not surprisingly, it is almost identical to the ``bootstrap3-jinja`` theme. 
The key difference is that is requires an additional stylesheet, so the 
webassets bundle and ``html_stylesheets()`` macro in ``base_helper.tmpl`` must 
be updated to reflect that. Our theme is going to be similar in that we use 
our own custom Boostrap stylesheet, compiled from Sass.

We will take care of this later, for now, let us get our Sass workflow up and
running.

Create the ``sass`` directory inside the root of the repo

.. code:: console

   $ cd <site-root>/themes/<repo-root>
   $ mkdir sass

Next, we must obtain the Sass sources for Bootstrap. There are many ways to do
this, either through Compass, Bower, directly from source, etc. I prefer to do
this through Bower.

- Install `npm`_, which is most easily done by installing `Node.js`_.
- Install `Bower`_

  .. code:: console

     $ npm install -g bower

Install ``boostrap-sass`` inside the ``sass`` directory.

.. code:: console

   $ cd <site-root>/themes/<repo-root>/sass
   $ bower install bootstrap-sass

You should now see all components installed in the ``bower_components`` 
directory.

Now we create a SCSS file, call it say, ``bootstrap-custom.scss``, which is the 
primary file that we will be compiling to CSS. It will be the main entrypoint 
that imports the Bootstrap sources, as well as any other customizations we 
make. We create a file ``_variables-custom.scss`` to isolate all the 
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

At this point

bundle
  Copy the contents of ``bundle``

  .. code::

     assets/css/all-nocdn.css=bootstrap.css,bootstrap-theme.css,rst.css,code.css,colorbox.css,theme.css,custom.css
     assets/css/all.css=rst.css,code.css,colorbox.css,theme.css,custom.css
     assets/js/all-nocdn.js=jquery.min.js,bootstrap.min.js,jquery.colorbox-min.js,moment-with-locales.min.js,fancydates.js
     assets/js/all.js=jquery.colorbox-min.js,moment-with-locales.min.js,fancydates.js

  .. code::

     assets/css/all.css=bootstrap-custom.css,rst.css,code.css,colorbox.css,theme.css,custom.css
     assets/js/all-nocdn.js=jquery.min.js,bootstrap.min.js,jquery.colorbox-min.js,moment-with-locales.min.js,fancydates.js
     assets/js/all.js=jquery.colorbox-min.js,moment-with-locales.min.js,fancydates.js

.. _`Mako`: http://www.makotemplates.org/
.. _`Jinja2`: http://jinja.pocoo.org/
.. _`new repository on Github`: https://github.com/new
.. _`bootstrap3-gradients-jinja`: https://themes.getnikola.com/#bootstrap3-gradients-jinja
.. _`Node.js`: https://nodejs.org/
.. _`npm`: http://blog.npmjs.org/post/85484771375/how-to-install-npm
.. _`Bower`: http://bower.io/#install-bower
.. _`bootstrap-sass`: https://github.com/twbs/bootstrap-sass#c-bower
.. _`install Sass`: http://sass-lang.com/install