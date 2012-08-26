import os

from crispy_forms.helper import FormHelper
from django import forms
from django.contrib.sites.models import Site
from django.core.files.uploadedfile import UploadedFile
from django.utils.translation import ugettext_lazy as _
from olwidget.widgets import EditableMap
from taarifa_config.helpers import parse
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

    # When setting valid file extensions, include the dot. That way no extra processing is required!
    extensions = ['.osm',]
    file = forms.FileField()

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        super(MapDataForm, self).__init__(*args, **kwargs)

    # The clean method in a formwizard is called twice
    # after the first time, the file is stored in memory
    def clean_file(self, *args, **kwargs):
        file = self.cleaned_data['file']
        ext = os.path.splitext(file.name)[1].lower()

        # This is the second time the file is called by the wizard
        # Likely not the best place to parse the information, but for sake
        # of logical togetherness it's the only place which made sense
        # Example: this form is used outside the context of a wizard
        if type(file) == UploadedFile:
            parse(ext, file, True)

        # The first time, run validation on its extension
        elif ext not in self.extensions:
            raise forms.ValidationError("File extension must be of type %s" % ", ".join(self.extensions))

        return file
