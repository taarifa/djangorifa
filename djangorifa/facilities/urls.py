from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('facilities.views',
    url(r'^(\d+)/report/$', 'view_report'),
    url(r'^(\d+)/report/new/$', 'new_report')
)