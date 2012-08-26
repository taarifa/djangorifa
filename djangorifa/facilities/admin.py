from django.contrib import admin
from olwidget.admin import GeoModelAdmin
from facilities.forms import FacilityForm, FacilityIssueForm
from facilities.models import Facility, FacilityCategory, FacilityReportable, FacilityIssue
from facilities.helpers import get_class
from facilities.listfilters import FacilityListFilter
from taarifa_config.models import TaarifaConfig

# Dynamically creates the admin inline stuff, for however many reportable objects there are
# Also registers them with the admin site
class FacilityCategoryAdmin(admin.ModelAdmin):

    def __init__(self, *args, **kwargs):
        super(FacilityCategoryAdmin, self).__init__(*args, **kwargs)
        # Dynamically generate the inlines
        self.inlines = []
        for fr in FacilityReportable.__subclasses__():
            reportable = get_class("facilities.models.%s" % fr.__name__)
            admin.site.register(reportable)
            self.inlines.append(self.get_inline(reportable))

    def get_inline(self, reportable):
        class Inline(admin.TabularInline):
            reportable.category.through._meta.verbose_name = reportable._meta.verbose_name
            reportable.category.through._meta.verbose_name_plural = reportable._meta.verbose_name_plural
            model = reportable.category.through
        return Inline

# Deals with the admin of reported facility issues
class FacilityIssueAdmin(GeoModelAdmin):
    related_lookup_fields = {
        'generic': [['content_type', 'object_id'],],
    }
    form = FacilityIssueForm
    list_filter = ('status', FacilityListFilter)
    list_display = ('__unicode__', 'facility', 'status', 'cost')
    list_editable = ('status','cost')
    list_map = ['facility.location',]
    list_map_options = {
        'cluster': True,
        'no_list_display_links': True,
        'map_div_style': {
            'width': '100%',
        },
    }

    # This removes the link to be able to edit the model instance
    def __init__(self, *args, **kwargs):
        super(FacilityIssueAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None,)

    # Prevent someone from EVER editing the model instance - they should not change ANYTHING
    # other than status. This is a user-defined report, and therefore should not be editable.
    def change_view(self, request, obj=None):
        from django.core.urlresolvers import reverse
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect(reverse('admin:facilities_facilityissue_changelist'))

    # Remove add and delete permissions
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request):
        return False

# Register the defined admins
admin.site.register(FacilityCategory, FacilityCategoryAdmin)
admin.site.register(FacilityIssue, FacilityIssueAdmin)

class FacilityIssueInline(admin.TabularInline):
    model = FacilityIssue
    exclude = ('object_id',)
    readonly_fields = ('content_type',)

    #TODO implement such that if locked, cannot edit cost
    def __init__(self, obj, *args, **kwargs):
        super(FacilityIssueInline, self).__init__(obj, *args, **kwargs)

    def has_add_permission(self, *args, **kwargs):
        return False
    def has_delete_permission(self, *args, **kwargs):
        return False

# Enables the OSM for facility changing
class FacilityAdmin(GeoModelAdmin):
    form = FacilityForm
    inlines = (FacilityIssueInline,)

    list_map = ['location']
    list_map_options = TaarifaConfig.objects.get_current_options()
    list_map_options.update({'cluster':True})
    list_display = ('__str__', 'no_issues')

    def __init__(self, *args, **kwargs):
        super(FacilityAdmin, self).__init__(*args, **kwargs)
        self.change_list_template = "admin/facilities/facility/change_list.html"

    def queryset(self, request):
        from django.db.models import Count
        qs = super(FacilityAdmin, self).queryset(request)
        qs = qs.annotate(Count('facilityissue'))
        return qs

    def no_issues(self, obj):
        return obj.facilityissue_set.filter(status__lte=3).count()
    no_issues.admin_order_field = 'facilityissue__count'

    def has_delete_permission(self, *args, **kwargs):
        return False

admin.site.register(Facility, FacilityAdmin)
