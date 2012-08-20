from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('users.views',
    # All profiles are private, so the only thing that can be done is the user
    # can view or edit their own profile
    url(r'^edit/$', 'edit', name='users-edit'),
    url(r'^$', 'view', name='users-view'),
)