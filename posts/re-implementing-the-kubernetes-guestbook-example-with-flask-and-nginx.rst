.. title: Re-implementing the Kubernetes Guestbook Example with Flask and NGINX
.. slug: re-implementing-the-kubernetes-guestbook-example-with-flask-and-nginx
.. date: 2016-05-25 14:10:00 UTC+10:00
.. tags: kubernetes, docker, flask, nginx, uwsgi, html, angularjs, redis
.. category: 
.. link: 
.. description: 
.. type: text

The official Kubernetes_ `walkthrough guides`_ often points to the `guestbook
application`_ as a quintessential example of how a simple, but complete multi-tier 
web application can be deployed with Kubernetes. As described in the README_, it
consists of a web frontend, a redis master (for storage), and a replicated set of 
redis 'slaves'.

..  image:: //cloud.google.com/container-engine/images/guestbook.png
    :align: center

This seemed like an ideal starting point for deploying my Flask_ applications 
with a similar stack, and also makes use of redis master/slaves. The difficulty 
I found with readily making use of this example as a starting point is that the 
frontend is implemented in PHP, which is considerably different to modern paradigms
(Node.js, Flask/Django, Rails, etc.) As described in the README:

    A frontend pod is a simple PHP server that is configured to talk to either 
    the slave or master services, depending on whether the client request is a 
    read or a write. It exposes a simple AJAX interface, and serves an 
    Angular-based UX. Again we'll create a set of replicated frontend pods 
    instantiated by a Deployment — this time, with three replicas.

I figured re-implementing the frontend pod in with Flask would require minimal 
changes - the UI would remain mostly the same, and the actual interaction with 
the redis master/slaves is quite trivial. 

.. TEASER_END

Perhaps the biggest challenge is that the PHP server can be served with a HTTP 
server (the example uses Apache), alongside the static assets (``index.html``, 
``controller.js``, etc.) while Flask will require a `WSGI server`_, in addition 
to a HTTP/reverse proxy server. This means the frontend pod will have multiple 
containers. A common practice for deploying Flask applications is to use uWSGI_ 
as the WSGI server with NGINX_ as the reverse proxy. 

First we fork from the `official Kubernetes repo`_ and create an exact copy of 
the guestbook example:

..  code:: console
    
    $ git clone https://github.com/ltiao/kubernetes
    $ cd kubernetes/examples/
    $ cp -r guestbook guestbook-flask

The current directory structure looks like this:

..  code:: console

    $ tree guestbook-flask
    guestbook-flask
    ├── README.md
    ├── all-in-one
    │   ├── frontend.yaml
    │   ├── guestbook-all-in-one.yaml
    │   └── redis-slave.yaml
    ├── frontend-deployment.yaml
    ├── frontend-service.yaml
    ├── legacy
    │   ├── frontend-controller.yaml
    │   ├── redis-master-controller.yaml
    │   └── redis-slave-controller.yaml
    ├── php-redis
    │   ├── Dockerfile
    │   ├── controllers.js
    │   ├── guestbook.php
    │   └── index.html
    ├── redis-master-deployment.yaml
    ├── redis-master-service.yaml
    ├── redis-slave
    │   ├── Dockerfile
    │   └── run.sh
    ├── redis-slave-deployment.yaml
    └── redis-slave-service.yaml

    4 directories, 19 files

Let's track these files:

..  code:: console

    $ git add guestbook-flask/

.. _official Kubernetes repo: https://github.com/kubernetes/kubernetes

Reverse Proxy Server (NGINX) Container
--------------------------------------

We begin by setting up the reverse proxy server container. Let's create a 
new directory for the files associated with this container.

..  code:: console

    $ mkdir guestbook-flask/nginx

