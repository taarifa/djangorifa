from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import permission_required
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('taarifa_config.views',
    url(r'^setupforthefirstime/',
        'setup',
        name='setup',
    ),
)

urlpatterns += patterns('django.views.generic.simple',
    url(r'^setupdone/',
        'direct_to_template',
        {'template': 'taarifa_config/setup_done.html'},
        name='setupdone',
    ),
)
