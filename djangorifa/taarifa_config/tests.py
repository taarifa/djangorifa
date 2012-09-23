import os
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.test import TestCase
from django.test.client import Client
from facilities.models import Facility, FacilityCategory
from taarifa_config.models import TaarifaConfig
from taarifa_config.helpers import diff_osm

class TaarifaConfigSyncOSMTestCase(TestCase):
    def setUp(self):
        self.path = os.path.join(settings.STATIC_ROOT, "mapdata_test.osm")
        self.osm_new = '<?xml version="1.0" encoding="UTF-8"?>\n<osm version="0.6" generator="Overpass API">\n<note>The data included in this document is from www.openstreetmap.org. The data is made available under ODbL.</note>\n<meta osm_base="2012-09-23T13:53:02Z"/>\n  <node id="942567777" lat="-5.0047500" lon="31.0247500"/>\n  <node id="942567785" lat="-5.0007500" lon="31.0402500"/>\n  <node id="942567826" lat="-5.0042500" lon="31.0250000"/>\n  <node id="259712678" lat="1" lon="1">\n    <tag k="amenity" v="drinking_water"/>\n    <tag k="is_in" v="Kigoma, Tanzania"/>\n    <tag k="name" v="Nguruka"/>\n    <tag k="place" v="town"/>\n  </node>\n  <node id="259712679" lat="1" lon="100">\n    <tag k="amenity" v="drinking_water"/>\n    <tag k="is_in" v="Kigoma, Tanzania"/>\n    <tag k="name" v="Nguruka"/>\n    <tag k="place" v="town"/>\n  </node></osm>'.replace("\n    ", "").replace("\n  </node>", "</node>")
        self.osm_update = '<?xml version="1.0" encoding="UTF-8"?>\n<osm version="0.6" generator="Overpass API">\n<note>The data included in this document is from www.openstreetmap.org. The data is made available under ODbL.</note>\n<meta osm_base="2012-09-23T14:53:02Z"/>\n  <node id="942567777" lat="-5.0047500" lon="31.0247500"/>\n  <node id="942567785" lat="-5.0007500" lon="31.0402500"/>\n  <node id="942567826" lat="-5.0042500" lon="31.0250000"/>\n  <node id="259712678" lat="1" lon="1">\n    <tag k="amenity" v="drinking_water"/>\n    <tag k="is_in" v="Kigoma, Tanzania"/>\n    <tag k="name" v="Moo"/>\n    <tag k="place" v="town"/>\n  </node>\n  <node id="259712679" lat="1" lon="100">\n    <tag k="amenity" v="drinking_water"/>\n    <tag k="is_in" v="Kigoma, Tanzania"/>\n    <tag k="name" v="Nguruka"/>\n    <tag k="place" v="town"/>\n  </node></osm>'.replace("\n    ", "").replace("\n  </node>", "</node>")

    def tearDown(self):
        os.remove(self.path)

    def test_created_updated(self):
        # I always forget the Site is automagically created!
        site = Site.objects.get_current()
        TaarifaConfig.objects.create(site=site,bounds='POLYGON ((0.0000000000000000 0.0000000000000000, 0.0000000000000000 50.0000000000000000, 50.0000000000000000 50.0000000000000000, 50.0000000000000000 0.0000000000000000, 0.0000000000000000 0.0000000000000000))', sync_with_osm=True)

        diff_osm(self.path, self.osm_new)
        cat_num = FacilityCategory.objects.count()
        self.assertEqual(cat_num, 1, "Wrong number of categories: %d" % cat_num)
        fac_num = Facility.objects.count()
        self.assertEqual(fac_num, 1, "Wrong number of facilities: %d" % fac_num)
        facility = Facility.objects.get(pk=1)
        self.assertEqual(facility.name, "Nguruka", "Name wrong: %s" % facility.name)
        diff_osm(self.path, self.osm_update)
        facility = Facility.objects.get(pk=1)
        self.assertEqual(facility.name, "Moo", "Name wrong: %s" % facility.name)
