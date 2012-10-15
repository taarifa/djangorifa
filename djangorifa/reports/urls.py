from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('django.views.generic.simple',
    url(r'^ajax/reported/(?P<id>\d+)/$', 'direct_to_template', {'template': 'reports/reported.html'}, name='ajax_reported'),
)

urlpatterns += patterns('reports.views',
    url(r'^$', 'reported_issues'),
    url(r'^coords/$', 'coords'),
    #url(r'^(?P<uid>\d+)/report/(?P<rid>\d+)$', 'user'),
    #url(r'^(?P<uid>\d+)/report/(?P<rid>\d+)$', 'user')
)
