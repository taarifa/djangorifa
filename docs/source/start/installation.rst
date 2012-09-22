############
Installation
############

This installation assumes you are slightly familiar with Django and Python. There is an install script in the root directory of the download. This will automatically install the requirements listed below (although version numbers may be wrong if this is installed after a version upgrade). In order to run this script, please read the information provided below specific for your operating system.

************
Requirements
************
* `Python`_ 2.6+
* `python-dev`
* `libjpeg`
* `postgresql`_ 9.1.4
* `postgis`_ 1.5.3
* `RabbitMQ`_ 2.5.0
* `psycopg2`_ 2.4.5
* `Django`_ 1.4
* `South`_ 0.76
* `PIL`
* `django-admin-tools`_ 0.4.1
* `django-sekizai`_ 0.6.1
* `Celery`_ 3.0.5
* `django-celery`_ 3.0.4
* `kombu`_ 2.4.3
* `django-mailer`_ 0.1.0
* `django-registration`_ 0.8.0
* `django-extensions`_ 0.9
* `django_nose`_ 1.1.0
* `django_mobile`_ 0.2.3
* `django-crispy-forms`_ 1.2.0
* `django-generic-m2m`_ (version unknown)
* `django-sendsms`_ 0.2.2
* `django-sekizai`_ 0.6.1
* `pillow`

All Systems
===========

When emails and SMS messages are sent, it will take too much server resource and not have enough feedback to send as soon as the user requests. All mails and SMSs are therefore placed in a queue and that queue sends mail in bulk. Celery and RabbitMQ are used for this. If Kombu is *not* version 2.4.3, when starting the Celery server, the error "No such transport: amqp" will occur.

The installation script assumes you are working in a virtualenv. Therefore, create a virtualenv.

Please see below for specific installation instructions for your platform.

On Ubuntu
=========
This installation assumes you have already installed postgresql and postgis. For detailed instructions on how to do this, look at the Django reference https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/#ubuntu. Installation code: (read stuff below as well)

.. code-block:: bash

  $ sudo apt-get install python-dev python-setuptools python-pip
  $ sudo apt-get install libjpeg62 libjpeg62-dev zlib1g-dev libfreetype6 libfreetype6-dev
  $ sudo pip install virtualenv
  $ sudo apt-get install virtualenvwrapper

If you install virtualenvwrapper via pip you need to export some variables (see details here http://virtualenvwrapper.readthedocs.org/). However, if you used apt (as above) this is not necessary. Once virtualenvwrapper is installed, starting a new bash shell (or logging in and logging out again) should create the necessary wrapper scripts. So note this will not be triggered if you use a different shell like zsh.

.. code-block:: bash

  # Change Envs to whatever you like, the default is ~/.virtualenvs
  $ export WORKON_HOME=~/Envs
  $ source /usr/local/bin/virtualenvwrapper.sh

  # navigate to the directory where you'll checkout djangorifa
  $ cd /my/git/projects
  # create the virtualenv and clone the repo
  $ mkvirtualenv --no-site-packages djangorifa
  $ git clone https://github.com/cazcazn/djangorifa.git
  $ cd djangorifa

  # now edit the django settings file
  $ vim djangorifa/django_config/settings.py

  # Change the database password from facebook to whatever you want to use
  # also change the SECRET_KEY. Exit vim.

The source comes with a database installation script. This script will create the template_postgis template if it doesn't already exist and a postgresql user (or role) called djangorifa.
Once the user is created, a database will be created also named djangorifa.

The script does no checking for whether or not the version of PostGIS is correct (>= 1.5), so run incorrectly at your peril.

.. code-block:: bash

  # To run it first change to the postgres user. Make sure you have installed postgis before doing this!
  # The script will prompt you for a password, use whatever you put in the settings.py file.
  $ chmod 777 install_database.sh
  $ sudo su - postgres
  $ cd /my/git/projects/djangorifa
  $ ./install_database.sh
  $ exit

  # go back the respository directory
  $ cd /my/git/projects/djangorifa

There is also an install_django_stuff.sh script (TODO: this should be replaced by the standard setup.py script eventually). The script will use pip to pull in all the necessary python package dependencies and this will take a while. If you installed all the required dependencies via apt (see above) this should finish without error.

The script then initializes the django database and any migrations. This will prompt for an admin username and password for administrative control of the website. Pick whatever you like.

.. code-block:: bash

  # run the install_django_stuff script
  $ chmod 777 install_django_stuff.sh
  $ ./install_django_stuff.sh

  # if that finishes without error, start the django server
  $ python djangorifa/manage.py runserver

Then open a browser at 127.0.0.1:8000 and run through the setup. In the second step select a polygon around Tanzania and in the 3rd step upload the tandale.osm file from the taarifa_config directory.


On Mac
======
This installation assumes you have already installed postgresql and postgis. For detailed instructions on how to do this, look at the Django reference https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/#macosx.

I assume that the script runs virtually the same for a Mac user as a Linux user, but not having a Mac I cannot test this.

On Windows
==========
Yeah. Change OS.

.. _Python: http://www.python.org
.. _postgresql: http://www.postgresql.org/
.. _postgis: http://postgis.refractions.net/
.. _RabbitMQ: http://www.rabbitmq.com/
.. _psycopg2: http://initd.org/psycopg/
.. _Django: http://www.djangoproject.com
.. _South: http://south.aeracode.org/
.. _django-sekizai: https://github.com/ojii/django-sekizai/
.. _django-admin-tools: https://bitbucket.org/izi/django-admin-tools/
.. _Celery: http://celeryproject.org/
.. _django-celery: https://github.com/celery/django-celery
.. _django-mailer: http://code.google.com/p/django-mailer/
.. _django-registration: https://bitbucket.org/ubernostrum/django-registration/
.. _django-extensions: https://github.com/django-extensions/django-extensions
.. _django-filter-actually-maintained: https://github.com/subsume/django-filter-actually-maintained
.. _django_nose: https://github.com/jbalogh/django-nose/
.. _django_mobile: https://github.com/gregmuellegger/django-mobile
.. _django-crispy-forms: https://github.com/maraujop/django-crispy-forms/
.. _django-generic-m2m: https://github.com/coleifer/django-generic-m2m
.. _django-sendsms: https://github.com/stefanfoulis/django-sendsms


###########
Known IssueS
############
It might be that when running the second install script, there is a complaint when creating a superuser to do with decoding. When Django doesn't know what the locale is, it throws a hissy. This is a known bug: https://code.djangoproject.com/ticket/16017. Simply export the locale and run the second script again: export LC_ALL="en_US.UTF-8".

If you have problems with PostGIS not being available or something similar, see http://stackoverflow.com/questions/8459361/postgis-install
