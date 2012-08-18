from django.conf.urls import patterns, include, url

urlpatterns = patterns('taarifa_config.views',
    url(r'^setupforthefirstime/', 'setup'),
)
