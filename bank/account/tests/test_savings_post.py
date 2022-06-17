from django.test import TestCase, Client
from AccountProfile.models import AccountProfile
from django.urls import reverse
from django.contrib.auth.models import User

class CreditTest(TestCase):
    def setUp(self):
        user = User.objects.create(username="luvo@k.com", password="password")
        self.profile = AccountProfile(user=user, name="luvo", surname="dlulisa", \
            identity_number="908327", email="luvo@k.com", contact="098766")
        self.profile.save()

    def test_no_initial_amount(self):
        client = Client()
        data = {"profile": self.profile.pk}
        response = client.post(reverse("savings"), data)
        self.assertEqual(400, response.status_code)
    
    def test_amount_less_than_limit(self):
        client = Client()
        data = {"profile": self.profile.pk, "account": 20}
        response = client.post(reverse("savings"), data)
        self.assertEqual(400, response.status_code)