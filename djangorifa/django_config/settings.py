# Django settings for taarifa project.
import os, sys
import djcelery
djcelery.setup_loader()
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

DEBUG = True
#DEBUG = not DEBUG
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'djangorifa',
        'USER': 'djangorifa',
        'PASSWORD': 'facebook',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(SITE_ROOT, '../static/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
#ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'r70qb#tbh9%5w)xb_o)2#r)djsa5df4itg7*(xnw^y4swrppw8'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django_mobile.loader.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django_mobile.middleware.MobileDetectionMiddleware',
    'django_mobile.middleware.SetFlavourMiddleware',
    'taarifa_config.middleware.CheckConfigSet',
)

ROOT_URLCONF = 'django_config.urls'

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, '../templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django.contrib.humanize',
    'django.contrib.formtools',

    # Admin
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.admin',
    'django.contrib.admindocs',

    # Third Party Apps
    'south',
    'sekizai',
    'djcelery',
    'mailer',
    'registration',
    'django_extensions',
    'django_filters',
    'django_nose',
    'django_mobile',
    'crispy_forms',
    'genericm2m',
    'sendsms',

    # Overwritten Apps
    'olwidget',

    # Custom Apps
    'theme',
    'theme.admin',
    'taarifa_config',
    'users',
    'reports',
    'facilities',
    #'auctions',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.contrib.messages.context_processors.messages',
    'django_mobile.context_processors.flavour',
    'sekizai.context_processors.sekizai',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Third party settings
ACCOUNT_ACTIVATION_DAYS = 1
ADMIN_MEDIA_PREFIX = '/static/admin/'
ADMIN_TOOLS_MENU = 'theme.admin.menu.CustomMenu'
ADMIN_TOOLS_INDEX_DASHBOARD = 'theme.admin.dashboard.CustomDashboard'
CRISPY_TEMPLATE_PACK = "uni_form"
OLWIDGET_DEFAULT_OPTIONS = {
    'overlay_style': {
        'pointRadius': 10,
        'strokeColor': '#FF6F00',
        'fillColor': '#FF6F00'
    }
}

# For geolocation
GEOIP_PATH = os.path.join(SITE_ROOT, 'geo/')

# For testing
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
if 'test' in sys.argv:
    print "moo"
    # Setup the test database with a user with permissions
    DATABASES['default'] = {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'djangorifa',
        'USER': 'test_djangorifa',
        'PASSWORD': 'change',
        'HOST': 'localhost',
        'PORT': '',
    }

# Disable south from running migrations whilst testing
SOUTH_TESTS_MIGRATE = False

# Send the report mails every 5 minutes
from datetime import timedelta
CELERYBEAT_SCHEDULE = {
    "send-mail": {
        "task": "reports.tasks.mail",
        "schedule": timedelta(minutes=5),
    },
}

# For logging in via mobile phone number, not email
AUTH_PROFILE_MODULE = 'users.UserProfile'

# Email settings
EMAIL_USE_TLS = True
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587

# Celery / RabbitMQ settings
BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_VHOST = "vhost"
BROKER_USER = ""
BROKER_PASSWORD = ""
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
