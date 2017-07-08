.. title: Quick reference: Upgrading all outdated pip packages
.. slug: quick-ref-upgrading-all-outdated-pip-packages
.. date: 2015-04-02 00:41:22 UTC+11:00
.. tags: python, pip, bash
.. category: coding
.. link: 
.. description: 
.. type: text

Simply execute:

.. code-block:: console

   $ pip list --outdated | cut -d' ' -f1 | xargs pip install --upgrade

for any version of ``pip`` that has the ``list`` command (which I believe
is 1.3+.)
