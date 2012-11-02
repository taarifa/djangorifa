from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from registration.views import register

admin.autodiscover()
urlpatterns = patterns('',
    url(r'^admin_tools/', include('admin_tools.urls')),

    # Admin and documentation
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # Registration and user
    # url(r'^accounts/register/$', register, {'backend': 'users.backends.MobilePhoneBackend'}, name='registration_register'),
    # url(r'^accounts/', include('registration.backends.default.urls')),
    # url(r'^users/', include('users.urls')),

    # Initial configuration
    url(r'^taarifa_config/', include('taarifa_config.urls', namespace='taarifa_config')),

    # Reports
    # url(r'^$', 'reports.views.add'),
    # url(r'^reports/', include('reports.urls')),
    # url(r'^facilities/', include('facilities.urls')),

    url(r'^forms/', include('form_designer.urls')),
    url(r'^', include('cms.urls')),

)

if settings.DEBUG:
    urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'', include('django.contrib.staticfiles.urls')),
) + urlpatterns
