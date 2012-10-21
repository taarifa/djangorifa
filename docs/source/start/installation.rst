############
Installation
############

This installation assumes you are slightly familiar with Django and Python.
There is an install script in the root directory of the download. This will
automatically install the requirements listed below (although version numbers
may be wrong if this is installed after a version upgrade). In order to run
this script, please read the information provided below specific for your
operating system.

************
Requirements
************
* `Python`_ 2.6+
* `python-dev`
* `libjpeg`
* `postgresql`_ 9.1+
* `postgis`_ 1.5+
* `pytz`_
* `RabbitMQ`_
* `psycopg2`_
* `Django`_ 1.4+
* `South`_
* `PIL`_
* `django-admin-tools`_
* `django-sekizai`_
* `Celery`_
* `django-celery`_
* `kombu`_
* `django-mailer`_
* `django-registration`_
* `django-extensions`_
* `django_nose`_
* `django_mobile`_
* `django-crispy-forms`_
* `django-generic-m2m`_
* `django-sendsms`_
* `django-sekizai`_
* `pillow`_
* `pycurl`_

All Systems
===========

When emails and SMS messages are sent, it will take too much server resource
and not have enough feedback to send as soon as the user requests. All mails
and SMSs are therefore placed in a queue and that queue sends mail in bulk.
Celery and RabbitMQ are used for this.

The installation script assumes you are working in a virtualenv. Therefore,
create a virtualenv.

Please see below for specific installation instructions for your platform, and
then see the instructions for RabbitMQ.

On Ubuntu
=========

This installation assumes you have already installed postgresql and postgis.
For detailed instructions on how to do this, look at the `Django Ubuntu postgis
installation guide`_.

Installation code: (read stuff below as well)

.. _Django Ubuntu postgis installation guide: https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/#ubuntu

.. code-block:: bash

  $ sudo apt-get install python-dev python-setuptools python-pip
  $ sudo apt-get install libjpeg62 libjpeg62-dev zlib1g-dev libfreetype6 libfreetype6-dev libcurl4-gnutls-dev
  $ sudo pip install virtualenv
  $ sudo apt-get install virtualenvwrapper

If you install virtualenvwrapper via pip you need to export some variables
(see the `virtualenvwrapper docs`_). However, if you used apt (as above) this
is not necessary. Once virtualenvwrapper is installed, starting a new bash
shell (or logging in and logging out again) should create the necessary
wrapper scripts. So note this will not be triggered if you use a different
shell like zsh.

.. _virtualenvwrapper docs: http://virtualenvwrapper.readthedocs.org/

.. code-block:: bash

  # Change Envs to whatever you like, the default is ~/.virtualenvs
  # This is only necessary if you pip installed virtualenvwrapper
  $ export WORKON_HOME=~/Envs
  $ source /usr/local/bin/virtualenvwrapper.sh

  # navigate to the directory where you'll checkout djangorifa
  $ cd /my/git/projects
  # create the virtualenv and clone the repo
  $ mkvirtualenv --no-site-packages djangorifa
  $ git clone https://github.com/taarifa/djangorifa.git
  $ cd djangorifa

  # now edit the django settings file
  $ vim djangorifa/django_config/settings.py

  # Change the database password from facebook to whatever you want to use
  # also change the SECRET_KEY. Exit vim.

The source comes with a database installation script. This script will create
the template_postgis template if it doesn't already exist and a postgresql
user (or role) called djangorifa.

Once the user is created, a database will be created also named djangorifa.

The script does no checking for whether or not the version of PostGIS is
correct (>= 1.5), so run incorrectly at your peril.

.. code-block:: bash

  # To run it first change to the postgres user. Make sure you have installed postgis before doing this!
  # The script will prompt you for a password, use whatever you put in the settings.py file.
  $ sudo su - postgres
  $ cd /my/git/projects/djangorifa
  $ ./install_database.sh
  $ exit

  # go back the respository directory
  $ cd /my/git/projects/djangorifa

To verify PostGIS is working, run the following as the *postgres* user:

.. code-block:: bash

  $ psql djangorifa
  djangorifa=# SELECT PostGIS_full_version();

You should see output like

.. code-block:: bash

  POSTGIS="1.5.3" GEOS="3.2.2-CAPI-1.6.2" PROJ="Rel. 4.7.1, 23 September 2009" LIBXML="2.7.8" USE_STATS

There is also an ``install_django_stuff.sh`` script (TODO: this should be
replaced by the standard setup.py script eventually). The script will use pip
to pull in all the necessary python package dependencies and this will take a
while.  If you installed all the required dependencies via apt (see above)
this should finish without error.

