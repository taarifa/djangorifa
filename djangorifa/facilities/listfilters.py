from django.contrib import admin
from django.db.models import Count
from django.utils.encoding import force_unicode
from facilities.models import Facility

class FacilityListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Facility'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'facility'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each tuple is the coded value for the option that will
        appear in the URL query. The second element is the human-readable name for the option that will appear
        in the right sidebar.
        """
        return [(f.pk, force_unicode(f)) for f in Facility.objects.annotate(num_issues=Count('facilityissue')).filter(num_issues__gt=0)]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value provided in the query string and retrievable via
        `self.value()`.
        """
        if not self.value(): return queryset
        return queryset.filter(facility__id=self.value())