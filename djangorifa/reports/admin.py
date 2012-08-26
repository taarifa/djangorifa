from django.contrib import admin
from reports.models import Report

class ReportAdmin(admin.ModelAdmin):
    #form = FacilityIssueForm
    list_filter = ('status', 'user')

    # Make all fields read only
    readonly_fields = ('status', 'created', 'user', 'description', 'modified')

    def __init__(self, *args, **kwargs):
        super(ReportAdmin, self).__init__(*args, **kwargs)
        self.list_display = self.list_display + ('created', 'user', 'description', 'status')

    def has_delete_permission(self, *args, **kwargs):
        return False
    def has_add_permission(self, *args, **kwargs):
        return False


# Register the defined admins
admin.site.register(Report, ReportAdmin)
