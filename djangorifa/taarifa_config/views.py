from django.shortcuts import render
from taarifa_config.forms import SiteForm, TaarifaConfigForm, SetupWizard

def setup(request):
    # Create the form wizard
    # Need the Site creation form
    # Taarifa Config form
    print SetupWizard([SiteForm, TaarifaConfigForm])
    return render(request, "taarifa_config/setup.html", {'form':SetupWizard([SiteForm, TaarifaConfigForm])})
