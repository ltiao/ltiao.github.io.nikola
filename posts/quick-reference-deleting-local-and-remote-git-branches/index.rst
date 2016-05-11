.. title: Quick Reference: Deleting Local and Remote Git Branches
.. slug: quick-reference-deleting-local-and-remote-git-branches
.. date: 2016-05-11 17:16:05 UTC+10:00
.. tags: git
.. category: coding 
.. link: 
.. description: 
.. type: text

From http://stackoverflow.com/questions/2003505/delete-a-git-branch-both-locally-and-remotely:

Deleting a Local Git Branch:

..  code:: console

    $ git branch -D <branch-name>
    Deleted branch <branch-name> (was <commit-hash>).

Deleting a Remote Git Branch (available as of `Git 1.7.0`_)

..  code:: console

    $ git push origin --delete <branch-name>
    To <git-remote-origin-url>
     - [deleted]         <branch-name>

.. _Git 1.7.0: https://github.com/git/git/blob/c2c5f6b1e479f2c38e0e01345350620944e3527f/Documentation/RelNotes/1.7.0.txt#L154
