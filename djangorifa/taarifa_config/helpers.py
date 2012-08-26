from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.db import transaction
from facilities.models import Facility, FacilityCategory
from xml.dom import minidom

def parse(filetype, file, clear_db=True):
    if filetype == ".osm":
        parse_osm(file, clear_db)

def parse_osm(file, clear_db=True):
    if clear_db:
        Facility.objects.all().delete()
        FacilityCategory.objects.all().delete()

        # Assuming we're on Postgres - just because I prefer numbers to restart when dealing
        # with categories as it makes it SO much easier when testing in shell!
        Facility.objects.raw('ALTER SEQUENCE facilities_facility_id_seq RESTART WITH 1;')
        FacilityCategory.objects.raw('ALTER SEQUENCE facilities_facility_id_seq RESTART WITH 1;')

    doc = minidom.parse(file)
    lat = lng = ft = n = o = None

    # This ensures that the database is hit once only - speeding up the process
    with transaction.commit_on_success():
        for node in doc.getElementsByTagName('node'):
            lat = float(node.getAttribute('lat'))
            lng = float(node.getAttribute('lon'))
            point = Point(lng, lat, srid=4326)

            # If there are points within 12m, it's a double (this needs confirming)
            if Facility.objects.filter(location__distance_lte=(point, D(m=12))).count() > 0: continue

            ft = n = o = None
            for tag in node.getElementsByTagName('tag'):
                k = tag.getAttribute('k')
                v = tag.getAttribute('v')

                if k == "amenity":
                    ft = v
                elif k == "operator":
                    o = v.title()
                elif k == "name":
                    n = v.title()
            ftt, created = FacilityCategory.objects.get_or_create(name=ft)
            f = Facility(name=n, location=point, category=ftt)
            f.save()