index.html
''''''''''

The ``index.html`` page can remain exactly the same. We can just copy this directly:

..  code:: console

    $ cp guestbook/php-redis/index.html guestbook-flask/nginx/index.html

controllers.js
''''''''''''''

The ``controllers.js`` file just needs to be modified slightly:

..  code:: console

    $ cp guestbook/php-redis/controllers.js guestbook-flask/nginx/controllers.js

Since we are doing away with PHP, the HTTP endpoint URLs just need to be updated.
I simply update ``guestbook.php`` to ``guestbook/`` (in the subsequent section, 
we will set up the Flask routes and NGINX location blocks to be consistent with 
this):

..  code:: console

    $ diff -u guestbook/php-redis/controllers.js guestbook-flask/nginx/controllers.js

..  code:: diff

    --- guestbook/php-redis/controllers.js  2016-06-02 14:01:30.000000000 +1000
    +++ guestbook-flask/nginx/controllers.js    2016-06-02 14:45:10.000000000 +1000
    @@ -9,7 +9,7 @@
         this.scope_.messages.push(this.scope_.msg);
         this.scope_.msg = "";
         var value = this.scope_.messages.join();
    -    this.http_.get("guestbook.php?cmd=set&key=messages&value=" + value)
    +    this.http_.get("guestbook/?cmd=set&key=messages&value=" + value)
                 .success(angular.bind(this, function(data) {
                     this.scope_.redisResponse = "Updated.";
                 }));
    @@ -21,7 +21,7 @@
             $scope.controller.location_ = $location;
             $scope.controller.http_ = $http;

    -        $scope.controller.http_.get("guestbook.php?cmd=get&key=messages")
    +        $scope.controller.http_.get("guestbook/?cmd=get&key=messages")
                 .success(function(data) {
                     console.log(data);
                     $scope.messages = data.data.split(",");

nginx.conf
''''''''''

We create a minimal NGINX configuration which serves the static assets at `/` 
(``index.html``, ``controllers.js``) and proxies requests at `/guestbook/` to
an upstream uWSGI server (``127.0.0.1:8080``) defined in subsequent sections.

..  code:: console

    $ vim guestbook-flask/nginx/nginx.conf

..  code:: nginx

    worker_processes 1;

    events {

        worker_connections 1024;
    }

    http {

        sendfile on;

        client_max_body_size    2000M;

        # Configuration containing list of application servers
        upstream uwsgicluster {

            server 127.0.0.1:8080;
        }

        # Configuration for Nginx
        server {

            # Running port
            listen 80;

            location / {

                root html;
                index index.html;
            }

            # Proxying connections to application servers
            location /guestbook/ {

                include uwsgi_params;
                uwsgi_pass uwsgicluster;

                uwsgi_param Host $host;
                uwsgi_param X-Real-IP $remote_addr;
                uwsgi_param X-Forwarded-For $proxy_add_x_forwarded_for;
                uwsgi_param X-Forwarded-Proto $http_x_forwarded_proto;
            }
        }
    }

Some useful guides on configuring Nginx as an application gateway with uWSGI and
Python WSGI applications:

- `Using NGINX as an application gateway with uWSGI and Django <https://www.nginx.com/resources/admin-guide/gateway-uwsgi-django/>`_ 
- `Setting up Django and your web server with uWSGI and nginx <http://uwsgi.readthedocs.io/en/latest/tutorials/Django_and_nginx.html>`_
- `How to Deploy Python WSGI Applications Using uWSGI Web Server with Nginx <https://www.digitalocean.com/community/tutorials/how-to-deploy-python-wsgi-applications-using-uwsgi-web-server-with-nginx>`_

Note that some of these guides are specifically aimed at deploying Django, but
it is actually even easier to modify it to work for Flask.

Dockerfile
''''''''''

Finally, we create the Dockerfile for our image and use the `official nginx base 
image`_. All that needs to be done is copy our NGINX configuration file to the
primary configuration location (``/etc/nginx/nginx.conf``) and all static assets
(``index.html``, ``controllers.js``) to ``/etc/nginx/html/``:

..  code:: console

    $ vim guestbook-flask/nginx/Dockerfile

..  code:: docker

    FROM nginx:latest

    COPY nginx.conf /etc/nginx/nginx.conf
    COPY index.html controllers.js /etc/nginx/html/

See the official nginx base image documentation for more information on how to 
fully leverage this image, and `How to Configure Nginx <https://www.linode.com/docs/websites/nginx/how-to-configure-nginx>`_ 
for more information on NGINX configuration files.

Before moving on, let's track our additions:

..  code:: console

    $ git add guestbook-flask/nginx/

Now we build and push the image:

..  code:: console

    $ docker build -t tiao/gb-frontend-nginx guestbook-flask/nginx
    $ docker push tiao/gb-frontend-nginx

While the WSGI server is not yet ready, we can still run the container as a 
sanity test to make sure the static files are being served correctly:

..  code:: console

    $ docker run -d -p 80:80 tiao/gb-frontend-nginx

Now you should be able to see the guestbook UI at ``http://$(docker-machine ip):80``:

..  thumbnail:: ../../images/guestbook.png
    :align: center

Of course, the form and the 'Submit' button won't do anything useful... just yet. 

The Flask/uWSGI Container
-------------------------

Now we re-implement the server that interacts with redis in Flask. First, let's 
create a new directory for the files associated with this container.

..  code:: console

    $ mkdir guestbook-flask/flask-redis

requirements.txt
''''''''''''''''

