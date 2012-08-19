from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import permission_required
from django.views.generic.simple import direct_to_template
from taarifa_config.forms import SetupWizard, SiteForm, TaarifaConfigForm

@permission_required('taarifa_config.add_taarifaconfig')
def setup_wizard_perm(*args, **kwargs):
    return SetupWizard([SiteForm, TaarifaConfigForm], *args, **kwargs)

urlpatterns = patterns('taarifa_config.views',
    url(r'^setupforthefirstime/',
        SetupWizard([SiteForm, TaarifaConfigForm]),
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
