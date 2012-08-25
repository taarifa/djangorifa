# Install the requirements
../bin/pip install psycopg2
../bin/pip install pillow
../bin/pip install django-celery
../bin/pip install django-admin-tools
../bin/pip install South
../bin/pip install django-mailer
../bin/pip install django-registration
../bin/pip install django_extensions
../bin/pip install django_nose
../bin/pip install django_mobile
../bin/pip install django-crispy-forms
../bin/pip install django-generic-m2m
../bin/pip install django-sendsms
../bin/pip install django-sekizai

../bin/python djangorifa/manage.py syncdb --all
../bin/python djangorifa/manage.py migrate --fake
