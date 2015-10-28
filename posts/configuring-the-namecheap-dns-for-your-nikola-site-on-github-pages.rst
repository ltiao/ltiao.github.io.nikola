.. title: Configuring the Namecheap DNS for your Nikola site on Github Pages
.. slug: configuring-the-namecheap-dns-for-your-nikola-site-on-github-pages
.. date: 2015-10-07 22:49:06 UTC+11:00
.. tags: nikola, github, namecheap, dns, hosting, devops
.. category: coding 
.. link: 
.. description: 
.. type: text

Namecheap overhauled their Account Panel a few weeks ago 
(https://blog.namecheap.com/ready-to-roll-your-new-account-panel/). 
Nonetheless, the popular guide on `Setting the DNS for GitHub Pages on Namecheap`_
is still applicable and the instructions remain practically the same, if not
even simpler now due to the new interface.

.. TEASER_END

This posts adapts the steps outlined in the aforementioned guide to the
new Namecheap account panel interface and also includes additional steps for
static sites generated with Nikola.

Consider the following scenario. You have your static site hosted on your 
Github User Page at ``http://<username>.github.io`` and you just bought a 
shiny new domain name from Namecheap, say, ``<username>.me``. Say you want to
and want to still host your static site on Github, but additioanlly, you would 
like to:

- Let ``<username>.me`` be the primary domain
- Redirect ``<username>.github.io`` to ``<username>.me``
- Redirect ``www.<username>.me`` to ``<username>.me``

Configure the Host Records
--------------------------

*Work in progress*

https://help.github.com/articles/tips-for-configuring-an-a-record-with-your-dns-provider/#configuring-an-a-record-with-your-dns-provider

.. thumbnail:: ../images/namecheap.png
   :align: center
   :class: img-thumbnail

Adding the ``CNAME`` file to your repo
--------------------------------------

We add the ``CNAME`` file like we would `add any other file in Nikola`_, by 
placing it in in the ``files/`` directory, which will then be copied to 
``output`` by the ``copy_files`` task.

.. code:: console

   $ cd <nikola-project-root>
   $ echo "louistiao.me" > files/CNAME 
   $ nikola github_deploy

https://help.github.com/articles/tips-for-configuring-an-a-record-with-your-dns-provider/#configuring-a-www-subdomain

Additional Resources
--------------------

- https://help.github.com/articles/tips-for-configuring-a-cname-record-with-your-dns-provider/
- https://help.github.com/articles/tips-for-configuring-an-a-record-with-your-dns-provider/
- https://help.github.com/articles/setting-up-a-custom-domain-with-github-pages/
- https://help.github.com/articles/about-custom-domains-for-github-pages-sites/

.. _`Setting the DNS for GitHub Pages on Namecheap`:
   http://davidensinger.com/2013/03/setting-the-dns-for-github-pages-on-namecheap/
.. _`add any other file in Nikola`:
   https://getnikola.com/handbook.html#adding-files
