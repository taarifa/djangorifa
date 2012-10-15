import difflib
from celery.schedules import schedule
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.db import transaction
from facilities.models import Facility, FacilityCategory
from taarifa_config.models import TaarifaConfig
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

def update_osm(path, file_data, diff):
    # If there is a diff read from that
    osm = diff if diff else file_data
    doc = minidom.parseString(osm)

    with transaction.commit_on_success():
        for node in doc.getElementsByTagName('node'):
            category = name = None
            latitude = float(node.getAttribute('lat'))
            longitude = float(node.getAttribute('lon'))
            point = Point(longitude, latitude, srid=4326)

            for tag in node.getElementsByTagName('tag'):
                k = tag.getAttribute('k')
                v = tag.getAttribute('v')

                if k == "amenity":
                    category = v
                elif k == "name":
                    name = v.title()

            # Only create a point if there's a category, otherwise we have no idea what it is
            if category:
                fc, created = FacilityCategory.objects.get_or_create(name=category)
                f, created = Facility.objects.get_or_create(location=point, category=fc)
                f.is_synced = True
                f.category = fc
                f.name = name
                f.save()

    # Remove all facilities which are synced not within bounds
    bounds = TaarifaConfig.objects.get_current().bounds
    Facility.objects.filter(is_synced=True, location__disjoint=bounds).delete()

    # Write the osm file
    f = open(path, 'w')
    f.write(file_data)
    f.close()

def diff_osm(path, osm_new):
    try: osm_old = open(path, 'r')
    except: return update_osm(path, osm_new, None)

    old_set = set(osm_old.read().splitlines())

    # Compare the OSM files and update the information if it's changed
    osm_diff = set(osm_new.split("\n")) - old_set
    print osm_diff

    if len(osm_diff) > 1:
        print osm_diff
        # Add tags around the nodes
        osm_data = "<osm>%s</osm>" % "\n".join(list(osm_diff))
        return update_osm(path, osm_new, osm_data)
