import os

from crispy_forms.helper import FormHelper
from django import forms
from django.contrib.gis.measure import Area
from django.contrib.sites.models import Site
from django.core.files.uploadedfile import UploadedFile
from django.utils.translation import ugettext_lazy as _
from djcelery.models import PeriodicTask
from olwidget.widgets import EditableMap
from taarifa_config.helpers import parse
from taarifa_config.models import TaarifaConfig
from taarifa_config.tasks import sync_osm
from users.forms import UserEditProfileForm

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

    # When the bounds change, need to redownload data from openstreetmap
    def save(self, *args, **kwargs):
        instance = super(TaarifaConfigForm, self).save(*args, **kwargs)

        # Add the celery task thing if sync is true
        if instance.sync_with_osm:
            p = PeriodicTask.objects.filter(name="do-stuff").update(enabled=True)
            sync_osm()

        # Otherwise don't
        else:
            p = PeriodicTask.objects.filter(name="do-stuff").update(enabled=False)

    # Need to ensure the user doesn't try to download too much data
    def clean_bounds(self, *args, **kwargs):
        bounds = self.cleaned_data['bounds']
        limit = 50.0

        # Transform the bounds to spherical mercator
        bounds.transform(900913)
        a = Area(sq_m=bounds.area)
        if a.sq_mi > limit:
            raise forms.ValidationError("Bounds cannot be more than %d square miles" % limit)
        return bounds

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

class UserCreateProfileForm(UserEditProfileForm):
    def __init__(self, *args, **kwargs):
        kwargs.update({'being_created': True})
        # Get the user profile for the current user
        super(UserCreateProfileForm, self).__init__(*args, **kwargs)
