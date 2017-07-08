.. title: Notes on BeautifulSoup4
.. slug: notes-on-beautifulsoup4
.. date: 2015-05-22 22:58:26 UTC+10:00
.. tags: BeautifulSoup, python, draft
.. category: coding
.. link: 
.. description: 
.. type: text

The following are equivalent

.. code:: python

   soup.findAll(...)
   soup.find_all(...)
   soup(...)

as are the following

.. code:: python

   soup.find('some_attr')
   soup.some_attr



