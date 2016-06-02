.. title: Re-implementing the Kubernetes Guestbook Example with Flask and NGINX
.. slug: re-implementing-the-kubernetes-guestbook-example-with-flask-and-nginx
.. date: 2016-05-25 14:10:00 UTC+10:00
.. tags: kubernetes, docker, flask, nginx, uwsgi, html, angularjs, redis
.. category: 
.. link: 
.. description: 
.. type: text

The official Kubernetes_ `walkthrough guides`_ often point to the `guestbook
application`_ as a quintessential example of how a simple, but complete multi-tier 
web application can be deployed with Kubernetes. As described in the README_, it
consists of a web frontend, a redis master (for storage), and a replicated set of 
redis 'slaves'.

..  image:: //cloud.google.com/container-engine/images/guestbook.png
    :align: center

This seemed like an ideal starting point for deploying my Flask_ applications that
uses a similar stack, and also makes use of redis master/slaves. The difficulty 
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

First we create an exact copy of the guestbook example:

..  code:: console
    
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


Updating the Frontend Deployment
--------------------------------




..  code:: console

    $ gst
    On branch master
    Your branch is up-to-date with 'origin/master'.
    Changes to be committed:
      (use "git reset HEAD <file>..." to unstage)

        new file:   examples/guestbook/flask-redis/Dockerfile
        new file:   examples/guestbook/flask-redis/README.md
        new file:   examples/guestbook/flask-redis/app.py
        new file:   examples/guestbook/flask-redis/conf.ini
        new file:   examples/guestbook/flask-redis/requirements.txt
        new file:   examples/guestbook/nginx/Dockerfile
        new file:   examples/guestbook/nginx/controllers.js
        new file:   examples/guestbook/nginx/index.html
        new file:   examples/guestbook/nginx/nginx.conf

    Changes not staged for commit:
      (use "git add/rm <file>..." to update what will be committed)
      (use "git checkout -- <file>..." to discard changes in working directory)

        modified:   examples/guestbook/README.md
        modified:   examples/guestbook/all-in-one/frontend.yaml
        modified:   examples/guestbook/all-in-one/guestbook-all-in-one.yaml
        modified:   examples/guestbook/frontend-deployment.yaml
        modified:   examples/guestbook/frontend-service.yaml
        deleted:    examples/guestbook/legacy/frontend-controller.yaml
        deleted:    examples/guestbook/legacy/redis-master-controller.yaml
        deleted:    examples/guestbook/legacy/redis-slave-controller.yaml
        deleted:    examples/guestbook/php-redis/Dockerfile
        deleted:    examples/guestbook/php-redis/controllers.js
        deleted:    examples/guestbook/php-redis/guestbook.php
        deleted:    examples/guestbook/php-redis/index.html

The directory structure.

..  code:: console

    $ tree kubernetes/examples/guestbook
    kubernetes/examples/guestbook
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
    │   ├── README.md
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

    4 directories, 21 files

https://cloud.google.com/container-engine/docs/tutorials/guestbook

.. _Kubernetes: http://kubernetes.io/
.. _guestbook application: https://github.com/kubernetes/kubernetes/tree/master/examples/guestbook
.. _walkthrough guides: http://kubernetes.io/docs/user-guide/walkthrough/
.. _README: https://github.com/kubernetes/kubernetes/blob/master/examples/guestbook/README.md
.. _Flask: http://flask.pocoo.org/
.. _WSGI server: https://www.fullstackpython.com/wsgi-servers.html
.. _uWSGI: https://uwsgi-docs.readthedocs.io/en/latest/
.. _NGINX: https://nginx.org/en/
.. _official nginx base image: https://hub.docker.com/_/nginx/