.. title: Louis does dotfiles... again
.. slug: louis-does-dotfiles-again
.. date: 2016-02-21 23:14:18 UTC+11:00
.. tags:
.. category: 
.. link: 
.. description: 
.. type: text

Switching to Zsh
----------------

First I created a `fork`_ of `Oh My Zsh`_ and added it as a submodule to my
existing `dotfiles repository`_ under a directory named ``.oh-my-zsh``:

..  code:: console

    $ cd $HOME/Dropbox/dotfiles
    $ git submodule add https://github.com/ltiao/oh-my-zsh.git .oh-my-zsh

Since my dotfiles repo is a fork of `Mathias Bynen's dotfiles`_, which is 
primarily for ``bash``, there shouldn't be any conflicts. In fact, we should
be able to switch seamlessly between using ``zsh`` and ``bash`` as the default
shell.

..  code:: console

    $ cp .oh-my-zsh/templates/zshrc.zsh-template .zshrc
    $ vim .zshrc

..  code:: bash

    export ZSH=$HOME/Dropbox/dotfiles/.oh-my-zsh

Add or modify files in ``.oh-my-zsh/custom``

Commit and push

..  code:: console

    $ stow --simulate --verbose=1 --ignore='(gitmodules|oh-my-zsh)' --dir=/Users/ltiao/Dropbox dotfiles
    $ stow --verbose=1 --ignore='(gitmodules|oh-my-zsh)' --dir=/Users/ltiao/Dropbox dotfiles
    $ chsh -s /bin/zsh

Switching to iTerm2
-------------------

1. Download and install `iTerm2`_
2. Key shortcuts 
3. `Solarized Dark`_:

   ..  code:: console

       $ curl -o "Solarized Dark.itermcolors" https://raw.githubusercontent.com/altercation/solarized/master/iterm2-colors-solarized/Solarized%20Dark.itermcolors

   `Tomorrow Night Eighties`_:

   ..  code:: console

       $ curl -o "Tomorrow Night Eighties.itermcolors" https://raw.githubusercontent.com/chriskempson/tomorrow-theme/master/iTerm2/Tomorrow%20Night%20Eighties.itermcolors

5. Background Opacity
6. Background dimming, animation

Themes
------

`Bullet Train for oh-my-zsh`_

..  code:: console

    $ cd .oh-my-zsh/custom/themes/
    $ curl -O https://raw.githubusercontent.com/caiogondim/bullet-train-oh-my-zsh-theme/master/bullet-train.zsh-theme

..  code:: bash

    ZSH_THEME="bullet-train"


Powerline-compatible Fonts
--------------------------

1. Download `Powerline fonts`_
2. Install a font. "Meslo LG S Regular for Powerline" is probably just as good
   as any.

   .. thumbnail:: ../../images/install_font.png
      :align: center

3. Configure iTerm2 to use font

   .. thumbnail:: ../../images/iterm2_font.png
      :align: center

Further Readings
----------------

- http://hiltmon.com/blog/2013/02/13/make-iterm-2-more-mac-like/
- https://ruigomes.me/blog/perfect-iterm-osx-terminal-installation/
- http://stackoverflow.com/questions/6801594/word-jumping-in-iterm2-or-terminal-in-osx-lion

- https://github.com/powerline/fonts
- https://powerline.readthedocs.org/en/latest/installation/osx.html#fonts-installation
- https://gist.github.com/agnoster/3712874

.. _iTerm2: https://www.iterm2.com/
.. _Oh My Zsh: https://github.com/robbyrussell/oh-my-zsh
.. _fork: https://github.com/ltiao/oh-my-zsh
.. _dotfiles repository: https://github.com/ltiao/dotfiles
.. _Mathias Bynen's dotfiles: https://github.com/mathiasbynens/dotfiles
.. _Solarized Dark: https://github.com/altercation/solarized/tree/master/iterm2-colors-solarized
.. _Bullet Train for oh-my-zsh: https://github.com/caiogondim/bullet-train-oh-my-zsh-theme
.. _iTerm Color Schemes: https://github.com/mbadolato/iTerm2-Color-Schemes
.. _Tomorrow Theme: https://github.com/chriskempson/tomorrow-theme
.. _Tomorrow Night Eighties: http://colorsublime.com/theme/Tomorrow_Night_Eighties
.. _Powerline fonts: https://github.com/powerline/fonts/archive/master.zip