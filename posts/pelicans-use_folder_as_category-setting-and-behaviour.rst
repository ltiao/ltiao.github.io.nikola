.. title: Pelican's USE_FOLDER_AS_CATEGORY setting and behaviour
.. slug: pelicans-use_folder_as_category-setting-and-behaviour
.. date: 2015-04-02 00:40:03 UTC+11:00
.. tags: python, pelican
.. category: coding
.. link: 
.. description: 
.. type: text

Pelican's `USE_FOLDER_AS_CATEGORY`_ setting is set to ``True`` by default.
If you place an article within a subfolder of the content folder, and don't
specify a category in your article metadata, then the name of the subfolder
will be the category of your article. However, the documentation does not
specify Pelican's behavior under all possible situations. E.g. What happens
if an article is within a subfolder, and its category is specified but different
the name of the subfolder?

We summarize Pelican's behavior under all possible circumstances here. 

+----------------------------+------------------------------------+--------------------------+-------------------------------+
| ``USE_FOLDER_AS_CATEGORY`` | Category *c* specified in metadata | Article in subfolder *d* |       Article's Category      |
+============================+====================================+==========================+===============================+
| ``True``                   | ``True``                           | ``True``                 | *c*                           |
+----------------------------+------------------------------------+--------------------------+-------------------------------+
| ``True``                   | ``True``                           | ``False``                | *c*                           |
+----------------------------+------------------------------------+--------------------------+-------------------------------+
| ``True``                   | ``False``                          | ``True``                 | *d*                           |
+----------------------------+------------------------------------+--------------------------+-------------------------------+
| ``True``                   | ``False``                          | ``False``                | ``DEFAULT_CATEGORY`` (*Misc*) |
+----------------------------+------------------------------------+--------------------------+-------------------------------+
| ``False``                  | ``True``                           | ``True``                 | *c*                           |
+----------------------------+------------------------------------+--------------------------+-------------------------------+
| ``False``                  | ``True``                           | ``False``                | *c*                           |
+----------------------------+------------------------------------+--------------------------+-------------------------------+
| ``False``                  | ``False``                          | ``True``                 | ``DEFAULT_CATEGORY`` (*Misc*) |
+----------------------------+------------------------------------+--------------------------+-------------------------------+
| ``False``                  | ``False``                          | ``False``                | ``DEFAULT_CATEGORY`` (*Misc*) |
+----------------------------+------------------------------------+--------------------------+-------------------------------+

.. _USE_FOLDER_AS_CATEGORY: http://docs.getpelican.com/en/3.5.0/settings.html#basic-settings