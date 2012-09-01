from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from django.test.client import Client
from auctions.models import Bid
from facilities.tests import GlobalTestCase

class BidTest(GlobalTestCase):
    def setUp(self):
        super(BidTest, self).setUp()
        # Create a group, a request and two users
        group = Group.objects.create(name="Worker")
        # User already defined in setup
        group.user_set.add(self.user)
        self.user2 = User.objects.create_user("baz", "baz@test.com", "password")
        group.user_set.add(self.user2)
        self.user3 = User.objects.create_user("naz", "naz@test.com", "password")

    def test_non_logged_in_cannot_access(self):
        # Assert non-logged
        client = Client()
        response = client.post('/jobs/', {'name-bid-1':'Bid!'})
        self.assertEqual(response.status_code, 302, "Non logged-in can view")

        # Assert non-group
        client.login(username="naz", password="password")
        response3 = client.post('/jobs/', {'name-bid-1':'Bid!'})
        self.assertEqual(response3.status_code, 302, "Non group can view")

    def test_multiple_yeses(self):
        # Set up two users on clients
        client1 = Client()
        client2 = Client()
        client1.login(username="caz", password="password")
        client2.login(username="baz", password="password")

        """" Need to check that when two users hit post, only one of them gets it """
        response1 = client1.post('/jobs/', {'name-bid-1':'Bid!'})
        response2 = client2.post('/jobs/', {'name-bid-1':'Bid!'})

        # Assert that the correct status codes are returned
        self.assertEqual(response1.status_code, 200, "Response code incorrect for logged in right group")
        self.assertEqual(response2.status_code, 200, "Response code incorrect for logged in right group")

        # Assert there is only one bid at the end
        self.assertEqual(Bid.objects.count(), 1, "Wrong number of bids")
