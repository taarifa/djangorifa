from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from django.http import QueryDict
from django.contrib.contenttypes.models import ContentType
from facilities.forms import FacilityReportableForm
from facilities.models import Maintenance, Part, Facility, FacilityCategory, FacilityIssue
from reports.models import Report
from django.contrib.gis.geos import Point

# Save from rewriting the setUp hundreds of times
class GlobalTestCase(TestCase):
    def setUp(self):
        # Create a facility category, facility, parts and a facility issue
        self.fc = FacilityCategory.objects.create(name='toilets')
        self.f = Facility.objects.create(name="moo", category=self.fc, location=Point(0,0))
        part = Part.objects.create(name="Tap", cost=1)
        maintenance = Maintenance.objects.create(name="Unblock drains")
        part.category.add(self.fc)
        maintenance.category.add(self.fc)
        self.part = part
        self.maintenance = maintenance
        m = ContentType.objects.get_for_model(Maintenance)
        self.issue = FacilityIssue.objects.create(content_type=m, object_id=1, facility=self.f, cost=10)
        self.user = User.objects.create_user("caz", "caz@test.com", "password")

class FacilitiesTest(GlobalTestCase):

    def test_new_report_issue(self):
        '''
        Need to test that when a new facility reportable form
        is created and saved that the reported issues are saved
        '''

        # Create a request and user
        factory = RequestFactory()
        request = factory.get('/facilities/1/report/new/')
        request.user = self.user

        # Submit for both reportables
        post = QueryDict('csrfmiddlewaretoken=c01d0b3d7c94d87c999befc4e56f8d09&submit=Report&description=asd&Part=1&Maintenance=1')
        request.POST = post

        # Create the form, validate and save
        form = FacilityReportableForm(1, post)
        self.assert_(form.is_valid(), form)
        form.save(self.request)

        # Ensure there are only two reported issues in the database
        self.assertEqual(FacilityIssue.objects.all().count(), 2, "Wrong number of reported issues")
        report = Report.objects.all()[0]
        self.assertEqual(report.issues.count(), 2, "Report issues wrong!")
        fi = FacilityIssue.objects.all()[0]
        self.assertEqual(fi.related.related_to().count(), 1, "Issue report wrong! %d" % fi.related.count())
