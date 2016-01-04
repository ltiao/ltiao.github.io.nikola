.. title: Python SimpleHTTPServer Recipe: Serve specific directory
.. slug: python-simplehttpserver-recipe-serve-specific-directory
.. date: 2015-12-10 17:38:27 UTC+11:00
.. tags: python
.. category: coding
.. link: 
.. description: 
.. type: text

- We need to be able to pass the path to the root of the directory tree we wish 
  to serve. 
- We can only pass arguments to the ``ServerClass`` and not ``HandlerClass``.
  Note however that ``HandlerClass`` is passed as an argument to ``ServerClass``
  so we should be able to propagate the argument to ``HandlerClass``.
- The ``translate_path`` method of ``SimpleHTTPRequestHandler`` takes the 
  ``/``-separated path specified in the URL and prepends ``os.getcwd()`` to it.
  We just have to instead prepend the  argument we propagated to 
  ``SimpleHTTPRequestHandler``.
- Lastly we modify the ``test`` function to take multiple optional arguments 
  (port and base path) using the excellent module ``argparse``.

.. TEASER_END

.. code:: python

    #! /usr/bin/env python

    import posixpath
    import argparse
    import urllib
    import os

    from SimpleHTTPServer import SimpleHTTPRequestHandler
    from BaseHTTPServer import HTTPServer


    class RootedHTTPServer(HTTPServer):

        def __init__(self, base_path, *args, **kwargs):
            HTTPServer.__init__(self, *args, **kwargs)
            self.RequestHandlerClass.base_path = base_path


    class RootedHTTPRequestHandler(SimpleHTTPRequestHandler):

        def translate_path(self, path):
            path = posixpath.normpath(urllib.unquote(path))
            words = path.split('/')
            words = filter(None, words)
            path = self.base_path
            for word in words:
                drive, word = os.path.splitdrive(word)
                head, word = os.path.split(word)
                if word in (os.curdir, os.pardir):
                    continue
                path = os.path.join(path, word)
            return path


    def test(HandlerClass=RootedHTTPRequestHandler, ServerClass=RootedHTTPServer):

        parser = argparse.ArgumentParser()
        parser.add_argument('--port', '-p', default=8000, type=int)
        parser.add_argument('--dir', '-d', default=os.getcwd(), type=str)
        args = parser.parse_args()

        server_address = ('', args.port)

        httpd = ServerClass(args.dir, server_address, HandlerClass)

        sa = httpd.socket.getsockname()
        print "Serving HTTP on", sa[0], "port", sa[1], "..."
        httpd.serve_forever()

    if __name__ == '__main__':
        test()


.. code:: console

   $ python server.py ~/Documents

.. code:: console

   $ python server.py ~/Documents 5000

.. _SocketServer: http://svn.python.org/projects/python/trunk/Lib/SocketServer.py
.. _BaseHTTPServer: http://svn.python.org/projects/python/trunk/Lib/BaseHTTPServer.py
.. _SimpleHTTPServer: http://svn.python.org/projects/python/trunk/Lib/SimpleHTTPServer.py
