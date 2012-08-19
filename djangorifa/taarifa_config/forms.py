from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.formtools.wizard import FormWizard
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from olwidget.widgets import EditableMap
from taarifa_config.models import TaarifaConfig

class SiteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        super(SiteForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Site

class TaarifaConfigForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        super(TaarifaConfigForm, self).__init__(*args, **kwargs)
        self.fields['site'].empty_label = None

    def save(self, *args, **kwargs):
        # Check to see if a foreign key for the site already exists
        if self.instance.site:
            # If it does, set this instance foreign key
            try:
                t = TaarifaConfig.objects.get(site=site)
                self.instance.pk = t.pk
            except: pass
        super(TaarifaConfigForm, self).save(*args, **kwargs)

    class Meta:
        model = TaarifaConfig
        widgets = {
            'bounds': EditableMap({'geometry': 'polygon'}, attrs={'id':'bounds-edit'})
        }

class SetupWizard(FormWizard):
    def done(self, request, form_list):
        # Since site is already saved, only need to worry about config
        form_list[1].save()
        return HttpResponseRedirect(reverse('taarifa_config:setupdone'))

    # Override to allow the site value in TaarifaConfig
    # to be set from what the user defined
    def process_step(self, request, form, step):
        # If step == 0 then it's the site form
        if not step:
            # Get the example site object
            site = Site.objects.get(pk=1)
            site.name = form.instance.name
            site.domain = form.instance.domain
            site.save()
