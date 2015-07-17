.. title: Notes on BeautifulSoup4
.. slug: notes-on-beautifulsoup4
.. date: 2015-05-22 22:58:26 UTC+10:00
.. tags: 
.. category: 
.. link: 
.. description: 
.. type: text

The following are equivalent

.. code::

   soup.findAll(...)
   soup.find_all(...)
   soup(...)

as are the following

.. code::

   soup.find('some_attr')
   soup.some_attr



