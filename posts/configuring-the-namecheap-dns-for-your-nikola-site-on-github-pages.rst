.. title: Configuring the Namecheap DNS for your Nikola site on Github Pages
.. slug: configuring-the-namecheap-dns-for-your-nikola-site-on-github-pages
.. date: 2015-10-07 22:49:06 UTC+11:00
.. tags: nikola, github, namecheap, dns, hosting, devops, draft
.. category: coding 
.. link: 
.. description: 
.. type: text

Namecheap overhauled their Account Panel a few weeks ago 
(https://blog.namecheap.com/ready-to-roll-your-new-account-panel/). 
Nonetheless, the popular guide on `Setting the DNS for GitHub Pages on Namecheap`_
is still relevant and the steps remain practically the same. 

This article will adapt the steps outlined in the aforementioned guide to the
new Namecheap account panel and the Nikola static site generator.

First I describe what I have now, and what I wish to achieve. Currently, I 
have :doc:`my Nikola-generated site <how-i-customized-my-nikola-powered-site>` 
hosted on my Github User Page (``http://ltiao.github.io``). Say I just bought 
a shiny new domain name from Namecheap, ``louistiao.me`` and I would like to:

- Let ``louistiao.me`` be the primary domain
- Redirect ``ltiao.github.io`` to ``louistiao.me``
- Redirect ``www.louistiao.me`` to ``louistiao.me``

Configure the Host Records
--------------------------

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

Further Reading
---------------

- https://help.github.com/articles/tips-for-configuring-a-cname-record-with-your-dns-provider/
- https://help.github.com/articles/tips-for-configuring-an-a-record-with-your-dns-provider/
- https://help.github.com/articles/setting-up-a-custom-domain-with-github-pages/
- https://help.github.com/articles/about-custom-domains-for-github-pages-sites/

.. _`Setting the DNS for GitHub Pages on Namecheap`:
   http://davidensinger.com/2013/03/setting-the-dns-for-github-pages-on-namecheap/
.. _`add any other file in Nikola`:
   https://getnikola.com/handbook.html#adding-files