To run Flask with uWSGI in our container, we just need to install ``flask`` and 
``uwsgi`` from PyPI. The only other Python package our Flask app depends on is 
`redis-py`_ (simply redis_ on PyPI_):

..  code:: console

    $ vim guestbook-flask/flask-redis/requirements.txt

..  code::

    flask
    uwsgi
    redis

.. _PyPI: https://pypi.python.org/
.. _redis: https://pypi.python.org/pypi/redis
.. _redis-py: https://redis-py.readthedocs.io/en/latest/

app.py
''''''

Our Flask app re-implements the PHP server (``guestbook.php``), which handles
requests and interacts with the redis master and slaves. The only supported route
is ``GET`` requests to ``/guestbook/``.

..  code:: console

    $ vim guestbook-flask/flask-redis/app.py

..  code:: python

    from flask import Flask, jsonify, request
    from redis import StrictRedis

    import os


    app = Flask(__name__)


    @app.route('/guestbook/')
    def redis():

        if 'cmd' in request.args:

            host = 'redis-master'
            if os.environ.get('GET_HOSTS_FROM') == 'env':
                host = os.environ.get('REDIS_MASTER_SERVICE_HOST')

            if request.args.get('cmd') == 'set':

                r = StrictRedis(host=host, port=6379)
                r.set(request.args.get('key'), request.args.get('value'))
                return jsonify(message='Updated')

            else:

                host = 'redis-slave'
                if os.environ.get('GET_HOSTS_FROM') == 'env':
                    host = os.environ.get('REDIS_SLAVE_SERVICE_HOST')

                r = StrictRedis(host=host, port=6379)
                value = r.get(request.args.get('key')) or b''
                return jsonify(data=value.decode('utf-8'))

For brevity, and also in the interest of remaining faithful to the original 
implementation, we intentionally omit any robust error handling. Just be aware 
that the above code will fail spectacularly in all sorts of cases (e.g. ``GET`` 
requests without queries), but so would the original ``guestbook.php``. It is 
only guaranteed to work correctly with the AngularJS controller 
(``controllers.js``) defined previously.

conf.ini
''''''''

Create and edit the uWSGI configuration file:

..  code:: console

    $ vim guestbook-flask/flask-redis/conf.ini

..  code:: ini

    [uwsgi]
    socket = :8080
    wsgi-file = app.py
    callable = app
    master = true
    processes = 4
    threads = 2

Refer to the `uWSGI documentation <https://uwsgi-docs.readthedocs.io/en/latest/WSGIquickstart.html#deploying-flask>`_ for more information on these settings.

