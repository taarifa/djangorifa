# Install the requirements
pip install psycopg2
pip install pillow
pip install django-celery
pip install django-admin-tools
pip install South
pip install django-mailer
pip install django-registration
pip install django_extensions
pip install django_nose
pip install django_mobile
pip install django-crispy-forms
pip install django-generic-m2m
pip install django-sendsms
pip install django-sekizai

python djangorifa/manage.py syncdb --all
python djangorifa/manage.py migrate --fake
