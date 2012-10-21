import cStringIO, difflib, os, pycurl, re
from celery.task import task
from djcelery.models import IntervalSchedule
from django.conf import settings
from taarifa_config.helpers import diff_osm
from taarifa_config.models import TaarifaConfig
from xml.dom import minidom

@task
def sync_osm(filename="mapdata.osm"):
    # Get the current bounds of the site
    bounds = ",".join(map(str,TaarifaConfig.objects.get_current().get_extent()))
    url = "http://www.overpass-api.de/api/xapi?node[bbox=%s]" % bounds

    # Get the osm file from OSM API - into temp string buffer
    buf = cStringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEFUNCTION, buf.write)
    c.perform()

    # Format whilst still ensuring it's valid XML
    osm_new = buf.getvalue().replace("\n    ", "").replace("\n  </node>", "</node>")

    # See if the on-file OSM file exists - if not, straight create
    return diff_osm(os.path.join(settings.SITE_ROOT, filename), osm_new)
