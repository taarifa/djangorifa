import os, shutil, tempfile

from djcelery.models import IntervalSchedule, PeriodicTask
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.formtools.wizard.views import SessionWizardView
from django.contrib.sites.models import Site
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from taarifa_config.forms import MapDataForm, SiteForm, TaarifaConfigForm, UserCreateProfileForm
from taarifa_config.models import TaarifaConfig
from users.models import UserProfile

class SetupWizard(SessionWizardView):
    temp_storage_location = tempfile.mkdtemp(dir=os.path.join(settings.SITE_ROOT, 'tmp'))
    file_storage = FileSystemStorage(location=temp_storage_location)
    template_name = "taarifa_config/setup.html"

    def done(self, form_list, **kwargs):
        # Delete the temporary file storage
        try:
            shutil.rmtree(self.temp_storage_location)
        except: pass
        for f in form_list:
            tipo = type(f)
            if tipo == TaarifaConfigForm:
                f.save()
            if tipo == UserCreateProfileForm:
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

@login_required
def setup(request):
    instances = {}

    # If the current user already has a profile, grab it, or create
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    print user_profile
    instances.update({'0': user_profile})

    # Get the current site
    site = Site.objects.get_current()
    instances.update({'1': site})

    # If there is already a TaarifaConfig
    try:
        taarifa_config = TaarifaConfig.objects.get(site=site)
        instances.update({'2': taarifa_config})
    except: pass

    # Because there's a possibility we're going to be using Celery,
    # need to create some intervals and schedule - these will be editable by an admin
    interval, created = IntervalSchedule.objects.get_or_create(every=5, period="minutes")
    task, created = PeriodicTask.objects.get_or_create(task="taarifa_config.tasks.sync_osm")
    if created:
        task.name = "Sync OSM"
        task.interval = interval
        task.save()

    sw = SetupWizard.as_view([UserCreateProfileForm, SiteForm, TaarifaConfigForm], instance_dict=instances)
    return sw(request)
