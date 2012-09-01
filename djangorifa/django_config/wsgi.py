"""
This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os, site, sys
prev_sys = list(sys.path)

for directory in ['/home/caz/Hosted/djangorifa/lib/python2.6/site-packages']:
	site.addsitedir(directory)
new_sys = []
for item in list(sys.path):
	if item not in prev_sys:
		new_sys.append(item)
		sys.path.remove(item)
sys.path[:0] = new_sys
sys.path.append('/home/caz/Hosted/djangorifa/djangorifa/djangorifa')
sys.path.append('/home/caz/Hosted/djangorifa/djangorifa/djangorifa/django_config')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_config.settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
