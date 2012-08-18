########
Settings
########

There are a few settings which are used by the system which also need to be configured. These can be set in the config/settings.py. Settings in that file not covered in this guide are covered in detail by Django https://docs.djangoproject.com/en/dev/topics/settings/.

*****************
Required Settings
*****************

.. setting:: SECRET_KEY

SECRET_KEY
==========

In future this will be automatically generated, but for now it needs to be made unique manually.

EMAIL_HOST
==========

This is currently blank which means there will be errors when emailing users. Set this to an email address which can send email.

EMAIL_HOST_USER
===============

This is the SMTP address of the email provider. For example, if it's a Gmail account, set this value to smtp.gmail.com.

EMAIL_HOST_PASSWORD
===================

The password for the account which mail is being sent from.

EMAIL_USE_TLS
=============

Default `True`.

If the SMTP account requires TLS.

EMAIL_PORT
==========

Default `587`.

The port the SMTP server requires.

BROKER_USER
===========

The user for which RabbitMQ is set up for.

BROKER_PASSWORD
===============

The password for RabbitMQ.

***************
Celery Settings
***************

Celery is used for task scheduling. Currently, it is only set up to send emails from a queue. For more information on celery, see the `celery documentation <http://docs.celeryproject.org/en/latest/index.html>`_ and the `django-celery documentation <http://docs.celeryproject.org/en/latest/django/index.html>`_.

CELERY_BEAT_SCHEDULE
====================

Default `5 minutes`

Django-mailer puts emails into queues so as not to overload the server when mails are sent. Django celery is used to automatically send these emails at scheduled times.

.. code-base:: python

  schedule: timedelta(minutes=5)

Change to minutes=n or days, seconds, etc. For more information on datetime and timedelta, see the `python documentation <http://docs.python.org/dev/library/datetime.html>`_.

**************
Other Settings
**************

Other settings are for django-grappelli, django-olwidget and django-crispy-forms. They are not discussed here.

TEST_RUNNER
===========

Django nose is used for testing purposes. The reasons for this are that it can store a copy of the database without tearing down after each test, which makes testing quicker. To use another test runner, change this setting.

AUTH_PROFILE_MODULE
===================

This a setting used by django-registration. This points to a custom backend which enables users to login with their mobile phones. It is highly recommended not to change this setting.
