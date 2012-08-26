from crispy_forms.helper import FormHelper
from django import forms
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
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
        print self.instance.site
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
            'bounds': EditableMap(
                options={
                    'geometry': 'polygon',
                    'map_div_style': {
                        'width': '100%',
                    }
                },
                attrs={
                    'id':'bounds-edit'
                }
            )
        }

class MapDataForm(forms.Form):
    template_name = "taarifa_config/map_data_form.html"
    file = forms.FileField()

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        super(MapDataForm, self).__init__(*args, **kwargs)

    # To keep the logic clean, the file is processed here.
    # Just because this takes time, this form should be at the end
    # of any form wizard
    def clean(self, *args, **kwargs):
        cleaned_data = super(MapDataForm, self).clean(*args, **kwargs)
        print cleaned_data
        raise forms.ValidationError("Stay here")
        return cleaned_data


    """
    def clean_file(self, *args, **kwargs):
        data = self.cleaned_data['file']
        print data
        raise forms.ValidationError("I don't want you moving on!")
        return data
    """
