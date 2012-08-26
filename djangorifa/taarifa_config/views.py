import os, shutil, tempfile

from django.conf import settings
from django.contrib.formtools.wizard.views import SessionWizardView
from django.contrib.sites.models import Site
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from taarifa_config.forms import SiteForm, TaarifaConfigForm, MapDataForm

temp_storage_location = tempfile.mkdtemp(dir=os.path.join(settings.SITE_ROOT, 'tmp'))
temp_storage = FileSystemStorage(location=temp_storage_location)

class SetupWizard(SessionWizardView):
    file_storage = temp_storage
    template_name = "taarifa_config/setup.html"

    def done(self, form_list, **kwargs):
        # Delete the temporary file storage
        shutil.rmtree(temp_storage_location)
        for f in form_list:
            tipo = type(f)
            if tipo == TaarifaConfigForm:
                f.save()
            #elif typo == MapDataForm:
            #    print f.cleaned_data['file']
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

    # If the forms define a template_name variable, that template
    # will be used instead of the default. The Django documentation
    # is very misleading on this and this is a bit of a funny implementation
    # but it's what you get!
    def get_template_names(self):
        # Get the current form (index is a string, but steps.index is int)
        current_form = self.form_list['%d' % self.steps.index]
        if hasattr(current_form, 'template_name'):
            return current_form.template_name
        return self.template_name