The script then initializes the django database and any migrations. This will
prompt for an admin username and password for administrative control of the
website. Pick whatever you like.

.. code-block:: bash

  # run the install_django_stuff script
  $ ./install_django_stuff.sh

  # if that finishes without error, start the django server
  $ python djangorifa/manage.py runserver

Then open a browser at ``localhost:8000`` and run through the setup. In the
second step select a polygon around Tandale (zoom in to Dar es Salaam on the
east coast of Tanzania) and in the 3rd step upload the ``tandale.osm`` file
from the ``taarifa_config`` directory.

On Mac
======

This installation assumes you have already installed postgresql and postgis.
For detailed instructions on how to do this, look at the `Django Mac postgis
installation guide`_.

.. _Django Mac postgis installation guide: https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/#macosx

I assume that the script runs virtually the same for a Mac user as a Linux
user, but not having a Mac I cannot test this.

On Windows
==========

Yeah. Change OS.

.. _Python: http://www.python.org
.. _postgresql: http://www.postgresql.org/
.. _postgis: http://postgis.refractions.net/
.. _pytz: https://launchpad.net/pytz
.. _RabbitMQ: http://www.rabbitmq.com/
.. _psycopg2: http://initd.org/psycopg/
.. _Django: http://www.djangoproject.com
.. _South: http://south.aeracode.org/
.. _PIL: http://www.pythonware.com/products/pil
.. _django-sekizai: https://github.com/ojii/django-sekizai/
.. _django-admin-tools: https://bitbucket.org/izi/django-admin-tools/
.. _Celery: http://celeryproject.org/
.. _django-celery: https://github.com/celery/django-celery
.. _kombu: http://github.com/celery/kombu
.. _django-mailer: http://code.google.com/p/django-mailer/
.. _django-registration: https://bitbucket.org/ubernostrum/django-registration/
.. _django-extensions: https://github.com/django-extensions/django-extensions
.. _django-filter-actually-maintained: https://github.com/subsume/django-filter-actually-maintained
.. _django_nose: https://github.com/jbalogh/django-nose/
.. _django_mobile: https://github.com/gregmuellegger/django-mobile
.. _django-crispy-forms: https://github.com/maraujop/django-crispy-forms/
.. _django-generic-m2m: https://github.com/coleifer/django-generic-m2m
.. _django-sendsms: https://github.com/stefanfoulis/django-sendsms
.. _pillow: https://github.com/python-imaging/Pillow
.. _pycurl: http://pycurl.sourceforge.net/

########
RabbitMQ
########

Install the RabbitMQ server (on Ubuntu):

.. code-block:: bash
  $ sudo apt-get install rabbitmq-server

Once RabbitMQ and Celery are installed, issue the following commands:

.. code-block:: bash

  $ sudo rabbitmqctl add_user myuser mypassword
  $ sudo rabbitmqctl add_vhost myvhost
  $ sudo rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"

where myuser, mypassword and myvhost are your choice. Update these in the
``django_config/settings`` file as ``BROKER_VHOST``, ``BROKER_USER`` and
``BROKER_PASSWORD`` respectively. To test this works:

.. code-block:: bash

  $ python manage.py celeryd -l INFO

If this returns no red error messages, you're sorted!

To daemonize celery, you need to download the `celery daemon`_ and save to
``/etc/init.d/celeryd``. A config file can be found in the examples section of
the repo. Copy this to ``/etc/default/celeryd``.

.. _celery daemon: https://raw.github.com/celery/celery/master/extra/generic-init.d/celeryd

.. code-block:: bash

  $ sudo useradd celery
  $ mkdir /var/log/celery
  $ mkdir /var/run/celery
  $ sudo chown celery:celery /var/log/celery
  $ sudo chown celery:celery /var/run/celery
  $ sudo chmod +x /etc/init.d/celeryd
  $ sudo /etc/init.d/celeryd start

############
Known Issues
############

Celery needs a matching version of Kombu. Celery 3.0.6 is known to work with
Kombu 2.4.3, 3.0.11 with 2.4.7. If the versions don't match the error ``No
such transport: amqp`` will occur when starting the Celery server.

It might be that when running the second install script, there is a complaint
when creating a superuser to do with decoding. When Django doesn't know what
the locale is, it throws a hissy. This is a `known bug`_.  Simply export the
locale and run the second script again: ``export LC_ALL="en_US.UTF-8"``.

.. _known bug: https://code.djangoproject.com/ticket/16017

If you have problems with PostGIS not being available or something similar,
see http://stackoverflow.com/questions/8459361/postgis-install
