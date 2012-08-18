from django import forms
from django.contrib.sites.models import Site
from taarifa_config.models import TaarifaConfig

class SiteForm(forms.ModelForm):
    class Meta:
        model = Site

class TaarifaConfigForm(forms.ModelForm):
    class Meta:
        model = TaarifaConfig
