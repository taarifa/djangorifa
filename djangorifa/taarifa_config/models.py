from django.contrib.gis.db import models
from django.contrib.sites.models import Site
from django.contrib.gis.geos import Point
from django.contrib.gis.admin.options import OSMGeoAdmin

class TaarifaConfigManager(models.GeoManager):
    def get_current(self):
        try: config = self.get(site=Site.objects.get_current())
        except: config = TaarifaConfig()
        return config

    def get_current_options(self):
        config = self.get_current()
        return config.get_options()

class TaarifaConfig(models.Model):
    site = models.OneToOneField(Site)
    bounds = models.PolygonField()

    objects = TaarifaConfigManager()

    def __unicode__(self):
        return ('%s Configuration') % (self.site.name)

    def get_extent(self):
        # If there is a configuration, return that.
        try: return self.bounds.extent
        # Otherwise return the default value
        except: return OSMGeoAdmin.restricted_extent

    def get_center(self):
        # Returns transformed points
        try: return self.bounds.centroid
        except: return Point(OSMGeoAdmin.default_lon, OSMGeoAdmin.default_lat)

    def get_options(self):
        default_lon, default_lat = self.get_center().coords
        return {
            'default_lon': default_lon,
            'default_lat': default_lat,
            'default_zoom': 15,
            'map_div_style': {
                'width': '100%',
            }
        }

    class Meta:
        app_label = 'taarifa_config'
        verbose_name = 'Configuration'
        verbose_name_plural = 'Configuration'

''' Signal stuff to try to reload admin - doesn't work'''

'''from django.db.models.signals import post_save

from django.core.cache import cache
from django.utils.cache import _generate_cache_header_key
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.conf import settings

def expire_cache(path, args=[], cacheName='default', isview=True):
    if settings.CACHES[cacheName].get('KEY_PREFIX', False):
        key_prefix = settings.CACHES[cacheName]['KEY_PREFIX']
    else:
        key_prefix = ''

    request = HttpRequest()
    if isview:
        request.path = reverse(path, args=args)
    else:
        request.path = path
    key = _generate_cache_header_key(key_prefix, request)

    if key:
        if cache.get(key):
            cache.set(key, None, 0)
        return True
    return False

def reload_admin_on_config_change(sender, **kwargs):
    expire_cache('admin:index')

post_save.connect(reload_admin_on_config_change, sender=TaarifaConfig)
'''
