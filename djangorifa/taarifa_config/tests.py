from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.test import TestCase
from django.test.client import Client
from taarifa_config.models import TaarifaConfig

class TaarifaConfigMiddlewareTestCase(TestCase):
    def setUp(self):
        # Create super super user
        self.caz = User.objects.create_user('caz', password='caz')
        self.caz.is_superuser = True
        self.caz.is_staff = True
        self.caz.save()

        # Create super user
        self.superuser = User.objects.create_user('super', password='caz')
        self.superuser.is_superuser = True
        self.superuser.save()

        # Create staff user
        self.staffuser = User.objects.create_user('staff', password='caz')
        self.staffuser.is_staff = True
        self.staffuser.save()

        # Requests and sessions and stuff
        self.client = Client()

    def test_middleware_redirect(self):
        # Call non-existent page with an anonymous user
        response = self.client.get('/accounts/')
        self.assertEqual(404, response.status_code, "Anonymous not 404.")

        # Login as super super user and confirm there is a redirect
        response = self.client.post('/accounts/login/', {'username':'caz', 'password':'caz'})
        response = self.client.get('/accounts/')
        self.assertEqual(302, response.status_code, "Accounts caz not redirect.")

        # Login as super user and confirm there is a redirect
        self.client.post('/accounts/login/', {'username': 'super', 'password': 'caz'})
        response = self.client.get('/accounts/')
        self.assertEqual(302, response.status_code, "Accounts super not redirect.")

        # Login as staff and confirm there is no redirect
        self.client.post('/accounts/login/', {'username': 'staff', 'password': 'caz'})
        response = self.client.get('/accounts/')
        self.assertEqual(404, response.status_code, "Staff not 404.")

    def test_middleware_no_redirect(self):
        # Values for things
        config_url = '/taarifa_config/setupforthefirstime/'
        polygon = 'POLYGON ((0.0000000000000000 0.0000000000000000, 0.0000000000000000 50.0000000000000000, 50.0000000000000000 50.0000000000000000, 50.0000000000000000 0.0000000000000000, 0.0000000000000000 0.0000000000000000))'
        form_data = ({
                '0-domain':'moo.com',
                '0-name':'moo',
                'setup_wizard-current_step': '0',
            },
            {
                '1-site': 1,
                '1-bounds': polygon,
                'setup_wizard-current_step': '1',
            })

        # Login as user who can redirect
        self.client.post('/accounts/login/', {'username': 'caz', 'password': 'caz'})

        # Assert that redirected to correct path
        response = self.client.get('/accounts/', follow=True)
        path, status_code = response.redirect_chain[0]
        self.assertEqual(path, 'http://testserver%s' % config_url, "Redirect: %s" % path)

        # Assert that there is no Taarifa Config
        tc_count = TaarifaConfig.objects.count()
        self.assertEqual(0, tc_count, "There is already a TaarifaConfig.")

        # Assert site is example.com - Django default
        site = Site.objects.get(pk=1)
        self.assertEqual(site.domain, "example.com", "Site is: %s." % site.domain)

        # Post the details for step 0 and assert site changed
        r = self.client.get(config_url)
        r = self.client.post(config_url, form_data[0])
        site = Site.objects.get(pk=1)
        self.assertEqual(site.domain, "moo.com", "Site:%s" % site.domain)

        # Post step 1 and assert config is created
        r = self.client.post(config_url, form_data[1])
        count = TaarifaConfig.objects.count()
        self.assertEqual(count, 1, "TaarifaConfig not created: %d" % count)
        tc = TaarifaConfig.objects.get(pk=1)
        self.assertEqual(tc.bounds, polygon, "Polygon not created.")
