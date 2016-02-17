.. title: Creating custom (Unix) fortunes
.. slug: creating-custom-unix-fortunes
.. date: 2016-02-18 01:15:42 UTC+11:00
.. tags: unix, fortune, cowsay, lolcat, bash, gtd 
.. category: coding
.. link: 
.. description: 
.. type: text

Like others, I include ``fortune`` in my ``.bash_profile`` so that I am 
greeted with a random, witty and thought-provoking epigram upon starting a 
new shell session. Eventually, however, I found most of the epigrams to be 
trite and vapid most of the time, and began growing tired of them. Instead of 
tinkering with the probabilities of sampling from the various datafiles 
available, I decided to roll with my own epigram datafile.

.. TEASER_END

..  pull-quote::

    People often say that motivation doesn't last. Well, neither does bathing 
    - that's why we recommend it daily.

    -- Zig Ziglar

I have a collection of favorite quotes scattered across various places -- 
Evernote, Goodreads, Reddit Saves, Kindle Annotations, etc. Usually, when I 
add something to that collection, it's likely the last I'll ever see of it. 
Recently, I had the idea of incorporating the review and curation of the 
collection as part of my `GTD Weekly Review`_ (or perhaps more appropriately,
a `"Bigger Picture" Review`_ of some sort). In addition to this, I thought it 
would be beneficial to see some subset of epigrams from my collection on a 
day-to-day basis. This way, it ensures there is a nonzero (albeit low) 
probability of encountering everything in my collection.

Getting Started
---------------

First note that I obtained ``fortune`` with Homebrew:

..  code:: console

    $ brew install fortune

After installing, we should be able to find the default datafiles in 
``/usr/local/share/games/fortunes/``:

..  code:: console

    $ ls /usr/local/share/games/fortunes/

Instead of simple plaintext files, ``fortune`` only works on files with 
formats that allow random access of its strings. Such as datafiles can be 
easily created with `strfile`_, which *"reads a file containing groups of 
lines separated by a line containing a single percent '%' sign and creates a 
data file which contains a header structure and a table of file offsets for 
each group of lines."*

So now let's create a text file with the properties prescribed above, e.g.:

..  code:: console

    $ touch quotes
    $ cat >> quotes
    Seeing much, suffering much, and studying much, are the three pillars of 
    learning.

    -- Benjamin Disraeli
    %
    While one person hesitates because he feels inferior, the other is busy 
    making mistakes and becoming superior.
    
    -- Henry C. Link
    %
    When nothing seems to help, I go and look at a stonecutter hammering away 
    at his rock, perhaps a hundred times without as much as a crack showing in 
    it. Yet at the hundred and first blow it will split in two, and I know it 
    was not that last blow that did it, but all that had gone before.

    -- Jacob A. Riis

Next we create the datafile with ``strfile``:

..  code:: console

    $ strfile quotes 
    "quotes.dat" created
    There were 3 strings
    Longest string: 310 bytes
    Shortest string: 106 bytes

and now we can randomly access a group of lines with ``fortune``:  

..  code:: console

    $ fortune quotes
    Seeing much, suffering much, and studying much, are the three pillars of 
    learning.

    -- Benjamin Disraeli

It is important to note that when we specify ``quotes`` as the argument to 
``fortune``, it will look for the datafile ``quotes.dat``, rather than the
plaintext file ``quotes``.

Just to amuse ourselves, we can pipe through to a number of humorous commands/
utilities (``cowsay``, ``lolcat``):

..  code:: console

    $ fortune quotes | cowsay -f turtle | lolcat

..  thumbnail:: ../../images/fortune_cowsay_lolcat.png
    :align: center

Anyways, back to the point! I created a repo on Github (`ltiao/fortunes`_) to 
centralize, manage, curate and source control my collection of epigrams. This
repo can contain several datafiles, so I have the option of logically grouping
epigrams into various datafiles, and get a random epigram from across all of 
the datafiles:

..  code:: console

    $ git clone https://github.com/ltiao/fortunes
    $ fortune fortunes
    [...]

Furthermore, I have the option of tweaking probabilities of sampling from a
particular datafile, and more! But I'll investigate more advanced features 
after I've built up my collection. For the time being, the relevant line in my 
``.bash_profile`` will simply be the above (piped to ``cowsay`` and 
``lolcat`` of course!)

.. _strfile: http://linuxcommand.org/man_pages/strfile1.html
.. _GTD Weekly Review: http://lifehacker.com/5908816/the-weekly-review-how-one-hour-can-save-you-a-weeks-worth-of-hassle-and-headache
.. _"Bigger Picture" Review: https://facilethings.com/blog/en/basics-big-picture-reviews
.. _ltiao/fortunes: https://github.com/ltiao/fortunes