Dockerfile
''''''''''

Finally, we create and edit the Dockerfile for this image:

..  code:: console

    $ vim guestbook-flask/flask-redis/Dockerfile

..  code:: docker

    FROM python:3.5.1-onbuild

    EXPOSE 8080
    CMD ["uwsgi", "--ini", "conf.ini"]

This image uses the `onbuild variant`_ of the `official Python image`_, which 
automatically copies our files (``app.py``, ``requirements.txt``, ``conf.ini``)
to the image, and uses ``pip`` to install the requirements. For more information
about the ``ONBUILD`` command please see the `Dockerfile reference`_.

Before moving on, let's track our additions:

..  code:: console

    $ git add guestbook-flask/flask-redis/

Like before, we build and push the image:

..  code:: console

    $ docker build -t tiao/gb-frontend-flask-redis guestbook-flask/flask-redis
    $ docker push tiao/gb-frontend-flask-redis

There is no point in running it as a sanity test, as none of the redis masters 
or slaves will exist, and because there is no error handling, everything will 
just crash immediately.

.. _official Python image: https://hub.docker.com/_/python/
.. _onbuild variant: https://github.com/docker-library/python/blob/0fa3202789648132971160f686f5a37595108f44/3.5/onbuild/Dockerfile
.. _Dockerfile reference: https://docs.docker.com/engine/reference/builder/#onbuild

Updating the Frontend Deployment
--------------------------------

Lastly, we modify the frontend Deployment to replace the existing container in 
the frontend Pod with the containers we just created and pushed.

..  code:: console

    $ vim guestbook-flask/frontend-deployment.yaml

Under ``.spec.template.spec.containers``, add the following containers:

..  code:: yaml

    containers:
    - name: flask-redis
      image: tiao/gb-frontend-flask-redis
      resources:
        requests:
          cpu: 100m
          memory: 100Mi
      env:
      - name: GET_HOSTS_FROM
        value: dns
        # If your cluster config does not include a dns service, then to
        # instead access environment variables to find service host
        # info, comment out the 'value: dns' line above, and uncomment the
        # line below.
        # value: env
      ports:
      - containerPort: 8080
    - name: nginx
      image: tiao/gb-frontend-nginx
      ports:
      - containerPort: 80

The change should look exactly like this: 

..  code:: diff

    --- guestbook/frontend-deployment.yaml  2016-06-02 14:01:30.000000000 +1000
    +++ guestbook-flask/frontend-deployment.yaml    2016-06-02 16:56:24.000000000 +1000
    @@ -24,8 +24,8 @@
             tier: frontend
         spec:
           containers:
    -      - name: php-redis
    -        image: gcr.io/google-samples/gb-frontend:v4
    +      - name: flask-redis
    +        image: tiao/gb-frontend-flask-redis
             resources:
               requests:
                 cpu: 100m
    @@ -39,4 +39,8 @@
               # line below.
               # value: env
             ports:
    +        - containerPort: 8080
    +      - name: nginx
    +        image: tiao/gb-frontend-nginx
    +        ports:
             - containerPort: 80

We also update the "all-in-one" variants of these configurations in exactly the 
same way:

..  code:: console

    $ vim guestbook-flask/all-in-one/frontend.yaml
    $ vim guestbook-flask/all-in-one/guestbook-all-in-one.yaml

At last, we can create all related Deployments and Services:

..  code:: console

    $ kubectl create -f guestbook-flask
    deployment "frontend" created
    service "frontend" created
    deployment "redis-master" created
    service "redis-master" created
    deployment "redis-slave" created
    service "redis-slave" created

Now you should be able to see a live, running Guestbook example with functionality 
and behavior identical to that of the original PHP implementation.

Wrapping Up
-----------

Time wrap things up. First, let's delete the Deployments and Services:

..  code:: console

    $ kubectl delete -f guestbook-flask
    deployment "frontend" deleted
    service "frontend" deleted
    deployment "redis-master" deleted
    service "redis-master" deleted
    deployment "redis-slave" deleted
    service "redis-slave" deleted

We can get rid of the PHP server, and other irrelevant legacy stuff:

..  code:: console

    $ rm -r guestbook-flask/legacy guestbook-flask/php-redis

At this point, the directory structure should look like this:

..  code:: console

    $ tree guestbook-flask
    guestbook-flask
    ├── README.md
    ├── all-in-one
    │   ├── frontend.yaml
    │   ├── guestbook-all-in-one.yaml
    │   └── redis-slave.yaml
    ├── flask-redis
    │   ├── Dockerfile
    │   ├── app.py
    │   ├── conf.ini
    │   └── requirements.txt
    ├── frontend-deployment.yaml
    ├── frontend-service.yaml
    ├── nginx
    │   ├── Dockerfile
    │   ├── controllers.js
    │   ├── index.html
    │   └── nginx.conf
    ├── redis-master-deployment.yaml
    ├── redis-master-service.yaml
    ├── redis-slave
    │   ├── Dockerfile
    │   └── run.sh
    ├── redis-slave-deployment.yaml
    └── redis-slave-service.yaml

    4 directories, 20 files

We can commit our changes and push to the fork:

..  code:: console

    $ git commit -am 'Re-implemented Guestbook example with Flask/uWSGI/NGINX'
    $ git push origin master

At some point, if deemed useful by the Kubernetes Development Team and Community, 
I will submit a pull request to incorporate this into the ``examples`` directory. 
For now, you can clone `my fork <https://github.com/ltiao/kubernetes>`_ if you 
wish to tinker with this example.

.. _Kubernetes: http://kubernetes.io/
.. _guestbook application: https://github.com/kubernetes/kubernetes/tree/master/examples/guestbook
.. _walkthrough guides: http://kubernetes.io/docs/user-guide/walkthrough/
.. _README: https://github.com/kubernetes/kubernetes/blob/master/examples/guestbook/README.md
.. _Flask: http://flask.pocoo.org/
.. _WSGI server: https://www.fullstackpython.com/wsgi-servers.html
.. _uWSGI: https://uwsgi-docs.readthedocs.io/en/latest/
.. _NGINX: https://nginx.org/en/
.. _official nginx base image: https://hub.docker.com/_/nginx/
