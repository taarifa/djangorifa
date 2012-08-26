from django import forms
from django.contrib.contenttypes.models import ContentType
from olwidget.utils import get_ewkt
from olwidget.fields import MapField, EditableLayerField, InfoLayerField
from facilities.models import FacilityReportable, Facility, FacilityIssue
from reports.forms import ReportForm
from reports.models import Reportable
from taarifa_config.models import TaarifaConfig

class FacilityIssueForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FacilityIssueForm, self).__init__(*args, **kwargs)
        choices = [item.__name__.lower() for sublist in Reportable.__subclasses__() for item in sublist.__subclasses__()]
        self.fields['content_type'].queryset = ContentType.objects.filter(model__in=choices)

class FacilityForm(forms.ModelForm):
    """
    # Displays a multi-layered map with information needed for adding facilities
    try:
        location = MapField(
            fields = [EditableLayerField({'geometry': 'point', 'name': 'Facility'}),
                      InfoLayerField([(get_ewkt(p.location), {
                          'html': p.name,
                          'style': {'fill_color': '#999'},
                      }) for p in Facility.objects.all()], {'name': 'Other Facilities'}),
                      InfoLayerField([[get_ewkt(config.get_extent()), "Boundary"]], {'name': 'Boundary'})],
        )
    except: pass
    """
    # Ensure that the facility is within the confines of the area
    def clean_location(self, *args, **kwargs):
        location = self.cleaned_data.get('location')
        bounds = TaarifaConfig.objects.get_current().bounding_points
        if not location[0].within(bounds):
            raise forms.ValidationError("Facility not within bounds")
        return location

    class Meta:
        model = Facility

"""
    Implements the interface provided by ReportForm
"""
class FacilityReportForm(ReportForm):
    reportables = [FacilityReportable,]
    reported_issue = FacilityIssue

    """ Adds additional options at initialisation """
    def __init__(self, facility, *args, **kwargs):
        self.facility = Facility.objects.get(pk=facility)
        self.action = '/facilities/%s/report/new/' % facility
        self.extra_reportable_args = {'category__pk':self.facility.category.pk}
        super(FacilityReportForm, self).__init__(*args, **kwargs)

    """ Implements the required method for the report form """
    def get_extra_create_args(self, reportable):
        return {'facility': self.facility,
                'cost': reportable.min_cost}

    """ Need to verify the URL matches the checkboxes """
    def clean_reportable(self, reportable_class, reportable_instances):
        qs = reportable_class.objects.filter(category__pk = self.facility.category.pk)

        if not set(reportable_instances).issubset(set(qs)):
            raise forms.ValidationError("The issue, %s, you are trying to report does not exist for this facility." % reportable_instances)
