from django.contrib.gis import admin
from taarifa_config.models import TaarifaConfig
#from taarifa_config.forms import TaarifaConfigForm
from olwidget.admin import GeoModelAdmin
from django.contrib.sites.models import Site

class TaarifaConfigModelAdmin(GeoModelAdmin):
#class TaarifaConfigModelAdmin(admin.ModelAdmin):
    #form = TaarifaConfigForm
    #fieldsets = (
    #    ('Location Settings', {
    #        'fields': ('site', 'bounding_points', 'radiuses')
    #    }),
    #)

    def generate_inlines(self):
        self.inlines = []

        def get_inline(model_name):
            # Temp class to define dynamically created inlines
            class Inline(admin.TabularInline):
                model = model_name
            return Inline

        # Loop through all relations in the config
        for ro in self.model._meta.get_all_related_objects():
            self.inlines.append(get_inline(ro.model))

    def __init__(self, *args, **kwargs):
        super(TaarifaConfigModelAdmin, self).__init__(*args, **kwargs)
        self.generate_inlines()

admin.site.register(TaarifaConfig, TaarifaConfigModelAdmin)
