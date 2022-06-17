from django.test import TestCase, Client
from AccountProfile.models import AccountProfile
from django.urls import reverse

class AdminTest(TestCase):
    def setUp(self):
        pass

    def test_invalid_primary_key_returns_400(self):
        client = Client()
        response = client.get(reverse("custom-admin", kwargs={"pk": 2}))
        self.assertEqual(400, response.status_code)