.. title: Louis does dotfiles
.. slug: louis-does-dotfiles
.. date: 2016-02-12 22:59:46 UTC+11:00
.. tags: osx, dotfiles, git, github, gnu stow
.. category: coding
.. link: 
.. description: 
.. type: text

..  thumbnail:: ../../images/bash.png
    :align: center

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

.. TEASER_END

Getting Started
---------------

Instead of starting from scratch, I decided to bootstrap off an existing 
dotfile repo. From going through `GitHub does dotfiles`_, I found 
`Mathias Bynens' dotfiles`_ to be by far the most popular. Not only that, it 
seemed to offer the most sensible defaults for OSX. 

First, I created a fork (`Louis' fork of Mathias' dotfiles`_) and cloned it
locally. From several blog posts, I have found that some people like to clone 
to a directory under ``~``, such as ``~/dotfiles``. Personally, I like to 
clone it to a synchronized directory, such as ``~/Dropbox/dotfiles``, so that 
I can still easily access it anywhere that has an internet connection, even if
it is infeasible to install and use ``git``. 

Now we need to create symlinks to these dotfiles inside the home directory.
While you can do this manually, it can become cumbersome to manage should you 
decide to remove or update these symlinks in the future. Hence, it might be
worthwhile to consider using one of the dotfile mananagement utilities. After
trying out `rcm`_ [#]_, and giving serious consideration to a few others that 
seemed promising (`homesick`_, `dfm`_), I settled on `GNU Stow`_.

GNU Stow
--------

First, we install GNU Stow with Homebrew:

..  code:: console

    $ brew install stow

A few good places to get started with GNU Stow are `Using GNU Stow to manage 
your dotfiles`_ and `Managing Dotfiles with GNU Stow`_. Perhaps the most 
important thing to know is the terminology it uses. Specifically, what 
*package*, *target directory* and *stow directory* are. From the ``man`` page:

    A "package" is a related collection of files and directories that you wish
    to administer as a unit [...]

    A "target directory" is the root of a tree in which one or more packages 
    wish to appear to be installed. [...]

    A "stow directory" is the root of a tree containing separate packages in
    private subtrees. When Stow runs, it uses the current directory as the 
    default stow directory.

Note that by default, the target directory is the parent of the stow 
directory. 

Since our dotfiles reside in ``~/Dropbox/dotfiles``, for our purposes, the 
*stow directory* should be ``~/Dropbox`` and the *package* should be 
``dotfiles``. The *target directory* is the parent of the *stow directory*, 
which is ``~``, so no further modifications are required. 

Additionally, there are a few bash scripts (``bootstrap.sh``, ``brew.sh``) 
which we don't wish to symlink to from our home directory, so we want Stow to
ignore those.

It may be a good idea to see what Stow will do to your filesystem without 
actually making any modifications. To do this, we can use the flags 
``--simulate --verbose=1``.

Putting it all together, we have:

..  code:: console

    $ stow --ignore='(bootstrap.sh|brew.sh)' \
           --simulate --verbose=1 \
           --dir=$HOME/Dropbox/ dotfiles
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

If you're happy with this, go ahead and remove the ``simulate`` option and run 
again! That's it!

Useful Links
------------

- https://github.com/barryclark/bashstrap
- https://github.com/webpro/awesome-dotfiles

..  [#] `rcm`_ is lightweight and easy to install but the documentation and
        "tutorial" (which is actually just the ``man`` page) leaves much to be
        desired. However, the major deal-breaker for me was baffling fact that
        dotfiles prefixed with a dot are **ignored** 
        (http://thoughtbot.github.io/rcm/rcm.7.html):

            A less common situation is for all the filenames in your dotfiles 
            directory to be prefixed with a period. These files are skipped by 
            the rcm suite, and thus would result in nothing happening. The 
            only option in this case is to rename all the files

        which makes this tool worthless for people whose dotfiles begins with,
        well, a dot. Which is most people.

.. _Homebrew: http://brew.sh/
.. _virtualenvwrapper: https://virtualenvwrapper.readthedocs.org/en/latest/
.. _GitHub does dotfiles: https://dotfiles.github.io/
.. _Mathias Bynens' dotfiles: https://github.com/mathiasbynens/dotfiles
.. _Louis' fork of Mathias' dotfiles: https://github.com/ltiao/dotfiles
.. _rcm: https://robots.thoughtbot.com/rcm-for-rc-files-in-dotfiles-repos
.. _homesick: https://github.com/technicalpickles/homesick
.. _dfm: https://github.com/justone/dfm
.. _GNU Stow: https://www.gnu.org/software/stow/
.. _Using GNU Stow to manage your dotfiles: http://brandon.invergo.net/news/2012-05-26-using-gnu-stow-to-manage-your-dotfiles.html
.. _Managing Dotfiles with GNU Stow: https://taihen.org/managing-dotfiles-with-gnu-stow/
