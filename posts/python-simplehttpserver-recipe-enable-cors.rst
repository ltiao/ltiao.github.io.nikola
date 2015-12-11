.. title: Python SimpleHTTPServer Recipe: Enable CORS
.. slug: python-simplehttpserver-recipe-enable-cors
.. date: 2015-12-10 15:56:08 UTC+11:00
.. tags: python, cors
.. category: coding
.. link: 
.. description: 
.. type: text

Create a file, let's call it ``cors_http_server.py``, with the code below:

.. code:: python

    #! /usr/bin/env python

    from SimpleHTTPServer import SimpleHTTPRequestHandler, test


    class CORSHTTPRequestHandler(SimpleHTTPRequestHandler):

        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            super(CORSHTTPRequestHandler, self).end_headers(self)

    if __name__ == '__main__':
        test(HandlerClass=CORSHTTPRequestHandler)

.. TEASER_END

Now we can start a server at ``0.0.0.0`` at port ``8000`` like so:

.. code:: console

    $ python cors_http_server.py
    Serving HTTP on 0.0.0.0 port 8000 ...

As with ``python -m SimpleHTTPServer``, we can specify a port as well:

.. code:: console

    $ python cors_http_server.py 5000
    Serving HTTP on 0.0.0.0 port 5000 ...

This server behaves exactly the same as ``SimpleHTTPServer``, except we send 
the extra header ``Access-Control-Allow-Origin: *`` to allow any origin to 
access the resource.

Further Resources
-----------------

- For more information on CORS, see `HTTP access control (CORS)`_.
- For a more robust version of this see (https://gist.github.com/enjalot/2904124).
- See this `StackOverflow answer`_ for some alternative solutions and other insights.

.. _HTTP access control (CORS): https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS
.. _StackOverflow answer: http://stackoverflow.com/questions/21956683/python-enable-access-control-on-simple-http-server
