.. title: Louis does dotfiles
.. slug: louis-does-dotfiles
.. date: 2016-02-12 22:59:46 UTC+11:00
.. tags: osx, dotfiles, git, github, gnu, stow
.. category: coding
.. link: 
.. description: 
.. type: text

For a long time, I kept a small set of minimalistic dotfiles
(``.bash_profile``, ``.gitconfig``, ``.vimrc``). You probably couldn't find 
anything in my ``.bash_profile`` other than exports and path definitions that 
were absolutely necessary to get tools such as `Homebrew`_ and 
`virtualenvwrapper`_ to work. Furthermore, I was dismissive towards spending 
any significant amount of time down the rabbit hole of perpetual dotfile 
customization and optimization.

Recently, while digging through my bookmarks saved from months ago, I came 
across `GitHub does dotfiles`_. Needless to say, after perusing through some 
of the most popular dotfiles, dotfile utilities and tutorials, I came away 
quite impressed. It disabused me of my previous misbelief that dotfile 
calibration is ultimately a fruitless and ceaseless task, and I decided to 
give it another shot.

Getting Started
---------------

Instead of starting from scratch, I decided to bootstrap off an existing 
dotfile repo.

By far the most popular is `Mathias Bynens' dotfiles`_. Not only that, it 
seemed to offer the most sensible defaults for OSX. First, I created a fork 
(`Louis' fork of Mathias' dotfiles`_) and cloned it to my computer.

From several blog posts, I have found that some people like to clone to a
directory under ``~``, such as ``~/dotfiles``. Personally, I like to clone it 
to a synchronized directory, such as ``~/Dropbox/dotfiles``, so that I can 
still easily access it anywhere that has an internet connection, even if it is 
infeasible to install and use ``git``. 

GNU Stow
--------

..  code:: console

    $ stow --dir=$HOME/Dropbox/ --target=$HOME dotfiles \
           --simulate --verbose=1 --ignore='(bootstrap.sh|brew.sh)'
    LINK: .aliases => ../Dropbox/dotfiles/.aliases
    LINK: .bash_profile => ../Dropbox/dotfiles/.bash_profile
    LINK: .bash_prompt => ../Dropbox/dotfiles/.bash_prompt
    LINK: .bashrc => ../Dropbox/dotfiles/.bashrc
    LINK: .curlrc => ../Dropbox/dotfiles/.curlrc
    LINK: .editorconfig => ../Dropbox/dotfiles/.editorconfig
    LINK: .exports => ../Dropbox/dotfiles/.exports
    LINK: .functions => ../Dropbox/dotfiles/.functions
    LINK: .gdbinit => ../Dropbox/dotfiles/.gdbinit
    LINK: .gitattributes => ../Dropbox/dotfiles/.gitattributes
    LINK: .gitconfig => ../Dropbox/dotfiles/.gitconfig
    LINK: .gvimrc => ../Dropbox/dotfiles/.gvimrc
    LINK: .hgignore => ../Dropbox/dotfiles/.hgignore
    LINK: .hushlogin => ../Dropbox/dotfiles/.hushlogin
    LINK: .inputrc => ../Dropbox/dotfiles/.inputrc
    LINK: .osx => ../Dropbox/dotfiles/.osx
    LINK: .path => ../Dropbox/dotfiles/.path
    LINK: .screenrc => ../Dropbox/dotfiles/.screenrc
    LINK: .vim => ../Dropbox/dotfiles/.vim
    LINK: .vimrc => ../Dropbox/dotfiles/.vimrc
    LINK: .wgetrc => ../Dropbox/dotfiles/.wgetrc
    LINK: bin => ../Dropbox/dotfiles/bin
    LINK: init => ../Dropbox/dotfiles/init
    WARNING: in simulation mode so not modifying filesystem.

Useful Links
------------

- https://github.com/webpro/awesome-dotfiles
- http://dotfiles.github.io/
- https://www.gnu.org/software/stow/
- http://brandon.invergo.net/news/2012-05-26-using-gnu-stow-to-manage-your-dotfiles.html
- https://taihen.org/managing-dotfiles-with-gnu-stow/
- https://github.com/barryclark/bashstrap

.. _Homebrew: http://brew.sh/
.. _virtualenvwrapper: https://virtualenvwrapper.readthedocs.org/en/latest/
.. _GitHub does dotfiles: https://dotfiles.github.io/
.. _`Mathias Bynens' dotfiles`: https://github.com/mathiasbynens/dotfiles
.. _`Louis' fork of Mathias' dotfiles`: https://github.com/ltiao/dotfiles
