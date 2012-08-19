from crispy_forms.helper import FormHelper
from django import forms
from django.contrib.sites.models import Site
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

