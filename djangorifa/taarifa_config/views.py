from django.contrib.formtools.wizard.views import SessionWizardView
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from taarifa_config.forms import SiteForm

class SetupWizard(SessionWizardView):
    template_name = "taarifa_config/setup.html"

    def done(self, form_list, **kwargs):
        print "done"
        # Since site is already saved, only need to worry about config
        form_list[1].save()
        return HttpResponseRedirect(reverse('taarifa_config:setupdone'))

    def process_step(self, form):
        # If we're dealing with saving a site, need to ensure
        # the next step can choose the user inputted data
        if type(form) == SiteForm:
            site = Site.objects.get(pk=1)
            site.name = form.instance.name
            site.domain = form.instance.domain
            site.save()
        return self.get_form_step_data(form)
