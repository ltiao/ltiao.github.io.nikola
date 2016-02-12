.. title: Setting up custom (Unix) fortunes
.. slug: setting-up-custom-unix-fortunes
.. date: 2016-02-10 14:56:54 UTC+11:00
.. tags: 
.. category: 
.. link: 
.. description: 
.. type: text

..  code:: console

    $ brew install fortune
    $ ls /usr/local/share/games/fortunes/
    $ touch quotes
    $ strfile quotes
    $ fortune quotes

..  code:: bash

    # Fortune / Cowsay Greeting / LOLCAT
    fortune Dropbox/fortunes | cowsay -f turtle | lolcat
