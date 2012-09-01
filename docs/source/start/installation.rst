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
The installation script assumes you are working in a virtualenv. Therefore, create a virtualenv. Change directories to the virtualenv and clone this repo.

The Django settings file can be found at djangorifa/config/settings.py. At the top of this file is a python dictionary with database settings. In the password field it says 'change'. It is recommended you do as the settings say and change the string written there. There is no need to do anything else for installation - the automatic installation script will take care of setting up the database and everything else. Please see below for specific installation instructions for your platform.

Install `RabbitMQ`_.

On Ubuntu
=========
This installation assumes you have already installed postgresql and postgis. For detailed instructions on how to do this, look at the Django reference https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/#ubuntu. Installation code: (read stuff below as well)

.. code-block:: bash

  $ sudo apt-get install python-dev python-setuptools python-pip
  $ sudo apt-get install libjpeg62 libjpeg62-dev zlib1g-dev libfreetype6 libfreetype6-dev
  $ sudo pip install virtualenv
  $ sudo apt-get install virtualenvwrapper

  # Once virtualenvwrapper is installed, you need to export some variables
  # Change Envs to whatever you like.
  $ export WORKON_HOME=~/Envs
  $ source /usr/local/bin/virtualenvwrapper.sh

  $ cd /path/to/djangorifa
  $ mkvirtualenv --no-site-packages djangorifa
  $ cd djangorifa
  $ git clone https://github.com/cazcazn/djangorifa.git
  $ cd djangorifa
  $ vim djangorifa/django_config/settings.py

  # Change the password in the database settings, and also change the SECRET_KEY. Exit vim.
  $ sudo su - postgres
  $ cd /path/to/repo
  $ chmod 777 install_database.sh
  $ exit

  $ cd /path/to/repo
  $ chmod 777 install_django_stuff.sh
  $ ./install_django_stuff.sh
  $ input password same as for settings above
  # Wait.


There is a script in djangorifa called install_djangorifa.sh. This script will create the template_postgis template if it doesn't already exist and a postgresql user (or role) called djangorifa. The script will prompt you to enter a password for the role and to confirm it. The password you enter **must** be the same as the database password in the settings file, or the installation will fail.

Once the user is created, a database will be created also named djangorifa. The script will then use the pip script at djangorifa/bin/python to install django-celery and psycopg2. These are not included in the virtualenv because they require compilation. The script will then use djangorifa/bin/python to syncdb --all (django command) and then migrate --fake (south command) to set up the database. This will prompt for an admin username and password for administrative control of the website.

Before running this script, ensure you are logged in as a user with full database control. The default method for this is:

.. code-block:: bash

  $ sudo su - postgres

The script assumes a PostGIS version installed of 1.5 if this is different, when running the script you can optionally specify which version number. To run the script:

.. code-block:: bash

  $ chmod 777 install_djangorifa.sh
  $ ./install_djangorifa.sh [1.5]

The script does no checking for whether or not the version of PostGIS is correct, so run incorrectly at your peril.

The default database and username for postgresql can be changed. They are variables at the top of the script (DATABASE_NAME and DATABASE_USER).

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
