from django.shortcuts import render
from taarifa_config.forms import SiteForm, TaarifaConfigForm

def setup(request):
    # Create the form wizard
    # Need the Site creation form
    # Taarifa Config form
    return render(request, "taarifa_config/setup.html", {'form':SiteForm})
