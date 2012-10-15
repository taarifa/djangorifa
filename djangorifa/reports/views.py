from django.shortcuts import render
from facilities.models import Facility
from olwidget.widgets import Map, InfoLayer
from reports.helpers import get_reported_issues
from taarifa_config.models import TaarifaConfig
from django.http import HttpResponse
from django.utils.encoding import force_unicode
import json

# Returns a dictionary of 'html', 'style' for use by the olwidget
def style_issues(f, issues):
    # If there are no reported issues is none, the points should be green
    if not issues:
        stroke_color = 'green'
        html = f.pk
    else:
        stroke_color = 'red'
        html = "Known Problems: %s" % ("<br />".join(map(force_unicode, issues)))

    # Add the status to the class and the pk of the facility
    return {'html': html, 'style': {'stroke_color': stroke_color}, 'pk': f.pk}

def add(request):
    # If viewing through full flavour
    #if False:
    if request.flavour == "full":
        # Show a big map with all facilities using olwidget
        template = "reports/add.html"

        # Get a list of all the issues for all facilities
        # Status shouldn't be hard-coded - update if time
        issues = [[f.location, style_issues(f, f.facilityissue_set.filter(status__lt=3))] for f in Facility.objects.select_related().all()]

        # Display a clickable list of facilities for the user
        fac_map = Map([
            InfoLayer(issues, {
                'name':'facilities',
                'cluster':True,
                'overlay_style': {
                    'fill_color':"${specialAttributeHandler}",
                },
                'overlay_style_context': {
                    'specialAttributeHandler': 'function(feature) {}',
                },
            })
        ], {
            'overlay_style': {'fill_opacity': 0.1, 'fill_color':'#ffa500', 'stroke_color':'#ffa500'},
            'default_zoom':18,
            'map_div_style':{'width':'100%', 'height':'100%'}
        },
        template="reports/add_map.html")

        context = {
            'map': fac_map,
        }
        return render(request, template, context)

    elif request.flavour == "mobile":
    #elif True:
        return render(request, "reports/mobile/add.html")

def coords(request):
    print "coords"
    if request.method == "POST":
        context = {'lat': request.POST.get('lat'), 'lon': request.POST.get('lon')}
        print context
    return render(request, "reports/mobile/report.html", context)


def reported_issues(request):
    config = TaarifaConfig.objects.get_current()
    issues = []

    # Get all subclasses of ReportedIssue and create a list
    for issue in get_reported_issues():
        issues.append(issue.objects.all())

    num_per_page = request.GET.get('num', 25) # Default to 25 reports per page

    # Need to write a custom filter / paginator which works across multiple models

    # Need to create a map to display

    return render(request, "reports/issues.html", {'issues': issues})
