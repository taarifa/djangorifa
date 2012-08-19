from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

class TaarifaConfigMiddlewareTestCase(TestCase):
    def setUp(self):
        # Create super super user
        self.caz = User.objects.create_user('caz')
        self.caz.is_superuser = True
        self.caz.is_staff = True
        self.caz.save()

        # Create super user
        self.superuser = User.objects.create_user('super')
        self.superuser.is_superuser = True
        self.superuser.save()

        # Create staff user
        self.staffuser = User.objects.create_user('staff')
        self.staffuser.is_staff = True
        self.staffuser.save()

        # Requests and sessions and stuff
        self.client = Client()

    def test_middleware_redirect(self):
        # Call non-existent page with an anonymous user
        response = self.client.get('/accounts/')
        self.assert_equal(404, response.status_code)

        # Login as super super user and confirm there is a redirect
        response = self.client.post('/accounts/login/', {'username':'caz'})
        self.assert_equal(200, response.status_code)
        response = self.client.get('/accounts/')
        self.assert_equal(302, response.status_code)

        # Login as super user and confirm there is a redirect
        self.client.post('/accounts/login/', {'username': 'super'})
        response = self.client.get('/accounts/')
        self.assert_equal(302, response.status_code)

        # Login as staff and confirm there is no redirect
        self.client.post('/accounts/login/', {'username': 'staff'})
        response = self.client.get('/accounts/')
        self.assert_equal(404, response.status_code)

    def test_middleware_no_redirect(self):
        response = self.client.post('/accounts/login/', {'username': 'caz'})
        self.assert_equal(response.request.get('PATH_INFO'), '/taarifa_config/setupforthefirstime/')

        # Post the details for step 0
        r = c.post(url, {'0-domain':'moo.com', '0-name':'moo.com'})

