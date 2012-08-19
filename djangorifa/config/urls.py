from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin_tools/', include('admin_tools.urls')),

    # Admin and documentation
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # Registration and user
    url(r'^accounts/', include('registration.backends.default.urls')),

    # Initial configuration
    url(r'^taarifa_config/', include('taarifa_config.urls', namespace='taarifa_config')),
)
