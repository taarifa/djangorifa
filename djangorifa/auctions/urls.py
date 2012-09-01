from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('auctions.views',
    url(r'^$', 'view_auction'),
    url(r'^(\d+)/$', 'view_jobs')
)