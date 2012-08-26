from facilities.tests import GlobalTestCase
from facilities.models import FacilityIssue
from django.contrib.auth.models import User
from mailer.models import Message, MessageLog
from reports.models import Report
from django.test.client import Client

class OneUserReportsTest(GlobalTestCase):
    def setUp(self):
        super(OneUserReportsTest, self).setUp()
        FacilityIssue.objects.filter(pk=1).update(cost=100)

    # Need to check that on a reported issue status change
    # emails are sent to every user defined as being interested
    def test_email_not_sent_on_cost_field_changed(self):
        self.assertEqual(MessageLog.objects.count(), 0, "Mail has been sent erroneously")
        self.assertEqual(Message.objects.count(), 0, "Mail has been sent erroneously")

    def test_email_sent_on_status_field_changed(self):
        pass
        # The facility issue has only been reported by one user, so there should be only one mail in the system
        #self.assertEqual(Message.objects.count(), 1, "Mail has not been sent")

class MultiUserReportsTest(GlobalTestCase):
    def setUp(self):
        super(MultiUserReportsTest, self).setUp()
        # Add another user to the issue
        User.objects.create_user("baz", "baz@test.com", "password")
        client = Client()
        client.login(username="baz", password="password")
        client.post("/facilities/1/report/new/", {'submit':'Report','description':'asd','Part':1})

    def test_report_status_changes(self):
        # Double check there are two reports
        self.assertEqual(Report.objects.count(), 2, "There are not two reports")

        #
        #report = Report.objects.all()[0]
        #issue = FacilityIssue.objects.all()[0]
        #self.assertEqual(report.status, issue.status, "Report out of sync with issue")
